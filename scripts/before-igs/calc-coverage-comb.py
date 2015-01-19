#! /usr/bin/env python
import sys, khmer
import argparse
import os
import screed

def main():
    parser = argparse.ArgumentParser(description="Get reads coverage matrix")
    
    parser.add_argument('hashname1')
    parser.add_argument('hashname2')
    parser.add_argument('hashname3')
    parser.add_argument('file1')
    parser.add_argument('file2')
    parser.add_argument('file3')
    parser.add_argument('output')

    args = parser.parse_args()
    hashname1 = args.hashname1
    hashname2 = args.hashname2
    hashname3 = args.hashname3
    output  = args.output
    file1 = args.file1
    file2 = args.file2
    file3 = args.file3
    outfp = open(output, 'w')

    print 'hashtable from', hashname1
    ht1 = khmer.load_counting_hash(hashname1)
    print 'hashtable from', hashname2
    ht2 = khmer.load_counting_hash(hashname2)
    print 'hashtable from', hashname3
    ht3 = khmer.load_counting_hash(hashname3)
    matrix1 = {}
    matrix2 = {}
    matrix3 = {}
#    set_x = set()
#    set_y = set()
    for file_n in [file1,file2,file3]:
        print 'reading reads file ',file_n
        for n, record in enumerate(screed.open(file_n)):
            if n > 0 and n % 100000 == 0:#100000
                print '...', n, file_n
            seq = record.sequence.replace('N', 'A')
            med1, _, _ = ht1.get_median_count(seq)
            med2, _, _ = ht2.get_median_count(seq)
            med3, _, _ = ht3.get_median_count(seq)
            to_print = str(med1)+' '+str(med2)+' ' +str(med3)+'\n'
            outfp.write(to_print)
    outfp.close()
    

if __name__ == '__main__':
    main()
