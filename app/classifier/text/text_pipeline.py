import dill
from classifier.text.processing_functions import proc_name_mapping


class TextPipeline:
    def __init__(self,
                 pipeline,
                 language_processor=None):
        self.language_processor = language_processor

        # processing functions to apply for feature creation
        self.pipeline = pipeline
        self.transform_params = None

    def fit_transform(self, X):
        transform_params = {}
        for name, fit_params in self.pipeline:
            if name in proc_name_mapping.keys():
                proc = proc_name_mapping[name]
            else:
                raise ValueError('unknown data transform %s' % name)

            X, params = proc(X, fit=True, **fit_params)
            transform_params[name] = params

        self.transform_params = transform_params
        return X

    def transform(self, X):
        for name, _ in self.pipeline:
            transform_params = self.transform_params[name]
            if name in proc_name_mapping.keys():
                proc = proc_name_mapping[name]
            else:
                raise ValueError('unknown data transform %s' % name)
            X, _ = proc(X, fit=False, **transform_params)
        return X

    def __getstate__(self):
        """Return state values to be pickled."""
        odict = self.__dict__.copy()
        if 'vector_model' in odict:
            del odict['vector_model']
        return odict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def save(self, filename, append=False):
        file_mode = 'ab' if append else 'wb'
        with open(filename, file_mode) as f:
            dill.dump(self, f)

    @staticmethod
    def load(filename, offset=0):
        with open(filename, 'rb') as f:
            f.seek(offset)
            text_pipeline = dill.load(f)

        return text_pipeline


