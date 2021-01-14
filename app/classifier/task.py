"""
Task runner.
"""
import numpy as np

from doccano.app.classifier.model import build_model
from doccano.app.classifier import build_vectorizer
from doccano.app.classifier import load_dataset, save_dataset, make_output, train_test_split


def run(filename):
    print('Loading dataset...')
    data = load_dataset(filename)
    x_train, x_test, y_train, ids = train_test_split(data)

    print('Building vectorizer and model...')
    vectorizer = build_vectorizer()
    clf = build_model()

    print('Vectorizing...')
    x_train = vectorizer.fit_transform(x_train)
    x_test = vectorizer.transform(x_test)

    print('Fitting...')
    clf.fit(x_train, y_train)

    print('Predicting...')
    y_pred = clf.predict(x_test)
    y_prob = clf.predict_proba(x_test)
    y_prob = np.max(y_prob, axis=-1)

    print('Saving...')
    data = make_output(data, ids, y_pred, y_prob)
    save_dataset(data, filename)
