"""Script to add AWI IC-vial numbers to Bern CFA logfiles"""
import pandas as pd
import numpy as np
from os import path
import sys


def yesno_prompt(question):
    """'Prompt user for yes/no answer"""
    prompt = '%s ? (y/n): ' % question
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno_prompt(question)
    if ans == 'y':
        return True
    return False


def vial_range_prompt():
    """Prompt user for first and last vial of run"""
    first_ic_vial = int(input('First IC vial? '))
    last_ic_vial = int(input('Last IC vial? '))
    return first_ic_vial, last_ic_vial


if __name__ == '__main__':
    try:
        logfile = sys.argv[1]
    except IndexError:
        print('Provide logfile as commandline argument')

    outdir = 'test_out'
    outfile = path.join(outdir, path.basename(logfile).replace('info', 'assign'))

    log_data = pd.read_csv(logfile, index_col=0)

    depth_top = log_data['Depth_top'].iloc[0]
    depth_bot = log_data['Depth_bot'].iloc[1]
    bags = log_data['Bag'].unique().tolist()
    nlogged = len(log_data)

    print('Processing: %s' % logfile)

    print('Depth range: %.3f - %.3f' % (depth_top, depth_bot))
    print('Bags: ', bags)
    print('Number of pulses logged: %g' % nlogged)

    first_ic_vial, last_ic_vial = vial_range_prompt()
    nfilled = last_ic_vial - first_ic_vial + 1
    print('Number of vials filled: %g' % nfilled)
    print()

    if nfilled == nlogged:
        print('Nice, logged and filled number of vials match')
    else:
        print('WARNING, logged and filled number of vials DO NOT MATCH')
        print('logged:', nlogged)
        print('filled:', nfilled)
        sys.exit(1)

    ic_vials = np.arange(first_ic_vial, last_ic_vial + 1)

    log_data['IC_Vial'] = np.arange(first_ic_vial, last_ic_vial + 1)
    print()
    print('Saving to: %s' % outfile)
    log_data.to_csv(outfile, index=True)
    print('done.')
