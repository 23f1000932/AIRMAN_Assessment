"""
STEP 3 — Training Progress Analytics
Cadet flight progress, completion forecasts, at-risk flags
"""
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA = os.path.join(BASE, "data")
REPORTS = os.path.join(BASE, "reports")
REF_DATE = pd.Timestamp('2026-05-15')

cadets  = pd.read_csv(os.path.join(DATA, "cadets.csv"))
sorties = pd.read_csv(os.path.join(DATA, "sorties.csv"))
toga    = pd.read_csv(os.path.join(DATA, "toga_study.csv"))

cadets['enrollment_date'] = pd.to_datetime(cadets['enrollment_date'])
for col in ['actual_start','actual_end']:
    sorties[col] = pd.to_datetime(sorties[col], errors='coerce')

# ── PER-CADET METRICS ─────────────────────────────────────────────────────────
cadets['progress_pct'] = (cadets['total_flown_hours'] / cadets['total_required_hours'] * 100).round(2)
cadets['remaining_hours'] = (cadets['total_required_hours'] - cadets['total_flown_hours']).clip(lower=0)
cadets['days_enrolled'] = (REF_DATE - cadets['enrollment_date']).dt.days.clip(lower=1)
cadets['flying_rate'] = (cadets['total_flown_hours'] / cadets['days_enrolled']).round(4)  # hrs/day

# Estimated completion
def est_days(row):
    if row['flying_rate'] <= 0:
        return np.nan
    return row['remaining_hours'] / row['flying_rate']

cadets['est_completion_days'] = cadets.apply(est_days, axis=1)
cadets['est_completion_date'] = cadets.apply(
    lambda r: (REF_DATE + pd.Timedelta(days=r['est_completion_days'])).date()
    if not np.isnan(r['est_completion_days']) else pd.NaT, axis=1)

# At-risk flag
def risk_flag(row):
    if row['flying_rate'] <= 0:
        return True, "Zero flying rate — no sorties completed"
    target_days = 180 if row['course'] == 'PPL' else 540  # 6mo / 18mo from enrollment
    deadline = row['enrollment_date'] + pd.Timedelta(days=target_days)
    if pd.Timestamp(str(row['est_completion_date'])) > deadline:
        overshoot = (pd.Timestamp(str(row['est_completion_date'])) - deadline).days
        return True, f"Est. completion {overshoot} days past target deadline"
    return False, "On track"

cadets[['at_risk', 'risk_reason']] = cadets.apply(
    lambda r: pd.Series(risk_flag(r)), axis=1)

# ── STUDY vs FLIGHT CROSS REFERENCE ──────────────────────────────────────────
study_avg = toga.groupby('cadet_id').agg(
    avg_quiz=('avg_quiz_score','mean'),
    avg_chapter_progress=('chapters_completed', lambda x: (x / toga.loc[x.index,'total_chapters']).mean()),
    practice_tests=('practice_tests_attempted','mean')
).reset_index()

cadets = cadets.merge(study_avg, on='cadet_id', how='left')

# Quadrant classification
high_flight_low_study = cadets[(cadets['progress_pct'] >= 50) & (cadets['avg_quiz'] < 50)]
low_flight_high_study = cadets[(cadets['progress_pct'] < 50) & (cadets['avg_quiz'] >= 60)]

# ── CANCELLATIONS PER CADET ───────────────────────────────────────────────────
cadet_cancel = sorties[sorties['status']=='cancelled'].groupby('cadet_id').size().reset_index(name='cancellations')
cadet_total  = sorties.groupby('cadet_id').size().reset_index(name='total_sorties')
cadet_cancel_rate = cadet_total.merge(cadet_cancel, on='cadet_id', how='left').fillna(0)
cadet_cancel_rate['cancel_rate'] = (cadet_cancel_rate['cancellations'] / cadet_cancel_rate['total_sorties']).round(3)
cadets = cadets.merge(cadet_cancel_rate[['cadet_id','cancel_rate']], on='cadet_id', how='left').fillna({'cancel_rate': 0})

# ── LESSON TYPE CANCELLATIONS ─────────────────────────────────────────────────
lesson_cancel = sorties.groupby('lesson_type').agg(
    total=('sortie_id','count'),
    cancelled=('status', lambda x: (x=='cancelled').sum())
).reset_index()
lesson_cancel['cancel_rate_pct'] = (lesson_cancel['cancelled']/lesson_cancel['total']*100).round(1)

