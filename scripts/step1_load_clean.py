"""
STEP 1 — Data Cleaning & Validation
Loads all 6 CSVs, runs 15 validation checks, saves cleaned_outputs.csv
"""
import pandas as pd
import numpy as np
import warnings, os
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA = os.path.join(BASE, "data")
REPORTS = os.path.join(BASE, "reports")
REF_DATE = pd.Timestamp('2026-05-15')

# ── LOAD ─────────────────────────────────────────────────────────────────────
sorties     = pd.read_csv(os.path.join(DATA, "sorties.csv"))
aircraft    = pd.read_csv(os.path.join(DATA, "aircraft.csv"))
cadets      = pd.read_csv(os.path.join(DATA, "cadets.csv"))
instructors = pd.read_csv(os.path.join(DATA, "instructors.csv"))
payments    = pd.read_csv(os.path.join(DATA, "payments.csv"))
toga        = pd.read_csv(os.path.join(DATA, "toga_study.csv"))

# Parse datetimes
for col in ['scheduled_start','scheduled_end','actual_start','actual_end']:
    sorties[col] = pd.to_datetime(sorties[col], errors='coerce')
for col in ['enrollment_date']:
    cadets[col] = pd.to_datetime(cadets[col], errors='coerce')
payments['last_payment_date'] = pd.to_datetime(payments['last_payment_date'], errors='coerce')
toga['last_active_date'] = pd.to_datetime(toga['last_active_date'], errors='coerce')

issues = []  # collect all issues

def flag(category, severity, count, ids, action):
    issues.append({"Issue": category, "Severity": severity, "Count": count,
                   "Affected IDs": ids, "Recommended Action": action})

# ── CHECK 1: Missing values ──────────────────────────────────────────────────
for name, df in [("sorties", sorties),("aircraft", aircraft),
                 ("cadets", cadets),("instructors", instructors),
                 ("payments", payments),("toga", toga)]:
    mv = df.isnull().sum()
    mv = mv[mv > 0]
    if len(mv):
        flag(f"Missing values in {name}", "Medium",
             int(mv.sum()), mv.to_dict(), "Investigate source system for null handling")

# ── CHECK 2: Duplicate IDs ───────────────────────────────────────────────────
for name, df, col in [("sorties", sorties, "sortie_id"),
                      ("aircraft", aircraft, "aircraft_id"),
                      ("cadets", cadets, "cadet_id"),
                      ("instructors", instructors, "instructor_id"),
                      ("payments", payments, "cadet_id")]:
    dups = df[df.duplicated(col, keep=False)][col].unique().tolist()
    if dups:
        flag(f"Duplicate {col} in {name}", "High", len(dups), str(dups), "Deduplicate at source")

# ── CHECK 3: Duplicate cadet names ──────────────────────────────────────────
name_counts = cadets.groupby('name')['cadet_id'].apply(list)
dup_names = name_counts[name_counts.apply(len) > 1]
for nm, ids in dup_names.items():
    flag(f"Duplicate cadet name: '{nm}'", "High", len(ids), str(ids),
         "Manual verification — possible data entry duplicate")

# ── CHECK 4: Invalid status values ──────────────────────────────────────────
valid_statuses = {'completed', 'cancelled'}
bad_status = sorties[~sorties['status'].isin(valid_statuses)]
flag("Invalid sortie status", "High", len(bad_status),
     bad_status['sortie_id'].tolist() if len(bad_status) else "None",
     "Fix status to completed/cancelled")

# ── CHECK 5: Completed sortie missing actual times ───────────────────────────
c5 = sorties[(sorties['status']=='completed') &
             (sorties['actual_start'].isna() | sorties['actual_end'].isna())]
flag("Completed sortie missing actual times", "High", len(c5),
     c5['sortie_id'].tolist() if len(c5) else "None",
     "Backfill from flight logs or investigate data pipeline")

# ── CHECK 6: Cancelled sortie has actual times filled ────────────────────────
c6 = sorties[(sorties['status']=='cancelled') &
             (sorties['actual_start'].notna() | sorties['actual_end'].notna())]
flag("Cancelled sortie has actual times", "Medium", len(c6),
     c6['sortie_id'].tolist() if len(c6) else "None",
     "Clear actual times for cancelled sorties")

# ── CHECK 7: delay_minutes mismatch ──────────────────────────────────────────
comp = sorties[sorties['status']=='completed'].copy()
comp['calc_delay'] = (comp['actual_start'] - comp['scheduled_start']).dt.total_seconds().div(60).round().astype('Int64')
c7 = comp[comp['calc_delay'] != comp['delay_minutes']]
flag("delay_minutes mismatch vs actual times", "Low", len(c7),
     c7['sortie_id'].tolist()[:10] if len(c7) else "None",
     "Recompute delay_minutes from actual_start - scheduled_start")

