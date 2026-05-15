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

1. **Did you use AI tools?** Yes,Claude was used to understand the problemstatement and refactor into multiple smaller problems, while Antigravity was used for code generation and structure.

2. **What prompts or tasks did AI help with?** 

## 1. WHO YOU ARE AND WHAT THIS IS

You are a Data Scientist completing a technical internship assessment for **AIRMAN Aeronautics Pvt. Ltd.**, an Indian aviation tech company. They build two products:

- **Skynet** — SaaS platform for Flight Training Organisations (FTOs) to manage operations, scheduling, aircraft, instructors
- **TOGA** — Mobile app for pilot cadets to study, track logbook hours, and plan pre-flight

The assessment asks you to analyse simulated FTO data and produce **business intelligence** for four stakeholders: FTO operations team, Chief Flying Instructor, Finance team, and the TOGA product team.

**This is not a generic data science task. Think aviation domain throughout.**

---

## 2. DATASETS — WHAT EXISTS AND WHAT IS IN THEM

All 6 CSV files are already created, cleaned, and placed in the project `data/` folder. Do NOT recreate them. Load them exactly as-is.

### `data/sorties.csv` — 300 rows
Flight sessions (called "sorties" in aviation). Each row is one scheduled flight.

| Column | Description |
|---|---|
| sortie_id | S0001–S0300 |
| cadet_id | Which cadet flew |
| instructor_id | Which instructor supervised |
| aircraft_id | Which aircraft was used |
| base_id | Which base (B01–B04) the sortie operated from |
| scheduled_start / scheduled_end | Planned datetime |
| actual_start / actual_end | Actual datetime (empty if cancelled) |
| status | `completed` or `cancelled` |
| delay_minutes | Minutes late from scheduled start (0 if on time or cancelled) |
| cancel_reason | Filled only if cancelled: Weather / Aircraft Defect / Instructor Unavailable / ATC Restriction / Fuel Delay |
| lesson_type | Circuit / Navigation / Solo / General Handling / Instrument Flying / Night Flying / Cross Country |

**Date range:** May 1, 2026 → June 30, 2026  
**Completed:** 253 sorties | **Cancelled:** 47 sorties | **Delayed (>0 min):** 222 sorties

---

### `data/aircraft.csv` — 120 rows
Fleet of aircraft across 4 bases.

| Column | Description |
|---|---|
| aircraft_id | A001–A120 |
| registration | Indian VT-XXXXX format |
| type | C152 / C172 / PA28 / DA40 / DA42 / SR20 |
| base_id | Home base B01–B04 |
| total_available_hours | Monthly available flight hours |
| maintenance_downtime_hours | Hours lost to maintenance |
| defect_count | Number of reported defects |

**Known planted issues:**
- A003, A009, A016: `maintenance_downtime_hours > total_available_hours` (impossible — flag this)
- Several aircraft have defect_count ≥ 12 (flag for operational review)

---

### `data/cadets.csv` — 150 rows
Student pilots enrolled at the FTO.

| Column | Description |
|---|---|
| cadet_id | C001–C150 |
| name | Full name |
| course | PPL (45 required hours) or CPL (200 required hours) |
| home_base | B01–B04 |
| total_required_hours | 45 for PPL, 200 for CPL |
| total_flown_hours | Hours flown so far |
| enrollment_date | When they joined |

**Known planted issues:**
- "Sanya Gupta", "Vikram Malhotra", "Rahul Patel" — each name appears twice with different cadet_ids (data entry duplicate risk)

---

### `data/instructors.csv` — 100 rows
Flying instructors across 4 bases.

| Column | Description |
|---|---|
| instructor_id | I001–I100 |
| name | Capt [Surname] [Number] |
| base_id | Home base B01–B04 |
| aircraft_qualified | Single aircraft type they are certified to instruct on |
| total_duty_hours | Total hours on duty this period |
| total_flight_hours | Hours actually flying/instructing |

---

### `data/payments.csv` — 150 rows
Fee collection status per cadet.

