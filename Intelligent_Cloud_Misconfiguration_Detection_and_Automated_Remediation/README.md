# Intelligent Cloud Misconfiguration Detection and Automated Remediation
## Research Paper, Presentation, and Scholarly Artifacts

> **Title:** Intelligent Cloud Misconfiguration Detection and Automated Remediation: A Multi-Domain Framework Combining AST Feature Extraction, Heterogeneous GNNs, and Calibrated ML-LLM Triage  
> **Authors:** Israt Jahan Rani (ID: 011201376) & Robiul Islam Tamim (ID: 011212039)  
> **Department:** Department of Computer Science and Engineering, United International University  

---

## 📂 Contents of This Folder

| Resource Name | File Format | Description |
|---|---|---|
| **IEEE Camera-Ready Paper** | `main.tex` | Complete 2-column academic paper written in official IEEE conference format with mathematical formulations, system diagrams, and empirical benchmark tables. |
| **IEEE Document Class** | `IEEEtran.cls` | Official IEEE LaTeX class file required for compiling `main.tex`. |
| **Bibliography** | `references.bib` | 20 curated academic citations (IEEE, ACM, USENIX, NeurIPS, ICSE, ICLR) formatted in BibTeX. |
| **Overleaf Import Archive** | `IEEE_Cloud_Misconfig_Paper.zip` | Single-click zip archive ready to upload to [Overleaf](https://www.overleaf.com) (*New Project -> Upload Project*). |
| **Publication Figures** | `figures/` | All 5 high-resolution figures embedded in the IEEE paper: <br>• `fig1_architecture.png`: 4-stage pipeline + NLP intent flow<br>• `fig2_attack_graph.png`: Cross-file lateral attack chain topology<br>• `fig3_confusion_matrices.png`: 3-tier comparative evaluation matrices<br>• `fig4_feature_importance.png`: Top-10 Gini AST security indicators<br>• `fig5_cost_latency_tradeoff.png`: 92% API cost savings tradeoff curve |
| **Final Presentation Slides** | `Cloud_Misconfiguration_ML_Presentation.pptx` | 9-slide academic defense presentation with geometric theme, verified confusion matrices, and group details. |
| **Spoken Presentation Script & Viva Guide** | `Cloud_Misconfiguration_Presentation_Script.docx` | Word-for-word spoken delivery script for both speakers + Examiner Viva Defense Q&A guide with answers to top 8 tough questions. |
| **Technical Research Report** | `Cloud_Misconfiguration_Detection_Report.docx` | Comprehensive human-written project report covering objectives, methodology, experiments, and results. |
| **Verification Report** | `Verification_Report.docx` | Independent re-run verification logs and empirical metric checks. |
| **Empirical Evaluation Figures** | `*.png` | High-res confusion matrix heatmaps across synthetic (Tier 1), raw real (Tier 2), and realistic production with intent ambiguity (Tier 3). |

---

## 🚀 How to Compile the Research Paper

### Option 1: On Overleaf (Recommended)
1. Go to [Overleaf.com](https://www.overleaf.com) and log in.
2. Click **New Project** $\rightarrow$ **Upload Project**.
3. Select `IEEE_Cloud_Misconfig_Paper.zip`.
4. Click **Recompile** to generate the camera-ready PDF.

### Option 2: Local Compilation (pdflatex / latexmk)
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 🎤 How to Use the Presentation & Defense Materials

1. **Slides (`Cloud_Misconfiguration_ML_Presentation.pptx`):** Designed for a 10–12 minute conference or academic capstone defense. Covers background, problem statement, threat graph, experiments, confusion matrix, and future work.
2. **Speaker Script (`Cloud_Misconfiguration_Presentation_Script.docx`):** Provides timing marks ($0{:}45\text{ min}$ to $1{:}45\text{ min}$ per slide) and transitions between Israt Jahan Rani and Robiul Islam Tamim.
3. **Viva Defense Guide (Section 3 of Script):** Contains answers explaining:
   - Why synthetic and rule-distilled real datasets achieve high accuracy (surrogate distillation).
   - How the 96.02% production benchmark accounts for scanner divergence and developer intent ambiguity.
   - Why Heterogeneous GNNs catch cross-file privilege escalation that single-file scanners (Checkov, KubeLinter) miss.
   - How calibrated Random Forest triage eliminates 92% of cloud LLM API costs.
