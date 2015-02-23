# 3	0	0	1
# 4	0	0	1
# 5	0	0	1
# 6	0	0	1
# 7	0	0	1
# 8	0	0	1
# 9	0	0	1
# 10	0	0	1
# 11	0	0	1
# 12	0	0	1
# 13	0	0	1
# 14	0	0	1
# 15	0	0	1
# 16	0	0	1
# 17	0	0	1
# 18	0	0	1
# 19	0	0	1
# 
# 4203559	9	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
# 4203560	9	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
# 4203561	9	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0

from skbio.diversity.beta import pw_distances
import numpy as np
from pandas import DataFrame, read_csv
import sys

file_igs = sys.argv[1]
file_list = sys.argv[2]
file_out = sys.argv[3]

file_out_obj = open(file_out,'w')


ids=[]
file_list_obj = open(file_list,'r')
for line in file_list_obj:
     line = line.rstrip()
     ids.append(line)


df = read_csv(file_igs,delim_whitespace=True,header=0) # with header!!
# for GOS data, header=None
# 
data=[]


for i in range(1,len(ids)+1):
     data.append(df[list(df.columns.values)[i]])

print(data)
 
 
bc_dm = pw_distances(data, ids, "braycurtis")

print(bc_dm)

for id in ids:
    d_string = id
    for d in bc_dm[id]:
        d_string = d_string + ' ' + str(d)
    file_out_obj.write(d_string+'\n')
    

        



