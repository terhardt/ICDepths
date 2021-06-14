# ICDepths

Small application to merge IC vial collection notes with CFA log files

This commandline application currently handles the two most common cases for the
log files:

- Number of vials logged and number of vials noted down agree (all good)
- Pulses where missed by the autosampler and a vial gets twice the amount it
  should have (merge vial with next)

All other cases need to be handled manually at the moment.

## Usage

The script can be called with only the path to a log file as an arguement and
all other information can be entered interactively.

Other usage cases can be found in the help of the script when called with the
`python icdepth.py -h` commandline argument:

    usage: icdepth.py [-h] [--vials VIAL VIAL] [-o O] [--outdir OUTDIR] vial_info_file

    Script to add AWI IC-vial numbers to Bern CFA logfiles

    This script should be used to re-concile Bern CFA logfiles and the notes
    taken during the fraction collection itself.

    positional arguments:
      vial_info_file     Vial info file produced from Bern CFA data

    optional arguments:
      -h, --help         show this help message and exit
      --vials VIAL VIAL  Vial range logged for file
      -o O               Overwrite if output is existing
      --outdir OUTDIR    Output directory for pricessed files (default: output)


The output files are saved in a specified directory (default: output) and
overwriting of existing output files needs to be explicitly allowed with the
`-o` commandline flag.
