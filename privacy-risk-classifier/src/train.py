from __future__ import annotations

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from src import config
from src.features import build_feature_df


def load_raw_data(path: str | None = None) -> pd.DataFrame:
    data_path = config.RAW_DATA_PATH if path is None else path
    return pd.read_csv(data_path)


def preprocess_raw() -> pd.DataFrame:
    """Ham CSV'den özellikli veri setini üretir ve kaydeder."""
    df_raw = load_raw_data()
    df_features = build_feature_df(df_raw)
    config.PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_features.to_csv(config.PROCESSED_DATA_PATH, index=False)
    return df_features


def train_models():
    """Temel modelleri eğitir, en iyisini kaydeder."""
    try:
        df_features = pd.read_csv(config.PROCESSED_DATA_PATH)
    except FileNotFoundError:
        df_features = preprocess_raw()

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

    metrics = {}
    best_model_name = None
    best_f1 = -1.0

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="macro")
        metrics[name] = {"accuracy": acc, "macro_f1": f1}

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    best_model = models[best_model_name]
    config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": best_model, "features": config.FEATURE_COLUMNS}, config.MODEL_PATH)

    return metrics, best_model_name


if __name__ == "__main__":
    preprocess_raw()
    metrics, best = train_models()
    print("Eğitim tamamlandı.")
    print("Metri̇kler:", metrics)
    print("En iyi model:", best)

