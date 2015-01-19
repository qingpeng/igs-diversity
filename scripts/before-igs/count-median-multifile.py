#! /usr/bin/env python
"""
Count the median/avg k-mer abundance for each sequence in the input file,
based on the k-mer counts in the given counting hash.  Can be used to
estimate expression levels (mRNAseq) or coverage (genomic/metagenomic).

% scripts/count-median.py <htname> <output> <input seqs> 

Use '-h' for parameter help.

The output file contains sequence id, median, average, stddev, and seq length.

NOTE: All 'N's in the input sequences are converted to 'G's.
"""
import sys, screed, os
import khmer
import argparse

###

def main():
    parser = argparse.ArgumentParser(description='Count k-mers summary stats for sequences')

    parser.add_argument('config_file')

    args = parser.parse_args()

    file_config = args.config_file
    
    f_config = open(file_config, 'r')
    lines = f_config.readlines()
    f_config.close()
    
    htfiles = lines[0].split()
    filenames = lines[1].split()
    
    for htfile in htfiles:
    
    
    print 'loading counting hash from', htfile
    ht = khmer.load_counting_hash(htfile)
    K = ht.ksize()

    print 'writing to', output_filename
    output = open(output_filename, 'w')
    
    for n, input_filename in enumerate(filenames):
        print 'consuming input', input_filename
        for record in screed.open(input_filename):
            seq = record.sequence.upper()
            if 'N' in seq:
                seq = seq.replace('N', 'G')

            if K <= len(seq):
                a, b, c = ht.get_median_count(seq)
                print >>output, record.name, a, b, c, len(seq)

if __name__ == '__main__':
    main()