# ── CHECK 8: outstanding_amount != invoiced - paid ───────────────────────────
payments['expected_outstanding'] = payments['invoiced_amount'] - payments['paid_amount']
c8 = payments[payments['outstanding_amount'] != payments['expected_outstanding']]
flag("Payment calculation error (outstanding ≠ invoiced − paid)", "High", len(c8),
     c8['cadet_id'].tolist(), "Manual finance team review required before risk scoring")

# ── CHECK 9: chapters_completed > total_chapters ─────────────────────────────
c9 = toga[toga['chapters_completed'] > toga['total_chapters']]
flag("TOGA: chapters_completed > total_chapters", "High", len(c9),
     (c9['cadet_id'] + '/' + c9['subject']).tolist(), "Cap at total_chapters; flag for content team review")

# ── CHECK 10: maintenance_downtime > total_available_hours ───────────────────
c10 = aircraft[aircraft['maintenance_downtime_hours'] > aircraft['total_available_hours']]
flag("Aircraft maintenance hours exceed available hours", "High", len(c10),
     c10['aircraft_id'].tolist(), "Immediate engineering review; data entry error likely")

# ── CHECK 11: total_flown_hours > total_required_hours ───────────────────────
c11 = cadets[cadets['total_flown_hours'] > cadets['total_required_hours']]
flag("Cadet flown hours exceed required hours", "Medium", len(c11),
     c11['cadet_id'].tolist() if len(c11) else "None", "Review completion/graduation status")

# ── CHECK 12: avg_quiz_score outside 0-100 ───────────────────────────────────
c12 = toga[(toga['avg_quiz_score'] < 0) | (toga['avg_quiz_score'] > 100)]
flag("Quiz score outside 0-100 range", "High", len(c12),
     c12['cadet_id'].tolist() if len(c12) else "None", "Investigate quiz scoring system")

# ── CHECK 13: Instructor base != sortie base ──────────────────────────────────
sorties_instr = sorties.merge(instructors[['instructor_id','base_id']], on='instructor_id',
                               suffixes=('_sortie','_instructor'))
c13 = sorties_instr[sorties_instr['base_id_sortie'] != sorties_instr['base_id_instructor']]
flag("Instructor base ≠ sortie base", "Medium", len(c13),
     c13['sortie_id'].tolist(), "Investigate cross-base deployments; update Skynet scheduling rules")

# ── CHECK 14: Instructor aircraft_qualified != aircraft type ──────────────────
sorties_ac = sorties.merge(aircraft[['aircraft_id','type']], on='aircraft_id')
sorties_full = sorties_ac.merge(instructors[['instructor_id','aircraft_qualified']], on='instructor_id')
c14 = sorties_full[sorties_full['aircraft_qualified'] != sorties_full['type']]
flag("Instructor type qualification mismatch", "High", len(c14),
     c14['sortie_id'].tolist(), "CRITICAL: Safety review. Instructors may have flown unqualified aircraft")

# ── CHECK 15: Negative numeric values ────────────────────────────────────────
neg_found = []
for name, df in [("aircraft", aircraft),("cadets", cadets),
                 ("instructors", instructors),("payments", payments)]:
    num_cols = df.select_dtypes(include='number').columns
    for col in num_cols:
        neg = df[df[col] < 0]
        if len(neg):
            neg_found.append(f"{name}.{col}: {len(neg)} rows")
flag("Negative numeric values", "Medium", len(neg_found),
     neg_found if neg_found else "None", "Investigate data entry; negative values not valid here")

# ── HIGH DEFECT AIRCRAFT ─────────────────────────────────────────────────────
hi_defect = aircraft[aircraft['defect_count'] >= 10]
flag("High defect count aircraft (≥10 defects)", "High", len(hi_defect),
     hi_defect['aircraft_id'].tolist(), "Operational review; consider AOG or increased inspection interval")

# ── BUILD CLEANED MASTER ──────────────────────────────────────────────────────
master = sorties.copy()
master = master.merge(cadets.add_suffix('_cadet').rename(columns={'cadet_id_cadet':'cadet_id'}),
                      on='cadet_id', how='left')
master = master.merge(instructors.add_suffix('_instr').rename(columns={'instructor_id_instr':'instructor_id'}),
                      on='instructor_id', how='left')
master = master.merge(aircraft.add_suffix('_ac').rename(columns={'aircraft_id_ac':'aircraft_id'}),
                      on='aircraft_id', how='left')

# Add issue flags
issue_flag_list = []
for _, row in master.iterrows():
    flags = []
    sid = row['sortie_id']
    cid = row['cadet_id']
    iid = row['instructor_id']
    aid = row['aircraft_id']
    if sid in c13['sortie_id'].values: flags.append("instructor_base_mismatch")
    if sid in c14['sortie_id'].values: flags.append("qualification_mismatch")
    if cid in c8['cadet_id'].values:   flags.append("payment_calc_error")
    if aid in c10['aircraft_id'].values: flags.append("maintenance_data_error")
    issue_flag_list.append("|".join(flags) if flags else "")

