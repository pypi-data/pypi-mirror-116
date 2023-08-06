from typing import List

import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.model_selection import cross_val_score
from tqdm import tqdm


class ForwardFeatureSelection(TransformerMixin):
    """Iteratively build an optimal feature set by starting with an empty or pre-
    defined feature set and adding new features to it. The algorithm looks as follows:

    1. test performance on initial feature set
    2. while not all features selected:
        1. foreach feature not in selected features:
            1. temporarily add feature to selected features
            2. cross-validate model
        2. find feature with best cross-validated performance
        3. if performance of best feature is better than overall best performance:
            * add feature to selected features
            * else: break

    Parameters
    ----------
    model:
        model with a ``fit`` and ``predict`` function.
        E.g., an sklearn :class:`RandomForestClassifier`.
    scoring:
        which scoring function to use. Forwarded to sklearn's cross_val_score function
    cv:
        how many folds to use to validate the performance of the classifier. The outcome
        is used to determine the performance of the model on the given feature set
    max_features:
        maximum amount of features to select (in addition to warmstart_cols)
    warmstart_cols:
        set of columns that are pre-selected
    speculative_rounds:
        normally, the algorithm would stop when the performance does not improve
        the first time. If speculative rounds are greater than 0, then the algorithm
        continues for the specified amount of iterations in the hope to find a better
        solution in the next iteration.
    progress_bar:
        whether to show a progress bar in each iteration

    Attributes
    ----------
    selected_: List[str]
        all selected features
    selected_extra_: List[str]
        features that have been selected in addition to the warmstart_cols
    improvements_: List[float]
        improvements of all features in selected_extra_, in terms of the ``scoring``
        function
    score_: float
        cross-validated score of the model on the selected features
    """

    def __init__(
        self,
        estimator: BaseEstimator,
        scoring=None,
        cv: int = 5,
        max_features: int = None,
        warmstart_cols: List[str] = None,
        speculative_rounds: int = 0,
        progress_bar: bool = True,
    ):
        self.estimator = estimator
        self.scoring = scoring
        self.cv = cv
        self.max_features = max_features
        self.warmstart_cols = warmstart_cols if warmstart_cols is not None else []
        self.speculative_rounds = speculative_rounds
        self.progress_bar = progress_bar

    def fit(self, X: pd.DataFrame, y):
        selected = self.warmstart_cols.copy()
        improvements: List[float] = []
        if len(selected) > 0:
            best_score = np.mean(
                cross_val_score(
                    self.estimator, X[selected], y, scoring=self.scoring, cv=self.cv
                )
            )
            self.baseline_ = best_score
            print(f"Baseline: {best_score}")
        else:
            best_score = float("-inf")
            self.baseline_ = None
        speculations = 0
        rounds = 0
        while len(selected) < X.shape[1] and (
            self.max_features is None or len(selected) < self.max_features
        ):
            rounds += 1
            print(f"Starting round #{rounds}...")
            candidates = set(X.columns) - set(selected)
            assert len(candidates) > 0
            best_candidate = None
            best_improvement = float("-inf")
            for c in tqdm(candidates, disable=not self.progress_bar):
                subset = selected + [c]
                score = np.mean(
                    cross_val_score(
                        self.estimator, X[subset], y, scoring=self.scoring, cv=self.cv
                    )
                )
                improvement = score - best_score if np.isfinite(best_score) else score
                if improvement > best_improvement:
                    best_candidate = c
                    best_improvement = improvement
                    best_candidate_score = score
            if best_improvement <= 0:
                speculations += 1
                if speculations > self.speculative_rounds:
                    print(f"No improvement for {speculations} rounds. Stopping.")
                    if speculations > 1:
                        # remove speculatively selected features
                        selected = selected[:-speculations]
                        improvements = improvements[:-speculations]
                    break
                print(f"No improvement. Starting speculative round #{speculations}...")

            selected.append(best_candidate)
            improvements.append(best_improvement)
            if best_improvement > 0:
                best_score = best_candidate_score
                speculations = 0
            print(
                f"Selecting {best_candidate}. "
                f"Improvement: {best_improvement:.3f}; best_score: {best_score:.2f}"
            )
        self.selected_ = selected
        self.selected_extra_ = selected[len(self.warmstart_cols) :]
        self.improvements_ = improvements
        self.score_ = best_score

    def transform(self, X: pd.DataFrame, y=None):
        """Return DataFrame that contains exactly the selected features"""
        return X[self.selected_]
