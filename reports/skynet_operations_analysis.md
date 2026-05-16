# Skynet Operations Analysis Report
*Period: May 1 – June 30, 2026 | Reference Date: 2026-05-15*

---
## 1. Fleet Utilisation

**Total aircraft in fleet:** 120  |  **Data anomalies (maintenance > available):** 3 aircraft

### 1.1 Fleet Utilization Summary

| Metric | Value |
|--------|-------|
| Total aircraft in fleet | 120 |
| Aircraft with utilization data | 117 (3 excluded — data integrity errors) |
| Average utilization rate | 1.9% |
| Aircraft with utilization ≥ 40% (adequate) | 0 |
| Aircraft with utilization < 40% (under-utilized) | 117 |
| Aircraft with utilization = 0% (no sorties flown) | 16 |

### Top 10 Best-Utilized Aircraft

| Aircraft | Type | Base | Avail Hrs | Flown Hrs | Util% | Status |
|----------|------|------|-----------|-----------|-------|--------|
| A084 | DA40 | B03 | 124 | 7.5 | 6.0% | Under-utilised (<40%) |
| A067 | SR20 | B04 | 148 | 8.5 | 5.7% | Under-utilised (<40%) |
| A002 | SR20 | B03 | 124 | 6.5 | 5.2% | Under-utilised (<40%) |
| A005 | C152 | B01 | 120 | 6.0 | 5.0% | Under-utilised (<40%) |
| A070 | SR20 | B01 | 135 | 6.5 | 4.8% | Under-utilised (<40%) |
| A104 | PA28 | B02 | 125 | 6.0 | 4.8% | Under-utilised (<40%) |
| A049 | C172 | B04 | 126 | 6.0 | 4.8% | Under-utilised (<40%) |
| A040 | DA42 | B01 | 209 | 9.5 | 4.5% | Under-utilised (<40%) |
| A023 | DA40 | B04 | 124 | 5.5 | 4.4% | Under-utilised (<40%) |
| A057 | DA40 | B01 | 183 | 8.0 | 4.4% | Under-utilised (<40%) |

### Bottom 10 Most Under-Utilized Aircraft

*Excluding A003, A009, A016 (data integrity errors — see below)*

| Aircraft | Type | Base | Avail Hrs | Flown Hrs | Util% | Status |
|----------|------|------|-----------|-----------|-------|--------|
| A014 | DA42 | B03 | 144 | 0.0 | 0.0% | Under-utilised (<40%) |
| A024 | PA28 | B04 | 123 | 0.0 | 0.0% | Under-utilised (<40%) |
| A021 | SR20 | B04 | 130 | 0.0 | 0.0% | Under-utilised (<40%) |
| A035 | PA28 | B03 | 184 | 0.0 | 0.0% | Under-utilised (<40%) |
| A034 | C172 | B01 | 161 | 0.0 | 0.0% | Under-utilised (<40%) |
| A020 | SR20 | B03 | 133 | 0.0 | 0.0% | Under-utilised (<40%) |
| A059 | C152 | B01 | 201 | 0.0 | 0.0% | Under-utilised (<40%) |
| A036 | C172 | B03 | 130 | 0.0 | 0.0% | Under-utilised (<40%) |
| A113 | SR20 | B01 | 172 | 0.0 | 0.0% | Under-utilised (<40%) |
| A114 | PA28 | B01 | 194 | 0.0 | 0.0% | Under-utilised (<40%) |

### Aircraft Requiring Operational Review (Defect Count ≥ 10)

| Aircraft | Type | Base | Defect Count | Avail Hrs | Flown Hrs | Util% |
|----------|------|------|-------------|-----------|-----------|-------|
| A049 | C172 | B04 | 15 | 126 | 6.0 | 4.8% |
| A050 | SR20 | B01 | 15 | 213 | 7.5 | 3.5% |
| A022 | DA40 | B03 | 15 | 189 | 1.5 | 0.8% |
| A103 | C152 | B02 | 15 | 159 | 3.5 | 2.2% |
| A120 | SR20 | B02 | 15 | 184 | 1.5 | 0.8% |
| A114 | PA28 | B01 | 14 | 194 | 0.0 | 0.0% |
| A070 | SR20 | B01 | 14 | 135 | 6.5 | 4.8% |
| A066 | DA40 | B02 | 14 | 185 | 2.0 | 1.1% |
| A083 | DA40 | B02 | 13 | 173 | 5.5 | 3.2% |
| A010 | DA42 | B04 | 13 | 170 | 2.0 | 1.2% |
| A088 | PA28 | B03 | 13 | 201 | 1.5 | 0.8% |
| A028 | PA28 | B04 | 13 | 186 | 2.5 | 1.3% |
| A098 | PA28 | B03 | 13 | 173 | 3.5 | 2.0% |
| A073 | C152 | B02 | 13 | 219 | 3.5 | 1.6% |
| A012 | DA40 | B03 | 12 | 182 | 4.0 | 2.2% |

*...and 20 more aircraft with defect_count ≥ 10 — full list in data_quality_report.md*

### Data Integrity Flags

The following aircraft have maintenance_downtime_hours exceeding total_available_hours (physically impossible). They are excluded from utilization calculations pending engineering review.

| Aircraft | Type | Base | Avail Hrs | Maintenance Hrs | Status |
|----------|------|------|-----------|-----------------|--------|
| A003 | DA40 | B03 | 126 | 146 | ⚠️ DATA ERROR |
| A009 | SR20 | B03 | 197 | 220 | ⚠️ DATA ERROR |
| A016 | C152 | B02 | 183 | 192 | ⚠️ DATA ERROR |

