
from BoostInference_round import Booster
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import sys
import rpy2
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
import rpy2.robjects as ro


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
# df_val = pd.read_csv('v', index_col=0).astype(float)
# df_test = pd.read_csv('t', index_col=0).astype(float)

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

# model = Booster(df_val=df_val,
#                 df_test=df_test.iloc[:,:-1],  # do not send test labels
#                 tree=tree,
#                 alpha=alpha
#                 )
#
# mod_df_test, pred = model.boost()
# print('mod_df_test:', mod_df_test.shape)
# mod_df_test['y'] = df_test['y']
#
# # compute prior
# prior_y1 = float(num_pos_train)/train_size
# prior_y0 = 1.-prior_y1
#
# # compute posterior
# mod_df_test['posterior_preds'] = mod_df_test.pgm_pred.swifter.apply \
#     (lambda x: ((prior_y1*np.exp(x))/((prior_y1*np.exp(x))+prior_y0))
#      )
#
# mod_df_test.to_csv(df_pgm_name)
mod_df_test = pd.read_csv(df_pgm_name, index_col=0)
pred = mod_df_test['pgm_pred'].values

def compute_auc_score(true_labels, predictions, min_prediction, max_prediction):
    '''

    :param true_labels: np array
    :param predictions: np array
    :param min_prediction:
    :param max_prediction:
    :return:
    '''
    div = (max_prediction - min_prediction) / 100
    req_range = np.arange(min_prediction, max_prediction, div)
    req_range = np.append(req_range, max_prediction)

    tpr = []; tnr = []
    for threshold in req_range:
        pred_labels = predictions.copy()

        # positive labels
        pos_labels = pred_labels[true_labels == 1]
        tp = np.where(pos_labels >= threshold)[0].shape[0]
        fn = np.where(pos_labels < threshold)[0].shape[0]

        # negative labels
        neg_labels = pred_labels[true_labels == 0]
        tn = np.where(neg_labels < threshold)[0].shape[0]
        fp = np.where(neg_labels >= threshold)[0].shape[0]

        tpr.append(float(tp) / (tp + fn))
        tnr.append(float(tn) / (tn + fp))

    return np.trapz(tpr, tnr)

def compute_aupr_score(true_labels, predictions, min_prediction, max_prediction):
    '''

    :param true_labels: np array
    :param predictions: np array
    :param min_prediction:
    :param max_prediction:
    :return:
    '''
    div = (max_prediction - min_prediction) / 100
    req_range = np.arange(min_prediction, max_prediction, div)
    req_range = np.append(req_range, max_prediction)

    precision = []; recall = []
    for threshold in req_range:
        pred_labels = predictions.copy()

        # positive labels
        pos_labels = pred_labels[true_labels == 1]
        tp = np.where(pos_labels >= threshold)[0].shape[0]
        fn = np.where(pos_labels < threshold)[0].shape[0]

        # negative labels
        neg_labels = pred_labels[true_labels == 0]
        tn = np.where(neg_labels < threshold)[0].shape[0]
        fp = np.where(neg_labels >= threshold)[0].shape[0]

        if tp+fp==0. or tp+fn==0.:
            continue

        precision.append(float(tp) / (tp + fp))
        recall.append(float(tp) / (tp + fn))

    precisions = np.array(precision)
    recalls = np.array(recall)
    sorted_index = np.argsort(recalls)
    recalls = recalls[sorted_index]
    precisions = precisions[sorted_index]

    return np.trapz(precisions, recalls)

def scikitlearn_calc_auPRC(y_true, y_score):
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    return auc(recall, precision)

def calc_auPRC(y_true, y_score):
    """Calculate auPRC using the R package

    """
    ro.globalenv['pred'] = y_score
    ro.globalenv['labels'] = y_true
    return ro.r('library(PRROC); pr.curve(scores.class0=pred, weights.class0=labels)$auc.davis.goadrich')[0]




base_auc = -10.
pgm_auc = -10.
pgm_posterior_auc=-10.

base_aupr = -10.
pgm_aupr = -10.
pgm_posterior_aupr=-10.

if num_pos_test > 0:
    base_auc = roc_auc_score(df_test['y'], df_test['hg38'])
    my_base_auc = compute_auc_score(df_test['y'].values, df_test['hg38'],
                                    np.min(df_test['hg38']),
                                    np.max(df_test['hg38'])
                                    )
    print('base_auc:', base_auc, 'my_base_auc:', my_base_auc)
    pgm_auc = roc_auc_score(df_test['y'], pred)
    pgm_posterior_auc = roc_auc_score(df_test['y'], mod_df_test['posterior_preds'])


    base_aupr = compute_aupr_score(df_test['y'].values,
                                   df_test['hg38'].values,
                                   0., 1.)
    print('base_aupr:', base_aupr,
          'scikitlearn_calc_auPRC:', scikitlearn_calc_auPRC(df_test['y'].values, df_test['hg38'].values),
          'calc_auPRC:', calc_auPRC(df_test['y'].values, df_test['hg38'].values
                                    )
          )
    exit(0)
    pgm_aupr = compute_aupr_score(df_test['y'].values,
                                  pred,
                                  np.min(pred), np.max(pred)
                                  )
    pgm_posterior_aupr = compute_aupr_score(df_test['y'].values,
                                      mod_df_test['posterior_preds'].values,
                                      np.min(mod_df_test['posterior_preds']), np.max(mod_df_test['posterior_preds'])
                                      )

    print('Min: hg38', np.min(df_test['hg38']), 'pgm pred:', np.min(pred),
          'pgm posterior:', np.min(mod_df_test['posterior_preds']),
          'Max: hg38', np.max(df_test['hg38']), 'pgm pred:', np.max(pred),
          'pgm posterior:', np.max(mod_df_test['posterior_preds']))

    # compute_base_auc = compute_auc_score(df_test['y'].values,
    #                                              df_test['hg38'].values,
    #                                              0., 1.)
    # compute_pgm_auc = compute_auc_score(df_test['y'].values,
    #                                 pred,
    #                                 np.min(pred), np.max(pred))
    #
    # print('compute_auc hg38:', compute_auc_score(df_test['y'].values,
    #                                              df_test['hg38'].values,
    #                                              0., 1.),
    #       'pgm:', compute_auc_score(df_test['y'].values,
    #                                 pred,
    #                                 np.min(pred), np.max(pred))
    #       )

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
