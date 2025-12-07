Overview

PrivacyRiskClassifier predicts an Android app’s privacy risk level (LOW/MEDIUM/HIGH) based on requested permissions.
It uses a permission taxonomy, rule-based weak labels, and baseline ML models to provide an interpretable, end-to-end classification pipeline.

Why Permissions?

Permission combinations can signal potential privacy exposure. This project turns raw permission lists into a simple, actionable risk estimate and serves as a focused classification case study with clear, explainable assumptions.

Approach (V1)

Group Android permissions into categories (Location, Contacts, Camera, Microphone, SMS/Call, Storage, Network).

Generate initial labels using transparent rules (weak supervision).

Engineer category-level count features from permission strings.

Train and compare baseline classifiers: Logistic Regression, Decision Tree, Random Forest.

Provide a reproducible CLI pipeline for preprocessing, training, evaluation, and prediction.

Quick Start
python cli.py preprocess
python cli.py train
python cli.py evaluate
python cli.py predict --permissions "android.permission.ACCESS_FINE_LOCATION;android.permission.READ_CONTACTS"

Limitations and Ethics

V1 uses a small sample dataset and rule-based labels; results are primarily for demonstration and learning.
This tool provides risk estimations based on permissions and does not guarantee malicious intent.
Some apps legitimately require sensitive permissions to deliver core functionality.
