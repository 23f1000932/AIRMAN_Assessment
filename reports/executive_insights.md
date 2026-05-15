# Executive Insight Report — AIRMAN FTO Intelligence
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
