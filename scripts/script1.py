import sys, time
import os
fname = sys.argv[1]
#fname = '/var/www/html/BIEN_470_interference/src/server/uploads/dummy.bed'
#fname = '../scripts/dummy.bed'
# fname = '..//src/server/uploads/dummy.bed'
print('fname:', fname)

# get chromosome name
chrom = open(fname).readlines()[0].split()[0]
print('chrom:', chrom)

dir_tag = 'temp_dir_'+str(time.time())
print('dir_tag:', dir_tag)

# create non-overlapping file
# python file.py input_bed chr temp_dir batch_size
cmd = 'python phylo_utils/utils/just_create_parts.py ' + fname + ' ' + chrom + ' ' + dir_tag + ' 1000' 
os.system(cmd)
print('just create parts done in script1')

# run mafsInRegion for all parts file
# e.g. part file: temp_dir/chr5-part-1.data
# e.g. path_alignment: 100WayAlignment/chromosome.anc.
cmd = 'python phylo_utils/utils/just_create_mafs.py ' + \
      dir_tag+'/'+chrom+'-part-1.data ./phylo_utils/mafsInRegion ' + \
      '/var/www/html/BIEN_470_interference/100WayAlignment/' + chrom + '.anc.maf.fixed'

os.system(cmd)
print('just create mafs done in script1')

# collect the mafs
cmd = 'python phylo_utils/utils/just_collect_mafs.py '+\
      dir_tag+'/'+chrom+'-part-1.data.maf ' + \
      dir_tag+'/'+chrom+'-part-1.data ' + \
      dir_tag+'/'+chrom+'-part-1.data.out'
os.system(cmd)
print('just collect mafs done in script1')
#exit(0)

# we need to run from 2 to 3 for N number of times
#for item in range(31):
#2 run RNATracker

outname = dir_tag + '/' + chrom + '-part-1.data.out'
rna_output = dir_tag + '/output-rnatracker.csv'
#cmd = 'python ./RNATracker/pred_rna_tracker.py ' + outname + ' ./RNATracker/10_PARCLIP_ELAVL1A_hg19/base_model.pth ' + rna_output
cmd = 'python ./RNATracker/pred_rna_tracker.py ' + outname + ' ./RNATracker/m.pth ' + rna_output

os.system(cmd)
print('done RNA tracker in script1')

# format the rnatracker output to phyloPGM input
pred_data= rna_output
pgm_input= dir_tag + '/input_phyloPGM.csv'



# may replace it with complete tree
info_tree='./phyloPGM/tree.pkl'
cmd='python ./scripts/create_phyloPGM_input.py '+pred_data+' '+pgm_input+' '+info_tree+' 1000'
os.system(cmd)
print('done format input for PhyloPGM in script1')


#3 run phyloPGM
pgm_output=  dir_tag + '/df-pgm.csv'
cmd = 'python ./phyloPGM/expt_rna.py ./toy-data/df-train-100.csv '+pgm_input+' '+info_tree+' '+pgm_output+' 0.1'
os.system(cmd)
print('done phyloPGM in script1')


# run the tree visualization
cmd='python ./scripts/make_tree_and_bar.py '+pgm_output
os.system(cmd)
print('done tree visualization in script1')

## Add specific print command to be picked up by React?


## remove the temp dir
#cmd='\rm -rf ' + dir_tag
#os.system(cmd)
#print('temporary directory removed')



















