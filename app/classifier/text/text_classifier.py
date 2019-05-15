import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from app.classifier.model import BaseClassifier
from app.classifier.text.text_pipeline import TextPipeline
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

    def run_on_file(self, input_filename, output_filename, user_id, label_id=None, pipeline=None):
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
