import sys, time
import os
fname = sys.argv[1]

print('fname:', fname)

# get chromosome name
chrom = open(fname).readlines()[0].split()[0]
print('chrom:', chrom)

dir_tag = 'temp_dir_'+str(time.time())
print('dir_tag:', dir_tag)

# create non-overlapping file
cmd = 'python ./phylo_utils/utils/just_create_parts.py ' + fname + ' ' + chrom + ' ' + dir_tag
os.system(cmd)

# run mafsInRegion for all parts file
# e.g. part file: temp_dir/chr5-part-1.data
# e.g. path_alignment: 100WayAlignment/chromosome.anc.
cmd = 'python ./phylo_utils/utils/just_create_mafs.py ' + \
      dir_tag+'/'+chrom+'-part-1.data mafsInRegion ' + \
      dir_tag+'/'+chrom+'-part-1.data.maf'

os.system(cmd)

# collect the mafs
cmd = 'python ./phylo_utils/utils/just_collect_mafs.py '+\
      dir_tag+'/'+chrom+'-part-1.data.maf ' + \
      dir_tag+'/'+chrom+'-part-1.data ' + \
      dir_tag+'/'+chrom+'-part-1.data.out'
os.system(cmd)

# we need to run from 2 to 3 for N number of times
#for item in range(31):
#2 run RNATracker
cmd = 'python ./RNATracker/pred_rna_tracker.py ./toy-data/out_name.txt ./RNATracker/m.pth ./toy-data/output-rnatracker.csv'
os.system(cmd)

# format the rnatracker output to phyloPGM input
pred_data='./toy-data/output-rnatracker.csv'
pgm_input='./toy-data/input-phyloPGM.csv'
# may replace it with complete tree
info_tree='./phyloPGM/tree.pkl'
cmd='python ./scripts/create_phyloPGM_input.py '+pred_data+' '+pgm_input+' '+info_tree+' 1000'
os.system(cmd)

#3 run phyloPGM
pgm_output='./toy-data/df-pgm.csv'
cmd = 'python ./phyloPGM/expt_rna.py ./toy-data/df-train-100.csv '+pgm_input+' '+info_tree+' '+pgm_output+' 0.1'
os.system(cmd)

# run the tree visualization
cmd='python ./scripts/make_tree_and_bar.py '+pgm_output
os.system(cmd)
























