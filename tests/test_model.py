from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import numpy as np

from app.model.train import evaluate_model


def test_evaluate_model_metrics():
    X, y = make_classification(n_samples=100, n_features=5, random_state=42, weights=[0.9, 0.1])
    X_train, X_test = X[:80], X[80:]
    y_train, y_test = y[:80], y[80:]

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)

    # expected metric keys
    expected_keys = {"accuracy", "precision", "recall", "f1", "roc_auc"}
    assert expected_keys.issubset(set(metrics.keys()))

    # values in [0,1] or None for roc_auc
    for k, v in metrics.items():
        if v is not None:
            assert 0.0 <= v <= 1.0
