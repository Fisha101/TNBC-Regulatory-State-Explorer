# TNBC Regulatory State Explorer

An interactive single-cell regulatory-network framework for exploring transcription-factor activity and regulatory heterogeneity in triple-negative breast cancer cells.

## Overview

Single-cell RNA-seq is commonly used to characterize cellular heterogeneity through gene-expression patterns. However, cells with relatively continuous expression profiles may still differ in the regulatory programs controlling those expression states.

**TNBC Regulatory State Explorer** analyzes transcription-factor regulatory activity in MDA-MB-231 triple-negative breast cancer cells and provides an interactive interface for exploring regulatory heterogeneity at single-cell resolution.

The project combines gene regulatory network inference, motif-supported regulon reconstruction, single-cell regulon activity estimation, dimensionality reduction, and matrix factorization.

The final dataset contains:

- **24,073 single cells**
- **225 transcription-factor regulons**
- **8 exploratory regulatory components**

---

## Biological Question

**Which transcription-factor regulatory programs define heterogeneity within MDA-MB-231 TNBC cells?**

The project also asks whether regulatory-network analysis can reveal localized or structured regulatory states that are less apparent when the same cells are represented using gene expression alone.

---

## Analysis Workflow

```text
scRNA-seq
    ↓
Quality control & preprocessing
    ↓
GRNBoost2
Gene regulatory network inference
    ↓
cisTarget
Motif-supported regulon reconstruction
    ↓
AUCell
Cell-level regulon activity
    ↓
Regulatory PCA / UMAP
    ↓
NMF regulatory components
    ↓
Target & pathway enrichment
    ↓
Interactive Streamlit explorer
```

### 1. Single-cell RNA-seq preprocessing

After quality control, **24,073 MDA-MB-231 cells** and **16,432 genes** were retained.

For the regulatory-network analysis, raw counts corresponding to the QC-passed cells and genes were reconstructed and normalized using total-count normalization followed by log transformation.

A mild gene-detection filter was applied while retaining transcription factors from the Lambert human transcription-factor reference.

The resulting input for regulatory-network inference contained:

**24,073 cells × 10,311 genes**

### 2. Gene regulatory network inference

**GRNBoost2** was used to infer associations between candidate transcription factors and potential target genes.

The analysis produced approximately **673,000 TF–target associations**.

These associations represent predictive relationships and should not be interpreted as evidence of direct or causal regulation.

### 3. Motif-supported regulons

**cisTarget** motif enrichment was used to refine the inferred network using human hg38 motif-ranking databases.

This resulted in **225 motif-supported transcription-factor regulons**.

Motif enrichment provides sequence-level support for TF–target relationships but does not demonstrate direct binding.

### 4. Single-cell regulon activity

**AUCell** was used to estimate the activity of each regulon in each individual cell.

The resulting regulatory activity matrix contains:

**24,073 cells × 225 regulons**

AUCell scores represent enrichment of regulon target genes among highly ranked genes in individual cells and should not be interpreted as direct measurements of TF protein activity.

### 5. Regulatory landscape

PCA and UMAP were applied to the regulon-activity representation.

The same cells were also represented in gene-expression space to enable comparison between:

- gene-expression structure
- regulatory-activity structure

The regulatory representation showed additional branching and localized structure within a largely continuous expression-space population.

This observation is treated as evidence of alternative structure in the regulatory representation rather than proof of distinct cell types.

### 6. Regulatory components

Non-negative matrix factorization (**NMF**) was applied to the non-negative AUCell matrix.

An **8-component representation** was retained as a compact exploratory description of recurring patterns of regulon activity.

The components include both broad regulatory gradients and more localized regulatory axes.

These components are continuous and potentially overlapping and should not be interpreted as eight discrete biological cell populations.

### 7. Functional interpretation

For each regulatory component, the top-loading regulons were used to retrieve motif-supported target genes.

Functional enrichment was evaluated using:

- GO Biological Process
- Reactome
- WikiPathways

Because many enrichment results were broad or shared between components, components were intentionally retained as **Regulatory Component 1–8** rather than assigning unsupported biological labels.

---

## Interactive Explorer

The Streamlit application contains four main sections.

### Overview

Compare the same cells in:

- **Gene Expression space**
- **Regulatory Activity space**

This allows direct exploration of how cell organization changes when cells are represented by inferred regulatory activity rather than gene expression.

### Regulon Explorer

Explore any of the **225 TF regulons**.

For each regulon, the app displays:

- regulatory UMAP activity
- AUCell activity
- prevalence across cells
- mean activity
- variability
- 95th percentile activity
- descriptive activity pattern
- external biological annotation for the corresponding transcription factor

### Regulatory Components

Explore all **8 NMF regulatory components**.

For each component, the app displays:

- activity across the regulatory landscape
- top contributing TF regulons
- NMF loadings
- functional enrichment results when sufficiently specific enrichment is available

### Methods & About

Provides a concise description of the analysis pipeline and important interpretation limitations.

---

## Key Observations

Regulon prevalence was strongly heterogeneous across the dataset.

Among the 225 inferred regulons:

- **76 regulons** were detected in ≤5% of cells
- **107 regulons** were detected in ≥95% of cells

This suggests a combination of broadly distributed regulatory activity and highly localized regulatory patterns.

The regulatory UMAP additionally revealed localized and branching structure not as apparent in the expression-space visualization.

NMF further summarized this landscape into broad regulatory gradients together with more localized regulatory axes.

These findings are exploratory and provide hypotheses for subsequent biological validation.

---

## Technology Stack

**Single-cell analysis**
- Python
- Scanpy
- AnnData

**Regulatory-network inference**
- pySCENIC
- GRNBoost2
- cisTarget
- AUCell

**Downstream analysis**
- pandas
- NumPy
- scikit-learn
- NMF
- UMAP

**Functional interpretation**
- g:Profiler
- GO Biological Process
- Reactome
- WikiPathways

**Interactive application**
- Streamlit
- Plotly

---

## Running the Explorer

Activate the analysis environment:

```bash
conda activate scrna
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open locally in a web browser.

---

## Project Structure

```text
mda_mb231_scRNA_project/
│
├── app.py
├── pipeline.ipynb
├── regulatory_analysis.ipynb
├── app_development.ipynb
│
├── app_data/
│   ├── cell_data.csv
│   ├── regulon_activity.csv
│   ├── regulon_summary.csv
│   ├── program_loadings.csv
│   ├── program_regulons.csv
│   ├── program_enrichment.csv
│   └── tf_annotations.csv
│
└── README.md
```

Large intermediate files and regulatory-network databases are not required to run the final explorer.

---

## Interpretation & Limitations

This project is designed for **exploratory research and hypothesis generation**.

Several limitations are important:

- regulon activity is inferred rather than directly measured;
- motif support does not demonstrate direct TF binding;
- NMF components are exploratory continuous axes rather than discrete cell types;
- UMAP is a nonlinear visualization and its geometry should not be interpreted as literal biological distance;
- functional enrichment provides biological context but does not demonstrate pathway activation;
- the current analysis is based on a single MDA-MB-231 dataset and therefore does not establish general TNBC regulatory states.

Independent TNBC datasets and experimental validation would be required to establish the generality and biological significance of the observed regulatory patterns.

---

## Purpose

**TNBC Regulatory State Explorer** demonstrates how single-cell gene-regulatory-network analysis can be transformed into an interpretable interactive tool for investigating regulatory heterogeneity in cancer cells.

The application is intended for research use and is **not a clinical or diagnostic tool**.
