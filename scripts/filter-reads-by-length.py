#! /usr/bin/env python2
#
# This file is part of khmer, http://github.com/ged-lab/khmer/, and is
# Copyright (C) Michigan State University, 2009-2013. It is licensed under
# the three-clause BSD license; see doc/LICENSE.txt.
# Contact: khmer-project@idyll.org
#
"""
Accept or discard sequences XXX, based on the given counting
hash table.  Output sequences will be placed in 'infile.medfilt'.

% python sandbox/filter-median.py <counting.ct> <data1> [ <data2> <...> ]

Use '-h' for parameter help.
"""
import sys
import screed.fasta
import os
import khmer
from khmer.thread_utils import ThreadedSequenceProcessor, verbose_loader
import argparse
import random

###

DEFAULT_LENGTH = 65


def main():
    parser = argparse.ArgumentParser(description='XXX')
    parser.add_argument('--length', '-L', dest='length',
                        default=DEFAULT_LENGTH, type=int)

    parser.add_argument('input_filenames', nargs='+')

    args = parser.parse_args()

    infiles = args.input_filenames



    # the filtering function.
    def process_fn(record):
        name = record['name']
        seq = record['sequence']

        if len(seq) < args.length:
            return None, None

        return name, seq

    # the filtering loop
    for infile in infiles:
        print 'filtering', infile
        outfile = os.path.basename(infile) + '.length_filter'
        outfp = open(outfile, 'w')

        tsp = ThreadedSequenceProcessor(process_fn)
        tsp.start(verbose_loader(infile), outfp)

        print 'output in', outfile

if __name__ == '__main__':
    main()
