"""
Ham izin listelerinden sayısal özellikleri üretir.
"""

from __future__ import annotations

from typing import Dict, Iterable, List

import pandas as pd

from src import config
from src.labeling import label_risk
from src.permission_taxonomy import (
    CAMERA,
    CONTACTS,
    LOCATION,
    MICROPHONE,
    NETWORK,
    OTHER,
    SMS_CALL,
    STORAGE,
    get_category,
)


def parse_permissions(raw: str | None) -> List[str]:
    """
    Noktalı virgülle ayrılmış izin dizgesini listeye dönüştürür.
    """
    if not raw:
        return []
    return [p.strip() for p in raw.split(";") if p.strip()]


def count_categories(permissions: Iterable[str]) -> Dict[str, int]:
    """
    İzin listesini kategori bazında sayar.
    """
    counts = {
        "location_count": 0,
        "contacts_count": 0,
        "camera_count": 0,
        "microphone_count": 0,
        "sms_call_count": 0,
        "storage_count": 0,
        "network_count": 0,
        "other_count": 0,
    }

    for perm in permissions:
        category = get_category(perm)
        if category == LOCATION:
            counts["location_count"] += 1
        elif category == CONTACTS:
            counts["contacts_count"] += 1
        elif category == CAMERA:
            counts["camera_count"] += 1
        elif category == MICROPHONE:
            counts["microphone_count"] += 1
        elif category == SMS_CALL:
            counts["sms_call_count"] += 1
        elif category == STORAGE:
            counts["storage_count"] += 1
        elif category == NETWORK:
            counts["network_count"] += 1
        else:
            counts["other_count"] += 1

    counts["sensitive_category_count"] = sum(
        1
        for key in [
            "location_count",
            "contacts_count",
            "camera_count",
            "microphone_count",
            "sms_call_count",
        ]
        if counts[key] > 0
    )
    return counts


def build_feature_row(app_row: pd.Series) -> Dict[str, int | str]:
    """
    Tek bir uygulama satırından özellik sözlüğü çıkarır.
    """
    permissions = parse_permissions(app_row.get("permissions", ""))
    counts = count_categories(permissions)
    label = label_risk(counts)

    feature_row: Dict[str, int | str] = {
        "app_name": app_row.get("app_name", ""),
        "category": app_row.get("category", ""),
        "source": app_row.get("source", ""),
        "total_permissions": len(permissions),
        **{k: counts[k] for k in counts if k != "other_count"},
    }
    feature_row["label"] = label
    return feature_row


def build_feature_df(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Ham veriden öznitelik ve etiket DataFrame'i üretir.
    """
    feature_rows = [build_feature_row(row) for _, row in df_raw.iterrows()]
    df_features = pd.DataFrame(feature_rows)
    # Sütun sıralamasını sabitle
    ordered_cols = ["app_name", "category", "source"] + config.FEATURE_COLUMNS + [
        "label"
    ]
    return df_features[ordered_cols]

