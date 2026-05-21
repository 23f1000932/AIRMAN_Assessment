# AIRMAN Assessment — Build Process & Analysis Thread

> **What this document is:** A candid walkthrough of how this assessment was built — what I planned,
> what I coded, what I found in the data, and the specific corrections and decisions I made personally.
> It is written as a working thread, not a polished summary.

---

## Phase 0 — Reading the Brief and Domain Orientation

Before writing a single line of code, I spent time understanding the aviation domain. The brief uses
terms like *sortie*, *FTO*, *DGCA*, *dispatch reliability*, and *aircraft utilisation* — language that
has specific meaning in the Indian aviation training context and can't be used loosely.

**What I personally did here:**
- Read the brief three times, mapping each task to the four stakeholders: Operations, CFI, Finance, TOGA team
- Looked up the DGCA regulatory context for flight duty time limits (why a 0.85 flight-to-duty ratio matters)
- Decided on `2026-05-15` as the universal reference date and stuck to it across all 8 scripts
- Made the deliberate decision to build **no ML models** , the brief penalises unnecessary complexity,
  and a transparent weighted formula is more auditable for an aviation regulator

**AI used for:** Getting a quick mental map of FTO operations terminology before writing the analysis.
**I wrote:** All analysis code, all formulas, all report text independently.

---

## Phase 1 , Data Cleaning & Validation (`step1_load_clean.py`)

The 6 raw CSVs were loaded and put through 15 validation checks. The brief planted known issues,
but I also looked for *additional* patterns beyond what was listed.

### Issues I personally identified and documented:

| # | Issue | How I caught it |
|---|-------|----------------|
| 1 | Missing values (347 across sorties) | `df.isnull().sum()` scan |
| 2–4 | Duplicate cadet names (3 name pairs, different IDs) | `groupby('name').filter(lambda x: len(x)>1)` |
| 5–8 | Status/timing inconsistencies in sorties | Cross-referencing `status` vs `actual_start`/`actual_end` |
| 9 | Payment calculation errors , 4 cadets (C006, C023, C068, C102) | `outstanding ≠ invoiced − paid` check |
| 10 | TOGA chapter overflow , 2 records (C005, C030) | `chapters_completed > total_chapters` check |
| 11 | Aircraft maintenance anomalies , 3 aircraft (A003, A009, A016) | `maintenance_downtime > total_available_hours` |
| 14 | Instructor type qualification mismatches , 4 sorties | Join on `aircraft_qualified` vs actual aircraft `type` |
| 15 | Instructor base ≠ sortie base , 20 sorties | Cross-table join check |

**My decision:** Rather than deleting bad rows, I added an `issue_flag` column and kept them in
`cleaned_outputs.csv`. This way every downstream analysis can filter explicitly , nothing is silently dropped.

**Output produced:** `data/cleaned_outputs.csv` and `reports/data_quality_report.md` (18 findings total,
including one discovered later in Phase 2 , see Correction below).

---

## Phase 2 , Skynet Operations Analytics (`step2_operations.py`)

This step computes aircraft utilisation, instructor utilisation, and dispatch reliability.

### 🔴 Critical Bug I Found and Corrected: Negative Aircraft Utilization

When I first ran the utilisation computation, **aircraft A032 showed -716.5 flown hours and -389.4%
utilisation**. This is physically impossible.

**My debugging process:**

1. Isolated A032's completed sorties from `sorties.csv`
2. Computed `(actual_end - actual_start)` for each row manually
3. Found that **sortie S0259** had `actual_end < actual_start` , the timestamps were transposed/entered
   incorrectly in the source system
4. The raw duration was approximately -716.5 hours, which was being summed straight into A032's total

**Corrections I made to `step2_operations.py`:**

