# get alpha estimation like metagenome size
# based on number of IGS, 
# size of metagenome = # of IGS * read_length



from pandas import DataFrame, read_csv
import numpy as np
from skbio.diversity.alpha import *
import sys

file_alpha = sys.argv[1]
reads_length = sys.argv[2]
file_out = sys.argv[3]

df = read_csv(file_alpha,header = 0,index_col=0,sep='\t')

def alpha(df):
    alpha_df = DataFrame(columns = ["observed_IGS","ace","goods_coverage","simpson_evenness","estimated_genome_size"] )
    for column in df.columns:
        sample = df[column]
        alpha_df.loc[column] =    [observed_otus(sample),ace(sample),goods_coverage(sample),simpson_e(sample),
ace(sample)*(int(reads_length))]
    return alpha_df   

alpha_df = alpha(df)
alpha_df.to_csv(file_out,index_label="sample")



