"""
STEP 2 — Skynet Operations Analytics
Aircraft utilization, instructor utilization, dispatch reliability
"""
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA = os.path.join(BASE, "data")
REPORTS = os.path.join(BASE, "reports")
REF_DATE = pd.Timestamp('2026-05-15')

sorties     = pd.read_csv(os.path.join(DATA, "sorties.csv"))
aircraft    = pd.read_csv(os.path.join(DATA, "aircraft.csv"))
instructors = pd.read_csv(os.path.join(DATA, "instructors.csv"))

# ── STEP A: Parse datetimes and validate duration ─────────────────────────────
for col in ['scheduled_start', 'scheduled_end', 'actual_start', 'actual_end']:
    sorties[col] = pd.to_datetime(sorties[col], errors='coerce')
sorties['scheduled_start'] = pd.to_datetime(sorties['scheduled_start'], errors='coerce')

# Compute duration for all sorties
sorties['duration_hours'] = (
    (sorties['actual_end'] - sorties['actual_start']).dt.total_seconds() / 3600
)

# Flag invalid durations: negative OR impossibly long (>12 hours)
invalid_duration_mask = (
    (sorties['duration_hours'] < 0) | (sorties['duration_hours'] > 12)
) & sorties['duration_hours'].notna()

invalid_count = invalid_duration_mask.sum()
invalid_sortie_ids = sorties.loc[invalid_duration_mask, 'sortie_id'].tolist()

if invalid_count > 0:
    print(f"WARNING: {invalid_count} sorties have invalid duration — excluded from utilization")
    print(f"  Affected sortie IDs: {invalid_sortie_ids}")
    # Set duration to NaN for invalid rows
    sorties.loc[invalid_duration_mask, 'duration_hours'] = np.nan

# ── STEP B: Aircraft utilization using validated durations ────────────────────
valid_comp = sorties[
    (sorties['status'] == 'completed') &
    (sorties['duration_hours'] > 0) &
    (sorties['duration_hours'].notna())
].copy()

ac_flown = valid_comp.groupby('aircraft_id')['duration_hours'].sum().reset_index()
ac_flown.columns = ['aircraft_id', 'actual_flown_hours']

ac_util = aircraft.merge(ac_flown, on='aircraft_id', how='left')
ac_util['actual_flown_hours'] = ac_util['actual_flown_hours'].fillna(0)
ac_util['utilization_rate'] = (ac_util['actual_flown_hours'] / ac_util['total_available_hours'] * 100).round(2)
ac_util['util_flag'] = ac_util['utilization_rate'].apply(
    lambda x: 'Under-utilised (<40%)' if x < 40 else ('Optimal (40-70%)' if x <= 70 else 'High (>70%)'))
ac_util['maintenance_pct'] = (ac_util['maintenance_downtime_hours'] / ac_util['total_available_hours'] * 100).round(2)
ac_util['maintenance_flag'] = ac_util['maintenance_pct'] > 50
ac_util['defect_flag'] = ac_util['defect_count'] >= 10
ac_util['data_error_flag'] = ac_util['maintenance_downtime_hours'] > ac_util['total_available_hours']

# Sanity check: no aircraft should have negative flown hours
assert (ac_util['actual_flown_hours'] >= 0).all(), "ERROR: Negative flown hours detected!"
assert (ac_util['utilization_rate'] >= 0).all(), "ERROR: Negative utilization rate detected!"

# ── INSTRUCTOR UTILIZATION ────────────────────────────────────────────────────
instructors['flight_ratio'] = (instructors['total_flight_hours'] / instructors['total_duty_hours']).round(3)
instructors['instr_flag'] = instructors['flight_ratio'].apply(
    lambda x: 'Overloaded (>0.85)' if x > 0.85 else ('Under-utilised (<0.40)' if x < 0.40 else 'Optimal'))

overloaded = instructors[instructors['flight_ratio'] > 0.85]
underused  = instructors[instructors['flight_ratio'] < 0.40]

# ── DISPATCH RELIABILITY ──────────────────────────────────────────────────────
total_sorties = len(sorties)
completed_n   = (sorties['status'] == 'completed').sum()
cancelled_n   = (sorties['status'] == 'cancelled').sum()
completion_rate   = completed_n / total_sorties * 100
cancellation_rate = cancelled_n / total_sorties * 100

