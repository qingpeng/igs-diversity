#! /usr/bin/env python
import sys, khmer
import argparse
import os
import screed

def main():
    parser = argparse.ArgumentParser(description="Output k-mer abundance distribution.")
    
    parser.add_argument('hashname')
    parser.add_argument('histout')
    parser.add_argument('input_filenames', nargs='+')

    args = parser.parse_args()
    hashfile = args.hashname
    histout = args.histout
    filenames = args.input_filenames

    outfp = open(histout, 'w')

    print 'hashtable from', hashfile
    ht = khmer.load_counting_hash(hashfile)

    hist = {}
    
    for n, filename in enumerate(filenames):
        print 'consuming input', filename

        for n, record in enumerate(screed.open(filename)):
            if n > 0 and n % 100000 == 0:
                print '...', n

            seq = record.sequence.replace('N', 'A')
            med, _, _ = ht.get_median_count(seq)

            hist[med] = hist.get(med, 0) + 1

    maxk = max(hist.keys())

    for i in range(maxk + 1):
        outfp.write('%d %d\n' % (i, hist.get(i, 0)))
    outfp.close()

if __name__ == '__main__':
    main()
