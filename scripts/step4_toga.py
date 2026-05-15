"""
STEP 4 — TOGA Study Intelligence
Study readiness scores, weak subjects, cadet TOGA profiles
"""
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA = os.path.join(BASE, "data")
REPORTS = os.path.join(BASE, "reports")
REF_DATE = pd.Timestamp('2026-05-15')

cadets = pd.read_csv(os.path.join(DATA, "cadets.csv"))
toga   = pd.read_csv(os.path.join(DATA, "toga_study.csv"))
toga['last_active_date'] = pd.to_datetime(toga['last_active_date'])

# Cap impossible chapter progress
toga['chapters_completed'] = toga[['chapters_completed','total_chapters']].min(axis=1)

# ── STUDY READINESS SCORE ─────────────────────────────────────────────────────
toga['subject_progress'] = toga['chapters_completed'] / toga['total_chapters']
toga['practice_score']   = (toga['practice_tests_attempted'] / 10).clip(upper=1.0) * 100
toga['days_inactive']    = (REF_DATE - toga['last_active_date']).dt.days.clip(lower=0)

per_cadet = toga.groupby('cadet_id').agg(
    mean_quiz=('avg_quiz_score','mean'),
    mean_progress=('subject_progress','mean'),
    mean_practice_score=('practice_score','mean'),
    last_active=('last_active_date','max'),
    practice_tests_sum=('practice_tests_attempted','sum'),
    practice_tests_mean=('practice_tests_attempted','mean')
).reset_index()

per_cadet['study_readiness'] = (
    0.40 * per_cadet['mean_quiz'] +
    0.30 * per_cadet['mean_progress'] * 100 +
    0.30 * per_cadet['mean_practice_score']
).round(2)

per_cadet['days_since_active'] = (REF_DATE - per_cadet['last_active']).dt.days
per_cadet['inactive_flag'] = per_cadet['days_since_active'] > 7

# Weak subjects
weak = toga[toga['avg_quiz_score'] < 50][['cadet_id','subject','avg_quiz_score']]
weak_by_cadet = weak.groupby('cadet_id')['subject'].apply(list).reset_index()
weak_by_cadet.columns = ['cadet_id','weak_subjects']

# Practice test readiness level
def ptest_level(mean_tests):
    if mean_tests < 3:   return "Low"
    elif mean_tests < 7: return "Medium"
    else:                return "High"
per_cadet['ptest_level'] = per_cadet['practice_tests_mean'].apply(ptest_level)

per_cadet = per_cadet.merge(weak_by_cadet, on='cadet_id', how='left')
per_cadet['weak_subjects'] = per_cadet['weak_subjects'].apply(lambda x: x if isinstance(x, list) else [])
per_cadet = per_cadet.merge(cadets[['cadet_id','name','course']], on='cadet_id', how='left')

# ── RECOMMENDED ACTIONS ───────────────────────────────────────────────────────
def recommend(row):
    actions = []
    if row['weak_subjects']:
        subj = row['weak_subjects'][0]
        actions.append(f"Focus on {subj} — complete remaining chapters and attempt 3 practice tests before next sortie")
    if row['inactive_flag']:
        actions.append(f"Re-engage on TOGA — last activity was {row['days_since_active']} days ago")
    if row['ptest_level'] == 'Low':
        actions.append("Increase practice test frequency to minimum 1 per subject per week")
    if not actions:
        actions.append("Maintain current study rhythm; challenge with advanced practice tests")
    return "; ".join(actions)

def intervention(row):
    if row['study_readiness'] < 40:
        return "Yes — readiness critically low; CFI should review before clearing for solo/navigation sorties"
    if row['inactive_flag'] and row['study_readiness'] < 60:
        return "Yes — inactive + below average readiness"
    return "No"

per_cadet['recommended_action'] = per_cadet.apply(recommend, axis=1)
per_cadet['intervention_required'] = per_cadet.apply(intervention, axis=1)

# ── WRITE REPORT ──────────────────────────────────────────────────────────────
lines = [
    "# TOGA Study Intelligence Report",
    f"*Reference Date: {REF_DATE.date()} | Total cadets analysed: {len(per_cadet)}*\n",
    "---\n## 1. Fleet-Wide Study Summary\n",
    f"- **Average Study Readiness Score:** {per_cadet['study_readiness'].mean():.1f}/100",
    f"- **Cadets inactive >7 days:** {per_cadet['inactive_flag'].sum()}",
    f"- **Cadets with ≥1 weak subject (quiz <50):** {(per_cadet['weak_subjects'].apply(len) > 0).sum()}",
    f"- **Low practice test readiness:** {(per_cadet['ptest_level']=='Low').sum()} cadets\n",
    "---\n## 2. Subject-Level Weak Areas (Fleet-Wide)\n",
    "| Subject | Avg Quiz Score | Cadets Scoring <50 |",
    "|---------|---------------|-------------------|",
]
subject_stats = toga.groupby('subject').agg(
    avg_score=('avg_quiz_score','mean'),
    weak_cadets=('avg_quiz_score', lambda x: (x<50).sum())
).reset_index().sort_values('avg_score')
for _, row in subject_stats.iterrows():
    lines.append(f"| {row['subject']} | {row['avg_score']:.1f} | {int(row['weak_cadets'])} |")

lines += [
    "\n---\n## 3. Cadet TOGA Profile Cards\n",
    "*Showing all cadets — prioritised by readiness score (lowest first)*\n",
]
for _, row in per_cadet.sort_values('study_readiness').iterrows():
    weak_str = ", ".join(row['weak_subjects']) if row['weak_subjects'] else "None"
    inactive_str = f"Inactive {row['days_since_active']} days" if row['inactive_flag'] else "Active (within 7 days)"
    lines += [
        f"### {row['name']} ({row['cadet_id']})",
        f"- **Study Readiness Score:** {row['study_readiness']:.1f}/100",
        f"- **Weak Subjects:** {weak_str}",
        f"- **Activity Status:** {inactive_str} | Last active: {str(row['last_active'])[:10]}",
        f"- **Practice Test Readiness:** {row['ptest_level']} (avg {row['practice_tests_mean']:.1f} tests/subject)",
        f"- **Recommended Action:** {row['recommended_action']}",
        f"- **Instructor Intervention Required:** {row['intervention_required']}\n",
    ]

lines += [
    "---\n## 4. TOGA Product Recommendations\n",
    "1. **Push notifications:** Send TOGA reminder if cadet inactive >5 days with message: 'Your next sortie is approaching — complete your pre-flight study!'",
    "2. **Weak subject spotlight:** On app launch, highlight the subject with lowest quiz score with a quick 5-question review.",
    "3. **Pre-sortie readiness gate:** Require minimum study_readiness ≥ 40 before cadet can book a Navigation or Solo sortie through TOGA.",
]

with open(os.path.join(REPORTS, "toga_study_intelligence.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# Save enriched TOGA data
per_cadet.to_csv(os.path.join(DATA, "toga_enriched.csv"), index=False)
print("DONE: toga_study_intelligence.md")
print(f"Avg readiness: {per_cadet['study_readiness'].mean():.1f}")
print(f"Inactive cadets: {per_cadet['inactive_flag'].sum()}")
print(f"Intervention needed: {(per_cadet['intervention_required'].str.startswith('Yes')).sum()}")
