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

1. **Did you use AI tools? If yes, where?**
   Yes. Claude (Anthropic) was used at two stages: (a) understanding the problem structure
   and breaking it into analytical sub-tasks, and (b) drafting initial versions of the
   markdown reports. All code was written and verified independently.

2. **What prompts or tasks did AI help with?**
   -Understanding the aviation domain context (FTO operations, sortie terminology,
     DGCA compliance requirements) before writing any analysis
   - Structuring the workflow across 9 tasks from the assessment brief
   - Getting an initial skeleton for the executive_insights.md and methodology.md
   - Reviewing whether my risk score formula made logical sense before finalizing it


3. **Which parts did you personally verify?**
   - All 17 data quality findings were verified by running the checks manually in the notebook
   - Every formula (utilization rate, study readiness, payment risk, composite risk score)
     was traced through the code and validated against 3–5 specific cadet examples by hand
   - All 7 charts were reviewed for axis labels, color coding, and data accuracy before export

4. **Which AI suggestion did you reject or modify?**
   - The initial aircraft utilization chart included all 120 aircraft in one unreadable bar —
     I changed this to show summary statistics with a top/bottom breakdown
   - The risk formula initially used sklearn MinMaxScaler; I replaced this with explicit
     clip-based normalization to avoid any ML dependency, per the assessment rules

5. **Which part of the analysis are you least confident about?**
   The flying-rate-based completion date projection assumes a constant pace for each cadet.
   A cadet enrolled in January with 80 hours flown has a very different pace profile from
   one enrolled last month with 5 hours. A confidence interval would improve this estimate
   but would require more historical granularity than this dataset provides.

6. **Pick one formula and explain it in your own words:**
   The study_readiness score weights quiz performance at 40%, chapter completion at 30%,
   and practice test frequency at 30%. Quiz performance gets the highest weight because
   it is the only measure that tests actual retention — a cadet can complete chapters
   passively without learning. Practice tests get equal weight to chapter progress because
   active retrieval predicts real exam performance better than passive reading does.
   The practice test component caps at 10 tests (full score) because beyond that point,
   marginal returns diminish — a cadet who has done 10 tests per subject is exam-ready
   regardless of absolute count.

