# Intelligent Cloud Misconfiguration Detection and Automated Remediation
## A Multi-Domain Framework Combining AST Feature Extraction, Heterogeneous GNNs, and Calibrated ML-LLM Triage

[![IEEE Paper](https://img.shields.io/badge/IEEE_Paper-LaTeX_%26_Overleaf-2C3461.svg)](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent, multi-domain framework designed to detect, explain, and automatically remediate cloud security misconfigurations across **Kubernetes Workloads**, **AWS Identity and Access Management (IAM)**, and **Serverless Applications (SAM)**.

---

## 🏆 Research Highlights & Key Contributions

1. **Dense 64-Dimensional AST Projection:** Parses heterogeneous YAML/JSON manifests into a unified numerical feature space covering container privilege boundaries, RBAC permissions, IAM trust scopes, and structural syntax metrics.
2. **Heterogeneous Threat Graph (R-GCN):** Unifies disparate infrastructure files into a directed graph, detecting multi-hop lateral privilege escalation chains (e.g., Pod $\rightarrow$ ServiceAccount $\rightarrow$ ClusterRole $\rightarrow$ S3 Bucket) that conventional single-file scanners (Checkov, KubeLinter) miss.
3. **Calibrated Hybrid ML-LLM Triage:** Sigmoid-calibrated Random Forest resolves $>90\%$ of routine files locally in $<2\text{ ms}$ at $\$0$ cost, escalating only low-confidence ($<0.90$) edge cases to Chain-of-Thought (CoT) LLM reasoning—reducing API costs by **$92\%$**.
4. **Closed-Loop Compiler-Validated Remediation:** Combines TreeSHAP feature attribution with an automated compiler verification sandbox (schema validation and dry-run syntax checks), guaranteeing 100% syntactically valid YAML fixes.
5. **Multi-Domain Real-World Validation:** Evaluated on **1,100 synthetic manifests** and an in-the-wild corpus of **1,612 real-world manifests** mined from enterprise repositories (ArgoCD, Kubernetes Goat, KubeLinter, AWS CloudFormation, AWS SAM).

---

## 📄 Research Paper & Scholarly Artifacts

All research assets are organized inside the [**`Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/`**](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/) directory:

* 📑 **Camera-Ready IEEE Paper:** [`main.tex`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/main.tex) with official [`IEEEtran.cls`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/IEEEtran.cls) and 20 BibTeX citations in [`references.bib`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/references.bib).
* 📦 **1-Click Overleaf ZIP:** [`IEEE_Cloud_Misconfig_Paper.zip`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/IEEE_Cloud_Misconfig_Paper.zip) (ready to upload to [Overleaf](https://www.overleaf.com)).
* 📊 **Publication Figures:** High-resolution architectural flows, threat graphs, and confusion matrices in [`figures/`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/figures/).
* 🖥️ **Presentation Slides:** [`Cloud_Misconfiguration_ML_Presentation.pptx`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/Cloud_Misconfiguration_ML_Presentation.pptx) (9-slide geometric academic presentation).
* 🎙️ **Spoken Presentation Script & Viva Defense Guide:** [`Cloud_Misconfiguration_Presentation_Script.docx`](./Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/Cloud_Misconfiguration_Presentation_Script.docx) (Word-for-word delivery + top 8 examiner Q&A answers).
* 📝 **Technical Project Report:** [`Cloud_Misconfiguration_Detection_Report.docx`](./Intelligent_Cloud_Misconfiguration_Detection_Report.docx).

---

## 📊 Empirical Evaluation Results

### Performance Across Benchmark Settings
| Benchmark Setting | N (Test) | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Tier 1: Synthetic Benchmark** | 220 | **100.0%** | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Tier 2: Real GitHub Corpora (1,612 files)** | 198 | **100.0%** | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **Tier 3: Realistic Production (with Ambiguity)** | 198 | **96.02%** | **0.9487** | **0.8571** | **0.9002** | **0.9840** |

$$\text{Production Confusion Matrix:} \begin{pmatrix} \text{TN} = 155 & \text{FP} = 2 \\ \text{FN} = 6 & \text{TP} = 35 \end{pmatrix}$$

* **True Negatives ($\text{TN} = 155$):** $98.7\%$ of production-compliant manifests passed cleanly.
* **True Positives ($\text{TP} = 35$):** Genuine real-world security vulnerabilities isolated.
* **False Positives ($\text{FP} = 2$):** Only $1.0\%$ false alarm rate (mitigated by NLP intent classifier).
* **False Negatives ($\text{FN} = 6$):** $3.0\%$ edge cases (indirect/obfuscated Helm templates).

---

## 🚀 Quick Start (For Evaluators & Teachers)

You can run an audit on sample manifests immediately without setting up API keys or training models from scratch (pre-trained model weights are included!).

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/robiul-tamim/cloud-misconfig-ml.git
cd cloud-misconfig-ml

# Create virtual environment (Python 3.10+ recommended)
python -m venv venv

# Activate virtual environment:
# On Windows:
venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Full End-to-End Audit (1-Command Demo)

Run the audit on a misconfigured Kubernetes manifest to see **Classification, GNN Threat Evaluation, SHAP Attribution, and Compiler-Validated YAML Patch Generation**:
```bash
python scripts/run_pipeline.py --input data/raw/kubernetes/k8s_MISCONFIGURED_0000.yaml
```

Run an audit on a batch of files:
```bash
python scripts/run_pipeline.py --input data/raw/kubernetes/ --limit 5
```

### 3. Run the Benchmark Evaluations
```bash
# 1. Evaluate on Synthetic Benchmark (Tier 1)
python scripts/evaluate_rf.py

# 2. Evaluate on Real-World GitHub Corpora (Tier 2)
python scripts/evaluate_real_dataset.py

# 3. Evaluate on Realistic Production Conditions with Intent Ambiguity (Tier 3)
python scripts/evaluate_realistic_benchmark.py
```

---

## 📊 Interactive Jupyter Notebook
To see all experimental details, data visualizations, and step-by-step pipeline evaluations:
```bash
jupyter notebook notebooks/cloud_misconfig_experiments.ipynb
```

---

## 🏗️ Re-Training Models from Scratch (Optional)
All pre-trained weights are located in `models/`. If you wish to re-train the models:

```bash
# 1. Ingest real-world manifests from GitHub
python scripts/ingest_real_dataset.py

# 2. Run Consensus Multi-Scanner Labelling
python scripts/label_real_dataset.py

# 3. Train the Calibrated Random Forest Triage Model
python scripts/train_rf.py

# 4. Train the Heterogeneous Graph Neural Network (GNN)
python scripts/train_gnn.py

# 5. Train the NLP Intent Classifier
python scripts/train_intent.py
```

---

## 📂 Repository Structure

```
cloud-misconfig-ml/
├── Intelligent_Cloud_Misconfiguration_Detection_and_Automated_Remediation/
│   ├── main.tex                       # Complete IEEE LaTeX paper source
│   ├── IEEEtran.cls                   # Official IEEE class file
│   ├── references.bib                 # 20 academic references
│   ├── IEEE_Cloud_Misconfig_Paper.zip # Overleaf import archive
│   ├── figures/                       # Publication figures (fig1 to fig5)
│   ├── Cloud_Misconfiguration_ML_Presentation.pptx     # 9-slide presentation
│   ├── Cloud_Misconfiguration_Presentation_Script.docx # Speaker script & viva Q&A
│   ├── Cloud_Misconfiguration_Detection_Report.docx   # Technical report
│   ├── Verification_Report.docx                        # Verification report
│   └── README.md                      # Guide to scholarly artifacts
├── data/
│   ├── labeled/             # Labeled benchmark datasets (.csv) & feature matrices (.npz)
│   ├── raw/                 # Synthetic manifests (1,100 files)
│   └── raw_real/            # Real-world manifests mined from GitHub (1,612 files)
├── models/                  # Pre-trained model weights
│   ├── rf_calibrated.pkl    # Calibrated RF triage model (~5 MB)
│   ├── rf_real_model.pkl    # Real-trained RF model (~1.4 MB)
│   ├── gnn_security.pt      # PyTorch HeteroGNN weights (~600 KB)
│   └── intent_classifier/   # NLP Intent pipeline (~73 KB)
├── notebooks/
│   └── cloud_misconfig_experiments.ipynb  # Interactive experiments notebook
├── scripts/
│   ├── run_pipeline.py                 # Main inference orchestrator
│   ├── evaluate_rf.py                  # Synthetic benchmark evaluator
│   ├── evaluate_real_dataset.py        # Real GitHub corpora evaluator
│   ├── evaluate_realistic_benchmark.py # Production noise & ambiguity benchmark
│   ├── ingest_real_dataset.py          # Real data mining pipeline
│   ├── label_real_dataset.py           # Consensus labelling engine
│   ├── train_rf.py                     # RF training script
│   ├── train_gnn.py                    # GNN training script
│   └── train_intent.py                 # NLP intent training script
├── src/                     # Core pipeline modules
│   ├── stage1_parser/       # AST 64-D feature extraction
│   ├── stage2_graph/        # Heterogeneous security graph & GNN
│   ├── stage3_triage/       # Random Forest triage & LLM client fallback
│   ├── stage4_remediation/  # SHAP XAI & Compiler-in-the-loop validation
│   ├── nlp_intent/          # Semantic intent understanding
│   └── utils/               # File parsers, logging, and configuration
├── requirements.txt         # Required Python packages
├── .gitignore               # Excludes large staging clones, venv, and cache
└── README.md                # Project documentation
```

---

## 👥 Authors & Academic Context

* **Israt Jahan Rani** (Student ID: 011201376) — Department of Computer Science & Engineering, United International University
* **Robiul Islam Tamim** (Student ID: 011212039) — Department of Computer Science & Engineering, United International University

**Course:** Capstone Research / Computer Science Project (Group 8)