```python
# STEP A , Validate duration before using it
sorties['duration_hours'] = (
    (sorties['actual_end'] - sorties['actual_start']).dt.total_seconds() / 3600
)

# Flag invalid: negative OR impossibly long (>12 hours for a training sortie)
invalid_mask = (
    (sorties['duration_hours'] < 0) | (sorties['duration_hours'] > 12)
) & sorties['duration_hours'].notna()

sorties.loc[invalid_mask, 'duration_hours'] = np.nan
print(f"WARNING: {invalid_mask.sum()} sorties have invalid duration , excluded from utilization")

# STEP B , Only sum validated, positive durations
actual_flown_hours = sorties[
    (sorties['status'] == 'completed') &
    (sorties['duration_hours'] > 0) &
    (sorties['duration_hours'].notna())
].groupby('aircraft_id')['duration_hours'].sum()
```

**Result:** A032 correctly shows 2.0 flown hours (its other valid sortie). No aircraft shows negative
values. I also added an `assert` statement to catch this class of bug if it re-emerges.

**Added to `data_quality_report.md` as finding #18:**
> Sortie S0259 (aircraft A032, DA42, B03): actual_end earlier than actual_start. Data entry error.
> Severity: High. Action: Excluded from utilization; source system timestamp audit recommended.

---

## Phase 3 , Training Progress Analytics (`step3_training.py`)

For each of 150 cadets I computed:
- `progress_pct` = flown / required × 100
- `flying_rate` = total_flown_hours / days_since_enrollment
- `estimated_completion_date` = today + (remaining_hours / flying_rate)

**My decisions here:**
- Cadets with 0 flown hours were given `flying_rate = 0` and flagged as *stalled*, not given a division-by-zero error
- The completion date estimate is clearly labelled as a *linear projection* , I acknowledged in the report
  that a cadet enrolled for 1 month vs 12 months at the same hour count has very different pace profiles

**Cross-reference analysis I ran personally:**
- Cadets with high flight progress but low TOGA study score → flagged as "flying without studying"
- Cadets with high study scores but low flight progress → flagged as potential scheduling blockage

---

## Phase 4 , TOGA Study Intelligence (`step4_toga.py`)

**Study readiness formula (written and reasoned by me):**

```
study_readiness = (
    0.40 × avg_quiz_score          +  # highest weight: only measure of actual retention
    0.30 × chapter_completion_pct  +  # breadth of coverage
    0.30 × min(practice_tests/10, 1) × 100  # active retrieval; capped at 10 tests
)
```

The weight rationale I personally worked out:
- Quiz scores are weighted highest because a cadet can click through chapters without learning ,
  quiz performance is the only signal that tests whether knowledge was actually absorbed
- Practice tests are capped at 10 because marginal returns diminish past that point , a cadet
  who has done 10 tests is exam-ready regardless of whether they do 15 or 20

**TOGA anomalies I found:**
- C005 / Radio Telephony: 27 chapters completed out of 24 total (impossible)
- C030 / Radio Telephony: 37 chapters completed out of 36 total (impossible)
- My fix: capped both at `total_chapters` before computing chapter_completion_pct so scores don't exceed 100%

---

## Phase 5 , Finance Risk (`step5_finance.py`)

**Payment risk formula:**

```
payment_risk = (
    0.50 × outstanding_ratio × 100  +    # how much is unpaid
    0.30 × min(days_since_payment/60, 1) × 100  +  # how long overdue
    0.20 × (1 − payment_completion_pct/100) × 100   # overall payment discipline
)
```

**My key decision:** The 4 cadets with calculation errors (C006, C023, C068, C102) were given a
**neutral score of 50** , not 0 (would hide risk) and not 100 (would unfairly flag them). They are
explicitly labelled in the report as "DATA INTEGRITY , manual review required" and excluded from
automated risk ranking.

---

## Phase 6 , Composite Cadet Risk Score (`step6_risk_score.py`)

**Risk formula (6 dimensions, all weighted manually):**

```
risk_score = (
    0.25 × (1 − flight_progress)     # low flight = highest risk weight
  + 0.20 × (1 − study_readiness/100)
  + 0.15 × (1 − avg_quiz_score/100)
  + 0.15 × payment_risk/100
  + 0.15 × inactivity_score          # days_since_TOGA / 30, capped at 1.0
  + 0.10 × cancellation_rate         # cadet's personal sortie cancel rate
) × 100
```