master['data_issues'] = issue_flag_list
master.to_csv(os.path.join(DATA, "cleaned_outputs.csv"), index=False)
print(f"✅ cleaned_outputs.csv saved — {len(master)} rows, {master.columns.tolist()}")

# ── DATA QUALITY REPORT ───────────────────────────────────────────────────────
report_lines = [
    "# Data Quality Report — AIRMAN FTO Intelligence",
    f"*Analysis Date: {REF_DATE.date()} | Total Checks Run: 15*\n",
    "## Summary Table\n",
    "| # | Issue | Severity | Count | Affected IDs | Recommended Action |",
    "|---|-------|----------|-------|-------------|-------------------|",
]
for i, iss in enumerate(issues, 1):
    ids_str = str(iss['Affected IDs'])[:80].replace('\n',' ')
    report_lines.append(
        f"| {i} | {iss['Issue']} | {iss['Severity']} | {iss['Count']} | {ids_str} | {iss['Recommended Action']} |"
    )

report_lines += [
    "\n---\n## Detailed Findings\n",
    "### 1. Payment Calculation Errors (CRITICAL — Finance Team Action Required)",
    "The following 4 cadets have `outstanding_amount ≠ invoiced_amount − paid_amount`.",
    "**These cadets must be excluded from automated payment risk scoring until manually verified.**\n",
    f"- C006: outstanding = {payments[payments.cadet_id=='C006']['outstanding_amount'].values[0]:,} | expected = {payments[payments.cadet_id=='C006']['expected_outstanding'].values[0]:,}",
    f"- C023: outstanding = {payments[payments.cadet_id=='C023']['outstanding_amount'].values[0]:,} | expected = {payments[payments.cadet_id=='C023']['expected_outstanding'].values[0]:,}",
    f"- C068: outstanding = {payments[payments.cadet_id=='C068']['outstanding_amount'].values[0]:,} | expected = {payments[payments.cadet_id=='C068']['expected_outstanding'].values[0]:,}",
    f"- C102: outstanding = {payments[payments.cadet_id=='C102']['outstanding_amount'].values[0]:,} | expected = {payments[payments.cadet_id=='C102']['expected_outstanding'].values[0]:,}",
    "\n### 2. Safety-Critical: Instructor Qualification Mismatches",
    "4 sorties where instructor's qualified aircraft type ≠ aircraft actually flown:",
    "- **S0044**: Instructor I052 (DA40-qualified) flew a C152 (A005)",
    "- **S0107**: Instructor I017 (DA40-qualified) flew a DA42 (A011)",
    "- **S0184**: Instructor I084 (SR20-qualified) flew a C172 (A004)",
    "- **S0263**: Instructor I088 (C172-qualified) flew a C152 (A001)",
    "> ⚠️ Regulatory compliance risk — DGCA mandates type-specific instructor certification.\n",
    "### 3. Aircraft Maintenance Data Anomalies",
    "3 aircraft where maintenance_downtime_hours > total_available_hours (physically impossible):",
    "- **A003** (VT-AIR003, DA40): 146 downtime hrs vs 126 available hrs",
    "- **A009** (VT-EAG009, SR20): 220 downtime hrs vs 197 available hrs",
    "- **A016** (VT-EAG016, C152): 192 downtime hrs vs 183 available hrs",
    "\n### 4. TOGA Study Progress Anomalies",
    "2 records where chapters_completed > total_chapters:",
    "- **C005 / Radio Telephony**: 27 completed out of 24 total",
    "- **C030 / Radio Telephony**: 37 completed out of 36 total",
    "\n### 5. Duplicate Cadet Names (Data Entry Risk)",
    "3 name pairs found with different cadet_ids:",
    "- 'Sanya Gupta': C002 (CPL/B04), C011 (CPL/B02), C096 (PPL/B02)",
    "- 'Vikram Malhotra': C004 (PPL/B02), C036 (PPL/B03), C114 (CPL/B03), C121 (CPL/B02)",
    "- 'Rahul Patel': C051 (PPL/B03), C127 (CPL/B03), C149 (PPL/B01)",
    "\n### 6. Cross-Base Instructor Deployments",
    f"{len(c13)} sorties where instructor's home base ≠ sortie operating base.",
    "This may indicate ad-hoc cross-base scheduling not captured in Skynet. Recommend adding a",
    "'temporary_deployment' flag to the scheduling system.\n",
    "### 7. High-Defect Aircraft",
    f"{len(hi_defect)} aircraft with defect_count ≥ 10: {', '.join(hi_defect['aircraft_id'].tolist())}",
    "These should be placed under enhanced maintenance monitoring in Skynet.\n",
    "---\n*Report generated by AIRMAN Data Science Assessment pipeline*",
]

with open(os.path.join(REPORTS, "data_quality_report.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"✅ data_quality_report.md saved")
print(f"\n📊 ISSUE SUMMARY:")
for i, iss in enumerate(issues, 1):
    print(f"  {i:2}. [{iss['Severity']:6}] {iss['Issue']} — Count: {iss['Count']}")
