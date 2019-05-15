# Name: labelers_comparison_functions
# Author: yonathan.guttel@gong.io
# Date: 22 November 2018
# Editing: 30 December 2018

import pandas as pd
import numpy as np
import os
from sklearn.metrics import cohen_kappa_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import scipy as sp
from sklearn.model_selection import train_test_split


def merge_labeling_tables(dir_path,samples_column_name, label_column_name):
    '''
    :param dir_path: path to folder containing separate labelers csv files
    :param samples_column_name: name of samples column
    :param label_column_name:  name of labels column
    :return: labelers_df - a df a df in which each column is a labeler and each row a sample, with a column with samples too
    '''
    files_list=os.listdir(dir_path)
    for counter, file in enumerate(files_list):
        col_name = file.split(".")[0]
        if counter == 0:
            labelers_df = pd.read_table(os.path.join(dir_path,file), sep=",")
            labelers_df.columns = [col_name if x == label_column_name else x for x in labelers_df.columns]
        else:
            new_df = pd.read_table(os.path.join(dir_path,file), sep=",")
            labelers_df= pd.merge(labelers_df,new_df, on=samples_column_name, how="outer")
            labelers_df.columns = [col_name if x == label_column_name else x for x in labelers_df.columns]
    return labelers_df



def create_kappa_comparison_df(labelers_df, filter_double_score=False):
    '''
    :param labelers_df: a df in which each column is a labeler and each row a sample
    :param filter_double_score: does the resulted df should contained doubled score(full table) or only keep one side
           and a single score for each pair
    :return: comparison_df - a cohen kappa distance matrix of the labelers
    '''
    col_list = list(labelers_df.columns)
    comparison_df = pd.DataFrame(index=col_list,columns=col_list)
    for name1 in col_list:
        for name2 in col_list:
            set1 = labelers_df[name1].astype('str')
            set2 = labelers_df[name2].astype('str')
            score = cohen_kappa_score(set1, set2)
            comparison_df.loc[name1, name2] = score
            comparison_df.loc[name2, name1] = score
            if filter_double_score:
                comparison_df.loc[name2,name1] = None

    return comparison_df.astype('float64')


def rank_labelers(comparison_df):
    '''
    :param comparison_df: a cohen kappa distance matrix of the labelers
    :return: a rank list of labelers mean kappa cohen distance from the rest of the labelers
    '''
    df = comparison_df.copy()
    np.fill_diagonal(df.values, None)
    return df.mean(axis=1).sort_values(ascending=False)


def find_most_common_labeling(labelers_df):
    '''
    :param labelers_df: a df in which each column is a labeler and each row a sample
    :return: a pd.Series of the most abundant label for each sample
    '''
    def most_common_label(x):
        return x.value_counts().index[0]
    return labelers_df.apply(most_common_label, axis=1)


def calc_agreement(labelers_df, y):
    '''
    :param labelers_df: a df in which each column is a labeler and each row a sample
    :param y: the name of the column to which we want to test the agreement
    :return: a pd.Series of the labelers agreement prop with the chosen column
    '''
    labeler_cols = [c for c in labelers_df.columns if c!=y]
    def calc_agreement_row(x):
        values = x.loc[labeler_cols]
        true_y = x.loc[y]
        return (values==true_y).mean()
    return labelers_df.apply(calc_agreement_row, axis=1)


def calc_entropy(labelers_df):
    '''
    :param labelers_df: a df in which each column is a labeler and each row a sample
    :return: a pd.Series of the entropy score of each samples
    '''
    classes = np.unique(labelers_df)
    return labelers_df.apply(lambda x: sp.stats.entropy([list(x).count(c) for c in classes]), axis=1)


def add_agreement_columns(labelers_df,y=None):
    '''
    :param labelers_df: a df in which each column is a labeler and each row a sample
    :param y: the "true" labels column name
    :return: the labelers_df with 3 or 4 new columns
    '''
    df_copy = labelers_df.copy()
    cols = df_copy.columns
    if y != None:
        df_copy['true_agreement_prop'] = calc_agreement(df_copy[cols], y)
    df_copy['most_common'] = find_most_common_labeling(df_copy[cols])
    df_copy['most_common_agreement_prop'] = calc_agreement(df_copy[list(cols) + ['most_common']], 'most_common')
    df_copy['entropy'] = calc_entropy(df_copy[cols])
    return df_copy


