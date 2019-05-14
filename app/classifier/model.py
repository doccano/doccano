"""
Baseline model.
"""

import dill
import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report, confusion_matrix
from gong_utils.os.sanitize_filename import sanitize_filename

logger = logging.getLogger()


class BaseClassifier:
    _model = None
    processing_pipeline = None
    columns_ = None
    param_grid = {}

    def __init__(self, model, params=None):
        """model must be serializable and implement the following functions:
        set_params, fit, predict, predict_proba, score"""
        self._model = model
        self.model_type = self._model.__class__.__name__
        if params is None:
            params = {}
        self.params = params
        self.set_params(params)

    def __getstate__(self):
        """Return state values to be pickled. feature maker can't be pickled directly"""
        odict = self.__dict__.copy()
        if 'processing_pipeline' in odict:
            del odict['processing_pipeline']
        return odict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def save(self, filename):
        with open(filename, 'wb') as f:
            dill.dump(self, f)

        if self.processing_pipeline is None:
            logger.warning("cannot save processing pipeline, pipeline not set")
            Warning("cannot save processing pipeline, pipeline not set")
        else:
            self.processing_pipeline.save(filename, append=True)
        return self

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            classifier = dill.load(f)
            offset = f.tell()

        classifier.processing_pipeline = None
        return classifier, offset

    def __str__(self):
        return str(self._model)

    @property
    def name(self):
        model_name = self._model.__class__.__name__
        name_list = ['{k}_{v}'.format(k=k, v=v) for k, v in self.params.items()]
        name = model_name + '__' + "__".join(name_list)
        name = sanitize_filename(name)
        return name

    @property
    def features(self):
        return self.columns_

    def set_params(self, params):
        for k, v in params.items():
            self._model.set_params(**{k: v})
        return self

    def set_preprocessor(self, pipeline, **processing_params):
        pass

    def pre_process(self, X, fit):
        if self.processing_pipeline is None:
            raise ValueError("processing pipeline not set")

        if fit:
            X = self.processing_pipeline.fit_transform(X)
        else:
            X = self.processing_pipeline.transform(X)
        return X

    def fit(self, X, y):
        self.columns_ = getattr(X, 'columns', None)
        self._model.fit(X, y)

    def predict(self, X):
        # warn if label appears, and about set difference between columns
        if self.columns_ is not None:
            if not set(self.columns_) == set(X.columns):
                print(set(X.columns).symmetric_difference(set(self.columns_)))
                raise ValueError('Mismatched columns in transform. Expected %r, got %r' % (self.columns_, X.columns))
            X = X[self.columns_]
        return self._model.predict(X)

    def predict_proba(self, X):
        if self.columns_ is not None:
            if not set(self.columns_) == set(X.columns):
                print(set(X.columns).symmetric_difference(set(self.columns_)))
                raise ValueError('Mismatched columns in transform. Expected %r, got %r' % (self.columns_, X.columns))
            X = X[self.columns_]
        return self._model.predict_proba(X)

    def optimize_hyper_parameters(self, X_train, y_train, score_func=None, verbose= False):
        if score_func is None:
            score_func = 'f1_macro'

        print("Running grid search...")
        clf = GridSearchCV(self._model, self.param_grid, cv=5, scoring=score_func, verbose= verbose )

        clf.fit(X_train, y_train)
        print("Best parameters set found on development set:")
        print(clf.best_params_)

        self.set_params(clf.best_params_)
        self._model.fit(X_train, y_train)
        return self

    def score(self, X, y):
        return self._model.score(X, y)

    def get_scores(self, X, y):
        predictions = self._model.predict(X)
        results = precision_recall_fscore_support(y, predictions, average='macro')
        return results

    def evaluate(self, X, y):
        evaluation_result = ''
        y_pred = self._model.predict(X)

        print(classification_report(y, y_pred))
        evaluation_result = evaluation_result + classification_report(y, y_pred)

        results = precision_recall_fscore_support(y, y_pred, average='macro')
        print("Precision: {:.3}, Recall: {:.3},  F1 Score: {:.3}\n".format(results[0], results[1], results[2]))
        evaluation_result = evaluation_result + "\nPrecision: {:.3}, Recall: {:.3},  F1 Score: {:.3}\n".format(results[0], results[1], results[2])

        conf_mat = confusion_matrix(y, y_pred)
        print(conf_mat)
        evaluation_result = evaluation_result + conf_mat

        return y_pred, evaluation_result

    def run_on_file(self, input_filename, output_filename, user_id, label_id=None, pipeline=None, **processing_params):
        pass
