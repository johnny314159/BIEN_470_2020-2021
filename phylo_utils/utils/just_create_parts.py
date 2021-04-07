
from phylo_utils import ExtractOrthologs
import sys, os
from os import path

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print('python file.py input_bed chr temp_dir batch_size')
        exit(0)

    input_bed = sys.argv[1]
    chrom = sys.argv[2]
    temp_dir = sys.argv[3]
    #batch_size = int(sys.argv[4])

    extract_obj = ExtractOrthologs.Extractor(input_bed=input_bed,
                                             temp_dir=temp_dir
                                             )

    extract_obj.df = extract_obj.df[extract_obj.df[0]==chrom]

    num_files = extract_obj.create_parts(extract_obj.df,
                                         path.join(temp_dir, chrom),
                                         #batch_size=batch_size

                                         )
    print('Done. creating non-overlapping files. num_files:', num_files)




