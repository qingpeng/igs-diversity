#! /usr/bin/env python
import sys, khmer
import argparse
import os
import screed

def main():
    parser = argparse.ArgumentParser(description="Get reads coverage matrix")
    
    parser.add_argument('hashname1')
    parser.add_argument('hashname2')
    parser.add_argument('file1')
    parser.add_argument('file2')
    parser.add_argument('output')

    args = parser.parse_args()
    hashname1 = args.hashname1
    hashname2 = args.hashname2
    output  = args.output
    file1 = args.file1
    file2 = args.file2
    outfp = open(output, 'w')

    print 'hashtable from', hashname1
    ht1 = khmer.load_counting_hash(hashname1)
    ht2 = khmer.load_counting_hash(hashname2)

    for n, record in enumerate(screed.open(file1)):
        if n > 0 and n % 100000 == 0:#100000
            print '...', n, file1
        seq = record.sequence.replace('N', 'A')
        med1, _, _ = ht1.get_median_count(seq)
        med2, _, _ = ht2.get_median_count(seq)
        to_print = record.name+' '+str(med1)+' '+str(med2)+'\n'
        outfp.write(to_print)

    for n, record in enumerate(screed.open(file2)):
        if n > 0 and n % 100000 == 0:#100000
            print '...', n, file2
        seq = record.sequence.replace('N', 'A')
        med1, _, _ = ht1.get_median_count(seq)
        med2, _, _ = ht2.get_median_count(seq)
        to_print = record.name+' '+str(med1)+' '+str(med2)+'\n'
        outfp.write(to_print)

    outfp.close()
    

if __name__ == '__main__':
    main()
