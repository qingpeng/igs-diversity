#! /usr/bin/env python
"""
Get the list of IGSs with abundance across samples and # of IGSs with different
coverage spectrum

% scripts/seperate_IGS.py <spectrum file> <MAP file>

Use '-h' for parameter help.

There are two output files - *.IGS_abund and *.IGS

Firstly, get the number of different IGSs by dividing sum of reads across 
samples with that coverage spectrum by sum of numbers in coverage spectrum.
For example, for a coverage spectrum like:

1-3-2-4 10 33 22 49

Theoretically, the ratio of the numbers of reads with that spectrum across samples
is similar to the ratio of the numbers in that coverage spectrum.

10:33:22:49 ~= 1:3:2:4

Here the number of different IGSs is calculated like this:

# of IGSs  = (10+33+22+49) / (1+3+2+4) = 11.4

Secondly, list all the IGSs with the coverage spectrum across samples in 
the table format that is a typical species-abundance matrix used in 
traditional ecology or OTU-abundance matrix used in 16s-based analysis.

The sample IDs in MAP file will be used as the header in .IGS file.



.spectrum file example:(generated by count_spectrum_freq_multiple_files.py)

0-0-0-1 0 0 0 87943
0-0-0-2 0 0 0 24609
0-0-0-3 0 0 0 1578
0-0-0-4 0 0 0 75
0-0-0-5 0 0 0 4
1-0-0-0 27040 0 0 0
1-0-0-1 10326 0 0 58349
1-0-0-2 765 0 0 33028
1-0-0-3 38 0 0 3167
1-0-0-4 4 0 0 217
1-0-0-5 0 0 0 14
1-0-0-6 0 0 0 3
1-0-1-0 13115 0 13115 0
1-0-1-1 5367 0 5367 22585


.IGS file example:

1       0       0       0       1
2       0       0       0       1
3       0       0       0       1
4       0       0       0       1
5       0       0       0       1
6       0       0       0       1
7       0       0       0       1
8       0       0       0       1
9       0       0       0       1
10      0       0       0       1
11      0       0       0       1


.IGS_abund example:

0-0-0-1 87943.0
0-0-0-2 12304.5
0-0-0-3 526.0
0-0-0-4 18.75
0-0-0-5 0.8
1-0-0-0 27040.0
1-0-0-1 34337.5
1-0-0-2 11264.3333333
1-0-0-3 801.25
1-0-0-4 44.2
1-0-0-5 2.33333333333
1-0-0-6 0.428571428571
1-0-1-0 13115.0
1-0-1-1 11106.3333333
1-0-1-2 3656.5
1-0-1-3 289.8

"""

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('spectrum')
parser.add_argument('map_file')

args = parser.parse_args()


file_in = args.spectrum
file_map = args.map_file

file_out1 = file_in + '.IGS_abund'
file_out2 = file_in + '.IGS'


file_in_o = open(file_in,'r')
file_map_o = open(file_map,'r')

file_out1_o = open(file_out1,'w')
file_out2_o = open(file_out2,'w')

file_map_o.readline()
ID_list = []
for line in file_map_o:
  line = line.rstrip()
  ID_list.append(line.split()[0])
  
to_print_IGS = '#OTU ID'+'\t'+'\t'.join(ID_list)+'\n'
file_out2_o.write(to_print_IGS) # write header  

IGS_count = 0


for line in file_in_o:
    line = line.rstrip()
    f1 = line.split()
    f2 = f1[0].split('-')
    sum_count = 0
    for freq in f1[1:]:
        sum_count = sum_count + int(freq)

    sum_spectr = 0
    for freq in f2:
        sum_spectr = sum_spectr + int(freq)
        
    if sum_spectr == 0:
        continue
        
    IGS_abundance =  sum_count/float(sum_spectr)
    file_out1_o.write(f1[0]+' '+str(IGS_abundance) + '\n')

    
    if int(IGS_abundance)>=1:
        for i in range(int(IGS_abundance)):
            IGS_count += 1
            new_spectr = '\t'.join(f2)
            file_out2_o.write(str(IGS_count)+'\t'+new_spectr+'\n')
            


        