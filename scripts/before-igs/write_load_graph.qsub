import sys

file_in = open(sys.argv[1],'r')


for line in file_in:
    line = line.rstrip()
    qsubfile = line+'.qsub'
    f_qsub = open(qsubfile,'w')

    lines = '''
    
    
#!/bin/bash -login
#PBS -l walltime=30:00:00,nodes=1:ppn=4,mem=25g
#PBS -q main
#PBS -M qingpeng@gmail.com
#PBS -m abe
#PBS -A ged-intel11

module load khmer/1.0.1-rc2
module load screed

cd $PBS_O_WORKDIR
'''
    f_qsub.write(lines)
    write = "python /opt/software/khmer/1.0.1-rc2--GCC-4.4.5/scripts/load-graph.py --ksize 20 --n_tables 4 --threads 4 --min-tablesize 40e9  --no-build-tagset " + line + '.hashbits ' + line

    f_qsub.write(write)
    f_qsub.close()
    
    