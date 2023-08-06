# inspired by https://github.com/scikit-learn/scikit-learn/issues/4813#issuecomment-204162467
# and https://github.com/koaning/scikit-lego/blob/main/sklego/meta/thresholder.py

from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, MetaEstimatorMixin
from sklearn.metrics import precision_recall_curve
from sklearn.utils.validation import check_is_fitted


class ThresholdClassifier(BaseEstimator, ClassifierMixin, MetaEstimatorMixin):
    def __init__(self, estimator, thresholds: List[float], fallback_class):
        """
        Classify samples based on a list of `thresholds` for each possible class.
        `fallback_class` shall be returned if none of the predicted classes meets it's threshold.
        """
        self.estimator = estimator
        self.thresholds = thresholds
        self.fallback_class = fallback_class

    def __getattr__(self, name):
        try:
            return getattr(self.estimator, name)
        except AttributeError:
            raise AttributeError("`estimator` object has no attribute '%s'" % name)

    def fit(self, X, y, **kwargs):
        self.estimator.fit(X, y, **kwargs)
        return self

    def predict(self, X):
        check_is_fitted(self.estimator)
        class_confidences = pd.DataFrame(
            columns=self.classes_,
            data=self.estimator.predict_proba(X)
        )
        predicate = class_confidences >= self.thresholds  # mask
        class_confidences[~predicate] = 0  # negate and set to zero
        class_labels = class_confidences.idxmax(axis=1)  # get labels (column names)
        all_zeros_idx = (class_confidences.sum(axis=1) == 0)
        class_labels[all_zeros_idx] = self.fallback_class
        return class_labels


def threshold_at_precison(
    y_true: List[int], probas_pred: List[float], precision_threshold: float = 0.8
) -> float:
    """Find the threshold given a min. precision of `precision_threshold`,
    based on `sklearn.metrics.precision_recall_curve(y_true, probas_pred)`.

    Args:
        y_true: True binary labels, either {-1, 1} or {0, 1}.
        probas_pred: Estimated probabilities or output of a decision function.
        precision_threshold: Minimum precision to be reached.

    Returns:
        float: threshold value
    """
    precision, _, thresholds = precision_recall_curve(y_true, probas_pred)

    precision_above = (precision >= precision_threshold).nonzero()[0][0]
    return thresholds[min(precision_above, len(thresholds)-1)]
