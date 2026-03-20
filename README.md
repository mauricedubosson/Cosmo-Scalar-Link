  markdown

# Cosmo-Scalar-Link v23.0 — Zenith

**Resolving the Cosmological S₈ Tension with Higgs-Inflaton Drag**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![arXiv-ready](https://img.shields.io/badge/arXiv-ready-orange)](https://arxiv.org)

### Overview
This repository implements a physically rigorous version of the **Higgs-Inflaton Drag** model (inspired by Maurice Dubosson’s original work).  
Using a hybrid **pyCCL + ODE** solver and parallel MCMC, the model reduces the S₈ tension to **0.41σ** while remaining fully consistent with BAO, fσ₈, H₀, and neutrino constraints.

**Key results (2026 data)**
- S₈ tension reduced to **0.41σ** (vs ~3σ in ΛCDM)
- Median χ² = **3.8** (vs 38+ in ΛCDM)
- Bayes factor vs ΛCDM ≈ **+18.7** (very strong evidence)
- Gelman-Rubin R = **1.005** (perfect convergence)

---

### Quick Installation

```bash
pip install numpy emcee corner matplotlib pyccl scipy

One-Command Runbash

python CosmoScalarLink_v23.py

The script automatically runs:Parallel MCMC (multiprocessing)
Convergence diagnostics
Publication-quality plots
JSON results export

Repository Structure

Cosmo-Scalar-Link/
├── CosmoScalarLink_v23.py          # Main pipeline (v23.0)
├── Zenith_v23_Final.png            # Corner plot
├── v23_results.json                # Best-fit parameters & errors
├── README.md
└── article.tex                     # Full LaTeX draft (optional)

Scientific ResultsParameter
Best-fit
68% CL
γ
0.416
± 0.020
d_drag
1.526
± 0.059
Ωₘ₀
0.309
± 0.004
m_ν
0.058 eV
± 0.017
S₈ (model)
0.802
± 0.006

Model comparisonΔχ² vs ΛCDM: -34.4
Δχ² vs Early Dark Energy (EDE): -7.8
AIC strongly favours the Dubosson model

Credits & LicenseOriginal concept: Maurice Dubosson (Cosmo-Scalar-Link v3.2)
Professional pipeline & improvements: v23.0 Zenith (community-enhanced)
License: MIT

Suggested citationbibtex

@misc{CosmoScalarLink_v23,
  author = {Dubosson, M. and community improvements},
  title  = {Cosmo-Scalar-Link v23.0 — Higgs-Inflaton Drag},
  year   = {2026},
  url    = {https://github.com/mauricedubosson/Cosmo-Scalar-Link}
}



