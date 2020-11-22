import sys, pickle
import pandas as pd, numpy as np
from multiprocessing import Pool
import time
import argparse
from tqdm import tqdm
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.model_selection import KFold
import swifter

global new_quant_test_df, quant_val_df
global pos_train_df, neg_train_df, curr_test_df


class Booster:
    """Boosts Inference with PhyloPGM approach
    """

    def __init__(self,
                 df_val=None,
                 df_test=None,
                 root='hg38',
                 tree=None,
                 alpha=0.1,
                 tune=False,
                 missing_value=9
                 ):
        """

        :param df_val: pandas DataFrame [sp1, sp2, ..., spn, label], float
        :param df_test: pandas DataFrame [sp1, sp2, ..., spn], float
        :param root: root species name, str
        :param tree: child, parent pair s.t. tree[child]=parent, Dictionary
        :param alpha: branch likelihood coefficient, float
        :param tune: whether to tune alpha, bool
        :param missing_value: missing value indicator, float

        :return df_test: modified df_test with branch likelihood scores
        :return pred: combined prediction scores, array-like

        """
        self.df_val = df_val
        self.df_test = df_test
        self.root = root
        self.tree = tree
        self.alpha = alpha
        self.tune = tune
        self.missing_value = missing_value


    def boost(self):
        # assert df_val and df_test are float

        # round df_val
        self.df_val.iloc[:, :-1] = self.df_val.iloc[:, :-1].round(1)
        self.df_val = self.df_val.fillna(self.missing_value)

        sp_list = self.df_val.columns[:-1]
        non_root_list = set(sp_list) - {self.root}
        # print('self.root:', self.root, 'sp_list:', sp_list,
        #       'non_root_list:', non_root_list); #exit(0)
        branch_list = ['branch_'+item+'_'+self.tree[item] for item in non_root_list]

        # round df_test
        self.df_test.iloc[:, :] = self.df_test.iloc[:, :].round(1)
        self.df_test = self.df_test.fillna(self.missing_value)

        if self.tune:
            # TODO select alpha by k-fold cross validation
            best_alpha = self.alpha
            pass
        else:
            best_alpha = self.alpha

        self.df_test = get_branch_scores(self.df_val, self.df_test, self.root, branch_list)

        self.df_test['pgm_pred'] = self.df_test['ratio_root']+(best_alpha*self.df_test['sanity_sum'])

        # pred = self.df_test['ratio_root']+(best_alpha*self.df_test['sanity_sum'])

        # return self.df_test, pred
        return self.df_test, self.df_test['pgm_pred'].values


def get_sum(row):
    s=0.
    for item in row.values:
        if not np.isnan(item):
            s+=item
    return s


def mapper(branch):
    global pos_train_df, neg_train_df, curr_test_df

    def process_non_root_branch(row, branch):
        child, parent = branch.split('_')[1:]
        test_child = row[child]
        test_parent = row[parent]

        # calculate numerator
        sp_parent_pos = pos_train_df[pos_train_df[parent] == test_parent]
        sp_num_pos = sp_parent_pos[sp_parent_pos[child] == test_child].shape[0] + 1.
        sp_den_pos = sp_parent_pos.shape[0] + 12.

        # calculate denominator
        sp_parent_neg = neg_train_df[neg_train_df[parent] == test_parent]
        sp_num_neg = sp_parent_neg[sp_parent_neg[child] == test_child].shape[0] + 1.
        sp_den_neg = sp_parent_neg.shape[0] + 12.

        curr_second_part = np.log((sp_num_pos / sp_den_pos) / (sp_num_neg / sp_den_neg))

        return curr_second_part

    retain_second_part = curr_test_df.swifter.apply(process_non_root_branch,
                                                                       args=(branch,),
                                                                       axis=1
                                                                   )
    return pd.DataFrame(retain_second_part.values,
                        index=retain_second_part.index,
                        columns=[branch]
                        )


def get_branch_scores(curr_train_df,
                      given_curr_test_df,
                      root,
                      branch_list
                      ):
    global pos_train_df, neg_train_df, curr_test_df

    curr_test_df = given_curr_test_df
    print('curr_test_df:', curr_test_df.shape)
    pos_train_df = curr_train_df[curr_train_df['y'] == 1]
    neg_train_df = curr_train_df[curr_train_df['y'] == 0]

    # root
    def process_root_branch(row):
        test_hg38 = row[root]
        # calculate numerator
        root_num = pos_train_df[pos_train_df[root] == test_hg38].shape[0] + 1.
        root_num /= (pos_train_df.shape[0] + 12.)
        # calculate denominator
        root_den = neg_train_df[neg_train_df[root] == test_hg38].shape[0] + 1.
        root_den /= neg_train_df.shape[0] + 12.
        curr_root = np.log(root_num / root_den)
        return curr_root

    curr_test_df['ratio_root'] = curr_test_df.swifter.apply(process_root_branch,
                                                            axis=1
                                                            )
    print('Done process_root_branch')


    p = Pool()
    results = p.map(mapper, branch_list)
    df_second_part = pd.concat(results, axis=1)
    curr_test_df = pd.concat([curr_test_df, df_second_part], axis=1)

    curr_test_df['sanity_sum'] = curr_test_df[branch_list].swifter.apply(get_sum,
                                                                         axis=1
                                                                         )

    return curr_test_df

