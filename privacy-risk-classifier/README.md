
# PrivacyRiskClassifier

Android uygulamalarının istediği izinlerden yola çıkarak gizlilik riski (LOW/MEDIUM/HIGH) seviyesini tahmin eden örnek proje. Küçük bir örnek veri kümesi, izin taksonomisi, kural tabanlı zayıf etiketleme ve basit ML modelleri ile uçtan uca çalışan bir akış sunar.

## Neden izinler?
- İzinler, uygulamanın hangi verilere/kapasitelere eriştiğini gösterir.
- Konum, kişiler, kamera/mikrofon, SMS/arama gibi hassas izin kombinasyonları daha yüksek gizlilik riski doğurabilir.
- Bu proje, izinlerden yola çıkarak hızlı bir risk sezgisi üretmeyi hedefler (kötü niyet garantisi vermez).

## Yaklaşım
- **İzin taksonomisi:** LOCATION, CONTACTS, CAMERA, MICROPHONE, SMS_CALL, STORAGE, NETWORK, OTHER.
- **Zayıf etiketleme:** Basit kurallar ile (sms_call>0, konum+kişiler, kamera+mikrofon, hassas kategori>=3) HIGH; hassas kategori 1-2 ise MEDIUM; aksi LOW.
- **Özellik çıkarımı:** Toplam izin sayısı + kategori sayımları.
- **Modeller:** Logistic Regression, Decision Tree, Random Forest. En yüksek macro F1 skoruna sahip model kaydedilir.

## Kurulum
```bash
pip install -r requirements.txt
```

## Veri
- Örnek ham CSV: `data/raw/apps_permissions.csv`
- İşlenmiş özellikler: `data/processed/apps_features.csv` (CLI ile üretilir)

## CLI Kullanımı
Tüm komutlar repo kökünde çalıştırılır:
```bash
# 1) Ham veriyi işle
python cli.py preprocess

# 2) Modelleri eğit ve en iyisini kaydet
python cli.py train

# 3) Değerlendir (accuracy, macro F1, classification report, confusion matrix)
python cli.py evaluate

# 4) İzin dizesinden tahmin yap
python cli.py predict --permissions "android.permission.ACCESS_FINE_LOCATION;android.permission.READ_CONTACTS"
```

## Notebooks
- `notebooks/01_eda_and_labeling.ipynb`: Ham veriyi görselleştirme ve kural tabanlı etiketleme örnekleri.
- `notebooks/02_model_baselines.ipynb`: Basit model eğitim/değerlendirme örnekleri.

## Sınırlamalar ve etik
- Bu proje sadece bir risk tahmini sunar; kötü amaçlılık veya gerçek gizlilik ihlali garantisi vermez.
- Küçük ve sentetik veri, genellenebilirliği sınırlar; gerçek dünyada daha büyük ve dengeli veri gerekir.
- İzinler her zaman kullanım bağlamını yansıtmaz; karar vermede insan gözetimi önemlidir.


