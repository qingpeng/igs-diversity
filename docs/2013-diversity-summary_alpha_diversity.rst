
Using IGS to do alpha-diversity
===============================

This notebook includes many experiments I have tried. Many of them did
not lead to meaningful results. But, this is how research works. :)

For the whole picture about doing diversity analysis to metagenomics
samples using IGS, please check:
http://nbviewer.ipython.org/github/qingpeng/2013-diversity/blob/master/notebook/2013-diversity-summary.ipynb

pipeline to do alpha diversity analysis of simulated ecoli reads dataset
------------------------------------------------------------------------

1. get simulated reads
~~~~~~~~~~~~~~~~~~~~~~

-  50X and 150X
-  1%, 2% and 0% error rate

git clone https://github.com/ctb/dbg-graph-null.git

e.coli\_reference.fa from 2013-khmer-counting repo

::

    python dbg-graph-null/make-reads.py -C 150 ~/Dropbox/Manuscript/2013-diversity/pipeline/e.coli_reference.fa  >e.coli_150x_0.01e_100.fa
    python dbg-graph-null/make-reads.py -C 50 ~/Dropbox/Manuscript/2013-diversity/pipeline/e.coli_reference.fa  >e.coli_50x_0.01e_100.fa
    python dbg-graph-null/make-reads.py -e 0.00 -C 50 ~/Dropbox/Manuscript/2013-diversity/pipeline/e.coli_reference.fa  >e.coli_50x_0.00e_100.fa
    python dbg-graph-null/make-reads.py -e 0.02 -C 50 ~/Dropbox/Manuscript/2013-diversity/pipeline/e.coli_reference.fa  >e.coli_50x_0.02e_100.fa

2. create graph file
~~~~~~~~~~~~~~~~~~~~

print\_load\_sh.sh:

::

    for i in *.fa; do echo load-into-counting.py -x 1e8 -k 20 $i.kh $i \&;  done

    bash print_load_sh.sh  >load-into-counting.sh
    bash load-into-counting.sh

3. generate config.txt for counting reads coverage spectrum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    [qingpeng@dev-intel14 Ecoli_Alpha]$ more config.txt 
    e.coli_150x_0.01e_100.fa.kh  e.coli_50x_0.00e_100.fa.kh  e.coli_50x_0.01e_100.fa.kh  e.coli_50x_0.02e_100.fa.kh
    e.coli_150x_0.01e_100.fa  e.coli_50x_0.00e_100.fa  e.coli_50x_0.01e_100.fa  e.coli_50x_0.02e_100.fa
    10000000000

4. count reads coverage spectrum across species for each reads file(get .comb)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    python ~/Dropbox/Manuscript/2013-diversity/scripts/get_comb_multi.py config.txt &

5. get .comb list file and get spectrum frequency across samples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    ls *.comb >comb.list
    python ~/Dropbox/Manuscript/2013-diversity/scripts/count_spectrum_freq_multiple_files.py comb.list e.coli.spectrum   

