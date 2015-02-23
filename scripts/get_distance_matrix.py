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



df = read_csv('GOS.freq.IGS',delim_whitespace=True,header=None)

data=[]
for i in range(1,45):
     data.append(df[i])
 


ids=[]
file_list_obj = open('comb.list','r')
for line in file_list_obj:
     line = line.rstrip()
     ids.append(line)

bc_dm = pw_distances(data, ids, "braycurtis")

print(bc_dm)



