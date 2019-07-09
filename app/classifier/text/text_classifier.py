import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from classifier.model import BaseClassifier
from classifier.text.text_pipeline import TextPipeline
from sklearn.linear_model import LogisticRegression
import logging

logger = logging.getLogger('text classifier')
ngram_range = (1, 1)

class TextClassifier(BaseClassifier):
    @classmethod
    def load(cls, filename):
        # super loads only the model
        classifier, offset = super().load(filename)

        # inherited class loads the pipeline
        try:
            processing_pipeline = TextPipeline.load(filename, offset)
        except EOFError:
            logger.warning('EOF reached when trying to load pipeline')
            processing_pipeline = None
        classifier.processing_pipeline = processing_pipeline
        return classifier

    @property
    def important_features(self, k=None):
        column_order = ['feature_name', 'importance', 'class']
        try:
            importances = self._model.feature_importances_
            feature_names = self.features
            feature_importance_df = pd.DataFrame({'feature_name': feature_names,
                                                  'importance': importances,
                                                  'class': np.nan}).sort_values(by='importance', ascending=False)
            if isinstance(k, int):
                feature_importance_df = feature_importance_df.head(k)
        except:
            feature_names = self.features
            if len(self._model.classes_) > 2:
                feature_importances_per_class = []
                for i, c in enumerate(self._model.classes_):
                    importances = self._model.coef_[i]
                    per_class_df = pd.DataFrame({'feature_name': feature_names[importances > 0],
                                                 'importance': importances[importances > 0],
                                                 'class': c}).sort_values(by='importance', ascending=False)
                    if isinstance(k, int):
                        per_class_df = per_class_df.head(k)
                    feature_importances_per_class.append(per_class_df)

                feature_importance_df = pd.concat(feature_importances_per_class, sort=True)
            else:
                importances = self._model.coef_[0]
                feature_importance_df = pd.DataFrame({'feature_name': feature_names,
                                                      'importance': abs(importances),
                                                      'class': [
                                                          self._model.classes_[0] if imp < 0 else self._model.classes_[
                                                              1] for imp in importances]})

        return feature_importance_df.sort_values(by=['class', 'importance'], ascending=False)[column_order]

    def set_preprocessor(self, pipeline):
        self.processing_pipeline = TextPipeline(pipeline)

    def run_on_file(self, input_filename, output_filename, user_id, project_id, label_id=None,
                    pipeline=None, bootstrap_iterations=0, bootstrap_threshold=0.9, run_on_entire_dataset=False):
        print('Reading input file...')
        df = pd.read_csv(input_filename, encoding='latin1')
        if 'label_id' in df.columns:
            df['label'] = df['label_id']
        elif 'label' not in df.columns:
            raise ValueError("no columns 'label' or 'label_id' exist in input file")

        df = df[~pd.isnull(df['text'])]
        print('Pre-processing text and extracting features...')
        self.set_preprocessor(pipeline)

        if label_id:
            df_labeled = df[df['label_id'] == label_id]
            df_labeled = pd.concat([df_labeled, df[df['label_id'] != label_id].sample(df_labeled.shape[0])])
            df_labeled.loc[df_labeled['label_id'] != label_id, 'label_id'] = 0
        else:
            df_labeled = df[~pd.isnull(df['label_id'])]

        X = self.pre_process(df_labeled, fit=True)

        if 'label_id' not in df_labeled.columns:
            raise RuntimeError("column 'label_id' not found")
        else:
            y = df_labeled['label_id'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

        print('Training the model...')
        self.fit(X_train, y_train)

        print('Performance on train set:')
        _, evaluation_text = self.evaluate(X_train, y_train)
        result = 'Performance on train set: \n' + evaluation_text

        print('Performance on test set:')
        _, evaluation_text = self.evaluate(X_test, y_test)
        result = result + '\nPerformance on test set: \n' + evaluation_text

        df_gold_labels = df[ df['user_id']=='gold_label' ]
        X_gold_labels = self.pre_process(df_gold_labels, fit=False)
        y_gold_labels = df_gold_labels['label_id'].values
        if len(y_gold_labels)>0:
            print('Performance on gold labels set:')
            _, evaluation_text = self.evaluate(X_gold_labels, y_gold_labels)
            result = result + '\nPerformance on gold labels set: \n' + evaluation_text
        else:
            print('Gold labels do not exist - skipping the evaluation of model performance on them.')

        if run_on_entire_dataset:
            print('Running the model on the entire dataset...')
            df_cpy = df.copy()
            df_cpy['label_id'] = None
            X = self.pre_process(df_cpy, fit=False)
            y = df['label_id']

            print('Bootstrapping...')
            for i in range(bootstrap_iterations):
                print('bootstrap iteration ', i, '/', bootstrap_iterations, ' ', [x for x in zip(np.unique(y[~pd.isna(y)], return_counts=True))])
                y = self.bootstrap(X, y=y, th=bootstrap_threshold)

            prediction_df = self.get_prediction_df(X, y=df['label_id'])

            prediction_df['document_id'] = df['document_id']
            prediction_df['user_id'] = user_id
            prediction_df = prediction_df.rename({'confidence': 'prob'}, axis=1)
            prediction_df['label_id'] = prediction_df['prediction']

            print('Saving output...')
            prediction_df[['document_id', 'label_id', 'user_id', 'prob']].to_csv(output_filename, index=False, header=True)

        class_weights = self.important_features
        class_weights_filename = os.path.dirname(input_filename)+'/ml_logistic_regression_weights_{project_id}.csv'.format(project_id=project_id)
        class_weights.to_csv(class_weights_filename, header=True, index=False)

        model_save_filename = os.path.dirname(input_filename)+'/ml_model_{project_id}.pickle'.format(project_id=project_id)
        self.save(model_save_filename)

        print('Done running the model!')
        return result

def run_model_on_file(input_filename, output_filename, user_id, project_id, label_id=None, method='bow', run_on_entire_dataset=False):
    # rf = RandomForestClassifier(verbose=True, class_weight='balanced')
    # lr = LogisticRegression(verbose=False, class_weight='balanced', random_state=0, penalty='l2', C=1)
    lr = LogisticRegression(verbose=False, class_weight='balanced', random_state=0, penalty='l1',
                            multi_class='ovr')
    clf = TextClassifier(model=lr)
    # pipeline functions are applied sequentially by order of appearance
    pipeline = [('base processing', {'col': 'text', 'new_col': 'processed_text'}),
                ('bag of words', {'col': 'processed_text',
                                  'min_df': 1, 'max_df': 1., 'binary': True, 'ngram_range': ngram_range,
                                  'stop_words': 'english', 'strip_accents': 'ascii', 'max_features': 5000}),
                ('drop columns', {'drop_cols': ['label_id', 'text', 'processed_text']})]

    result = clf.run_on_file(input_filename, output_filename, user_id, project_id, label_id, pipeline=pipeline, run_on_entire_dataset=run_on_entire_dataset)
    return result


if __name__ == '__main__':
    from app.settings import ML_FOLDER, INPUT_FILE, OUTPUT_FILE

    run_model_on_file(
        # input_filename='../../ml_models/ml_input.csv',
        # output_filename='../../ml_models/ml_out_manual.csv',
        input_filename=INPUT_FILE,
        output_filename=OUTPUT_FILE,
        project_id=9999,
        user_id=2,
        label_id=None,
        run_on_entire_dataset=False)
