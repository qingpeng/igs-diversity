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
    
    matrix1 = {}
    matrix2 = {}
    set_x = set()
    set_y = set()
    for n, record in enumerate(screed.open(file1)):
        if n > 0 and n % 100000 == 0:#100000
            print '...', n, file1
        seq = record.sequence.replace('N', 'A')
        med1, _, _ = ht1.get_median_count(seq)
        set_x.add(med1)
        med2, _, _ = ht2.get_median_count(seq)
        set_y.add(med2)
        key = str(med1)+'-'+str(med2)
        matrix1[key] = matrix1.get(key,0) + 1

    for n, record in enumerate(screed.open(file2)):
        if n > 0 and n % 100000 == 0:#100000
            print '...', n, file2
        seq = record.sequence.replace('N', 'A')
        med1, _, _ = ht1.get_median_count(seq)
        set_x.add(med1)
        med2, _, _ = ht2.get_median_count(seq)
        set_y.add(med2)
        key = str(med1)+'-'+str(med2)
        matrix2[key] = matrix2.get(key,0) + 1

    for x in range(max(list(set_x))):
        for y in range(max(list(set_y))):
            to_print = str(x)+'-'+str(y)+' '+ \
            str(matrix1.get(str(x)+'-'+str(y),0))+' '+ \
            str(matrix2.get(str(x)+'-'+str(y),0))+' '+ \
            str(matrix1.get(str(x)+'-'+str(y),0)+matrix2.get(str(x)+'-'+str(y),0))+'\n'
            
            outfp.write(to_print)
    outfp.close()
    

if __name__ == '__main__':
    main()