def asses_accuracy_of_labels(labeler1, labeler2, verbose=False):
    '''
    :param labeler1: a list/pd.Series of the first labeler labeling
    :param labeler2: a list/pd.Series of the first labeler labeling
    :param verbose: should results be printed?
    :return: a dictionary with 3 elements: 1. classification_report, 2.confusion_matrix, 3. Kappa score
    '''
    if verbose:
        print('classification_report:', '\n', classification_report(labeler1, labeler2), '\n')
        print('confusion_matrix:', '\n', pd.DataFrame(confusion_matrix(labeler1, labeler2)), '\n')
        print('Kappa score:', '\n', cohen_kappa_score(labeler1, labeler2) )
    result = {
        'classification_report':        classification_report(labeler1, labeler2),
        'confusion_matrix':             confusion_matrix(labeler1, labeler2),
        'kappa':                        cohen_kappa_score(labeler1, labeler2)
    }
    return result

def draw_conf_accuracy_plot (df, x_conf,slope, intercept, prediction_col):
    '''
    :param df: a df with 3 column
    :param x_conf:  the name of the model prediction confidence column
    :param slope: the correlation slope calculated
    :param intercept:  the correlation intercept calculated
    :param prediction_col: the name of the model prediction true/false (0/1) column
    :return: a
    '''
    plt.figure()
    ax = sns.regplot(x=df[x_conf],
                     y=df[prediction_col],
                     x_estimator=np.mean,
                     x_ci='ci',
                     line_kws={'label': "y={0:.1f}x+{1:.1f}".format(slope, intercept)})
    ax.legend()


def calc_conf_accuracy_correlation(df, y, x, x_conf, draw_plot=True):
    '''
    :param df: a df with 3 column;
    :param y: the name of the true labels column
    :param x: the name of the predicted labels column
    :param x_conf: the name of the model prediction confidence column
    :param draw_plot: should plot be drawn?
    :return: slope, intercept, r_value, p_value, std_err of the interaction
    '''
    df['prediction'] = (df[y] == df[x]) * 1
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[x_conf], df['prediction'])
    if draw_plot:
        draw_conf_accuracy_plot(df, x_conf, slope, intercept,  prediction_col ='prediction')
    return slope, intercept, r_value, p_value, std_err



def train_labelers_based_model(labelers_df, y):
    '''
    :param labelers_df: a df in which each column is a labeler and each row a sample
    :param y: the "true" labels column name
    :return: model scores
    '''
    from nlp.action_items.src.models.classifiers.RandomForest import RandomForest
    from nlp.action_items.src.models.classifiers.KernelSVM import KernelSVM
    from nlp.action_items.src.models.classifiers.LinearSVM import LinearSVM
    from nlp.action_items.src.models.classifiers.GradientBoostedTrees import GradientBoostedTrees
    from nlp.action_items.src.models.classifiers.NaiveBayes import NaiveBayes
    from nlp.action_items.src.models.classifiers.LogReg import LogReg
    
    X = labelers_df.drop(y, axis=1)
    y = labelers_df[y]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model_instance_list = [RandomForest(), KernelSVM(), LinearSVM(), GradientBoostedTrees(), NaiveBayes(), LogReg()]
    for model in model_instance_list:
        model.fit(X_train, y_train)
        print(model.name)
        print("\n Per class Precision and Recall on Train:")
        results = model.get_scores(X_train, y_train)
        print("Precision: {:.3}, Recall: {:.3},  F1 Score: {:.3}\n".format(results[0], results[1], results[2]))
        print("\n Per class Precision and Recall on Test:")
        results = model.get_scores(X_test, y_test)
        print("Precision: {:.3}, Recall: {:.3},  F1 Score: {:.3}\n".format(results[0], results[1], results[2]))
        print('********************', '\n\n')



if __name__ == '__main__':
    df = pd.read_csv(r'C:\Users\omri.allouche\Downloads\labeler_agreement.csv')
    pivot_table = df.pivot(index='document_id', columns='user_id', values='label_id')
    create_kappa_comparison_df(pivot_table)