6. generate MAP file (prepare for QIIME run) (also used in seperate\_IGS.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

e.coli\_Map.txt:

::

    #SampleID   BarcodeSequence LinkerPrimerSequence    Description coverage  error_rate  file_name
    sampleA A   A   e.coli_150x_0.01e_100 150x  0.01  e.coli_150x_0.01e_100.fa.comb
    sampleB A   A   e.coli_50x_0.00e_100  50x 0.00  e.coli_50x_0.00e_100.fa.comb
    sampleC A   A   e.coli_50x_0.01e_100  50x 0.01  e.coli_50x_0.01e_100.fa.comb
    sampleD A A e.coli_50x_0.02e_100  50x 0.02  e.coli_50x_0.02e_100.fa.comb

7. get .IGS and .IGS\_abund files from \*.spectrum file, listing all the IGSs and get the IGS-abundance matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    python ~/Dropbox/Manuscript/2013-diversity/scripts/seperate_IGS.py e.coli.spectrum e.coli_Map.txt 

8. convert .IGS file to .biom format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    module load QIIME/1.7.0
    biom convert -i e.coli.spectrum.IGS -o e.coli.spectrum.IGS.biom --table-type="OTU table"

9. get summary from .biom file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    biom summarize-table -i  e.coli.spectrum.IGS.biom -o e.coli.spectrum.IGS.biom.summary.txt

    [qingpeng@dev-intel14 Ecoli_Alpha]$ more e.coli.spectrum.IGS.biom.summary.txt
    Num samples: 4
    Num observations: 260333
    Total count: 2105023
    Table density (fraction of non-zero values): 0.408
    Table md5 (unzipped): 6b71f7e4f1d3957fb47f669a0231de6f

    Counts/sample summary:
     Min: 310594.0
     Max: 1016129.0
     Median: 389150.000
     Mean: 526255.750
     Std. dev.: 287829.236
     Sample Metadata Categories: None provided
     Observation Metadata Categories: None provided

    Counts/sample detail:
     sampleB: 310594.0
     sampleC: 328731.0
     sampleD: 449569.0
     sampleA: 1016129.0

10. decide min max step for saturation curve, run .qsub with QIIME scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    qsub ~/Dropbox/Manuscript/2013-diversity/pipeline/e_coli_alpha_diversity.qsub

new method (treat each IGSs seperately totally) ------

From step 7:

treat IGSs in different seperately

7.  python
    ~/Dropbox/Manuscript/2013-diversity/scripts/seperate\_IGS\_for\_alpha.py
    e.coli.spectrum e.coli\_Map.txt

8.  biom convert -i e.coli.spectrum.IGS.alpha -o
    e.coli.spectrum.IGS.alpha.biom --table-type="OTU table"

9.  biom summarize-table -i e.coli.spectrum.IGS.alpha.biom -o
    e.coli.spectrum.IGS.alpha.biom.summary.txt
10. 

qsub
~/Dropbox/Manuscript/2013-diversity/pipeline/e\_coli\_alpha\_diversity\_for\_alpha\_biom.qsub

file:///Users/qingpeng/Google%20Drive/Dropbox/Manuscript/2013-diversity/Data/rare\_plot\_alpha/rarefaction\_plots.html

beginning of curve:

/mnt/home/qingpeng/Manuscript/2013-diversity/data/Ecoli\_Alpha/Begin\_curve

new method (removing low abundance k-emrs with filter\_abund.py firstly)
------------------------------------------------------------------------

filter-abund.py -C 2 e.coli\_50x\_0.00e\_100.fa.kh
e.coli\_50x\_0.00e\_100.fa -V filter-abund.py -C 2
e.coli\_50x\_0.01e\_100.fa.kh e.coli\_50x\_0.01e\_100.fa -V
filter-abund.py -C 2 e.coli\_50x\_0.02e\_100.fa.kh
e.coli\_50x\_0.02e\_100.fa -V

::

    DONE writing.
    processed 2319837 / wrote 2041907 / removed 277930
    processed 231983700 bp / wrote 167487805 bp / removed 64495895 bp
    discarded 27.8%
    output in e.coli_50x_0.01e_100.fa.abundfilt
    done loading in sequences
    DONE writing.
    processed 2319837 / wrote 1915430 / removed 404407
    processed 231983700 bp / wrote 144771412 bp / removed 87212288 bp
    discarded 37.6%
    output in e.coli_50x_0.02e_100.fa.abundfilt

::

    for i in *.fa.abundfilt; do echo load-into-counting.py -x 1e8 -k 20 $i.kh $i \&;  done >load-into-counting-abund.py
    bash load-into-counting-abund.py

config-abund.txt:

::

    e.coli_50x_0.01e_100.fa.abundfilt.kh  e.coli_50x_0.02e_100.fa.abundfilt.kh
    e.coli_50x_0.01e_100.abundfilt.fa  e.coli_50x_0.02e_100.abundfilt.fa
    10000000000

::

    [qingpeng@dev-intel14 Ecoli_Alpha]$ cat >get_comb_multi.qsub
    #!/bin/bash -login
    #PBS -l walltime=2:00:00,nodes=01:ppn=1,mem=5gb
    #PBS -q main
    #PBS -M qingpeng@gmail.com
    #PBS -m abe
    #PBS -A ged-intel11

    module load khmer
    module load screed
    cd $PBS_O_WORKDIR
    python ~/Dropbox/Manuscript/2013-diversity/scripts/get_comb_multi.py config-abund.txt
    ^C
    [qingpeng@dev-intel14 Ecoli_Alpha]$ qsub get_comb_multi.qsub



    [qingpeng@dev-intel10 Ecoli_Alpha]$ cat >comb-abund.list
    e.coli_50x_0.01e_100.fa.abundfilt.comb
    e.coli_50x_0.02e_100.fa.abundfilt.comb


    python ~/Dropbox/Manuscript/2013-diversity/scripts/count_spectrum_freq_multiple_files.py comb-abund.list e.coli-abund.spectrum

    [qingpeng@dev-intel10 Ecoli_Alpha]$ cat >e.coli_Map-abund.txt
    #SampleID   BarcodeSequence LinkerPrimerSequence    Description coverage    error_rate  file_name
    sampleE A   A   e.coli_50x_0.01e_100-abund  50x 0.01    e.coli_50x_0.01e_100.fa.abundfilt.comb
    sampleF A   A   e.coli_50x_0.02e_100-abund  50x 0.02    e.coli_50x_0.02e_100.fa.abundfilt.comb

    python ~/Dropbox/Manuscript/2013-diversity/scripts/seperate_IGS_for_alpha.py e.coli-abund.spectrum e.coli_Map-abund.txt
    biom convert -i e.coli-abund.spectrum.IGS.alpha -o e.coli-abund.spectrum.IGS.alpha.biom --table-type="OTU table"
    biom summarize-table -i e.coli-abund.spectrum.IGS.alpha.biom -o e.coli-abund.spectrum.IGS.alpha.biom.summary.txt

Prepare for plotting:

::

    cd Filter_Abund/
    ln -fs ../e.coli_Map-abund.txt .
    ln -fs ../e.coli-abund.spectrum.IGS.alpha.biom .
    qsub plot_curve.qsub

plotting in directory: rare\_plot\_alpha\_filter\_abund

Method 3: do error correction firstly!!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

in ~/Github/

::

    git clone https://github.com/ged-lab/khmer.git
    git remote add ged https://github.com/ged-lab/khmer.git
    source /mnt/home/qingpeng/env/bin/activate
    make
    make test

    export PYTHONPATH=~/Github/khmer

run alpha.sh