**Under-utilised aircraft (<40%):** 120 aircraft
**High maintenance burden (>50% of available hrs):** 0 aircraft
**High defect count (≥10 defects):** 35 aircraft — A002, A010, A012, A018, A022, A023, A027, A028, A029, A031, A039, A040, A041, A045, A048, A049, A050, A052, A066, A067, A070, A071, A073, A080, A083, A087, A088, A089, A092, A098, A103, A105, A114, A116, A120

**Skynet Dashboard Alert:** Flag A003, A009, A016 as 'DATA INTEGRITY ERROR — maintenance hours exceed available hours'. Engineering team must verify actual downtime records before these aircraft are returned to the dispatch schedule.

---
## 2. Instructor Utilisation

**Total instructors:** 100
**Overloaded (flight ratio >0.85):** 22 — Risk of instructor fatigue and DGCA duty-hour breaches
**Under-utilised (flight ratio <0.40):** 16 — Scheduling inefficiency

### Top 5 Overloaded Instructors
| Instructor | Base | Qualified Type | Duty Hrs | Flight Hrs | Ratio |
|------------|------|---------------|----------|------------|-------|
| I088 (Capt Sharma 88) | B03 | C172 | 87 | 87 | 1.00 |
| I095 (Capt Singh 95) | B03 | C152 | 114 | 113 | 0.99 |
| I006 (Capt Verma 6) | B01 | SR20 | 101 | 100 | 0.99 |
| I097 (Capt Kapoor 97) | B04 | DA42 | 201 | 199 | 0.99 |
| I054 (Capt Singh 54) | B01 | DA40 | 159 | 156 | 0.98 |

**Skynet Action:** Instructors I003, I006, I018, I019, I027, I031, I044, I045, I048, I054, I058, I065, I067, I078, I079, I083, I088, I091, I095, I097, I098, I099 should be reviewed for duty-hour compliance. Skynet should enforce a 0.85 flight-to-duty ratio cap and alert the CFI when any instructor approaches this threshold.

---
## 3. Dispatch Reliability

**Total sorties scheduled:** 300
**Completed:** 253 (84.3%)
**Cancelled:** 47 (15.7%)
**Delayed (>0 min):** 222 of 253 completed sorties (87.7%)
**Average delay (completed sorties):** 28.2 minutes

### 3.1 Cancellation Breakdown
| Reason | Count | % of Cancellations |
|--------|-------|-------------------|
| Instructor Unavailable | 11 | 23.4% |
| ATC Restriction | 10 | 21.3% |
| Fuel Delay | 9 | 19.1% |
| Aircraft Defect | 9 | 19.1% |
| Weather | 8 | 17.0% |

### 3.2 Completion Rate by Base
| Base | Total | Completed | Cancelled | Completion% |
|------|-------|-----------|-----------|-------------|
| B01 | 83 | 67 | 16 | 80.7% |
| B02 | 70 | 63 | 7 | 90.0% |
| B03 | 94 | 79 | 15 | 84.0% |
| B04 | 53 | 44 | 9 | 83.0% |

### 3.3 Cancellation Rate by Lesson Type
| Lesson Type | Total | Cancelled | Cancel Rate% |
|-------------|-------|-----------|--------------|}
| Cross Country | 45 | 10 | 22.2% |
| Instrument Flying | 36 | 7 | 19.4% |
| Solo | 52 | 9 | 17.3% |
| Navigation | 41 | 6 | 14.6% |
| Night Flying | 41 | 6 | 14.6% |
| General Handling | 46 | 5 | 10.9% |
| Circuit | 39 | 4 | 10.3% |

### 3.4 Average Delay by Day of Week
| Day | Avg Delay (min) |
|-----|----------------|
| Monday | 31.5 |
| Tuesday | 29.7 |
| Wednesday | 29.4 |
| Sunday | 28.3 |
| Thursday | 28.1 |
| Saturday | 25.6 |
| Friday | 25.6 |

### 3.5 Average Delay by Lesson Type
| Lesson Type | Avg Delay (min) |
|-------------|----------------|
| Navigation | 36.7 |
| General Handling | 30.9 |
| Night Flying | 29.9 |
| Instrument Flying | 28.1 |
| Circuit | 27.0 |
| Cross Country | 24.4 |
| Solo | 21.3 |

---
## 4. Key Operational Insights for Skynet

1. **Weather-related cancellations** are the leading cause. Skynet should integrate MET data to flag high-risk weather days pre-scheduling.
2. **Aircraft Defect cancellations** account for significant disruption. Skynet maintenance module should proactively block aircraft with escalating defect counts.
3. **Instructor base mismatches** detected in 20 sorties — Skynet scheduling must enforce base-assignment checks before confirming bookings.
4. **Night Flying and Cross Country** sorties have the highest average delays — likely pre-flight briefing time. Skynet should add 15-min buffer to these lesson type templates.
5. **4 qualification mismatch sorties** are a regulatory red flag. Skynet must hard-block any sortie where instructor's `aircraft_qualified` ≠ the assigned aircraft type.

**Data Quality Note:** 1 sortie(s) with invalid actual_end/actual_start timestamps were detected and excluded from utilization calculations. Affected sortie IDs: S0259. These are likely data entry errors.