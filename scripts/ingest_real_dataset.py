"""
ingest_real_dataset.py
───────────────────────
Phase 1 (Real Data) — Clone & Curate Real-World Cloud Manifests

Clones top open-source production and benchmark repositories, extracts
clean Kubernetes, IAM/CloudFormation, and Serverless SAM manifests,
deduplicates via SHA-256, and stores them in data/raw/real/{domain}/.

All filenames are neutral (e.g. k8s_real_0001.yaml) to ensure zero label leakage.
"""

import sys
import os
import shutil
import subprocess
import hashlib
import yaml
import json
from pathlib import Path
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.logger import get_logger

log = get_logger("ingest_real")

TEMP_DIR = ROOT / "data" / "staging_repos"
REAL_RAW_DIR = ROOT / "data" / "raw_real"
REAL_K8S_DIR = REAL_RAW_DIR / "kubernetes"
REAL_IAM_DIR = REAL_RAW_DIR / "iam"
REAL_SAM_DIR = REAL_RAW_DIR / "serverless"

# Repositories to clone
REPOS = [
    # Kubernetes Vulnerable & Benchmark Repositories
    {
        "url": "https://github.com/madhuakula/kubernetes-goat.git",
        "name": "kubernetes-goat",
        "domain": "kubernetes",
        "subpath": "scenarios"
    },
    {
        "url": "https://github.com/stackrox/kube-linter.git",
        "name": "kube-linter",
        "domain": "kubernetes",
        "subpath": "test/testdata"
    },
    {
        "url": "https://github.com/GoogleCloudPlatform/microservices-demo.git",
        "name": "gcp-microservices",
        "domain": "kubernetes",
        "subpath": "kubernetes-manifests"
    },
    {
        "url": "https://github.com/prometheus/prometheus.git",
        "name": "prometheus",
        "domain": "kubernetes",
        "subpath": "documentation/examples"
    },
    {
        "url": "https://github.com/argoproj/argo-cd.git",
        "name": "argo-cd",
        "domain": "kubernetes",
        "subpath": "manifests"
    },
    # AWS IAM & CloudFormation Repositories
    {
        "url": "https://github.com/awslabs/aws-cloudformation-templates.git",
        "name": "aws-cft",
        "domain": "iam",
        "subpath": "aws"
    },
    {
        "url": "https://github.com/nccgroup/PMapper.git",
        "name": "pmapper",
        "domain": "iam",
        "subpath": "test"
    },
    # Serverless SAM Repositories
    {
        "url": "https://github.com/aws-samples/serverless-patterns.git",
        "name": "serverless-patterns",
        "domain": "serverless",
        "subpath": ""
    }
]


def clone_repo(repo_url: str, dest_dir: Path) -> bool:
    """Performs a shallow clone (depth 1) of the target repository."""
    if dest_dir.exists():
        log.info(f"Using cached clone for {dest_dir.name}")
        return True
    try:
        log.info(f"Cloning {repo_url} (depth 1)...")
        cmd = ["git", "clone", "--depth", "1", repo_url, str(dest_dir)]
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        return True
    except Exception as e:
        log.warning(f"Failed to clone {repo_url}: {e}")
        return False


def is_valid_k8s_manifest(content: str) -> bool:
    """Checks if content resembles a valid Kubernetes manifest."""
    try:
        data = yaml.safe_load(content)
        if isinstance(data, dict):
            return "apiVersion" in data and "kind" in data
    except Exception:
        pass
    return False


def is_valid_iam_manifest(content: str) -> bool:
    """Checks if content resembles AWS IAM or CloudFormation template."""
    content_lower = content.lower()
    if "awstemplateformatversion" in content_lower or "resources" in content_lower:
        return True
    if "statement" in content_lower and ("action" in content_lower or "effect" in content_lower):
        return True
    return False


def is_valid_sam_manifest(content: str) -> bool:
    """Checks if content resembles AWS Serverless Application Model (SAM)."""
    content_lower = content.lower()
    return "aws::serverless" in content_lower or "transform: aws::serverless-2016-10-31" in content_lower


def sanitize_and_collect():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    REAL_K8S_DIR.mkdir(parents=True, exist_ok=True)
    REAL_IAM_DIR.mkdir(parents=True, exist_ok=True)
    REAL_SAM_DIR.mkdir(parents=True, exist_ok=True)

    seen_hashes = set()
    counts = {"kubernetes": 0, "iam": 0, "serverless": 0}

    for repo_info in REPOS:
        repo_dir = TEMP_DIR / repo_info["name"]
        if not clone_repo(repo_info["url"], repo_dir):
            continue

        search_path = repo_dir / repo_info["subpath"] if repo_info["subpath"] else repo_dir
        if not search_path.exists():
            search_path = repo_dir

        domain = repo_info["domain"]
        dest_dir = REAL_K8S_DIR if domain == "kubernetes" else (REAL_IAM_DIR if domain == "iam" else REAL_SAM_DIR)

        # Collect all YAML and JSON files
        exts = ["*.yaml", "*.yml", "*.json"]
        found_files = []
        for ext in exts:
            found_files.extend(search_path.rglob(ext))

        log.info(f"Scanning {len(found_files)} files in {repo_info['name']} for {domain}...")

        for fpath in found_files:
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
                if len(text.strip()) < 50 or len(text) > 200_000:
                    continue

                # Filter by domain structure
                if domain == "kubernetes" and not is_valid_k8s_manifest(text):
                    continue
                elif domain == "iam" and not is_valid_iam_manifest(text):
                    continue
                elif domain == "serverless" and not is_valid_sam_manifest(text):
                    continue

                # Hash deduplication
                h = hashlib.sha256(text.encode("utf-8")).hexdigest()
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                # Save with neutral naming
                counts[domain] += 1
                ext = fpath.suffix if fpath.suffix in [".yaml", ".yml", ".json"] else ".yaml"
                prefix = "k8s_real" if domain == "kubernetes" else ("iam_real" if domain == "iam" else "sam_real")
                out_name = f"{prefix}_{counts[domain]:04d}{ext}"
                
                (dest_dir / out_name).write_text(text, encoding="utf-8")

            except Exception:
                continue

    log.info("=== Real Data Ingestion Completed ===")
    for d, c in counts.items():
        log.info(f"  {d:>12}: {c} unique real manifests")
    return counts


if __name__ == "__main__":
    sanitize_and_collect()
