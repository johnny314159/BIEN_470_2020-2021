"""Creates ortholog mafs
Input: Bed file 4 fields (chr start end tag)
Ouput: Bed file 4 fields in csv format (region,species,sequence,tag)
email: zaifyahsan@gmail.com
(c) Faizy Ahsan
"""

# time /home/zaify/scratch/final-csail-data/cnn.csail.mit.edu/mafsInRegion \
# -outDir $pname out-$chr-$part ~/scratch/100WayAlignment/$chr.anc.maf.fixed
#
# time /home/zaify/scratch/final-csail-data/cnn.csail.mit.edu/mafsInRegion  \
# $p maf-$p ~/scratch/100WayAlignment/$chr.anc.maf.fixed

import pandas as pd
import os, re
from os import path
import numpy as np
from tqdm import tqdm
# import swifter

class Extractor:
    '''
    Extract ancestral/extant orthologs
    '''
    def __init__(self,
                 input_bed='',
                 path_to_mafsinregion='',
                 pth_alignments='',
                 temp_dir=''
                 ):
        '''

        :param input_bed: path to tab separated bed file, 4 fields (chr start end tag)
                    (tag contains label e.g. chr1:start-end-label), str
        '''
        self.df = pd.read_csv(input_bed, sep='\t', header=None) if input_bed!='' else []
        # path_to_mafsinregion = '/home/zaify/scratch/final-csail-data/cnn.csail.mit.edu/mafsInRegion'
        self.path_to_mafsinregion = path_to_mafsinregion
        self.pth_alignments = pth_alignments
        self.temp_dir = temp_dir
        if self.temp_dir != '':
            # create temp dir
            os.system('mkdir -p ' + self.temp_dir)

    def extract(self, out_fname):
        '''

        :param out_fname:
        :return:
        '''

        chr_list = ['chr' + str(i) for i in range(1, 23)] + ['chrX', 'chrY']

        # # create temp dir
        # os.system('mkdir -p ' + self.temp_dir)

        # separate chromosomes
        for chr in chr_list:
            df_chr = self.df[self.df[0] == chr]
            if df_chr.shape[0] == 0:
                continue

            print('Working on', chr)

            # create non overlapping intervals
            num_files = self.create_parts(df_chr, path.join(self.temp_dir, chr))
            # # create maf regions
            # for i in tqdm(range(1, num_files+1)):
            #     self.create_mafs(pth=path.join(self.temp_dir, chr+'-part-' + str(i) + '.data'),
            #                      pth_alignments=path.join(self.pth_alignments, chr+'.anc.maf.fixed'),
            #                      )
            # print('Done. maf creations')
            # collect maf regions
            for i in tqdm(range(1, num_files+1)):
                self.collect_mafs(maf_name=path.join(self.temp_dir, chr+'-part-' + str(i) + '.data.maf'),
                                  part_name=path.join(self.temp_dir, chr+'-part-' + str(i) + '.data'),
                                  out_name=path.join(self.temp_dir, chr+'-part-' + str(i) + '.data.out')
                                  )
            print('Done. maf collections')


        # put collected maf regions in one place
        cmd = 'cat '+path.join(self.temp_dir, '*.out')+' > '+out_fname
        os.system(cmd)
        print('Extracted regions are in', out_fname)

        return

    def create_parts(self, df_chr=None, pth='', batch_size=100000):
        '''

        :param df_chr: pandas df
        :param pth: path to output non-overlapping files, str
        :return: counter: number of non-overlapping files, int
        '''

        def get_batch(iterable, n=1):
            l = len(iterable)
            for ndx in range(0, l, n):
                yield iterable[ndx:min(ndx + n, l)]

        counter = 1
        while True:
            # print('\n')
            # print('df_chr:', df_chr.shape)
            df_chr = df_chr.sort_values(1)
            df_chr.index = list(range(df_chr.shape[0]))
            # print('df_chr index:', df_chr.index)
            full_indices = set(range(df_chr.shape[0]))
            overlapping_indices = set()
            prev_end = -np.inf
            for index, row in df_chr.iterrows():
                curr_start = row[1]
                curr_end = row[2]
                if curr_start <= prev_end:
                    overlapping_indices.add(index)
                else:
                    prev_end = curr_end
            non_overlapping_indices = list(full_indices - overlapping_indices)

            print('overlapping:', len(overlapping_indices))
            print('non overlapping:', len(non_overlapping_indices))
            # exit(1)

            # print('overlapping indices:', len(overlapping_indices))
            if len(overlapping_indices) < 1:
                df_chr.sort_values(1).to_csv(pth + '-part-' + str(counter) + '.data',
                                             index=False,
                                             header=None,
                                             sep='\t'
                                             )
                break

            # create part files with non overlapping
            if df_chr.loc[non_overlapping_indices, :].shape[0] < batch_size:
                df_chr.loc[non_overlapping_indices, :].sort_values(1).to_csv(pth + '-part-' + str(counter) + '.data',
                                                                             index=False,
                                                                             header=None,
                                                                             sep='\t'
                                                                             )
                counter += 1
            else:
                for batch_counter, batch_ids in enumerate(get_batch(non_overlapping_indices, batch_size)):
                    df_chr.loc[batch_ids, :].sort_values(1).to_csv(pth + '-part-' + str(counter) + '.data',
                                                               index=False,
                                                               header=None,
                                                               sep='\t'
                                                               )
                    counter += 1

            # update df as overlapping
            df_chr = df_chr.loc[overlapping_indices, :]

        return counter

    def create_mafs(self, pth='', pth_alignments=''):
        '''

        :param pth: path to non-overlapping bed files, str
        :param chr: chromosome e.g. chr1, str
        :return:
        '''

        cmd = self.path_to_mafsinregion+' '+pth+' '+pth+'.maf'+' '+pth_alignments
        os.system(cmd)
        return

    def collect_mafs(self, maf_name, part_name, out_name):
        '''

        :param maf_name:
        :param part_name:
        :return:
        '''

        # print('maf_name:', maf_name,
        #       'part_name:', part_name,
        #       'out_name:', out_name
        #       )

        def process_seq(seq):
            seq = seq.upper()
            seq = re.sub('[^ACGT]', '', seq)
            return seq

        fid = open(out_name, 'w')

        part_lines = pd.read_csv(part_name,
                                 header=None,
                                 sep='\t'
                                 )
        # part_lines['custom_tag'] = part_lines.swifter.apply(
        #     lambda x: x[0] + ':' + str(x[1]) + '-' + str(x[2]) + '-' + x[3].split('-')[-1],
        #     axis=1)

        curr_end = -1
        curr_start = -1
        tag = -1
        new_region = False
        table = {}

        ctr = 0

        for line in open(maf_name):

            if line[0] != 's':
                continue

            line = line.strip().split()
            sp = line[1]
            curr_sp = sp.split('.')[0].replace('_', '')

            start = int(line[2])
            size = int(line[3])
            seq = process_seq(line[-1])

            # print('line:', line)
            # print('start:', start, 'size:', size, 'curr_sp:', curr_sp, 'seq:', seq)
            # print('tag:', tag, 'curr_end:', curr_end, 'new_region:', new_region)
            # # exit(0)

            # check if current start is start

            if curr_sp == 'hg38':
                if tag == -1:
                    req_loc = part_lines[part_lines[1] >= start].iloc[0, :].values
                    # print('rec_loc:', req_loc);  #exit(0)
                    tag = '-'.join(req_loc[3:])
                    curr_start = int(req_loc[1])
                    curr_end = int(req_loc[2])
                    # print('tag:', tag)
                    # print('curr_start:', curr_start)
                    # print('curr_end:', curr_end); #exit(0)
                if start > curr_end or start < curr_start:
                    new_region = True

            if new_region and curr_sp == 'hg38':
                for k, v in table.items():
                    # logging.debug('%s,%s,%s,%s', tag, k, v, len(v))
                    # print(tag, k, v, str(len(v)))
                    fid.write(tag+','+k+','+v+','+str(len(v))+'\n')
                # if len(table)>1:
                #     exit(0)
                # print('Done. line:', curr_part_line)
                # find the tag
                req_loc = part_lines[part_lines[1] >= start].iloc[0, :].values
                # print('rec_loc:', req_loc); #exit(0)
                tag = '-'.join(req_loc[3:])  # part_lines.iloc[curr_part_line, 3:].values)
                # curr_end = int(tag.split('-')[-2])
                # curr_start = int(tag.split('-')[-3].split(':')[-1])
                curr_start = int(req_loc[1]);
                curr_end = int(req_loc[2])
                # # exit(0)
                # print('tag:', tag)
                # print('curr_start:', curr_start)
                # print('curr_end:', curr_end);

                table = {}
                new_region = False

            if curr_sp in table.keys():
                table[curr_sp] += seq
            else:
                table[curr_sp] = seq

            # print(start+size, curr_end, curr_sp, table) ; exit(0)
            if curr_sp == 'hg38':
                if start + size == curr_end:
                    new_region = True
                    # curr_part_line += 1

            # exit(0)

            # if ctr == 20:
            #     exit(0)
            # ctr += 1

        for k, v in table.items():
            # logging.debug('%s,%s,%s,%s', tag, k, v, len(v))
            fid.write(tag + ',' + k + ',' + v + ','+ str(len(v)) + '\n')

        # print('Done. line:', curr_part_line)

    def remove_temp_dir(self):
        os.system('\\rm -rf '+ self.temp_dir)
