#! /usr/bin/env python2
#
# This file is part of khmer, http://github.com/ged-lab/khmer/, and is
# Copyright (C) Michigan State University, 2009-2013. It is licensed under
# the three-clause BSD license; see doc/LICENSE.txt.
# Contact: khmer-project@idyll.org
#
# using bloom filter to count unique kmers
import khmer
import sys
import math

def estimate_optimal_with_N_and_f(N,f):
    Z = math.log(f,0.5)
    intZ = int(Z)
    if intZ == 0:
        intZ = 1
# formula 1 (best)
    H1 = int(-N/(math.log(1-f**(1/float(intZ)))))
    M1 = H1 * intZ
    f1 = (1-math.exp(-N/float(H1)))**intZ

    return intZ, H1,M1,f1

filename = sys.argv[1]
fileout = filename+'.optimal_hash'

K = int(sys.argv[2])  # size of kmer
HT_SIZE = int(sys.argv[3])  # size of hashtable
N_HT = int(sys.argv[4])  # number of hashtables

fileout_obj = open(fileout,'w')
ht = khmer.new_hashbits(K, HT_SIZE, N_HT)

ht.consume_fasta(filename)
fp_rate = khmer.calc_expected_collisions(ht)

n_kmers = ht.n_unique_kmers()

print str(n_kmers)+' unique kmers\n fp_rate:'+str(fp_rate)

Z1,H1,M1,f1 = estimate_optimal_with_N_and_f(n_kmers,0.3)
Z2,H2,M2,f2 = estimate_optimal_with_N_and_f(n_kmers,0.1)

fileout_obj.write(str(n_kmers)+' unique kmers\n')
fileout_obj.write(str(Z1)+' '+str(H1)+' '+str(Z2)+' '+str(H2)+' '+str(fp_rate)+'\n')

