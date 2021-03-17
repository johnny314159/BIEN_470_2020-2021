from phylo_utils import ExtractOrthologs
import sys

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print('python file.py path_to_non_overlapping_bed path_to_mafsinregion path_alignments')
        exit(0)

    input_bed = sys.argv[1]
    path_to_mafsinreion = sys.argv[2]
    alignments = sys.argv[3]
    # temp_dir = sys.argv[4]

    extract_obj = ExtractOrthologs.Extractor(path_to_mafsinregion=path_to_mafsinreion,
                                             )

    extract_obj.create_mafs(pth=input_bed,
                            pth_alignments=alignments
                            )
    print('Done. creating maf files.')




