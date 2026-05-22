import os
import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN
import json
import numpy as np

from app.model.preprocess import build_preprocessor
from app.utils.config import (
    DATA_PATH,
    MODEL_PATH,
    PIPELINE_PATH,
    TARGET_COLUMN
)

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0)
    }

    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
        metrics["roc_auc"] = roc_auc_score(y_test, y_prob)
    elif hasattr(model, "decision_function"):
        y_score = model.decision_function(X_test)
        metrics["roc_auc"] = roc_auc_score(y_test, y_score)
    else:
        metrics["roc_auc"] = None

    return metrics


def train_model():

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    preprocessor = build_preprocessor(df, TARGET_COLUMN)

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Use SMOTEENN (SMOTE + Edited Nearest Neighbours) to handle class imbalance
    smote_enn = SMOTEENN(random_state=42)
    X_train_resampled, y_train_resampled = smote_enn.fit_resample(
        X_train_processed,
        y_train
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model.fit(X_train_resampled, y_train_resampled)

    # Evaluate on test set
    y_pred = model.predict(X_test_processed)
    y_prob = model.predict_proba(X_test_processed)[:, 1]

    metrics = evaluate_model(model, X_test_processed, y_test)
    print(f"Validation metrics: {metrics}")

    # Tune decision threshold to maximize F1 on the hold-out test set
    best_thresh = 0.5
    best_f1 = 0.0
    for t in np.linspace(0.01, 0.99, 99):
        preds = (y_prob >= t).astype(int)
        f1 = f1_score(y_test, preds, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = float(t)

    print(f"Best threshold by F1: {best_thresh:.2f} (F1={best_f1:.4f})")

    # Persist model, pipeline and metadata
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocessor, PIPELINE_PATH)

    metadata = {
        "accuracy": metrics.get("accuracy"),
        "precision": metrics.get("precision"),
        "recall": metrics.get("recall"),
        "f1": metrics.get("f1"),
        "roc_auc": metrics.get("roc_auc"),
        "best_threshold": best_thresh,
        "trained_samples": int(len(X_train_resampled))
    }

    meta_path = os.path.join(os.path.dirname(MODEL_PATH), "model_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print("Training complete. Model, pipeline, and metadata saved.")


if __name__ == "__main__":
    train_model()