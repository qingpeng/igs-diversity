# HWI-ST957:262:H7B0HADXX:2:1101:2010:2056/1 30674 590 650 1009 714 551 12 114
# HWI-ST957:262:H7B0HADXX:2:1101:2010:2056/2 65535 872 757 901 65535 797 1068 863
# HWI-ST957:262:H7B0HADXX:2:1101:4103:2117/1 1 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:4103:2117/2 1 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:5460:2076/1 1 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:5460:2076/2 1 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:6043:2199/1 17 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:6043:2199/2 18 0 0 0 0 7 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:6849:2118/2 21 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:8384:2137/1 8 12 0 11 0 19 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:8748:2195/1 4 0 0 0 0 0 0 0
# HWI-ST957:262:H7B0HADXX:2:1101:8748:2195/2 3 0 0 0 0 0 0 0
# 
# 1 0 0 0 0 0 0 0

import sys

f_in = open(sys.argv[1],'r')

#filter = sys.argv[3]
f_out1 = open(sys.artv[3],'w')
f_out2 = open(sys.argv[4],'w')
#numbers = filter.split()

for read in screed.open(sys.argv[2]):
    line = f_in.readline()
    number = line.split()[1:]
    if int(number[2]) == 0 and int(number[3]) == 0 and int(number[1]) ==0 and int(number[0]) >0 and int(number[4])>0 and int(number[5])>0 and int(number[6])>0 and int(number[7])>0:
        f_out1.write('>'+read.name+'\n')
        f_out1.write(read.sequence+'\n')
    if int(number[2]) > 0 and int(number[3]) > 0 and int(number[1]) >0 and int(number[0]) ==0 and int(number[4]) ==0 and int(number[5]) ==0 and int(number[6]) ==0 and int(number[7]) ==0:
        f_out2.write('>'+read.name+'\n')
        f_out2.write(read.sequence+'\n')
    

