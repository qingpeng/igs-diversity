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
    
    optimal03 = open(file_sample+".optimal",'r').readlines()[6].split()
    
    
    # load into hashtable
    command_load = "python "+IGS_PATH+"/scripts/load-into-counting-force.py --ksize 20 --n_tables "+optimal03[1]+" --min-tablesize "+optimal03[2] +" " + file_sample+".ht "+file_sample
    print command_load
    subprocess.call(command_load,shell=True)
    
preprocess_reads(sample)
    