| Column | Description |
|---|---|
| cadet_id | Links to cadets.csv |
| invoiced_amount | Total fees charged (₹) |
| paid_amount | Amount received so far (₹) |
| outstanding_amount | Should equal invoiced − paid |
| last_payment_date | Date of most recent payment |

**Known planted issues:**
- C006, C023, C068, C102: `outstanding_amount ≠ invoiced_amount − paid_amount` (deliberate calculation errors to catch)

---

### `data/toga_study.csv` — 450 rows
Study activity per cadet per subject (3 subjects per cadet).

| Column | Description |
|---|---|
| cadet_id | Links to cadets.csv |
| subject | Technical General / Radio Telephony / Flight Planning / Meteorology / Navigation / Human Performance / Air Regulations |
| chapters_completed | Chapters finished |
| total_chapters | Total chapters in that subject |
| avg_quiz_score | 0–100 quiz average |
| last_active_date | Last time they studied on TOGA |
| practice_tests_attempted | Number of mock tests taken |

**Known planted issues:**
- C005 / Radio Telephony: chapters_completed (27) > total_chapters (24)
- C030 / Radio Telephony: chapters_completed (37) > total_chapters (36)

---

### Additional known data quality issues across sorties:
- **20 sorties** where instructor's `base_id` (instructors.csv) ≠ sortie's `base_id` — operational anomaly
- **4 sorties** where instructor's `aircraft_qualified` type ≠ the aircraft `type` used in that sortie:
  - S0044, S0107, S0184, S0263

---

## 3. REQUIRED FOLDER STRUCTURE

Create this exact structure. Every file path below must exist after your work:

```
airman-data-science-assessment/
├── data/
│   ├── sorties.csv
│   ├── aircraft.csv
│   ├── cadets.csv
│   ├── instructors.csv
│   ├── toga_study.csv
│   ├── payments.csv
│   ├── cleaned_outputs.csv        ← you create this
│   └── risk_scores.csv            ← you create this
├── notebooks/
│   └── analysis.ipynb             ← you create this
├── reports/
│   ├── data_quality_report.md     ← you create this
│   ├── skynet_operations_analysis.md
│   ├── training_progress_analysis.md
│   ├── toga_study_intelligence.md
│   ├── finance_risk_analysis.md
│   ├── executive_insights.md
│   └── methodology.md
├── charts/
│   ├── aircraft_utilization.png
│   ├── cancellation_reasons.png
│   ├── cadet_progress.png
│   ├── study_readiness.png
│   ├── payment_risk.png
│   ├── cadet_risk_scores.png
│   └── flight_vs_study_progress.png
└── README.md
```

---

## 4. WHAT TO BUILD — STEP BY STEP

Complete every step in order. Each step corresponds to one task in the assessment.

---

### STEP 1 — Data Cleaning & Validation (`reports/data_quality_report.md` + `data/cleaned_outputs.csv`)

Load all 6 CSVs. Run validation checks and document every issue found. You already know the planted issues — catch them AND look for any additional patterns.

**Checks to run:**
```python
# 1. Missing values in each dataframe
# 2. Duplicate IDs per file
# 3. Duplicate cadet names (different IDs)
# 4. Invalid status values in sorties (only 'completed'/'cancelled' allowed)
# 5. Completed sortie with no actual_start or actual_end
# 6. Cancelled sortie that has actual_start/end filled in
# 7. delay_minutes mismatch: check if (actual_start - scheduled_start).minutes == delay_minutes
# 8. outstanding_amount != invoiced_amount - paid_amount  [expect 4 errors: C006,C023,C068,C102]
# 9. chapters_completed > total_chapters in toga_study    [expect 2 rows: C005,C030]
# 10. maintenance_downtime_hours > total_available_hours in aircraft [expect 3: A003,A009,A016]
# 11. total_flown_hours > total_required_hours (cadet done but still enrolled?)
# 12. avg_quiz_score outside 0-100 range
# 13. Instructor base != sortie base (expect ~20 sorties)
# 14. Instructor aircraft_qualified != aircraft type in sortie (expect 4 sorties)
# 15. Negative values anywhere numeric
```

