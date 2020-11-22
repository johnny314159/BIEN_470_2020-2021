
from BoostInference_round import Booster
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
num_pos_test = df_test[df_test['y']==1].shape[0]

print('train_size:', train_size,
      'num_pos_train:', num_pos_train,
      'test_size:', test_size,
      'num_pos_test:', num_pos_test
      )
# exit(0)

if num_pos_test==0.:
    exit(0)

model = Booster(df_val=df_val,
                df_test=df_test.iloc[:,:-1],  # do not send test labels
                tree=tree,
                alpha=alpha
                )

mod_df_test, pred = model.boost()
print('mod_df_test:', mod_df_test.shape)
mod_df_test['y'] = df_test['y']

# compute prior
prior_y1 = float(num_pos_train)/train_size
prior_y0 = 1.-prior_y1

# compute posterior
mod_df_test['posterior_preds'] = mod_df_test.pgm_pred.swifter.apply \
    (lambda x: ((prior_y1*np.exp(x))/((prior_y1*np.exp(x))+prior_y0))
     )

mod_df_test.to_csv(df_pgm_name)

# mod_df_test = pd.read_csv(df_pgm_name, index_col=0)
# pred = mod_df_test['pgm_pred'].values

def scikitlearn_calc_auPRC(y_true, y_score):
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    return auc(recall, precision)


base_auc = -10.
pgm_auc = -10.
pgm_posterior_auc=-10.

base_aupr = -10.
pgm_aupr = -10.
pgm_posterior_aupr=-10.

if num_pos_test > 0:
    base_auc = roc_auc_score(df_test['y'], df_test['hg38'])
    pgm_auc = roc_auc_score(df_test['y'], pred)
    pgm_posterior_auc = roc_auc_score(df_test['y'], mod_df_test['posterior_preds'])


    base_aupr = scikitlearn_calc_auPRC(df_test['y'].values, df_test['hg38'].values)
    pgm_aupr = scikitlearn_calc_auPRC(df_test['y'].values, pred)
    pgm_posterior_aupr = scikitlearn_calc_auPRC(df_test['y'].values, mod_df_test['posterior_preds'].values)


    print('Min: hg38', np.min(df_test['hg38']), 'pgm pred:', np.min(pred),
          'pgm posterior:', np.min(mod_df_test['posterior_preds']),
          'Max: hg38', np.max(df_test['hg38']), 'pgm pred:', np.max(pred),
          'pgm posterior:', np.max(mod_df_test['posterior_preds']))

print('Results train_size:', train_size, 'num_pos_train:', num_pos_train,
      'test_size:', test_size, 'num_pos_test:', num_pos_test,
      'base_auc:', base_auc,
      'alpha:', alpha,
      'pgm_auc:', pgm_auc,
      'pgm_posterior_auc:', pgm_posterior_auc,
      'base_aupr:', base_aupr,
      'pgm_aupr:', pgm_aupr,
      'pgm_posterior_aupr:', pgm_posterior_aupr
      )
