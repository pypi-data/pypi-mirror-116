'''
Coi


Example:

'''

import os
import sys
import csv
import argparse
import subprocess
import pkg_resources
from itertools import chain
from pathlib import Path
import glob



def main(argv=None):
    p = argparse.ArgumentParser(prog='coi',
                                formatter_class=argparse.RawTextHelpFormatter,
                                description=__doc__)

    version = pkg_resources.require('coi')[0].version
    p.add_argument('-v',
                   '--version',
                   action='version',
                   version=f'%(prog)s {version}')

    args = p.parse_args()

if __name__ == '__main__':
    main()  # pragma: no cover