**Output:** `data_quality_report.md` — structured markdown with a table for each issue category: issue name, severity (High/Medium/Low), count, affected IDs, recommended action.

**Also save:** `data/cleaned_outputs.csv` — a merged, cleaned master dataframe (sorties joined with cadet, instructor, aircraft info) with a `data_issues` flag column noting which rows had problems.

---

### STEP 2 — Skynet Operations Analytics (`reports/skynet_operations_analysis.md`)

**Aircraft Utilization:**
```python
utilization_rate = actual_flown_hours / total_available_hours
# actual_flown_hours per aircraft = sum of (actual_end - actual_start) for completed sorties
# Flag aircraft below 40% utilization as underutilized
# Flag aircraft with defect_count >= 10 for operational review
# Flag aircraft where maintenance_downtime > 50% of total_available_hours
```

**Instructor Utilization:**
```python
flight_ratio = total_flight_hours / total_duty_hours
# Flag instructors where ratio > 0.85 as potentially overloaded
# Flag instructors where ratio < 0.40 as underutilized
# Note: instructors.csv doesn't have per-sortie data so use aggregate columns
```

**Dispatch Reliability:**
```python
completion_rate = completed_sorties / total_sorties
cancellation_rate = cancelled_sorties / total_sorties
avg_delay = mean(delay_minutes) for completed sorties
# Break down cancellation reasons by count and %
# Break down delays by: base, lesson_type, day of week
# Identify which lesson types have highest cancellation rates
```

Write the report in aviation-appropriate language. Mention Skynet as the platform that should surface these metrics on its operations dashboard.

---

### STEP 3 — Training Progress Analytics (`reports/training_progress_analysis.md`)

```python
# Per cadet:
progress_pct = (total_flown_hours / total_required_hours) * 100
remaining_hours = total_required_hours - total_flown_hours

# Flying rate = total_flown_hours / days_since_enrollment
# Estimated completion days = remaining_hours / flying_rate
# Estimated completion date = today + timedelta(days=estimated_completion_days)

# At-risk flag: cadets whose estimated completion date is far beyond a reasonable target
# For PPL: 45 hours, target within 6 months of enrollment
# For CPL: 200 hours, target within 18 months of enrollment
```

Also cross-reference:
- Which cadets have high flight progress but low TOGA study scores (flying without studying — risk)
- Which cadets have high study scores but low flight progress (studying but not flying — possible scheduling issue)
- Which lesson types are cancelled most (blocks specific training milestones)

End with a table: cadet_id, course, progress_pct, flying_rate (hrs/day), estimated_completion_date, risk_flag, risk_reason.

---

### STEP 4 — TOGA Study Intelligence (`reports/toga_study_intelligence.md`)

```python
# Per cadet per subject:
subject_progress = chapters_completed / total_chapters

# Study readiness score (0-100) per cadet — simple weighted average:
study_readiness = (
    0.40 * mean(avg_quiz_score across subjects) +
    0.30 * mean(subject_progress * 100 across subjects) +
    0.30 * min(practice_tests_attempted / 10, 1) * 100  # cap at 10 tests = full score
)

# Inactivity flag: last_active_date older than 7 days from reference date (2026-05-15)
# Weak subject: avg_quiz_score < 50 for that subject
```

For each cadet generate a TOGA profile card:
```
Cadet: [name] ([cadet_id])
Study Readiness Score: [X]/100
Weak Subjects: [list]
Inactive Since: [date or 'Active']
Practice Test Readiness: [Low/Medium/High]
Recommended Action: [specific text]
Instructor Intervention Required: [Yes/No + reason]
```

The "recommended action" should be specific — not "study more" but "Focus on Meteorology chapters 8–21, attempt 3 practice tests before next flight."

---

### STEP 5 — Finance & Operational Risk (`reports/finance_risk_analysis.md`)

