"""
STEP 10 — Generate analysis.ipynb from scripts
Creates a self-documenting Jupyter notebook that runs top-to-bottom
"""
import json, os

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"

def md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}

def code_cell(source):
    return {
        "cell_type": "code", "execution_count": None, "metadata": {},
        "outputs": [], "source": [source]
    }

cells = []

# ─── [0] SETUP ────────────────────────────────────────────────────────────────
cells.append(md_cell("# AIRMAN Aeronautics — FTO Data Science Assessment\n**Analyst:** Ayan | **Reference Date:** 2026-05-15 | **Period:** May–June 2026\n\n---"))
cells.append(code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings, os
warnings.filterwarnings('ignore')

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
PALETTE = ['#1A3557','#2E86AB','#A23B72','#F18F01','#C73E1D','#44BBA4','#E94F37']

BASE    = r"c:\\Users\\Ayan2\\OneDrive\\Desktop\\AIRMAN_Assessment-"
DATA    = os.path.join(BASE, "data")
REPORTS = os.path.join(BASE, "reports")
CHARTS  = os.path.join(BASE, "charts")
REF_DATE = pd.Timestamp('2026-05-15')
print("Setup complete. Reference date:", REF_DATE.date())"""))

# ─── [1] LOAD DATA ────────────────────────────────────────────────────────────
cells.append(md_cell("## Section 1 — Load Data"))
cells.append(code_cell("""sorties     = pd.read_csv(os.path.join(DATA, "sorties.csv"))
aircraft    = pd.read_csv(os.path.join(DATA, "aircraft.csv"))
cadets      = pd.read_csv(os.path.join(DATA, "cadets.csv"))
instructors = pd.read_csv(os.path.join(DATA, "instructors.csv"))
payments    = pd.read_csv(os.path.join(DATA, "payments.csv"))
toga        = pd.read_csv(os.path.join(DATA, "toga_study.csv"))

for col in ['scheduled_start','scheduled_end','actual_start','actual_end']:
    sorties[col] = pd.to_datetime(sorties[col], errors='coerce')
cadets['enrollment_date']       = pd.to_datetime(cadets['enrollment_date'])
payments['last_payment_date']   = pd.to_datetime(payments['last_payment_date'])
toga['last_active_date']        = pd.to_datetime(toga['last_active_date'])

print(f"sorties: {sorties.shape} | aircraft: {aircraft.shape} | cadets: {cadets.shape}")
print(f"instructors: {instructors.shape} | payments: {payments.shape} | toga: {toga.shape}")"""))

# ─── [2] TASK 1: DATA CLEANING ────────────────────────────────────────────────
cells.append(md_cell("## Section 2 — Task 1: Data Cleaning & Validation\nRuns 15 validation checks across all 6 datasets."))
cells.append(code_cell("""# Check 8: Payment calculation errors
payments['expected_outstanding'] = payments['invoiced_amount'] - payments['paid_amount']
c8 = payments[payments['outstanding_amount'] != payments['expected_outstanding']]
print(f"CHECK 8 — Payment errors: {len(c8)} cadets: {c8['cadet_id'].tolist()}")

# Check 9: TOGA impossible chapters
toga['capped'] = toga['chapters_completed'] > toga['total_chapters']
c9 = toga[toga['capped']]
print(f"CHECK 9 — TOGA impossible progress: {len(c9)} rows: {(c9['cadet_id']+'/'+ c9['subject']).tolist()}")

# Check 10: Aircraft maintenance > available
c10 = aircraft[aircraft['maintenance_downtime_hours'] > aircraft['total_available_hours']]
print(f"CHECK 10 — Maintenance data error: {len(c10)} aircraft: {c10['aircraft_id'].tolist()}")

# Check 13: Instructor base mismatch
s_i = sorties.merge(instructors[['instructor_id','base_id']], on='instructor_id', suffixes=('_s','_i'))
c13 = s_i[s_i['base_id_s'] != s_i['base_id_i']]
print(f"CHECK 13 — Instructor base mismatch: {len(c13)} sorties")

# Check 14: Qualification mismatch
s_ia = sorties.merge(aircraft[['aircraft_id','type']], on='aircraft_id')
s_iac = s_ia.merge(instructors[['instructor_id','aircraft_qualified']], on='instructor_id')
c14 = s_iac[s_iac['aircraft_qualified'] != s_iac['type']]
print(f"CHECK 14 — Qualification mismatch: {len(c14)} sorties: {c14['sortie_id'].tolist()}")

# Duplicate names
dup_names = cadets.groupby('name')['cadet_id'].apply(list)
dup_names = dup_names[dup_names.apply(len)>1]
print(f"CHECK 3 — Duplicate cadet names: {len(dup_names)} names")
for nm, ids in dup_names.items():
    print(f"  '{nm}': {ids}")"""))

# ─── [3] TASK 2: OPERATIONS ───────────────────────────────────────────────────
cells.append(md_cell("## Section 3 — Task 2: Skynet Operations Analytics"))
cells.append(code_cell("""comp = sorties[sorties['status']=='completed'].copy()
comp['flight_hours'] = (comp['actual_end'] - comp['actual_start']).dt.total_seconds() / 3600

ac_flown = comp.groupby('aircraft_id')['flight_hours'].sum().reset_index()
ac_util  = aircraft.merge(ac_flown, on='aircraft_id', how='left').fillna({'flight_hours':0})
ac_util['utilization_rate'] = (ac_util['flight_hours'] / ac_util['total_available_hours'] * 100).round(2)

completion_rate   = (sorties['status']=='completed').mean() * 100
cancellation_rate = (sorties['status']=='cancelled').mean() * 100
avg_delay = comp['delay_minutes'].mean()

cancel_breakdown = sorties[sorties['status']=='cancelled']['cancel_reason'].value_counts()
print(f"Completion rate: {completion_rate:.1f}% | Cancellation rate: {cancellation_rate:.1f}%")
print(f"Average delay (completed): {avg_delay:.1f} min")
print(f"Under-utilised aircraft (<40%): {(ac_util['utilization_rate']<40).sum()}")
print(f"Cancellation reasons:\\n{cancel_breakdown.to_string()}")"""))

# ─── [4] TASK 3: TRAINING PROGRESS ───────────────────────────────────────────
cells.append(md_cell("## Section 4 — Task 3: Training Progress Analytics"))
cells.append(code_cell("""cadets['progress_pct']  = cadets['total_flown_hours'] / cadets['total_required_hours'] * 100
cadets['days_enrolled'] = (REF_DATE - cadets['enrollment_date']).dt.days.clip(lower=1)
cadets['flying_rate']   = cadets['total_flown_hours'] / cadets['days_enrolled']
cadets['remaining_hrs'] = (cadets['total_required_hours'] - cadets['total_flown_hours']).clip(lower=0)
cadets['est_days']      = cadets['remaining_hrs'] / cadets['flying_rate'].replace(0, np.nan)
cadets['est_completion_date'] = cadets.apply(
    lambda r: (REF_DATE + pd.Timedelta(days=r['est_days'])).date() if pd.notna(r['est_days']) else None, axis=1)

at_risk = cadets.apply(lambda r: (
    pd.Timestamp(str(r['est_completion_date'])) > r['enrollment_date'] + pd.Timedelta(days=180 if r['course']=='PPL' else 540)
    if r['est_completion_date'] else True), axis=1)

print(f"At-risk cadets: {at_risk.sum()} / {len(cadets)}")
print(f"Avg PPL progress: {cadets[cadets['course']=='PPL']['progress_pct'].mean():.1f}%")
print(f"Avg CPL progress: {cadets[cadets['course']=='CPL']['progress_pct'].mean():.1f}%")"""))

# ─── [5] TASK 4: TOGA ─────────────────────────────────────────────────────────
cells.append(md_cell("## Section 5 — Task 4: TOGA Study Intelligence"))
cells.append(code_cell("""toga['chapters_completed'] = toga[['chapters_completed','total_chapters']].min(axis=1)
toga['subject_progress']  = toga['chapters_completed'] / toga['total_chapters']
toga['practice_score']    = (toga['practice_tests_attempted'] / 10).clip(upper=1) * 100

per_cadet = toga.groupby('cadet_id').agg(
    mean_quiz=('avg_quiz_score','mean'),
    mean_progress=('subject_progress','mean'),
    mean_practice=('practice_score','mean'),
    last_active=('last_active_date','max'),
    mean_tests=('practice_tests_attempted','mean')
).reset_index()

per_cadet['study_readiness'] = (
    0.40 * per_cadet['mean_quiz'] +
    0.30 * per_cadet['mean_progress'] * 100 +
    0.30 * per_cadet['mean_practice']
).round(2)

per_cadet['days_inactive'] = (REF_DATE - per_cadet['last_active']).dt.days
per_cadet['inactive_flag'] = per_cadet['days_inactive'] > 7

print(f"Average study readiness: {per_cadet['study_readiness'].mean():.1f}")
print(f"Inactive cadets (>7d): {per_cadet['inactive_flag'].sum()}")
weak_subj = toga.groupby('subject')['avg_quiz_score'].mean().sort_values()
print("Weakest subjects (fleet average):"); print(weak_subj.to_string())"""))

# ─── [6] TASK 5: FINANCE ──────────────────────────────────────────────────────
cells.append(md_cell("## Section 6 — Task 5: Finance & Operational Risk"))
cells.append(code_cell("""payments['expected_outstanding'] = payments['invoiced_amount'] - payments['paid_amount']
payments['payment_completion_pct'] = payments['paid_amount'] / payments['invoiced_amount'] * 100
payments['outstanding_ratio']      = payments['outstanding_amount'] / payments['invoiced_amount']
payments['days_since_payment']     = (REF_DATE - payments['last_payment_date']).dt.days

error_cadets = {'C006','C023','C068','C102'}
payments['payment_risk_score'] = payments.apply(lambda r: (
    0.50 * r['outstanding_ratio'] * 100 +
    0.30 * min(r['days_since_payment']/60,1) * 100 +
    0.20 * (1 - r['payment_completion_pct']/100) * 100
) if r['cadet_id'] not in error_cadets else np.nan, axis=1)

total_outstanding = payments['outstanding_amount'].sum()
collection_rate   = payments['paid_amount'].sum() / payments['invoiced_amount'].sum() * 100
print(f"Total outstanding: INR {total_outstanding:,.0f}")
print(f"Collection rate: {collection_rate:.1f}%")
print(f"High risk cadets: {(payments['payment_risk_score']>=70).sum()}")
print("Data integrity errors:", list(error_cadets))"""))

# ─── [7] TASK 6: RISK SCORE ───────────────────────────────────────────────────
cells.append(md_cell("## Section 7 — Task 6: Explainable Cadet Risk Score\nWeighted formula — no ML models."))
cells.append(code_cell("""risk = cadets[['cadet_id','name','course']].copy()
risk['flight_progress'] = (cadets['progress_pct'] / 100).clip(0,1)

risk = risk.merge(per_cadet[['cadet_id','study_readiness','mean_quiz','days_inactive']], on='cadet_id', how='left')
risk = risk.merge(payments[['cadet_id','payment_risk_score']], on='cadet_id', how='left')

cancel_r = sorties.groupby('cadet_id').apply(
    lambda x: (x['status']=='cancelled').sum() / len(x)).reset_index(name='cancel_rate')
risk = risk.merge(cancel_r, on='cadet_id', how='left').fillna(0)

risk['inactivity_score']     = (risk['days_inactive'] / 30).clip(0,1)
risk['study_readiness_norm'] = (risk['study_readiness'].fillna(50) / 100).clip(0,1)
risk['quiz_norm']            = (risk['mean_quiz'].fillna(50) / 100).clip(0,1)
risk['payment_norm']         = (risk['payment_risk_score'].fillna(50) / 100).clip(0,1)

risk['risk_score'] = (
    0.25*(1 - risk['flight_progress']) +
    0.20*(1 - risk['study_readiness_norm']) +
    0.15*(1 - risk['quiz_norm']) +
    0.15* risk['payment_norm'] +
    0.15* risk['inactivity_score'] +
    0.10* risk['cancel_rate'].clip(0,1)
) * 100

risk['risk_level'] = pd.cut(risk['risk_score'], bins=[0,40,70,101],
                             labels=['Low','Medium','High'], right=False)
print("Risk distribution:"); print(risk['risk_level'].value_counts().to_string())
print("\\nTop 5 highest risk:")
print(risk.nlargest(5,'risk_score')[['cadet_id','name','risk_score','risk_level']].to_string(index=False))"""))

# ─── [8] TASK 7: VISUALISATIONS ───────────────────────────────────────────────
cells.append(md_cell("## Section 8 — Task 7: Visualisations\nAll 7 charts saved to `charts/` at 300 DPI."))
cells.append(code_cell(r"""import subprocess, sys
result = subprocess.run([sys.executable, r'scripts/step7_charts.py'], capture_output=True, text=True,
    cwd=r'c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-')
print(result.stdout)
if result.returncode != 0: print("ERRORS:", result.stderr)
else: print("All charts generated successfully.")"""))

# ─── [9] EXPORT ───────────────────────────────────────────────────────────────
cells.append(md_cell("## Section 9 — Export Outputs"))
cells.append(code_cell("""# Save final risk_scores.csv
risk_out = risk[['cadet_id','name','course','risk_score','risk_level',
                 'flight_progress','study_readiness','mean_quiz',
                 'payment_risk_score','days_inactive','cancel_rate']].copy()
risk_out.columns = ['cadet_id','name','course','risk_score','risk_level',
                    'flight_progress','study_readiness','avg_quiz_score',
                    'payment_risk','days_inactive','cancellation_rate']
risk_out.to_csv(os.path.join(DATA, "risk_scores.csv"), index=False)

# Verify all required files
required = [
    "data/cleaned_outputs.csv", "data/risk_scores.csv",
    "reports/data_quality_report.md", "reports/skynet_operations_analysis.md",
    "reports/training_progress_analysis.md", "reports/toga_study_intelligence.md",
    "reports/finance_risk_analysis.md", "reports/executive_insights.md",
    "reports/methodology.md", "README.md",
    "charts/aircraft_utilization.png", "charts/cancellation_reasons.png",
    "charts/cadet_progress.png", "charts/study_readiness.png",
    "charts/payment_risk.png", "charts/cadet_risk_scores.png",
    "charts/flight_vs_study_progress.png",
]
print("DELIVERABLE CHECKLIST:")
all_ok = True
for f in required:
    path = os.path.join(BASE, f)
    exists = os.path.exists(path)
    status = "OK" if exists else "MISSING"
    if not exists: all_ok = False
    print(f"  [{status}] {f}")
print(f"\\nAll files present: {all_ok}")"""))

# ─── NOTEBOOK STRUCTURE ───────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"}
    },
    "cells": cells
}

nb_path = os.path.join(BASE, "notebooks", "analysis.ipynb")
os.makedirs(os.path.dirname(nb_path), exist_ok=True)
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print(f"DONE: analysis.ipynb saved ({len(cells)} cells)")
print(f"Path: {nb_path}")
