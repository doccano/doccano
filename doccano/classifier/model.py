"""
Baseline model.
"""

from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC


def build_model():
    estimator = CalibratedClassifierCV(base_estimator=LinearSVC())

    return estimator