```python
# Per cadet:
payment_completion_pct = paid_amount / invoiced_amount * 100
outstanding_ratio = outstanding_amount / invoiced_amount

# Days since last payment (from 2026-05-15):
days_since_payment = (today - last_payment_date).days

# Payment risk score (0-100):
payment_risk = (
    0.50 * outstanding_ratio * 100 +
    0.30 * min(days_since_payment / 60, 1) * 100 +  # 60 days = max risk
    0.20 * (1 - payment_completion_pct / 100) * 100
)

# Risk level: 0-39=Low, 40-69=Medium, 70-100=High
```

Output table:
| cadet_id | name | outstanding (₹) | payment_completion% | days_since_payment | payment_risk_score | risk_level | reason |

Also note the 4 cadets with calculation errors — flag separately as "data integrity issue, manual review required."

Total outstanding across all cadets should also be computed as a revenue metric.

---

### STEP 6 — Explainable Cadet Risk Score (`data/risk_scores.csv` + part of `reports/methodology.md`)

Build a **weighted formula risk score** — no ML models. Simple, transparent, explainable.

```python
# Normalize each feature to 0-1 range first, then apply weights:

risk_score = (
    0.25 * (1 - flight_progress)        # low flight progress = higher risk
  + 0.20 * (1 - study_readiness/100)    # low study readiness = higher risk
  + 0.15 * (1 - avg_quiz_score/100)     # low quiz score = higher risk
  + 0.15 * payment_risk / 100           # high payment risk = higher risk
  + 0.15 * inactivity_score             # inactive on TOGA = higher risk
  + 0.10 * cancellation_rate_for_cadet  # frequent cancellations = higher risk
) * 100

# inactivity_score: days_since_last_active / 30, capped at 1.0
# cancellation_rate_for_cadet: cancelled_sorties / total_sorties for that cadet
```

Risk levels:
- 0–39: Low
- 40–69: Medium
- 70–100: High

Save `data/risk_scores.csv` with columns:
`cadet_id, name, course, risk_score, risk_level, flight_progress, study_readiness, avg_quiz_score, payment_risk, days_inactive, cancellation_rate, main_risk_reason`

The `main_risk_reason` column should be a short human-readable string like:
- "Low flight progress + high outstanding payment"
- "Inactive on TOGA for 18 days + low quiz scores"
- "Frequent sortie cancellations + payment risk"

---

### STEP 7 — Charts (`charts/` — 7 PNG files)

Use **matplotlib + seaborn**. Use a consistent color palette. Save each as 300 DPI PNG.

```python
# Style setup at top of notebook:
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
PALETTE = ['#1A3557','#2E86AB','#A23B72','#F18F01','#C73E1D','#44BBA4','#E94F37']
```

**Chart 1 — `aircraft_utilization.png`**
Horizontal bar chart. X-axis: utilization % (actual_flown / total_available). Color bars red if <40%, amber if 40–70%, green if >70%. Add a vertical dashed line at 40% and 70%.

**Chart 2 — `cancellation_reasons.png`**
Pie chart + bar chart side by side. Show count and % for each cancel reason: Weather, Aircraft Defect, Instructor Unavailable, ATC Restriction, Fuel Delay.

**Chart 3 — `cadet_progress.png`**
Grouped horizontal bar chart. For each cadet show `total_flown_hours` (filled) vs `total_required_hours` (outline). Color by course (PPL=blue, CPL=orange). Sort by progress %.

**Chart 4 — `study_readiness.png`**
Bar chart of study_readiness score per cadet. Color by score: red <40, amber 40–70, green >70. Add horizontal reference lines.

**Chart 5 — `payment_risk.png`**
Bar chart of outstanding_amount per cadet, colored by payment_risk_level (Low=green, Medium=amber, High=red). Sort by outstanding descending.

**Chart 6 — `cadet_risk_scores.png`**
Horizontal bar chart of final risk_score per cadet. Color by risk_level. Annotate each bar with the risk_level label. Sort descending.

