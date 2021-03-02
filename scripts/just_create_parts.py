import sys, os

print('OK: just_create_parts.py')


fname = sys.argv[1]
chrom = sys.argv[2]
dir_tag = sys.argv[3]


# dir will be created under root
cmd = 'mkdir -p ' + dir_tag
os.system(cmd)

fid = open(dir_tag+'/'+chrom+'-part-1.data', 'w')
fid.write('OK: just_create_parts.py\n')
fid.close()