# Methodology Document — AIRMAN Data Science Assessment

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
