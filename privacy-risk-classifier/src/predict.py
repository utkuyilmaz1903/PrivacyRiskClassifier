from __future__ import annotations

import joblib
import pandas as pd

from src import config
from src.features import count_categories, parse_permissions


def load_model(path: str | None = None):
    model_path = config.MODEL_PATH if path is None else path
    bundle = joblib.load(model_path)
    return bundle["model"], bundle["features"]


def permissions_to_features(permissions_str: str) -> pd.DataFrame:
    permissions = parse_permissions(permissions_str)
    counts = count_categories(permissions)
    row = {
        "total_permissions": len(permissions),
        "location_count": counts["location_count"],
        "contacts_count": counts["contacts_count"],
        "camera_count": counts["camera_count"],
        "microphone_count": counts["microphone_count"],
        "sms_call_count": counts["sms_call_count"],
        "storage_count": counts["storage_count"],
        "network_count": counts["network_count"],
        "sensitive_category_count": counts["sensitive_category_count"],
    }
    return pd.DataFrame([row])


def predict_risk(permissions_str: str, model_path: str | None = None) -> str:
    model, feature_cols = load_model(model_path)
    features = permissions_to_features(permissions_str)[feature_cols]
    return model.predict(features)[0]


if __name__ == "__main__":
    sample = "android.permission.ACCESS_FINE_LOCATION;android.permission.READ_CONTACTS"
    print("Örnek izinler:", sample)
    try:
        risk = predict_risk(sample)
        print("Tahmin edilen risk:", risk)
    except FileNotFoundError:
        print("Önce modeli eğitmek için: python cli.py train")

