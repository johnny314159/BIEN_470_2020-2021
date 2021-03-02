
# from fastBoostInference import Booster
from BoostInference_no_parallelization import Booster
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import sys


if len(sys.argv) < 6:
    print('python file.py input_val input_test tree.pkl df_pgm alpha')
    exit(0)

input_val = sys.argv[1]
input_test = sys.argv[2]
tree_fname = sys.argv[3]
df_pgm_name = sys.argv[4]
alpha = float(sys.argv[5])

df_val = pd.read_csv(input_val, index_col=0).astype(float)
df_test = pd.read_csv(input_test, index_col=0).astype(float)

print('df_val:', df_val.shape)
print('df_test:', df_test.shape)

tree = pickle.load(open(tree_fname, 'rb'))

train_size = df_val.shape[0]
num_pos_train = df_val[df_val['y']==1].shape[0]
test_size = df_test.shape[0]

print('train_size:', train_size,
      'num_pos_train:', num_pos_train,
      'test_size:', test_size,
      )

model = Booster(df_val=df_val.copy(),
                df_test=df_test.copy(),
                tree=tree,
                alpha=alpha
                )

mod_df_test, pred = model.boost()
print('mod_df_test:', mod_df_test.shape)


mod_df_test.to_csv(df_pgm_name)

