#!/usr/bin/env python
"""
Get number of reads that can be "mapped" to different reference genomes using
graph mapping method.
"""



ref_list = pd.read_csv('ref.list',header=None)[0]
comb_list = pd.read_csv('comb.list',header=None)[0]

name_list = ['read_id'] + list(ref_list)

result_frame = DataFrame(np.arange(len(ref_list)
      *len(comb_list)).reshape((len(comb_list),len(ref_list))), 
                         index=comb_list, columns = ref_list)

for file_comb in list(comb_list):
        frame = pd.read_csv(file_comb, sep='\s+', names=name_list )
        for ref_id in ref_list:
            filtered_frame = frame[frame[ref_id]>0]
            result_frame[ref_id][file_comb] = len(filtered_frame.index)

result_frame.index.name = 'read_name'