# ── WRITE REPORT ──────────────────────────────────────────────────────────────
lines = [
    "# Training Progress Analysis Report",
    f"*Period: May–June 2026 | Reference Date: {REF_DATE.date()}*\n",
    "---\n## 1. Fleet-Wide Training Summary\n",
    f"- **Total cadets enrolled:** {len(cadets)}",
    f"- **PPL cadets:** {(cadets['course']=='PPL').sum()} | **CPL cadets:** {(cadets['course']=='CPL').sum()}",
    f"- **Average PPL progress:** {cadets[cadets['course']=='PPL']['progress_pct'].mean():.1f}%",
    f"- **Average CPL progress:** {cadets[cadets['course']=='CPL']['progress_pct'].mean():.1f}%",
    f"- **At-risk cadets:** {cadets['at_risk'].sum()} ({cadets['at_risk'].mean()*100:.1f}% of cohort)\n",
    "---\n## 2. Cadet-Level Progress Table\n",
    "| cadet_id | Name | Course | Progress% | Flying Rate (hrs/day) | Est. Completion | At Risk | Reason |",
    "|----------|------|--------|-----------|-----------------------|-----------------|---------|--------|",
]
for _, row in cadets.sort_values('progress_pct').iterrows():
    est = str(row['est_completion_date']) if pd.notna(row['est_completion_date']) else "N/A"
    lines.append(
        f"| {row['cadet_id']} | {row['name']} | {row['course']} | "
        f"{row['progress_pct']:.1f}% | {row['flying_rate']:.3f} | {est} | "
        f"{'YES' if row['at_risk'] else 'No'} | {row['risk_reason']} |"
    )

lines += [
    "\n---\n## 3. Cross-Reference: Flight vs Study Performance\n",
    f"### 3.1 'Flying Without Studying' — High flight progress (≥50%) but low quiz scores (<50)",
    f"**{len(high_flight_low_study)} cadets identified:** These cadets risk failing ground school despite accumulating flight hours.\n",
    "| cadet_id | Name | Course | Progress% | Avg Quiz Score |",
    "|----------|------|--------|-----------|---------------|",
]
for _, row in high_flight_low_study[['cadet_id','name','course','progress_pct','avg_quiz']].iterrows():
    lines.append(f"| {row['cadet_id']} | {row['name']} | {row['course']} | {row['progress_pct']:.1f}% | {row['avg_quiz']:.1f} |")

lines += [
    f"\n### 3.2 'Studying But Not Flying' — Low flight progress (<50%) but high quiz scores (≥60)",
    f"**{len(low_flight_high_study)} cadets identified:** Possible scheduling bottleneck or instructor/aircraft availability issue.\n",
    "| cadet_id | Name | Course | Progress% | Avg Quiz Score |",
    "|----------|------|--------|-----------|---------------|",
]
for _, row in low_flight_high_study.head(10)[['cadet_id','name','course','progress_pct','avg_quiz']].iterrows():
    lines.append(f"| {row['cadet_id']} | {row['name']} | {row['course']} | {row['progress_pct']:.1f}% | {row['avg_quiz']:.1f} |")

lines += [
    "\n---\n## 4. Lesson Type Cancellation Impact on Training Milestones\n",
    "| Lesson Type | Total Sorties | Cancelled | Cancel Rate% |",
    "|-------------|--------------|-----------|--------------|",
]
for _, row in lesson_cancel.sort_values('cancel_rate_pct', ascending=False).iterrows():
    lines.append(f"| {row['lesson_type']} | {row['total']} | {row['cancelled']} | {row['cancel_rate_pct']}% |")

lines += [
    "\n> **Note:** Night Flying and Cross Country have among the highest cancellation rates.",
    "These are mandatory milestone sorties for CPL cadets — frequent cancellation directly delays CPL completion.\n",
    "---\n## 5. Recommendations\n",
    "1. **Chief Flying Instructor alert:** Cadets with >50% flight progress but <50 quiz score must complete 3 TOGA practice tests before their next sortie.",
    "2. **Skynet scheduling:** Priority-book Night Flying and Cross Country sorties in morning slots when weather and ATC availability are more predictable.",
    "3. **At-risk cadets** should be reviewed in monthly CFI meetings with both flight logbook and TOGA study data visible side-by-side.",
]

with open(os.path.join(REPORTS, "training_progress_analysis.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# Save for downstream use
cadets.to_csv(os.path.join(DATA, "cadets_enriched.csv"), index=False)
print("DONE: training_progress_analysis.md")
print(f"At-risk cadets: {cadets['at_risk'].sum()}")
print(f"Flying without studying: {len(high_flight_low_study)}")
print(f"Studying without flying: {len(low_flight_high_study)}")
