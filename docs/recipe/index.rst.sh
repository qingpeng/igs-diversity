. ~/dev/ipy7/bin/activate
set -e

# create 9 simulated genomes.
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 1  > genomeA.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 2  > genomeB.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 3  > genomeC.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 4  > genomeD.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 5  > genomeE.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 6  > genomeF.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 7  > genomeG.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 8  > genomeH.fa
python ~/dev/nullgraph/make-random-genome.py -l 10000 -s 9  > genomeI.fa
ls sample_*.kh | awk '{ ORS=" "; print; }'>config.txt
printf "n" >>config.txt
ls sample_*.fa | awk '{ ORS=" "; print; }' >>config.txt
printf "n" >>config.txt
printf "30000000" >>config.txt
./python get_comb_multi.py config.txt
ls *.comb >comb.list
python count_spectrum_freq_multiple_files.py comb.list all_sample.spectrum
python seperate_IGS.py all_sample.spectrum all_sample_MAP.txt

biom convert -i  all_sample.spectrum.IGS -o all_sample.spectrum.IGS.biom --table-type="OTU table"
biom summarize-table -i all_sample.spectrum.IGS.biom -o all_sample.spectrum.IGS.biom.summary.txt
beta_diversity_through_plots.py -i all_sample.spectrum.IGS.biom -o bdiv_even1000/ -m all_sample_MAP.txt -e 1000 -p p_file.txt
make_2d_plots.py -i bdiv_even1000/bray_curtis_pc.txt -m all_sample_MAP.txt -o beta_2d_plots/
jackknifed_beta_diversity.py -i all_sample.spectrum.IGS.biom -o bdiv_jk1000 -e 1000 -m  all_sample_MAP.txt -p p_file.txt
make_bootstrapped_tree.py -m bdiv_jk1000/bray_curtis/upgma_cmp/master_tree.tre -s bdiv_jk1000/bray_curtis/upgma_cmp/jackknife_support.txt -o bdiv_jk1000/bray_curtis/upgma_cmp/jackknife_named_nodes.pdf
python seperate_IGS_for_alpha.py all_sample.spectrum all_sample_MAP.txt
echo "alpha_diversity:metrics chao1,observed_species" > alpha_params.txt
alpha_rarefaction.py -i all_sample.spectrum.IGS.alpha.biom -m all_sample_MAP.txt -o wf_arare/ -p alpha_params.txt -f
