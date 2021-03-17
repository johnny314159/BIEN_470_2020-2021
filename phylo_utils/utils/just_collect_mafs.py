from phylo_utils import ExtractOrthologs
import sys
from os import path

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print('python file.py maf_name part_name out_name')
        exit(0)

    maf_name = sys.argv[1]
    part_name = sys.argv[2]
    out_name = sys.argv[3]

    extract_obj = ExtractOrthologs.Extractor()

    extract_obj.collect_mafs(maf_name=maf_name,
                             part_name=part_name,
                             out_name=out_name
                             )
    print('Done. Collecting maf regions')




