## Overview
PrivacyRiskClassifier predicts an Android app's privacy risk level (LOW/MEDIUM/HIGH) based on requested permissions.
It uses a permission taxonomy, rule-based weak labels, and baseline ML models to provide an interpretable starting point.

## Why permissions?
Permission combinations can reveal potential privacy exposure. This project aims to turn permission lists into a simple,
actionable risk signal for users and a clean classification case study for engineers.

## Approach (V1)
- Group permissions into categories (Location, Contacts, Camera, Microphone, SMS/Call, Storage, Network).
- Generate initial labels using transparent rules (weak supervision).
- Engineer category-level count features.
- Train and compare baseline classifiers: Logistic Regression, Decision Tree, Random Forest.
- Provide a CLI pipeline for preprocessing, training, evaluation, and prediction.

## Quick Start
python cli.py preprocess
python cli.py train
python cli.py evaluate
python cli.py predict --permissions "android.permission.ACCESS_FINE_LOCATION;android.permission.READ_CONTACTS"

## Limitations
V1 uses a small sample dataset and rule-based labels. Results are for demonstration and learning purposes.
This tool provides risk estimations based on permissions and does not guarantee malicious intent.

