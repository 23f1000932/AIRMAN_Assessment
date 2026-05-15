"""
STEPS 8, 9, 11 — Executive Insights, Methodology, README
"""
import os

BASE    = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
REPORTS = os.path.join(BASE, "reports")

# ── EXECUTIVE INSIGHTS ────────────────────────────────────────────────────────
exec_report = """# Executive Insight Report — AIRMAN FTO Intelligence
*Prepared by: Ayan | Data Period: May–June 2026 | Reference Date: 2026-05-15*

---

## 1. Top 5 Operational Insights (Skynet)

**1.1 — 100% of Fleet is Under-Utilised**
*Finding:* Every aircraft in the active fleet (excluding 3 data-error aircraft) has a utilisation rate below 40%, with the median below 15%. Total available fleet hours are severely under-deployed.
*Business Impact:* AIRMAN is absorbing fixed maintenance and depreciation costs on idle assets. At current utilisation, the FTO cannot support its cadet cohort growth.
*Recommended Action:* Skynet's ops dashboard should surface a "Fleet Efficiency" widget comparing daily scheduled vs actual flown hours per base. Target: raise average utilisation to 55% within 90 days by consolidating base scheduling.

**1.2 — Instructor Unavailability is the #1 Cancellation Cause**
*Finding:* 11 of 47 cancelled sorties (23.4%) cite "Instructor Unavailable." ATC Restriction follows at 10 sorties (21.3%).
*Business Impact:* Each cancelled sortie delays cadet completion timelines and erodes trust in the FTO's scheduling reliability.
*Recommended Action:* Skynet should implement a standby instructor pool — when an instructor marks unavailable, the system auto-proposes an available qualified substitute within the base.

**1.3 — 20 Cross-Base Instructor Deployments Not Tracked**
*Finding:* 20 sorties have an instructor operating from a different base than their home base. This is not flagged anywhere in the current data.
*Business Impact:* Untracked deployments create duty-hour blind spots, insurance liability gaps, and DGCA compliance risks.
*Recommended Action:* Add a `deployment_type` field to Skynet sorties: `home_base | temporary_deployment`. Alert the CFI when any instructor is deployed cross-base.

**1.4 — 4 Safety-Critical Qualification Mismatches (S0044, S0107, S0184, S0263)**
*Finding:* Four completed sorties show the instructor's type qualification did not match the aircraft flown. Example: S0044 — Capt (DA40-qualified) flew C152.
*Business Impact:* DGCA mandates instructor type certification. These sorties may be non-compliant with CAR regulations, potentially invalidating logged hours.
*Recommended Action:* Skynet must implement a **hard block** — the system should refuse to confirm any booking where `instructor.aircraft_qualified ≠ assigned_aircraft.type`. These 4 sorties require immediate DGCA notification.

**1.5 — Night Flying and Cross Country Carry the Highest Average Delays**
*Finding:* Night Flying and Cross Country sorties show the highest average delay minutes. These are milestone sorties for CPL cadets.
*Business Impact:* Cascading delays in milestone sorties push CPL completion timelines, affecting revenue and cadet morale.
*Recommended Action:* Skynet should add a 15-minute buffer to Night Flying and Cross Country lesson type templates, and pre-schedule pre-flight briefing slots separately.

---

## 2. Top 5 Training Progress Insights

**2.1 — 99 Cadets (66%) Are At Risk of Missing Their Training Deadline**
At current flying rates, 99 cadets will overshoot their PPL/CPL target completion dates. Many CPL cadets enrolled in 2025 are less than 50% complete with 200-hour programmes.

**2.2 — 50 Cadets Are Studying But Not Flying (Scheduling Bottleneck Signal)**
50 cadets have TOGA quiz scores ≥60 but flight progress <50%. This pattern suggests these cadets are motivated and prepared but cannot get sorties. Root cause: aircraft/instructor availability constraints at their home base.

**2.3 — 4 Cadets Flying Without Adequate Ground Study**
4 cadets have >50% flight progress but quiz scores below 50. These cadets risk failing the DGCA written examination despite accumulating airtime. CFI must mandate TOGA completion before their next advanced sortie.

**2.4 — Cadet C104 (Anjali Kale) — Highest Overall Risk**
C104 has very low flight progress, has been inactive on TOGA for multiple days, and carries high outstanding fees. Without immediate intervention across all three dimensions, this cadet's training programme is at serious risk.

**2.5 — CPL Cohort Average Progress: ~67%**
CPL cadets are collectively well advanced but the variation is extreme — some cadets (C071, C130, C135) are near completion while others (C067, C019) are below 15% with slow flying rates.

---

## 3. Top 3 TOGA Personalisation Opportunities

**3.1 — Adaptive Weak Subject Detection → Push Personalised Study Plans**
*Observation:* The data shows clear individual weak subjects per cadet (avg quiz <50). TOGA currently serves the same content to all cadets.
*Feature to build:* When a cadet opens TOGA, their personalised "Focus Zone" should immediately highlight their weakest subject with a targeted 10-question drill — before they can browse other content.

**3.2 — Pre-Sortie Readiness Gate Linked to Skynet**
*Observation:* 4 cadets are flying advanced sorties with sub-50 ground school scores.
*Feature to build:* TOGA should expose an API endpoint for Skynet. When a Navigation or Solo sortie is being booked, Skynet queries TOGA for the cadet's study_readiness_score. If below 40, Skynet flags the booking with a CFI approval requirement.

**3.3 — Inactivity Re-engagement Notifications**
*Observation:* 66 cadets have been inactive on TOGA for >7 days. Their inactivity correlates with higher overall risk scores.
*Feature to build:* TOGA sends a push notification at Day 5 of inactivity: "Your next sortie is in [X] days — your Meteorology chapter 8 is waiting. 15 minutes now = better airmanship."

---

## 4. Top 3 Finance Risks

**4.1 — ₹2,37,86,960 Total Outstanding Across All Cadets**
With a collection rate of only 62.4%, AIRMAN has significant revenue exposure. 13 cadets are High Risk and 63 are Medium Risk.

**4.2 — 4 Records with Data Integrity Errors (C006, C023, C068, C102)**
Outstanding amounts don't match invoiced − paid. Until corrected, these cadets cannot be accurately risk-scored. Finance team must manually reconcile and correct in Skynet.

**4.3 — Cadet C001 (Sanya Verma) — ₹4,15,025 Outstanding**
C001 has the second-highest raw outstanding balance and is 37 days since last payment. At 150.3/200 hours complete (75% progress), discontinuing training now would waste significant investment by both the cadet and the FTO.

---

## 5. Product Recommendations for Skynet

1. **Fleet Efficiency Dashboard:** Real-time tile showing utilisation % per base with red/amber/green colour coding. Drill down to aircraft level.
2. **Instructor Availability Heatmap:** Weekly view of instructor availability by base and qualification type — enables proactive scheduling before slots are blocked.
3. **Compliance Alert Engine:** Hard blocks for (a) qualification mismatches, (b) instructor base cross-deployment without approval, (c) aircraft in maintenance logging new sorties.
4. **Cadet Risk Widget on Ops View:** Show each cadet's composite risk score (traffic-light coloured) alongside their next scheduled sortie — so ops staff can flag concerns before the cadet shows up.
5. **Automated Payment Verification:** Outstanding amount field should be computed automatically as `invoiced − paid` and trigger a finance alert if any manual override differs by >₹1,000.

---

## 6. Product Recommendations for TOGA

1. **Study Readiness Score on Home Screen:** Show cadets their own readiness score and how it compares to the cohort average — motivating without being punitive.
2. **Subject-Level Progress Rings:** Visual circular progress rings per subject — tapping one shows which chapters remain and their estimated study time.
3. **Practice Test Streaks and Badges:** Gamify practice tests with streaks. Cadets with <3 tests per subject get a "Ground School Gap" badge that disappears once they complete 5 tests.
4. **Pre-Sortie Brief Mode:** 10-minute focused review of topics relevant to the day's lesson type (e.g., before a Navigation sortie, surface Navigation + Meteorology content).
5. **CFI View in TOGA:** A read-only CFI dashboard showing each cadet's readiness score, weak subjects, and inactivity days — so instructors arrive at briefings with data, not guesswork.

---

## 7. Data Quality Issues Found

| Issue | Severity | Count | Action |
|-------|----------|-------|--------|
| Payment calculation errors | High | 4 cadets | Manual finance review |
| Instructor qualification mismatches | High | 4 sorties | DGCA notification + Skynet hard block |
| Aircraft maintenance data errors | High | 3 aircraft | Engineering verification |
| TOGA impossible progress | High | 2 records | Content team review |
| Duplicate cadet names | High | 3 name groups | Manual identity verification |
| Instructor base mismatches | Medium | 20 sorties | Add deployment tracking |
| High defect aircraft | High | 35 aircraft | Enhanced inspection |
| Cross-base operations | Medium | 20 sorties | Policy clarification |

---

## 8. Suggested Additional Data Fields AIRMAN Should Collect

1. **`sortie.weather_conditions`** — Capture METAR/TAF data at sortie time. Would enable weather-specific dispatch reliability analysis and predictive cancellation modelling.
2. **`cadet.medical_expiry_date`** — Class 1/Class 2 medical certificate expiry. A lapsed medical halts training; Skynet should alert 30 days before expiry.
3. **`instructor.fatigue_level_self_reported`** — Simple 1–5 scale at duty start. Would enable proactive fatigue risk management per ICAO HF guidelines.
4. **`sortie.fuel_uplift_litres`** — Actual fuel loaded. Would allow Fuel Delay cancellations to be correlated with fuelling schedules and supplier performance.
5. **`aircraft.last_inspection_date` + `aircraft.next_due_date`** — Maintenance scheduling data. Would allow Skynet to block aircraft before they go AOG rather than after.
6. **`cadet.dgca_exam_date`** — Scheduled DGCA written exam date. Would allow TOGA to prioritise subjects based on time to exam.
7. **`toga.time_spent_minutes`** — Actual time the cadet spent on each chapter, not just completion status. Would distinguish rushed vs genuine learning.

---

## 9. Final Recommendation to AIRMAN Leadership

The data from this two-month analysis reveals an FTO that has strong cadet engagement and a committed instructor corps, but is constrained by three systemic gaps: **operational scheduling inefficiency, incomplete data discipline, and disconnected product intelligence.**

The most urgent action is the four qualification-mismatch sorties (S0044, S0107, S0184, S0263). These are not data curiosities — they are potential DGCA regulatory violations. AIRMAN leadership should engage legal and compliance immediately, notify the regulator proactively, and treat this as the forcing function to invest in Skynet's hard-block enforcement capabilities.

The medium-term opportunity is significant. A 62.4% fee collection rate on ₹2.38 crore outstanding is a cashflow problem that can be solved with basic CRM automation Skynet doesn't yet have. Similarly, 50 cadets who are study-ready but not flying represents wasted capacity — those cadets are prepared and willing, but the scheduling system isn't connecting them to aircraft and instructors efficiently. Fixing this one problem alone could meaningfully improve throughput without adding a single new cadet or aircraft.

TOGA's data confirms that cadet engagement correlates with outcomes — but the product is not yet intelligent enough to close the loop with Skynet. The pre-sortie readiness gate and CFI view are not complex features; they are API integrations that would make every briefing, every sortie booking, and every CFI meeting evidence-based rather than intuition-based. That is the core value proposition of the AIRMAN platform.
"""

