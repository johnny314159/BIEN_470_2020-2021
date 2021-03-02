import sys


path_to_part_file = sys.argv[1]
mafsInRegion = sys.argv[2]
path_alignment = sys.argv[3]

fid = open(path_alignment, 'w')
fid.write('orthologs regions\n')
fid.close()