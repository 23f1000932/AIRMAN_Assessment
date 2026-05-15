# AIRMAN Dataset — Planted Data Quality Issues
## (For your reference during the assessment — do NOT submit this file)

### 1. Payment Calculation Errors (4 rows)
`outstanding_amount ≠ invoiced_amount − paid_amount`
- C006, C023, C068, C102

### 2. Instructor Base Mismatches (20 sorties)
Instructor's `base_id` in instructors.csv ≠ `base_id` in the sortie.
Look for sorties where an instructor is operating far from their home base.

### 3. Qualification Mismatches (4 sorties)
Instructor's `aircraft_qualified` type ≠ the aircraft `type` used in sortie:
- S0044 → Capt (DA40-qualified) flew a C152
- S0107 → Capt (DA40-qualified) flew a DA42
- S0184 → Capt (SR20-qualified) flew a C172
- S0263 → Capt (C172-qualified) flew a C152

### 4. Aircraft Maintenance > Available Hours (3 aircraft)
- A003: available=126, maintenance=146
- A009: available=197, maintenance=220
- A016: available=183, maintenance=192

### 5. TOGA Impossible Study Progress (2 rows)
`chapters_completed > total_chapters`
- C005 / Radio Telephony: 27 completed out of 24 total
- C030 / Radio Telephony: 37 completed out of 36 total

### 6. Duplicate Cadet Names (3 pairs)
Same name, different cadet_id — possible data entry errors or duplicate records:
- "Sanya Gupta" (2 cadets)
- "Vikram Malhotra" (2 cadets)  — NOTE: there may be 3+ with this name
- "Rahul Patel" (2 cadets)

### 7. High Defect Count Aircraft
Aircraft with defect_count ≥ 12 should be flagged for operational review:
Check aircraft.csv for aircraft with very high defect counts.