**Chart 7 — `flight_vs_study_progress.png`**
Scatter plot. X = flight_progress (%), Y = study_readiness score. Color points by risk_level. Size points by outstanding_amount. Add quadrant labels:
- Top-right: "On Track"
- Top-left: "Studying but not flying"
- Bottom-right: "Flying but not studying"
- Bottom-left: "High Risk"

---

### STEP 8 — Executive Insight Report (`reports/executive_insights.md`)

Write a concise leadership report. No bullet dumps — each insight must have a number, a finding, and a specific action.

Structure:

```markdown
# Executive Insight Report — AIRMAN FTO Intelligence
*Prepared by: [Your Name] | Data Period: May–June 2026*

## 1. Top 5 Operational Insights (Skynet)
[Each: Finding → Business Impact → Recommended Action]

## 2. Top 5 Training Progress Insights
[Each: Cadet or pattern → Risk → Action]

## 3. Top 3 TOGA Personalisation Opportunities
[Each: Behaviour observed in data → Feature TOGA should build]

## 4. Top 3 Finance Risks
[Each: Cadet/amount → Risk to training continuity → Suggested action]

## 5. Product Recommendations for Skynet
[5 specific dashboard features or alerts Skynet should show the FTO ops team]

## 6. Product Recommendations for TOGA
[5 specific features TOGA should add for cadets based on this data]

## 7. Data Quality Issues Found
[Summary table]

## 8. Suggested Additional Data Fields AIRMAN Should Collect
[At least 5 new fields with justification]

## 9. Final Recommendation to AIRMAN Leadership
[2–3 paragraph strategic summary]
```

---

### STEP 9 — Methodology Document (`reports/methodology.md`)

Answer all 10 questions from the assessment clearly. Then add the risk score formula derivation.

**Questions to answer:**
1. Why did you choose your risk score formula?
2. Which features had the most impact and why?
3. What assumptions did you make?
4. What data quality issue could mislead the model?
5. What would you not automate or predict yet?
6. How would you validate this model with real FTO data?
7. How would you prevent unfair ranking of cadets?
8. How should AIRMAN display this insight without demotivating students?
9. What additional data would improve your model?
10. How would this analysis help Skynet and TOGA become more intelligent products?

---

### STEP 10 — Jupyter Notebook (`notebooks/analysis.ipynb`)

All computation must live here. Structure it with clear markdown cells as section headers:

```
[0]  Setup & Imports
[1]  Load Data
[2]  Task 1: Data Cleaning & Validation
[3]  Task 2: Skynet Operations Analytics
[4]  Task 3: Training Progress Analytics
[5]  Task 4: TOGA Study Intelligence
[6]  Task 5: Finance & Operational Risk
[7]  Task 6: Cadet Risk Score
[8]  Task 7: Visualizations
[9]  Export Outputs
```

Every section should end with a `print()` summary of its key findings so the notebook is self-documenting when run top-to-bottom.

---

### STEP 11 — README.md

Include all required sections:

```markdown
# AIRMAN Data Science Assessment — [Your Name]

## Project Overview
## Tools & Libraries Used
## Setup Instructions
## How to Run the Notebook
## Data Assumptions
## Metrics Calculated
## Risk Score Explanation
## Key Outputs
## Known Limitations
## What I Would Improve With More Time
## AI Usage Disclosure
  1. Did you use AI tools? If yes, where?
  2. What prompts or tasks did AI help with?
  3. Which parts did you personally verify?
  4. Which AI suggestion did you reject or modify?
  5. Which part of the analysis are you least confident about?
  6. Pick one formula or chart and explain it in your own words.
```

---