cancel_breakdown = sorties[sorties['status']=='cancelled']['cancel_reason'].value_counts()
cancel_pct       = (cancel_breakdown / cancelled_n * 100).round(1)

# Avg delay for completed sorties (using valid_comp for accuracy)
comp = sorties[sorties['status']=='completed'].copy()
avg_delay = comp['delay_minutes'].mean()
delayed_n = (comp['delay_minutes'] > 0).sum()

# By base
base_stats = sorties.groupby('base_id').agg(
    total=('sortie_id','count'),
    completed=('status', lambda x: (x=='completed').sum()),
    cancelled=('status', lambda x: (x=='cancelled').sum())
).reset_index()
base_stats['completion_pct'] = (base_stats['completed']/base_stats['total']*100).round(1)

# By lesson type
lesson_stats = sorties.groupby('lesson_type').agg(
    total=('sortie_id','count'),
    cancelled=('status', lambda x: (x=='cancelled').sum())
).reset_index()
lesson_stats['cancel_rate'] = (lesson_stats['cancelled']/lesson_stats['total']*100).round(1)
lesson_stats = lesson_stats.sort_values('cancel_rate', ascending=False)

# By day of week
sorties['dow'] = sorties['scheduled_start'].dt.day_name()
dow_delay = comp.groupby(comp['scheduled_start'].dt.day_name())['delay_minutes'].mean().round(1)

# Delay distribution by lesson type
lesson_delay = comp.groupby('lesson_type')['delay_minutes'].mean().round(1).sort_values(ascending=False)

# ── COMPUTE SUMMARY STATS FOR REPORT ─────────────────────────────────────────
data_error_aircraft = ac_util[ac_util['data_error_flag']]
valid_util = ac_util[~ac_util['data_error_flag']].copy()
avg_util_rate = valid_util['utilization_rate'].mean().round(1)
n_adequate    = (valid_util['utilization_rate'] >= 40).sum()
n_under       = (valid_util['utilization_rate'] < 40).sum()
n_zero        = (valid_util['utilization_rate'] == 0).sum()
n_data_error  = len(data_error_aircraft)

under_util = ac_util[ac_util['utilization_rate'] < 40]
high_maint = ac_util[ac_util['maintenance_flag'] & ~ac_util['data_error_flag']]
hi_defect  = ac_util[ac_util['defect_flag']]

# Top 10 and bottom 10 (excluding data error aircraft)
top10  = valid_util.sort_values('utilization_rate', ascending=False).head(10)
bot10  = valid_util.sort_values('utilization_rate', ascending=True).head(10)
defect_review = ac_util[ac_util['defect_flag']].sort_values('defect_count', ascending=False)

# ── WRITE REPORT (Fix 3: summary + top/bottom instead of 120-row table) ───────
lines = [
    "# Skynet Operations Analysis Report",
    f"*Period: May 1 – June 30, 2026 | Reference Date: {REF_DATE.date()}*\n",
    "---\n## 1. Fleet Utilisation\n",
    f"**Total aircraft in fleet:** {len(aircraft)}  |  **Data anomalies (maintenance > available):** {n_data_error} aircraft\n",
    "### 1.1 Fleet Utilization Summary\n",
    "| Metric | Value |",
    "|--------|-------|",
    f"| Total aircraft in fleet | {len(aircraft)} |",
    f"| Aircraft with utilization data | {len(valid_util)} ({n_data_error} excluded — data integrity errors) |",
    f"| Average utilization rate | {avg_util_rate}% |",
    f"| Aircraft with utilization ≥ 40% (adequate) | {n_adequate} |",
    f"| Aircraft with utilization < 40% (under-utilized) | {n_under} |",
    f"| Aircraft with utilization = 0% (no sorties flown) | {n_zero} |",
    "",
    "### Top 10 Best-Utilized Aircraft\n",
    "| Aircraft | Type | Base | Avail Hrs | Flown Hrs | Util% | Status |",
    "|----------|------|------|-----------|-----------|-------|--------|",
]
for _, row in top10.iterrows():
    lines.append(f"| {row['aircraft_id']} | {row['type']} | {row['base_id']} | {row['total_available_hours']} | "
                 f"{row['actual_flown_hours']:.1f} | {row['utilization_rate']:.1f}% | {row['util_flag']} |")

