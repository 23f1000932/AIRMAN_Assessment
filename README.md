# AIRMAN Data Science Assessment — Ayan

## Project Overview
Comprehensive business intelligence analysis of simulated FTO (Flight Training Organisation) data for AIRMAN Aeronautics Pvt. Ltd.
Covers operational analytics for the **Skynet** platform and product intelligence for the **TOGA** mobile app across a 150-cadet, 100-instructor, 120-aircraft FTO operating over May–June 2026.

## Tools & Libraries Used
- **Python 3.x**
- `pandas` — data loading, transformation, merging
- `numpy` — numerical computation
- `matplotlib` + `seaborn` — all 7 charts (300 DPI PNG)
- Standard library only — `os`, `warnings`, `datetime`
- **No ML models** — all scoring uses transparent weighted formulas

## Setup Instructions
```bash
pip install pandas numpy matplotlib seaborn
```

## How to Run

### Option A — Run individual scripts in order:
```bash
python scripts/step1_load_clean.py     # Data cleaning + data_quality_report.md
python scripts/step2_operations.py    # Skynet ops analysis
python scripts/step3_training.py      # Training progress
python scripts/step4_toga.py          # TOGA study intelligence
python scripts/step5_finance.py       # Finance risk
python scripts/step6_risk_score.py    # Cadet risk scores
python scripts/step7_charts.py        # All 7 charts
python scripts/step8_reports.py       # Executive insights + methodology
```

### Option B — Run the Jupyter notebook:
```bash
cd notebooks
jupyter notebook analysis.ipynb
```
Run all cells top-to-bottom (Kernel → Restart & Run All).

## Data Assumptions
- Reference date: `2026-05-15` (used as "today" for all time calculations)
- Flying rate extrapolated linearly from enrollment date to reference date
- 4 cadets with payment calculation errors (C006, C023, C068, C102) excluded from payment risk scoring with neutral score (50) pending manual reconciliation
- TOGA impossible progress (C005, C030) capped at total_chapters before scoring
- 3 aircraft with maintenance > available hours (A003, A009, A016) excluded from utilisation chart with data error flag

## Metrics Calculated
| Metric | Formula |
|--------|---------|
| Aircraft Utilisation | actual_flown_hours / total_available_hours × 100 |
| Instructor Flight Ratio | total_flight_hours / total_duty_hours |
| Cadet Flight Progress | total_flown_hours / total_required_hours × 100 |
| Flying Rate | total_flown_hours / days_since_enrollment |
| Study Readiness | 0.4×avg_quiz + 0.3×chapter_progress×100 + 0.3×min(tests/10,1)×100 |
| Payment Risk | 0.5×outstanding_ratio×100 + 0.3×min(days/60,1)×100 + 0.2×(1-completion%)×100 |

## Risk Score Explanation
The composite cadet risk score is a transparent weighted formula across 6 dimensions:
```
risk_score = (
    0.25 × low_flight_progress +
    0.20 × low_study_readiness +
    0.15 × low_quiz_scores +
    0.15 × payment_risk +
    0.15 × toga_inactivity +
    0.10 × cancellation_rate
) × 100
```
Scores: 0–39 = Low | 40–69 = Medium | 70–100 = High
No machine learning is used. Every score component is directly readable from the output CSV.

## Key Outputs
| File | Description |
|------|-------------|
| `data/cleaned_outputs.csv` | Master merged dataset with issue flags |
| `data/risk_scores.csv` | Composite risk score per cadet |
| `reports/data_quality_report.md` | 17 issues across 15 check types |
| `reports/skynet_operations_analysis.md` | Fleet & dispatch analytics |
| `reports/training_progress_analysis.md` | Per-cadet progress & forecasts |
| `reports/toga_study_intelligence.md` | Study readiness profiles |
| `reports/finance_risk_analysis.md` | Payment risk analysis |
| `reports/executive_insights.md` | Leadership summary |
| `reports/methodology.md` | 10-question methodology Q&A |
| `charts/*.png` | 7 visualisations at 300 DPI |

## Known Limitations
1. Flying rate projection assumes constant pace — no seasonal or scheduling-pattern adjustments
2. Payment risk excludes 4 cadets with data errors — their true risk is unquantified
3. Aircraft utilisation cannot be computed for A003, A009, A016 due to data integrity errors
4. TOGA data has only 3 subjects per cadet (not all 7 subjects) — readiness scores are partial
5. Instructor performance quality cannot be assessed from quantity metrics alone

## What I Would Improve With More Time
- Integrate real METAR weather data with sortie records for weather risk modelling
- Build a cadet-level cohort analysis (PPL vs CPL separately, per base)
- Add time-series trending (weekly utilisation, study activity patterns by day of week)
- Validate risk score weights against historical outcomes data
- Build an interactive HTML dashboard (Plotly/Dash) instead of static PNGs

## AI Usage Disclosure

1. **Did you use AI tools?** Yes — Antigravity (Claude-based coding assistant) was used for code generation and structure.

2. **What prompts or tasks did AI help with?** Writing Python scripts for data validation, generating report templates, structuring the risk formula implementation, and creating the 7 matplotlib charts.

3. **Which parts did you personally verify?** All 17 data quality findings were verified against the raw CSVs. The planted issues (payment errors, qualification mismatches, maintenance anomalies) were confirmed by manual inspection. All formula weights were reviewed against aviation training logic.

4. **Which AI suggestion did you reject or modify?** The initial chart for aircraft utilisation tried to include all 120 aircraft in a single chart — I modified it to exclude the 3 data-error aircraft and sort by utilisation for readability. The original risk formula suggestion used sklearn's MinMaxScaler; I replaced it with explicit clip-based normalisation to avoid any ML dependency.

5. **Which part of the analysis are you least confident about?** The flying rate extrapolation for completion date estimation. A cadet enrolled in February 2026 with 37 hours over 450 days has a very different pace profile than one enrolled in April 2026 with 8 hours over 30 days. A linear rate for both produces wide uncertainty bands I wasn't able to quantify.

6. **Pick one formula and explain it in your own words:** The **study_readiness score** (0-100) combines three signals: quiz performance (40% weight, because it directly measures retention), chapter completion progress (30% weight, because it shows breadth of coverage), and practice test frequency (30% weight, because active retrieval practice predicts real exam performance better than passive reading). The practice test component is capped at 10 tests = full score, because there are diminishing returns beyond that — a cadet who has done 10 tests per subject has demonstrated adequate preparation regardless of their absolute count.
