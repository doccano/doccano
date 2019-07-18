import numpy as np
import pandas as pd
# import spacy
from nltk.tokenize import WordPunctTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re
import logging

logger = logging.getLogger('text processing functions')

# default_nlp = spacy.load("en_core_web_md", disable=['parser', 'tagger', 'ner'])

""" ########################
    Text processing functions
    ######################## """


def base_processing(X, col=None, **params):
    if col not in X.columns:
        logger.warning('attempted to process non-existent column: %s' % col)
        return X, None

    def process_text(text):
        # remove non-english characters
        processed_text = re.sub("[^a-zA-Z]", " ", text)
        # remove punctuation marks
        processed_text = re.sub("\.,\?\!", "", processed_text)
        processed_text = re.sub("[ ]+", " ", processed_text)
        # lowercase
        processed_text = processed_text.lower().strip()
        return processed_text

    if 'new_col' in params:
        new_col = params['new_col']
    else:
        new_col = 'processed_text'

    if new_col not in X.columns:
        X[new_col] = None

    X.loc[:, new_col] = X[col].apply(process_text)
    transform_params = {'col': col, 'new_col': new_col}
    return X, transform_params


""" ########################
    Feature extraction functions
    ######################## """


def get_bag_of_words(X, fit=True, col=None, vectorizer=None, **params):
    if col not in X.columns:
        logger.warning('attempted to compute bag of word features for non-existent column: %s' % col)
        return X, None

    if fit:
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer(smooth_idf=True)

        # if not specified, setting default tokenizer to nltk.WordPunctTokenizer
        if 'tokenizer' not in params:
            vectorizer.set_params(**{'tokenizer': WordPunctTokenizer().tokenize})

        vectorizer.set_params(**params)
        texts = X[col].str.strip().fillna('')
        word_count_matrix = vectorizer.fit_transform(texts)
        vectorizer.set_params(**{'vocabulary': vectorizer.vocabulary_})
    else:
        if vectorizer is None:
            logger.warning('attempted to transform feature: %s with non-existent vectorizer' % col)
            return X, None
        texts = X[col].str.strip().fillna('')
        word_count_matrix = vectorizer.transform(texts)

    bag_of_words_feature_names = [col + '_w_' + feature_name for feature_name in vectorizer.get_feature_names()]
    bag_of_word_features_df = pd.DataFrame(word_count_matrix.todense(), columns=bag_of_words_feature_names, index=X.index.values)

    X = pd.merge(X, bag_of_word_features_df, right_index=True, left_index=True)
    transform_params = {'col': col, 'vectorizer': vectorizer}
    return X, transform_params


def get_word_embeddings(X, col=None, **params):
    if 'nlp' in params.keys():
        nlp = params['nlp']
    else:
        raise Exception
        # nlp = default_nlp

    if col not in X.columns:
        logger.warning('attempted to compute word vector features with non-existent column %s' % col)
        return X, None

    X['vec'] = X[col].apply(lambda x: nlp(x).vector)
    word_vectors = np.stack([np.array(x) for x in X['vec'].values], axis=0)
    word_vector_feature_names = [col + '_d_' + str(i) for i in range(word_vectors.shape[1])]
    word_vector_features_df = pd.DataFrame(word_vectors, columns=word_vector_feature_names, index=X.index)
    X = pd.merge(X, word_vector_features_df, right_index=True, left_index=True)
    transform_params = {'col': col}
    return X, transform_params


def drop_columns(X, drop_cols=(), **params):
    columns_to_drop = []
    for col in X.columns:
        idx = X[col].first_valid_index()

        # drop features that are all none
        if idx is None:
            columns_to_drop.append(col)
        else:
            # drop features that have lists as values
            if isinstance(X[col].loc[idx], list):
                columns_to_drop.append(col)

            # drop features that have strings as values
            if isinstance(X[col].loc[idx], str):
                columns_to_drop.append(col)

    X = X.drop(columns_to_drop, axis=1)

    # remove specific columns
    keep_columns = [col for col in X.columns if col not in drop_cols]
    X = X[keep_columns]
    return X, {'drop_cols': drop_cols}


proc_name_mapping = {'base processing': base_processing,
                     'bag of words': get_bag_of_words,
                     'word embeddings': get_word_embeddings,
                     'drop columns': drop_columns}