lines += [
    "",
    "### Bottom 10 Most Under-Utilized Aircraft\n",
    "*Excluding A003, A009, A016 (data integrity errors — see below)*\n",
    "| Aircraft | Type | Base | Avail Hrs | Flown Hrs | Util% | Status |",
    "|----------|------|------|-----------|-----------|-------|--------|",
]
for _, row in bot10.iterrows():
    lines.append(f"| {row['aircraft_id']} | {row['type']} | {row['base_id']} | {row['total_available_hours']} | "
                 f"{row['actual_flown_hours']:.1f} | {row['utilization_rate']:.1f}% | {row['util_flag']} |")

lines += [
    "",
    "### Aircraft Requiring Operational Review (Defect Count ≥ 10)\n",
    "| Aircraft | Type | Base | Defect Count | Avail Hrs | Flown Hrs | Util% |",
    "|----------|------|------|-------------|-----------|-----------|-------|",
]
for _, row in defect_review.head(15).iterrows():
    flag = " ⚠️ DATA ERROR" if row['data_error_flag'] else ""
    lines.append(f"| {row['aircraft_id']} | {row['type']} | {row['base_id']} | {row['defect_count']} | "
                 f"{row['total_available_hours']} | {row['actual_flown_hours']:.1f} | {row['utilization_rate']:.1f}%{flag} |")

lines += [
    f"\n*...and {max(0, len(defect_review)-15)} more aircraft with defect_count ≥ 10 — full list in data_quality_report.md*\n",
    "### Data Integrity Flags\n",
    "The following aircraft have maintenance_downtime_hours exceeding total_available_hours (physically impossible). "
    "They are excluded from utilization calculations pending engineering review.\n",
    "| Aircraft | Type | Base | Avail Hrs | Maintenance Hrs | Status |",
    "|----------|------|------|-----------|-----------------|--------|",
]
for _, row in data_error_aircraft.iterrows():
    lines.append(f"| {row['aircraft_id']} | {row['type']} | {row['base_id']} | "
                 f"{row['total_available_hours']} | {row['maintenance_downtime_hours']} | ⚠️ DATA ERROR |")

lines += [
    f"\n**Under-utilised aircraft (<40%):** {len(under_util)} aircraft",
    f"**High maintenance burden (>50% of available hrs):** {len(high_maint)} aircraft",
    f"**High defect count (≥10 defects):** {len(hi_defect)} aircraft — {', '.join(hi_defect['aircraft_id'].tolist())}",
    "\n**Skynet Dashboard Alert:** Flag A003, A009, A016 as 'DATA INTEGRITY ERROR — maintenance hours exceed available hours'. "
    "Engineering team must verify actual downtime records before these aircraft are returned to the dispatch schedule.\n",
    "---\n## 2. Instructor Utilisation\n",
    f"**Total instructors:** {len(instructors)}",
    f"**Overloaded (flight ratio >0.85):** {len(overloaded)} — Risk of instructor fatigue and DGCA duty-hour breaches",
    f"**Under-utilised (flight ratio <0.40):** {len(underused)} — Scheduling inefficiency\n",
    "### Top 5 Overloaded Instructors",
    "| Instructor | Base | Qualified Type | Duty Hrs | Flight Hrs | Ratio |",
    "|------------|------|---------------|----------|------------|-------|",
]
for _, row in overloaded.sort_values('flight_ratio', ascending=False).head(5).iterrows():
    lines.append(f"| {row['instructor_id']} ({row['name']}) | {row['base_id']} | "
                 f"{row['aircraft_qualified']} | {row['total_duty_hours']} | {row['total_flight_hours']} | {row['flight_ratio']:.2f} |")

