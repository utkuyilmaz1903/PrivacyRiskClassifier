from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from src import config
from src.train import preprocess_raw


def _load_features() -> pd.DataFrame:
    try:
        return pd.read_csv(config.PROCESSED_DATA_PATH)
    except FileNotFoundError:
        return preprocess_raw()


def evaluate_models():
    df_features = _load_features()
    X = df_features[config.FEATURE_COLUMNS]
    y = df_features[config.TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=config.RANDOM_STATE, stratify=y
    )

    models = {
        "log_reg": LogisticRegression(
            max_iter=500, multi_class="auto", n_jobs=-1, solver="lbfgs"
        ),
        "decision_tree": DecisionTreeClassifier(random_state=config.RANDOM_STATE),
        "random_forest": RandomForestClassifier(
            n_estimators=200, random_state=config.RANDOM_STATE
        ),
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="macro")
        print(f"Model: {name}")
        print(f"Accuracy: {acc:.3f} | Macro F1: {f1:.3f}")
        print("Classification report:")
        print(classification_report(y_test, preds))
        print("Confusion matrix:")
        print(confusion_matrix(y_test, preds))
        print("-" * 40)


if __name__ == "__main__":
    evaluate_models()

