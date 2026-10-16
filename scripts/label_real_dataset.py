"""
label_real_dataset.py
─────────────────────
Phase 2 (Real Data) — Multi-Scanner Consensus Labelling on Real Manifests

Iterates over data/raw_real/ (Kubernetes, IAM, Serverless), executes
multi-scanner consensus evaluation (Checkov + KubeLinter + Terrascan AST checks),
and produces data/labeled/real_benchmark.csv.

CRITICAL: Pure objective analysis — no filename keywords are used.
"""

import sys
from pathlib import Path
import pandas as pd
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.labelling.consensus_labeller import audit_manifest
from src.utils.logger import get_logger

log = get_logger("label_real")

REAL_RAW_DIR = ROOT / "data" / "raw_real"
OUT_CSV = ROOT / "data" / "labeled" / "real_benchmark.csv"


def main():
    if not REAL_RAW_DIR.exists():
        log.error(f"Directory {REAL_RAW_DIR} does not exist. Run ingest_real_dataset.py first.")
        sys.exit(1)

    domains = ["kubernetes", "iam", "serverless"]
    records = []

    for domain in domains:
        domain_dir = REAL_RAW_DIR / domain
        if not domain_dir.exists():
            continue

        files = sorted(list(domain_dir.glob("*.yaml")) + list(domain_dir.glob("*.yml")) + list(domain_dir.glob("*.json")))
        log.info(f"Labelling {len(files)} real {domain} manifests...")

        for fpath in tqdm(files, desc=f"Consensus Audit: {domain}"):
            try:
                rec = audit_manifest(fpath, domain=domain)
                records.append(rec)
            except Exception as e:
                log.warning(f"Error auditing {fpath.name}: {e}")

    if not records:
        log.error("No records audited.")
        sys.exit(1)

    df = pd.DataFrame(records)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)

    log.info(f"Saved {len(df)} labelled real manifests to {OUT_CSV}")

    # Summary Statistics
    print("\n" + "="*55)
    print("REAL DATASET CONSENSUS LABELLING SUMMARY")
    print("="*55)
    print(f"Total Unique Manifests : {len(df)}")
    print("\nClass Distribution:")
    print(df["label"].value_counts())
    print("\nBy Domain & Label:")
    print(pd.crosstab(df["domain"], df["label"]))
    print("\nSeverity Breakdown:")
    print(df["severity"].value_counts())
    print("="*55)


if __name__ == "__main__":
    main()
