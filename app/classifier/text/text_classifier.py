import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from app.classifier.model import BaseClassifier
from app.classifier.text.text_pipeline import TextPipeline
from sklearn.linear_model import LogisticRegression
import logging

logger = logging.getLogger('text classifier')


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
    def important_features(self, NUM_TOP_FEATURES=None, plot=False):
        try:
            importances = self._model.feature_importances_
        except:
            importances = self._model.coef_[0]

        indices = np.argsort(abs(importances))

        if isinstance(NUM_TOP_FEATURES, int):
            indices = indices[-NUM_TOP_FEATURES:]

        result = [(self.features[id], importances[id]) for id in indices]

        if plot:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 15))
            plt.title('Feature Importances')
            plt.barh(range(len(result)), [importance for name, importance in result], color='b', align='center')
            plt.yticks(range(len(result)), [name for name, importance in result])
            plt.xlabel('Relative Importance')
            plt.show()

        return result

    def set_preprocessor(self, pipeline):
        self.processing_pipeline = TextPipeline(pipeline)

    def run_on_file(self, input_filename, output_filename, user_id, project_id, label_id=None, pipeline=None):
        print('Reading input file...')
        df = pd.read_csv(input_filename, encoding='latin1')
        df = df[~pd.isnull(df['text'])]

        print('Pre-processing text and extracting features...')
        self.set_preprocessor(pipeline)

        if label_id:
            df_labeled = df[df['label'] == label_id]
            df_labeled = pd.concat([df_labeled, df[df['label'] != label_id].sample(df_labeled.shape[0])])
            df_labeled.loc[df_labeled['label'] != label_id, 'label'] = 0
        else:
            df_labeled = df[~pd.isnull(df['label'])]

        X = self.pre_process(df_labeled, fit=True)
        if 'label' not in df_labeled.columns:
            raise RuntimeError("column 'label' not found")
        else:
            y = df_labeled['label'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

        print('Training the model...')
        self.fit(X_train, y_train)

        print('Performance on train set:')
        _, evaluation_text = self.evaluate(X_train, y_train)
        result = 'Performance on train set: \n' + evaluation_text

        print('Performance on test set:')
        _, evaluation_text = self.evaluate(X_test, y_test)
        result = result + '\nPerformance on test set: \n' + evaluation_text

        print('Running the model on the entire dataset...')
        df_cpy = df.copy()
        df_cpy['label'] = None
        X = self.pre_process(df_cpy, fit=False)
        prediction_df = self.get_prediction_df(X, y=df['label'])

        prediction_df['user_id'] = user_id
        prediction_df = prediction_df.rename({'confidence': 'prob'}, axis=1)  # 'id': 'document_id'
        prediction_df['label_id'] = prediction_df['prediction']

        print('Saving output...')
        prediction_df[['label_id', 'user_id', 'prob']].to_csv(output_filename, index=False, header=True)  # 'document_id'

        class_weights = pd.Series({term: weight for (term, weight) in self.important_features})
        project_id = 999
        class_weights_filename = os.path.dirname(input_filename)+'/ml_logistic_regression_weights_{project_id}.csv'.format(project_id=project_id)
        class_weights.to_csv(class_weights_filename, header=False)

        print('Done running the model!')
        return result


def run_model_on_file(input_filename, output_filename, user_id, project_id, label_id=None, method='bow'):
    # rf = RandomForestClassifier(verbose=True, class_weight='balanced')
    lr = LogisticRegression(verbose=True, class_weight='balanced')
    clf = TextClassifier(model=lr)
    # pipeline functions are applied sequentially by order of appearance
    pipeline = [('base processing', {'col': 'text', 'new_col': 'processed_text'}),
                ('bag of words', {'col': 'processed_text', 'min_df': 1, 'max_df': 1., 'binary': True,
                                  'stop_words': 'english', 'strip_accents': 'ascii', 'max_features': 5000}),
                ('drop columns', {'drop_cols': ['label', 'text', 'processed_text']})]

    result = clf.run_on_file(input_filename, output_filename, user_id, project_id, label_id, pipeline=pipeline)
    return result


if __name__ == '__main__':
    run_model_on_file('../../ml_models/ml_input.csv', '../../ml_models/ml_out_manual.csv', project_id=9999, user_id=2, label_id=None)
