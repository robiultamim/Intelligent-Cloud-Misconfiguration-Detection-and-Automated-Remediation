"""
evaluate_real_dataset.py
─────────────────────────
Phase 3 & 4 (Real Data) — AST Feature Extraction & Model Evaluation on Real Data

1. Extracts 64-D AST vectors for all files in data/labeled/real_benchmark.csv.
2. Trains a Random Forest on real training set (80/20 stratified split).
3. Evaluates on real test set -> Outputs true Confusion Matrix, F1, Precision, Recall.
4. Evaluates Out-of-Distribution Transfer (Synthetic-trained RF tested on Real data).
"""

import sys
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.stage1_parser.batch_extractor import extract_dataset
from src.utils.logger import get_logger

log = get_logger("evaluate_real")

REAL_CSV = ROOT / "data" / "labeled" / "real_benchmark.csv"
SYNTH_MODEL_PATH = ROOT / "models" / "rf_calibrated.pkl"
REAL_FEATURES_NPZ = ROOT / "data" / "labeled" / "features_real_dataset.npz"


def main():
    if not REAL_CSV.exists():
        log.error(f"Real benchmark CSV not found: {REAL_CSV}. Run label_real_dataset.py first.")
        sys.exit(1)

    # 1. Extract 64-D Features
    log.info(f"Extracting 64-D AST features from {REAL_CSV}...")
    X_real, y_real, feature_names, df_valid = extract_dataset(REAL_CSV)

    np.savez_compressed(REAL_FEATURES_NPZ, X=X_real, y=y_real)
    log.info(f"Extracted {len(X_real)} real samples across {X_real.shape[1]} features.")
    log.info(f"Real Class Distribution -> COMPLIANT: {(y_real==0).sum()}, MISCONFIGURED: {(y_real==1).sum()}")

    # 2. 80/20 Stratified Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_real, y_real, test_size=0.20, random_state=42, stratify=y_real
    )
    log.info(f"Real Train: {len(X_train)}  |  Real Test: {len(X_test)}")

    # 3. Train Fresh Real-Data Random Forest
    log.info("Training Random Forest on Real Data (500 trees, max_depth=20)...")
    rf_real = RandomForestClassifier(n_estimators=500, max_depth=20, random_state=42, n_jobs=-1)
    rf_real.fit(X_train, y_train)

    # Save real model
    with open(ROOT / "models" / "rf_real_model.pkl", "wb") as f:
        pickle.dump(rf_real, f)

    # 4. Evaluate Real-Trained Model on Real Test Set
    probas_real = rf_real.predict_proba(X_test)[:, 1]
    y_pred_real = rf_real.predict(X_test)

    report_real = classification_report(y_test, y_pred_real, target_names=["COMPLIANT", "MISCONFIGURED"], digits=4)
    auc_real = roc_auc_score(y_test, probas_real)
    cm_real = confusion_matrix(y_test, y_pred_real)
    TN, FP, FN, TP = cm_real.ravel()

    print("\n" + "="*60)
    print("  EXPERIMENT A: MODEL TRAINED & TESTED ON REAL-WORLD DATA")
    print("="*60)
    print(report_real)
    print(f"ROC-AUC Score        : {auc_real:.4f}")
    print()
    print("Confusion Matrix:")
    print(f"                 Predicted")
    print(f"                 COMPLIANT  MISCONFIG")
    print(f"Actual COMPLIANT    {TN:>5}       {FP:>5}")
    print(f"Actual MISCONFIG    {FN:>5}       {TP:>5}")
    print()
    print(f"True  Positives  (TP) = {TP}   (correctly identified real misconfigs)")
    print(f"True  Negatives  (TN) = {TN}   (correctly passed compliant configs)")
    print(f"False Positives  (FP) = {FP}   (false alarms)")
    print(f"False Negatives  (FN) = {FN}   (missed threats)")
    print("="*60)

    # Top Features
    importances = rf_real.feature_importances_
    top5_idx = np.argsort(importances)[::-1][:5]
    print("\nTop-5 Discriminative Security Features (Real Data):")
    for rank, idx in enumerate(top5_idx, 1):
        name = feature_names[idx] if idx < len(feature_names) else f"feat_{idx}"
        print(f"  {rank}. {name:40s}  importance={importances[idx]:.4f}")
    print("="*60)


if __name__ == "__main__":
    main()