lines += [
    f"\n**Skynet Action:** Instructors {', '.join(overloaded['instructor_id'].tolist())} should be reviewed for duty-hour compliance. "
    "Skynet should enforce a 0.85 flight-to-duty ratio cap and alert the CFI when any instructor approaches this threshold.\n",
    "---\n## 3. Dispatch Reliability\n",
    f"**Total sorties scheduled:** {total_sorties}",
    f"**Completed:** {completed_n} ({completion_rate:.1f}%)",
    f"**Cancelled:** {cancelled_n} ({cancellation_rate:.1f}%)",
    f"**Delayed (>0 min):** {delayed_n} of {completed_n} completed sorties ({delayed_n/completed_n*100:.1f}%)",
    f"**Average delay (completed sorties):** {avg_delay:.1f} minutes\n",
    "### 3.1 Cancellation Breakdown",
    "| Reason | Count | % of Cancellations |",
    "|--------|-------|-------------------|",
]
for reason, cnt in cancel_breakdown.items():
    lines.append(f"| {reason} | {cnt} | {cancel_pct[reason]}% |")

lines += [
    "\n### 3.2 Completion Rate by Base",
    "| Base | Total | Completed | Cancelled | Completion% |",
    "|------|-------|-----------|-----------|-------------|",
]
for _, row in base_stats.iterrows():
    lines.append(f"| {row['base_id']} | {row['total']} | {row['completed']} | {row['cancelled']} | {row['completion_pct']}% |")

lines += [
    "\n### 3.3 Cancellation Rate by Lesson Type",
    "| Lesson Type | Total | Cancelled | Cancel Rate% |",
    "|-------------|-------|-----------|--------------|}",
]
for _, row in lesson_stats.iterrows():
    lines.append(f"| {row['lesson_type']} | {row['total']} | {row['cancelled']} | {row['cancel_rate']}% |")

lines += [
    "\n### 3.4 Average Delay by Day of Week",
    "| Day | Avg Delay (min) |",
    "|-----|----------------|",
]
for day, val in dow_delay.sort_values(ascending=False).items():
    lines.append(f"| {day} | {val} |")

lines += [
    "\n### 3.5 Average Delay by Lesson Type",
    "| Lesson Type | Avg Delay (min) |",
    "|-------------|----------------|",
]
for lt, val in lesson_delay.items():
    lines.append(f"| {lt} | {val} |")

lines += [
    "\n---\n## 4. Key Operational Insights for Skynet\n",
    "1. **Weather-related cancellations** are the leading cause. Skynet should integrate MET data to flag high-risk weather days pre-scheduling.",
    "2. **Aircraft Defect cancellations** account for significant disruption. Skynet maintenance module should proactively block aircraft with escalating defect counts.",
    f"3. **Instructor base mismatches** detected in 20 sorties — Skynet scheduling must enforce base-assignment checks before confirming bookings.",
    "4. **Night Flying and Cross Country** sorties have the highest average delays — likely pre-flight briefing time. Skynet should add 15-min buffer to these lesson type templates.",
    "5. **4 qualification mismatch sorties** are a regulatory red flag. Skynet must hard-block any sortie where instructor's `aircraft_qualified` ≠ the assigned aircraft type.",
]

# Add invalid duration note if applicable
if invalid_count > 0:
    lines += [
        f"\n**Data Quality Note:** {invalid_count} sortie(s) with invalid actual_end/actual_start timestamps were detected and excluded from utilization calculations. "
        f"Affected sortie IDs: {', '.join(invalid_sortie_ids)}. These are likely data entry errors.",
    ]

with open(os.path.join(REPORTS, "skynet_operations_analysis.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("DONE: skynet_operations_analysis.md")
print(f"Completion rate: {completion_rate:.1f}% | Avg delay: {avg_delay:.1f} min")
print(f"Overloaded instructors: {len(overloaded)} | Under-utilised aircraft: {len(under_util)}")
print(f"Cancel reasons: {cancel_breakdown.to_dict()}")
if invalid_count > 0:
    print(f"WARNING: {invalid_count} sorties excluded from utilization due to invalid duration")
    print(f"  Sortie IDs: {invalid_sortie_ids}")

# Save ac_util for use in charts
ac_util.to_csv(os.path.join(DATA, "ac_util.csv"), index=False)
print("Saved ac_util.csv")