## 5. LIBRARIES TO USE

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# All analysis in pandas/numpy — NO sklearn, NO ML models
# Charts: matplotlib + seaborn only
# Reports: write as .md files using Python file I/O
```

---

## 6. IMPORTANT RULES — DO NOT VIOLATE

1. **No ML models.** The risk score must be a transparent weighted formula. No RandomForest, no logistic regression, no clustering. The assessment penalises unnecessary ML.
2. **Every number must connect to a business decision.** "Aircraft A009 has 220 hours of downtime against 197 available hours" is more useful than "downtime is high."
3. **Write reports in aviation language.** Use terms like "sortie," "FTO," "dispatch reliability," "ground school," "airside operations" where appropriate.
4. **Charts must be readable.** Labels on axes, titles, legends, color coding with a legend. Every chart saved at 300 DPI.
5. **The notebook must run top-to-bottom without errors** on a fresh kernel.
6. **Reference date for "today":** Use `pd.Timestamp('2026-05-15')` consistently everywhere as the analysis date.
7. **Acknowledge the 4 payment errors** in the data quality report AND note they require manual finance team review before any payment risk scoring is applied to those cadets.
8. **Flag but don't delete** bad rows — add an `issue_flag` column instead and keep them in analysis with a note.

---

## 7. DELIVERABLE CHECKLIST

Before submitting, confirm every file exists:

- [ ] `data/cleaned_outputs.csv`
- [ ] `data/risk_scores.csv`
- [ ] `notebooks/analysis.ipynb` (runs clean, top to bottom)
- [ ] `reports/data_quality_report.md`
- [ ] `reports/skynet_operations_analysis.md`
- [ ] `reports/training_progress_analysis.md`
- [ ] `reports/toga_study_intelligence.md`
- [ ] `reports/finance_risk_analysis.md`
- [ ] `reports/executive_insights.md`
- [ ] `reports/methodology.md`
- [ ] `charts/aircraft_utilization.png`
- [ ] `charts/cancellation_reasons.png`
- [ ] `charts/cadet_progress.png`
- [ ] `charts/study_readiness.png`
- [ ] `charts/payment_risk.png`
- [ ] `charts/cadet_risk_scores.png`
- [ ] `charts/flight_vs_study_progress.png`
- [ ] `README.md`

**Total: 18 files across 4 folders.**

---

## 8. TONE & QUALITY BAR

The assessors will reject work that:
- Produces generic insights ("utilization is low") without specifics
- Cannot connect data findings to Skynet/TOGA product features
- Uses complex ML to avoid explaining decisions
- Ignores the data quality issues
- Produces charts without axis labels or context

The assessors will be impressed by work that:
- Names specific cadets, aircraft, instructors in insights
- Suggests what Skynet should show on its ops dashboard
- Suggests what TOGA should push as a notification to a cadet
- Acknowledges model limitations honestly
- Tells a clear operational story from the data

3. **Which parts did you personally verify?** All 17 data quality findings were verified against the raw CSVs. The planted issues (payment errors, qualification mismatches, maintenance anomalies) were confirmed by manual inspection. All formula weights were reviewed against aviation training logic.

4. **Which AI suggestion did you reject or modify?** The initial chart for aircraft utilisation tried to include all 120 aircraft in a single chart — I modified it to exclude the 3 data-error aircraft and sort by utilisation for readability. The original risk formula suggestion used sklearn's MinMaxScaler; I replaced it with explicit clip-based normalisation to avoid any ML dependency.

5. **Which part of the analysis are you least confident about?** The flying rate extrapolation for completion date estimation. A cadet enrolled in February 2026 with 37 hours over 450 days has a very different pace profile than one enrolled in April 2026 with 8 hours over 30 days. A linear rate for both produces wide uncertainty bands I wasn't able to quantify.

6. **Pick one formula and explain it in your own words:** The **study_readiness score** (0-100) combines three signals: quiz performance (40% weight, because it directly measures retention), chapter completion progress (30% weight, because it shows breadth of coverage), and practice test frequency (30% weight, because active retrieval practice predicts real exam performance better than passive reading). The practice test component is capped at 10 tests = full score, because there are diminishing returns beyond that — a cadet who has done 10 tests per subject has demonstrated adequate preparation regardless of their absolute count.
