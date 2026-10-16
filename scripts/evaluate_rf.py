"""
evaluate_rf.py
--------------
Trains a fresh Random Forest from scratch and evaluates it honestly.
Prints the classification report, confusion matrix, and ROC-AUC.
No file handle conflicts — trains entirely in-process.
"""

import sys
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.config import LABELED_DIR
from src.stage1_parser.batch_extractor import extract_dataset
from src.utils.logger import get_logger

log = get_logger("evaluate_rf")


def main():
    combined_csv = LABELED_DIR / "combined_benchmark.csv"
    if not combined_csv.exists():
        log.error(f"Dataset not found: {combined_csv}")
        sys.exit(1)

    # 1. Extract features
    X, y, feature_names, df_valid = extract_dataset(combined_csv)
    log.info(f"Dataset: {len(X)} samples, {X.shape[1]} features")
    log.info(f"Class distribution -> COMPLIANT: {(y==0).sum()}, MISCONFIGURED: {(y==1).sum()}")

    # 2. 80/20 stratified split (same seed as main training)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    log.info(f"Train: {len(X_train)}  |  Test: {len(X_test)}")

    # 3. Train a fresh RF (simpler, no calibration wrapping — raw results)
    log.info("Training fresh Random Forest (500 trees)...")
    rf = RandomForestClassifier(n_estimators=500, max_depth=20, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)

    # 4. Evaluate
    probas = rf.predict_proba(X_test)[:, 1]
    y_pred = rf.predict(X_test)

    report = classification_report(y_test, y_pred, target_names=["COMPLIANT", "MISCONFIGURED"], digits=4)
    auc    = roc_auc_score(y_test, probas)
    cm     = confusion_matrix(y_test, y_pred)

    TN, FP, FN, TP = cm.ravel()

    print("\n" + "="*60)
    print("  RF EVALUATION RESULTS  (fresh re-run, seed=42)")
    print("="*60)
    print(report)
    print(f"ROC-AUC Score        : {auc:.4f}")
    print()
    print("Confusion Matrix:")
    print(f"                 Predicted")
    print(f"                 COMPLIANT  MISCONFIG")
    print(f"Actual COMPLIANT    {TN:>5}       {FP:>5}")
    print(f"Actual MISCONFIG    {FN:>5}       {TP:>5}")
    print()
    print(f"True  Positives  (TP) = {TP}   (correctly caught misconfigs)")
    print(f"True  Negatives  (TN) = {TN}   (correctly passed compliant)")
    print(f"False Positives  (FP) = {FP}   (false alarms)")
    print(f"False Negatives  (FN) = {FN}   (missed misconfigs — dangerous!)")
    print("="*60)

    # 5. Feature importance top-5
    importances = rf.feature_importances_
    top5_idx = np.argsort(importances)[::-1][:5]
    print("\nTop-5 Most Important Features:")
    for rank, idx in enumerate(top5_idx, 1):
        name = feature_names[idx] if idx < len(feature_names) else f"feat_{idx}"
        print(f"  {rank}. {name:45s}  importance={importances[idx]:.4f}")
    print("="*60)


if __name__ == "__main__":
    main()
