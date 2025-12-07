from __future__ import annotations

import argparse

from src.evaluate import evaluate_models
from src.predict import predict_risk
from src.train import preprocess_raw, train_models


def cmd_preprocess(_: argparse.Namespace):
    df = preprocess_raw()
    print(f"İşlenmiş veri {df.shape[0]} satır ile kaydedildi: data/processed/apps_features.csv")


def cmd_train(_: argparse.Namespace):
    metrics, best = train_models()
    print("Eğitim tamamlandı. Modellerin performansı (macro F1):")
    for name, vals in metrics.items():
        print(f"- {name}: acc={vals['accuracy']:.3f} | f1={vals['macro_f1']:.3f}")
    print(f"En iyi model: {best} (data/processed/best_model.joblib)")


def cmd_evaluate(_: argparse.Namespace):
    evaluate_models()


def cmd_predict(args: argparse.Namespace):
    risk = predict_risk(args.permissions)
    print(f"Tahmin edilen gizlilik riski: {risk}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PrivacyRiskClassifier CLI - izinlerden gizlilik riski tahmini"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("preprocess", help="Ham CSV'den özellikli veri seti üret")
    sub.add_parser("train", help="Temel modelleri eğit ve en iyisini kaydet")
    sub.add_parser("evaluate", help="Modelleri test kümesinde değerlendir")

    predict_parser = sub.add_parser("predict", help="İzin dizesinden risk tahmini yap")
    predict_parser.add_argument(
        "--permissions",
        required=True,
        help='Noktalı virgülle ayrılmış izin listesi. Örn: "android.permission.ACCESS_FINE_LOCATION;android.permission.READ_CONTACTS"',
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "preprocess":
        cmd_preprocess(args)
    elif args.command == "train":
        cmd_train(args)
    elif args.command == "evaluate":
        cmd_evaluate(args)
    elif args.command == "predict":
        cmd_predict(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


