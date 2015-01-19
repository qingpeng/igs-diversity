#! /usr/bin/env python
import sys, khmer
import argparse
import os
import screed

def main():
    parser = argparse.ArgumentParser(description="Reads coverage increase")
    
    parser.add_argument('hashname')
    parser.add_argument('output')
    parser.add_argument('input_filename')

    args = parser.parse_args()
    hashfile = args.hashname
    histout = args.output
    filename = args.input_filename
    print filename
    outfp = open(histout, 'w')

    print 'hashtable from', hashfile
    ht = khmer.load_counting_hash(hashfile)
    count = 0
    for n, record in enumerate(screed.open(filename)):
        if n > 0 and n % 100000 == 0:#100000
            print '...', n
            outfp.write('%d %d %f\n' % (n, count, float(count)/n))

        seq = record.sequence.replace('N', 'A')
        med, _, _ = ht.get_median_count(seq)
        if med > 0:
            count = count + 1

    outfp.close()

if __name__ == '__main__':
    main()
