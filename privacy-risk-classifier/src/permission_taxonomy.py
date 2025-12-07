"""
Android izinlerini gizlilik risk kategorilerine eşlemek için basit bir taksonomi.
"""

from __future__ import annotations

from typing import Dict

# Kategoriler
LOCATION = "LOCATION"
CONTACTS = "CONTACTS"
CAMERA = "CAMERA"
MICROPHONE = "MICROPHONE"
SMS_CALL = "SMS_CALL"
STORAGE = "STORAGE"
NETWORK = "NETWORK"
OTHER = "OTHER"

CATEGORIES = [
    LOCATION,
    CONTACTS,
    CAMERA,
    MICROPHONE,
    SMS_CALL,
    STORAGE,
    NETWORK,
    OTHER,
]

# Android izin dizesi -> kategori eşlemesi
PERMISSION_TO_CATEGORY: Dict[str, str] = {
    # Konum
    "android.permission.ACCESS_FINE_LOCATION": LOCATION,
    "android.permission.ACCESS_COARSE_LOCATION": LOCATION,
    "android.permission.ACCESS_BACKGROUND_LOCATION": LOCATION,
    # Kişiler
    "android.permission.READ_CONTACTS": CONTACTS,
    "android.permission.WRITE_CONTACTS": CONTACTS,
    "android.permission.GET_ACCOUNTS": CONTACTS,
    # Kamera ve mikrofon
    "android.permission.CAMERA": CAMERA,
    "android.permission.RECORD_AUDIO": MICROPHONE,
    # SMS / çağrı
    "android.permission.READ_SMS": SMS_CALL,
    "android.permission.SEND_SMS": SMS_CALL,
    "android.permission.RECEIVE_SMS": SMS_CALL,
    "android.permission.RECEIVE_MMS": SMS_CALL,
    "android.permission.READ_CALL_LOG": SMS_CALL,
    "android.permission.WRITE_CALL_LOG": SMS_CALL,
    "android.permission.CALL_PHONE": SMS_CALL,
    # Depolama
    "android.permission.READ_EXTERNAL_STORAGE": STORAGE,
    "android.permission.WRITE_EXTERNAL_STORAGE": STORAGE,
    "android.permission.MANAGE_EXTERNAL_STORAGE": STORAGE,
    # Ağ
    "android.permission.INTERNET": NETWORK,
    "android.permission.ACCESS_WIFI_STATE": NETWORK,
    "android.permission.CHANGE_WIFI_STATE": NETWORK,
    "android.permission.ACCESS_NETWORK_STATE": NETWORK,
    "android.permission.CHANGE_NETWORK_STATE": NETWORK,
    # Diğer
    "android.permission.VIBRATE": OTHER,
    "android.permission.WAKE_LOCK": OTHER,
    "com.google.android.providers.gsf.permission.READ_GSERVICES": OTHER,
}


def normalize_permission(name: str) -> str:
    """İzin dizesini kıyaslama için normalize eder."""
    return name.strip()


def get_category(permission: str) -> str:
    """
    Verilen iznin kategorisini döndürür. Tanımsızsa OTHER.
    """
    normalized = normalize_permission(permission)
    return PERMISSION_TO_CATEGORY.get(normalized, OTHER)

