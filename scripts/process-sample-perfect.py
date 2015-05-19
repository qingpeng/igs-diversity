import os
import subprocess
import sys

# using big hash table, and no adjustment
# 
sample_list = sys.argv[1]
memory = sys.argv[2]
error_rate = sys.argv[3]

KHMER_PATH = "~/GDrive/Development/Github/khmer"
IGS_PATH = "~/GDrive/Development/Github/igs-diversity"
    
# preprocess reads file for a sample and load into hashtable.

def preprocess_reads(file_sample):
    
    #subprocess.call("source ~/GDrive/Development/env_for_khmer/bin/activate", shell = True)
        

    
    # estimate optimal for original reads
    command_optimal_1 = "python "+KHMER_PATH+"/sandbox/optimal_args_HLL.py --ksize 19 "+file_sample+" -R "+file_sample+".optimal"
    print command_optimal_1
    subprocess.call(command_optimal_1,shell=True)
    
    optimal03 = open(file_sample+".optimal",'r').readlines()[6].split()
    
    
    # load into hashtable
    command_load = "python "+IGS_PATH+"/scripts/load-into-counting-force.py --ksize 19 --n_tables 2 --min-tablesize 100000000"+" " + file_sample+".ht "+file_sample
    print command_load
    subprocess.call(command_load,shell=True)
    

for line in open(sample_list,'r'):
    sample = line.rstrip()
    print "processing",sample
    preprocess_reads(sample)
    

# run beta diversity analysis

fh_config = open("config.txt",'w')

ht_list = []
fa_list = []

for sample in open(sample_list,'r'):
    sample = sample.rstrip()
    print sample
    ht_list.append(sample+'.ht')
    fa_list.append(sample)

ht_list_line = " ".join(ht_list)
fa_list_line = " ".join(fa_list)

fh_config.write(ht_list_line+'\n')
fh_config.write(fa_list_line+'\n')
fh_config.write(str(memory)+'\n')
fh_config.write('100\n') # readlength
fh_config.write('19\n')#ksize
fh_config.close()

command_comb = "python "+IGS_PATH+"/scripts/get_comb_multi.py config.txt"
print command_comb
subprocess.call(command_comb,shell=True)

subprocess.call("ls *.comb >comb.list",shell=True)


command_spectrum = "python "+IGS_PATH+"/scripts/count_spectrum_freq_multiple_files.py comb.list all_sample.spectrum"
print command_spectrum
subprocess.call(command_spectrum,shell=True)

command_seperate = "python "+IGS_PATH+"/scripts/seperate_IGS_species.py all_sample.spectrum ../../all_sample_MAP.txt"
print command_seperate
subprocess.call(command_seperate,shell=True)

command_dm = "python "+IGS_PATH+"/scripts/get_distance_matrix_v3.py all_sample.spectrum.species ../../all_sample_MAP.txt matrix.txt"
print command_dm
subprocess.call(command_dm,shell=True)

command_sep_alpha = "python "+IGS_PATH+"/scripts/seperate_IGS_for_alpha_no_adjustment.py.py all_sample.spectrum ../../all_sample_MAP.txt "+str(error_rate)
print command_sep_alpha
subprocess.call(command_sep_alpha,shell=True)

command_alpha = "python "+IGS_PATH+"/scripts/get_alpha.py all_sample.spectrum.IGS.alpha 100 alpha.txt"
print command_alpha
subprocess.call(command_alpha,shell=True)



