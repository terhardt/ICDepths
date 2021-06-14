"""Script to add AWI IC-vial numbers to Bern CFA logfiles

This script should be used to re-concile Bern CFA logfiles and the notes
taken during the fraction collection itself.
"""
import pandas as pd
import numpy as np
from os import path
import sys


def prompt_vial_range():
    """Prompt user for first and last vial of run"""
    first_ic_vial = int(input('First IC vial? '))
    last_ic_vial = int(input('Last IC vial? '))
    return first_ic_vial, last_ic_vial


def prompt_vialnumber(first_vial, last_vial):
    """Prompt user for a vial number and check it against possible vial range"""
    n = input('Vial? ')
    try:
        n = int(n)
        if n > last_vial or n < first_vial:
            raise(ValueError('Number out of range'))
    except ValueError:
        print('Please enter an integer between %g and %g' % (first_vial, last_vial))
        return prompt_vialnumber(first_vial, last_vial)
    return n


def merge_with_next_vial(log_data, vial_idx):
    """Merge a missed vial with the next vial
    and update log_data table

    Used to correct for missed pulses
    """
    log_data.loc[vial_idx, 'Merged'] = 1
    log_data.loc[vial_idx, 'Depth_bot'] = log_data.loc[vial_idx + 1, 'Depth_bot']
    log_data.loc[vial_idx, 'Breaks'] = np.int64(np.any(log_data.loc[[vial_idx, vial_idx + 1], 'Breaks'] == 1))
    return log_data.drop(vial_idx + 1)


if __name__ == '__main__':
    try:
        logfile = sys.argv[1]
    except IndexError:
        print('Provide logfile as commandline argument')

    outdir = 'test_out'
    outfile = path.join(outdir, path.basename(logfile).replace('info', 'assign'))
    if path.exists(outfile):
        print('Output file already existing, exiting.')
        sys.exit(1)

    log_data = pd.read_csv(logfile, index_col=0)
    # Add column for merged flag
    log_data['Merged'] = 0

    depth_top = log_data['Depth_top'].iloc[0]
    depth_bot = log_data['Depth_bot'].iloc[1]
    bags = log_data['Bag'].unique().tolist()
    nlogged = len(log_data)

    print('Processing: %s' % logfile)

    print('Depth range: %.3f - %.3f' % (depth_top, depth_bot))
    print('Bags: ', bags)
    print('Number of pulses logged: %g' % nlogged)

    first_ic_vial, last_ic_vial = prompt_vial_range()
    nfilled = last_ic_vial - first_ic_vial + 1
    ic_vials = np.arange(first_ic_vial, last_ic_vial + 1)
    print('Number of vials filled: %g' % nfilled)
    print()

    if nfilled == nlogged:
        print('Nice, logged and filled number of vials match')
    else:
        print('WARNING, logged and filled number of vials DO NOT MATCH')
        print('logged:', nlogged)
        print('filled:', nfilled)
        # Ask how many pulses where missed during the run
        nmissed = input('Please enter the numbers of missed pulses (%g)' % (nlogged - nfilled))
        if nmissed == '':
            nmissed = nlogged - nfilled
        else:
            nmissed = int(nmissed)

        # Ask for all missed pulses befor changing log data
        # in reverse order to avoid indexing issues
        missed_vials = []
        print('Missed vials?')
        for imissed in range(nmissed):
            missed_vial = prompt_vialnumber(first_ic_vial, last_ic_vial)
            missed_vials.append(missed_vial)
        print()
        for missed_vial in sorted(missed_vials, reverse=True):
            pulse_idx = np.where(ic_vials == missed_vial)[0].item()
            print('Merging pulse %g with next vial' % pulse_idx)
            log_data = merge_with_next_vial(log_data, pulse_idx)

    log_data['IC_Vial'] = ic_vials
    print()
    print('Saving to: %s' % outfile)
    log_data.to_csv(outfile, index=True)
    print('done.')