# ── METHODOLOGY ───────────────────────────────────────────────────────────────
methodology = """# Methodology Document — AIRMAN Data Science Assessment

*Prepared by: Ayan | Reference Date: 2026-05-15*

---

## Risk Score Formula Derivation

The cadet composite risk score uses a **transparent weighted additive formula**:

```
risk_score = (
    0.25 × (1 − flight_progress)       # low flight progress = higher risk
  + 0.20 × (1 − study_readiness/100)   # low TOGA readiness = higher risk
  + 0.15 × (1 − avg_quiz_score/100)    # low quiz scores = higher risk
  + 0.15 × payment_risk/100            # high payment risk = higher risk
  + 0.15 × inactivity_score            # inactive on TOGA = higher risk
  + 0.10 × cancellation_rate           # frequent cancellations = higher risk
) × 100
```

All inputs are normalised to [0,1] before weighting. The score is then scaled to [0,100] for interpretability.

**Risk Levels:** 0–39 = Low | 40–69 = Medium | 70–100 = High

---

## Q1: Why did you choose this risk score formula?

The formula was designed around **aviation training outcomes** — what actually prevents a cadet from completing their programme safely and on time. Flight progress is the most direct outcome measure (weight 0.25). Study readiness (TOGA) represents theoretical knowledge, which DGCA requires alongside flight hours (weight 0.20). Payment risk affects whether training continues at all (weight 0.15). Quiz scores are partially captured in study readiness but carry independent signal for knowledge gaps (0.15). Inactivity on TOGA is a leading indicator — cadets who disengage before exams tend to underperform (0.15). Cancellation rate captures systemic scheduling barriers or behavioural patterns that slow progress (0.10).

No ML model was used. A transparent, explainable formula allows the CFI to understand exactly why any cadet has a given score and take targeted action.

---

## Q2: Which features had the most impact and why?

**Flight progress (0.25)** had the highest weight because it is the definitive outcome — a cadet who is not flying is not progressing toward their licence regardless of study performance. **Study readiness (0.20)** ranks second because DGCA written exams are mandatory gates; a cadet with 200 flight hours who fails the written exam cannot get a CPL. **Payment risk (0.15)** directly controls whether training continues — an FTO will and should halt sorties for cadets with significant outstanding balances.

---

## Q3: What assumptions did you make?

1. The reference date `2026-05-15` is "today" for all time-based calculations.
2. A cadet's historical flying rate (hours ÷ days enrolled) will continue at the same pace — no acceleration assumed.
3. Instructors' `total_duty_hours` and `total_flight_hours` cover the full May–June period.
4. Missing TOGA data for a cadet implies they are using the platform (no activity flag raised where data was simply absent).
5. The 4 cadets with payment calculation errors were excluded from payment risk scoring and given a neutral payment risk of 50 to avoid artificially inflating their risk scores.
6. Cross-base instructor deployments are operational decisions (not errors) — they were flagged but not excluded.

---

## Q4: What data quality issue could mislead the model?

The **payment calculation errors** for C006, C023, C068, C102 are the most dangerous. If used as-is, the incorrect outstanding amounts would produce wrong payment_risk_scores for these cadets, potentially under- or over-ranking them. We excluded them with a neutral score — but this means their true risk is unknown.

The **instructor qualification mismatches** in 4 sorties could also corrupt aircraft utilisation analysis if those flights were attributed to the wrong aircraft type in type-specific analyses.

---

## Q5: What would you not automate or predict yet?

1. **Solo sortie readiness assessment** — the decision to send a student solo is a CFI judgment that involves real-time aircraft handling assessment, not just data.
2. **Pass/fail prediction for DGCA exams** — we don't have the granular chapter-level topic data or practice test question content.
3. **Instructor performance rating** — the data shows duty hours and flight hours but not qualitative teaching effectiveness.
4. **Weather-based cancellation prediction** — we don't have MET data integrated with sortie scheduling.

---

## Q6: How would you validate this model with real FTO data?

1. **Historical validation:** Apply the formula to 12 months of historical data and check whether high-risk cadets at month 3 actually had worse outcomes (cancellations, dropout, exam failures) by month 12.
2. **CFI calibration:** Present the top 20 risk-ranked cadets to the CFI team and ask them to independently rate each cadet. Measure agreement (Cohen's Kappa) between model ranking and CFI ranking.
3. **Outcome tracking:** As a prospective test, tag cadets as risk levels today and track whether "High" cadets have 2x the dropout/delay rate of "Low" cadets over the next 6 months.
4. **Sensitivity analysis:** Vary the weights ±10% and observe how the top-20 ranking changes — if it's highly sensitive to one weight, that feature needs more careful calibration.

---

## Q7: How would you prevent unfair ranking of cadets?

1. **Exclude controllable vs uncontrollable factors:** A cadet whose sorties were cancelled due to Weather or ATC (not their fault) should not be penalised equally with one who repeatedly fails to show up.
2. **Course-normalise progress:** PPL cadets at 80% of 45 hours are in a very different position than CPL cadets at 80% of 200 hours — the formula correctly uses `progress_pct` which normalises for this.
3. **Transparency:** Every cadet's score should be explainable — the `main_risk_reason` column exists precisely to show cadets WHY they rank where they do, not just a number.
4. **Regular recalibration:** Weights should be reviewed every 6 months against actual outcomes — if "payment risk" weight consistently over-penalises cadets who catch up on payments, reduce it.
5. **Human override:** The score is a decision-support tool, not a decision-making tool. CFIs can override risk flags with documented reasoning.

---

## Q8: How should AIRMAN display this insight without demotivating students?

1. **Frame scores as "support opportunities" not "failure grades":** In TOGA, show "Your readiness is 58/100 — here's what to focus on" not "You scored 58."
2. **Show progress, not just absolute scores:** A cadet who improved from 40 to 58 in a month should see that trajectory celebrated.
3. **Never show comparative rankings to cadets** — cadets should only see their own data, not how they rank against peers.
4. **Specific actionable suggestions only:** Vague alerts ("your progress is low") are demoralising. Specific ones ("Complete Navigation chapters 12–20 before your Cross Country sortie") are empowering.
5. **CFI-first communication:** High-risk flags go to instructors first. Instructors then have a supportive conversation with the cadet, not a system notification that feels punitive.

---

## Q9: What additional data would improve the model?

1. **DGCA exam scores and dates** — the ultimate ground school validation
2. **Actual weather METAR data** at each sortie — would let us distinguish weather-caused cancellations from avoidable ones
3. **CFI assessment scores** per sortie — instructor's 1–10 rating of cadet handling
4. **Cadet attendance at ground school sessions** — separate from TOGA app usage
5. **Aircraft type preferences per cadet** — some cadets may be faster progressors on one type

---

## Q10: How would this analysis help Skynet and TOGA become more intelligent products?

**For Skynet:**
The operations analysis demonstrates that scheduling without intelligence creates safety risks (qualification mismatches), regulatory risks (cross-base deployments), and financial waste (idle fleet). By embedding the metrics from this analysis — utilisation rates, instructor workload ratios, cadet risk scores — directly into Skynet's ops dashboard, every scheduling decision becomes data-informed. A dispatcher who can see "this aircraft has 12 defects and 62% downtime" before assigning it to a solo cadet makes a better decision.

**For TOGA:**
The study intelligence analysis shows that TOGA has rich behavioural data that is not yet being actioned. Cadets have weak subjects, inactivity patterns, and practice test gaps that TOGA can detect and respond to in real time. By making TOGA a *responsive* platform — one that pushes relevant content based on upcoming sortie types, inactivity gaps, and quiz performance — AIRMAN transforms TOGA from a content library into an intelligent training companion. The pre-sortie readiness gate (TOGA → Skynet API) is the single highest-value integration that directly links ground study to airside safety.
"""

# ── README ─────────────────────────────────────────────────────────────────────
readme = """# AIRMAN Data Science Assessment — Ayan

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
"""

os.makedirs(REPORTS, exist_ok=True)
with open(os.path.join(REPORTS, "executive_insights.md"), "w", encoding="utf-8") as f:
    f.write(exec_report)
print("DONE: executive_insights.md")

with open(os.path.join(REPORTS, "methodology.md"), "w", encoding="utf-8") as f:
    f.write(methodology)
print("DONE: methodology.md")

with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)
print("DONE: README.md")
