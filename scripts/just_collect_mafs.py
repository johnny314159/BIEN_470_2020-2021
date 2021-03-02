import sys


path_to_maf_file = sys.argv[1]
path_to_part_file = sys.argv[2]
path_to_out_file = sys.argv[3]

fid = open(path_to_out_file, 'w')
fid.write('output regions\n')
fid.close()