from pathlib import Path

# Temel dosya yolları
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "apps_permissions.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "apps_features.csv"
MODEL_PATH = DATA_DIR / "processed" / "best_model.joblib"

# Eğitim/tahmin için kullanılacak özellik kolonları
FEATURE_COLUMNS = [
    "total_permissions",
    "location_count",
    "contacts_count",
    "camera_count",
    "microphone_count",
    "sms_call_count",
    "storage_count",
    "network_count",
    "sensitive_category_count",
]

TARGET_COLUMN = "label"
RANDOM_STATE = 42

