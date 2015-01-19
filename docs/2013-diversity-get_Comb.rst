
Two approaches to get .comb files
=================================

There are two approaches to get .comb files, which is the coverage in
different samples of each read in a sample data set:

GS000a.fa.comb
~~~~~~~~~~~~~~

::

    JCVI_READ_838489 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_839879 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_839881 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_839880 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_839883 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_840623 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_840621 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    JCVI_READ_840620 0 2 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0

1. Using get\_comb\_multi.py script to get the .comb files directly.
--------------------------------------------------------------------

1.1 get graph file for each read file using load-into-counting.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.2 create the config.txt file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.3 run get\_comb\_multi.py script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    python ~/Dropbox/Manuscript/2013-diversity/scripts/get_comb_multi.py config.txt &

This approach is good to smaller datasets. All the graph files for all
the datasets will be loaded into memory altogether. For bigger datasets,
this may not be pratical or efficient.

2. Do pairwise counting firstly then generate the .comb files
-------------------------------------------------------------

This is more appropriate to bigger datasets.

-  Each time only load one graph file for one sample
-  can be parallelized on HPC

Here, use Methit data set as an example:

::

    python ~/Dropbox/Manuscript/2013-diversity/scripts/generate_count_list_for_comb.py |bash

run a bash script to submit the qsub for different list

::

    bash  ~/Dropbox/Manuscript/2013-diversity/scripts/rebuild_freq_table_stream.sh



    python ~/Dropbox/Manuscript/2013-diversity/scripts/count_spectrum_freq_multiple_files.py comb.list GOS.freq

Next: try to get the distance matrix from GOS.freq.IGS IGS table.

::

    python /mnt/home/qingpeng/Dropbox/Manuscript/2013-diversity/scripts/get_distance_matrix_v2.py GOS.freq.IGS comb.list matrix.out