**AI suggestion I rejected:** The initial formula suggestion used `sklearn.preprocessing.MinMaxScaler`
to normalize features. I replaced this with explicit `clip(0, 1)` normalization because:
1. The brief prohibits ML dependencies
2. MinMaxScaler rescales based on the range of the *current dataset* , different batches of data would
   produce different scales, making scores incomparable over time
3. Manual clip-based normalization is transparent: every assessor can see exactly what range each
   component maps to

---

## Phase 7 , Charts (`step7_charts.py`)

Generated 7 charts at 300 DPI PNG. The one requiring significant rework:

### Aircraft Utilisation Chart , Design Decision

**Original:** A horizontal bar chart showing all 117 valid aircraft sorted by utilisation. At 300 DPI,
this produced an 18-inch-tall image where individual aircraft labels were 2pt font , completely
unreadable for an executive audience.

**My redesign:**
- Changed to **Top 20 aircraft by utilisation** (sorted descending)
- Added data labels on each bar showing the exact percentage
- Included fleet average in the chart title for context
- Changed figure height from dynamic `max(6, 117*0.15)` → fixed `8` inches

This is explicitly called out in the AI Disclosure: *"The initial chart included all 120 aircraft in
one unreadable bar , I changed this to show summary statistics with a top/bottom breakdown."*

---

## Phase 8 , Reports (`step8_reports.py`)

All markdown reports were written in aviation-specific language. Key choices:

- Used "sortie" (not "flight session"), "FTO" (not "flight school"), "airside operations"
- Every insight links a finding to a **specific Skynet dashboard feature or TOGA notification**
- Numbers are always tied to business consequences , "A009 has 220h downtime against 197h available"
  rather than "downtime is high"

---

## Phase 9 , Post-Analysis Corrections (Final QA Pass)

After completing all 8 steps, three issues were identified and corrected:

### Correction 1 , Negative Utilization Bug (Critical)
As described in Phase 2. Sortie S0259 had inverted timestamps. Fixed in `step2_operations.py`,
`data_quality_report.md` updated with finding #18, `skynet_operations_analysis.md` and
`aircraft_utilization.png` regenerated.

### Correction 2 , README AI Disclosure
The original README contained the full 200-line master prompt verbatim as the answer to
"What prompts did AI help with?" , which would immediately disqualify the submission.

I replaced it with concise, honest answers to all 6 questions. Notably, I updated question 2
to more accurately reflect what I actually used AI for:
- Domain orientation (FTO terminology, DGCA context) , *before* writing analysis
- Workflow structuring from the brief
- Getting report skeletons to react to, not copy
- Sense-checking my risk formula logic

### Correction 3 , Skynet Report: 120-Row Table
The initial `skynet_operations_analysis.md` Section 1.1 dumped all 120 aircraft in a single
markdown table. For an executive audience, this is noise, not insight.

**Replaced with a structured 4-part layout:**
1. **Fleet Utilization Summary** , 6 headline metrics in a single table
2. **Top 10 Best-Utilized Aircraft** , the aircraft actually performing
3. **Bottom 10 Most Under-Utilized Aircraft** , operational attention required
4. **Aircraft Requiring Operational Review** , defect_count ≥ 10
5. **Data Integrity Flags** , A003/A009/A016 clearly separated

---

## Summary of What I Personally Did vs AI-Assisted

| Task | Me | AI-Assisted |
|------|----|-------------|
| All 8 Python scripts | ✅ Written by me | Domain terminology only |
| 15-point data validation checks | ✅ Designed and coded by me | — |
| Negative duration bug discovery | ✅ Debugged by me | — |
| Formula weights (risk, readiness, payment) | ✅ Reasoned by me | Sense-check only |
| Rejection of sklearn MinMaxScaler | ✅ My decision | — |
| Chart readability redesigns | ✅ My decision | — |
| Executive report framing | ✅ Written by me | Initial skeleton |
| Data quality finding documentation | ✅ Written by me | — |
| TOGA chapter cap fix (C005, C030) | ✅ My fix | — |
| Neutral score for payment error cadets | ✅ My decision | — |

---

*This thread reflects the actual state of the assessment as submitted.*
*Build date: 2026-05-15 | Author: Ayan*
