# converts species predictions into dataframe
# Input: region,species,label, prediction_score
#        chr1:345-347, hg38, 0, 0.45
#        .....
# Output: _, species1, species2, ..., speciesn, y
#         chr1:345-347, 0.23, 0.42, ..., 0.21, 0
# email: zaifyahsan@gmail.com
# (c) Faizy Ahsan

import pandas as pd, numpy as np, pickle as pkl
import sys
import swifter
global df_req
from multiprocessing import Pool




def get_batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


if len(sys.argv) < 5:
    print('python file.py pred_data output_name info_tree batch_size')
    exit(1)

pred_data = sys.argv[1]
output_name = sys.argv[2]
info_tree = pkl.load(open(sys.argv[3], 'rb'))
batch_size = int(sys.argv[4])
total_species = len(info_tree)


# species_list = [item[0] for item in sorted(info_tree.items(), key=lambda x: x[1])]
species_list = list(info_tree.keys())


# # load pred data
# req_lines = []
# collected_line = ''
# for line in open(pred_data):
#     # print('line:', line)
#
#     if 'DEBUG' in line:
#         req_lines.append(collected_line)
#         collected_line = line.strip()
#     else:
#         collected_line += ' ' + line.strip()
#
# print('req_lines:', req_lines[:5])
#
# req_lines = [item.split(',') for item in req_lines if '[' in item and ']' in item]
#
# print('modified req_lines:', req_lines[:5])
#
#
# df = pd.DataFrame(req_lines)

chklines = open(pred_data).readlines()
if len(chklines) <= 1:
    exit(0)

df = pd.read_csv(pred_data,
                 # header=None,
                 sep=',',
                 index_col=0
                 )
print('df:', df.head())
print('df:', df.shape)
# exit(1)
# df.columns = ['region','species','label','pred']
df.columns = ['region','species','pred']
# df['region'] = df.region.apply(lambda x: x.split('root:')[1])
print('df:', df.head())

uniq_index = df['region'].unique()
# uniq_index = df[0].unique()

df_req = pd.DataFrame(index=uniq_index, columns=species_list) #+['y'])
# df_req.index = uniq_index
print('df_req:', df_req.shape)

df_group = df.groupby('region')

print('group done')


def mapper(ids):
    def reform(x):
        index = x.name
        # print('index:', index)
        # print('x:', x)
        # sub_df = df[df['hg38_location']==index].T.values
        sub_df = df_group.get_group(index).T.values
        curr_df.loc[index, sub_df[1]] = sub_df[-1]
        # curr_df.loc[index, 'y'] = sub_df[-2][0]
        return
    curr_df = pd.DataFrame(index=ids, columns=species_list) # + ['y'])
    curr_df.swifter.apply(reform,
                                    axis=1)
    # print('curr_df:', curr_df['hg38'])

    return curr_df


# n = 5000
list_ids = [uniq_index[i:i + batch_size] for i in range(0, len(uniq_index), batch_size)]

# print('list_ids:', list_ids)

p = Pool()
results = p.map(mapper, list_ids)

df_req = pd.concat(results)

# for item in results:
#     print(item)
# exit(1)
# print('check:', df_req.loc[uniq_index[-5], species_list].sum())
# print('check2:', df[df['hg38_location'] == uniq_index[-5]]['pred_phylocnn'].sum())

df_req.to_csv(output_name)
