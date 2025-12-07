"""
Basit kural tabanlı gizlilik risk etiketleyici.

Kurallar:
- HIGH:
    * sms_call_count > 0
    * veya (location_count > 0 ve contacts_count > 0)
    * veya (camera_count > 0 ve microphone_count > 0)
    * veya sensitive_category_count >= 3
- MEDIUM:
    * sensitive_category_count 1 ya da 2 ise
    * sms_call_count == 0
    * ve HIGH kombinasyonlarından hiçbiri yoksa
- LOW: diğer tüm durumlar
"""

from __future__ import annotations

from typing import Dict

SENSITIVE_KEYS = [
    "location_count",
    "contacts_count",
    "camera_count",
    "microphone_count",
    "sms_call_count",
]


def label_risk(permission_counts: Dict[str, int]) -> str:
    """
    Kategori bazlı izin sayımlarından gizlilik risk seviyesi üretir.
    """
    counts = {k: int(permission_counts.get(k, 0)) for k in permission_counts.keys()}

    location = counts.get("location_count", 0)
    contacts = counts.get("contacts_count", 0)
    camera = counts.get("camera_count", 0)
    microphone = counts.get("microphone_count", 0)
    sms_call = counts.get("sms_call_count", 0)
    sensitive = counts.get("sensitive_category_count", 0)

    high_combo = (location > 0 and contacts > 0) or (camera > 0 and microphone > 0)

    if sms_call > 0 or high_combo or sensitive >= 3:
        return "HIGH"

    if sensitive in (1, 2) and sms_call == 0 and not high_combo:
        return "MEDIUM"

    return "LOW"

