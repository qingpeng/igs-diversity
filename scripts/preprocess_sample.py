import os
import subprocess
import sys

sample = sys.argv[1]

KHMER_PATH = sys.argv[2]
IGS_PATH = sys.argv[3]


#KHMER_PATH = "~/GDrive/Development/Github/khmer"
#IGS_PATH = "~/GDrive/Development/Github/igs-diversity"
    
# preprocess reads file for a sample and load into hashtable.

def preprocess_reads(file_sample):
    
    #subprocess.call("source ~/GDrive/Development/env_for_khmer/bin/activate", shell = True)
        

    
    # estimate optimal for original reads
    command_optimal_1 = "python "+KHMER_PATH+"/sandbox/optimal_args_HLL.py --ksize 20 "+file_sample+" -R "+file_sample+".optimal"
    print command_optimal_1
    subprocess.call(command_optimal_1,shell=True)
    
    optimal01 = open(file_sample+".optimal",'r').readlines()[6].split()
    
    # correct error
    command_correct = "python "+KHMER_PATH+"/sandbox/correct-errors.py --ksize 20 --n_hashes "+optimal01[1]+" --hashsize "+optimal01[2] +" " + file_sample
    print command_correct
    subprocess.call(command_correct,shell=True)
    
    # trimming reads not working for low coverage data set.
#    command_trim = "python "+KHMER_PATH+"/sandbox/trim-low-abund.py --ksize 20 --n_hashes "+optimal01[1]+" --hashsize "+optimal01[2] +" " + file_sample+".corr"
#    print command_trim
#    subprocess.call(command_trim,shell=True)
    
    
    # filter reads by length
    command_filter = "python "+IGS_PATH+"/scripts/filter-reads-by-length.py --length 65 "+ file_sample+".corr"
    print command_filter
    subprocess.call(command_filter,shell=True)
    
    # estimate optimal for processed reads
    command_optimal_2 = "python "+KHMER_PATH+"/sandbox/optimal_args_HLL.py --ksize 20 "+file_sample+".corr.length_filter"+" -R "+file_sample+".corr.length_filter.optimal"
    print command_optimal_2
    subprocess.call(command_optimal_2,shell=True)
    
    
    optimal03 = open(file_sample+".corr.length_filter.optimal",'r').readlines()[8].split()
    
    # load into hashtable
    command_load = "python "+IGS_PATH+"/scripts/load-into-counting-force.py --ksize 20 --n_tables "+optimal03[1]+" --min-tablesize "+optimal03[2] +" " + file_sample+".corr.length_filter.ht "+file_sample+".corr.length_filter"
    print command_load
    subprocess.call(command_load,shell=True)
    
    
preprocess_reads(sample)
    