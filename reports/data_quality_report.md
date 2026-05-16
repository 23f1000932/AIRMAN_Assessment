# Data Quality Report — AIRMAN FTO Intelligence
*Analysis Date: 2026-05-15 | Total Checks Run: 16*

## Summary Table

| # | Issue | Severity | Count | Affected IDs | Recommended Action |
|---|-------|----------|-------|-------------|-------------------|
| 1 | Missing values in sorties | Medium | 347 | {'actual_start': 47, 'actual_end': 47, 'cancel_reason': 253} | Investigate source system for null handling |
| 2 | Duplicate cadet name: 'Rahul Patel' | High | 3 | ['C051', 'C127', 'C149'] | Manual verification — possible data entry duplicate |
| 3 | Duplicate cadet name: 'Sanya Gupta' | High | 3 | ['C002', 'C011', 'C096'] | Manual verification — possible data entry duplicate |
| 4 | Duplicate cadet name: 'Vikram Malhotra' | High | 4 | ['C004', 'C036', 'C114', 'C121'] | Manual verification — possible data entry duplicate |
| 5 | Invalid sortie status | High | 0 | None | Fix status to completed/cancelled |
| 6 | Completed sortie missing actual times | High | 0 | None | Backfill from flight logs or investigate data pipeline |
| 7 | Cancelled sortie has actual times | Medium | 0 | None | Clear actual times for cancelled sorties |
| 8 | delay_minutes mismatch vs actual times | Low | 0 | None | Recompute delay_minutes from actual_start - scheduled_start |
| 9 | Payment calculation error (outstanding ≠ invoiced − paid) | High | 4 | ['C006', 'C023', 'C068', 'C102'] | Manual finance team review required before risk scoring |
| 10 | TOGA: chapters_completed > total_chapters | High | 2 | ['C005/Radio Telephony', 'C030/Radio Telephony'] | Cap at total_chapters; flag for content team review |
| 11 | Aircraft maintenance hours exceed available hours | High | 3 | ['A003', 'A009', 'A016'] | Immediate engineering review; data entry error likely |
| 12 | Cadet flown hours exceed required hours | Medium | 0 | None | Review completion/graduation status |
| 13 | Quiz score outside 0-100 range | High | 0 | None | Investigate quiz scoring system |
| 14 | Instructor base ≠ sortie base | Medium | 20 | ['S0015', 'S0024', 'S0027', 'S0046', 'S0095', 'S0097', 'S0108', 'S0134', 'S0138' | Investigate cross-base deployments; update Skynet scheduling rules |
| 15 | Instructor type qualification mismatch | High | 4 | ['S0044', 'S0107', 'S0184', 'S0263'] | CRITICAL: Safety review. Instructors may have flown unqualified aircraft |
| 16 | Negative numeric values | Medium | 0 | None | Investigate data entry; negative values not valid here |
| 17 | High defect count aircraft (≥10 defects) | High | 35 | ['A002', 'A010', 'A012', 'A018', 'A022', 'A023', 'A027', 'A028', 'A029', 'A031', | Operational review; consider AOG or increased inspection interval |
| 18 | Sortie with negative actual duration | High | 1 | ['S0259'] | Excluded from utilization calculation; data entry error likely — actual_end < actual_start |

---
## Detailed Findings

### 1. Payment Calculation Errors (CRITICAL — Finance Team Action Required)
The following 4 cadets have `outstanding_amount ≠ invoiced_amount − paid_amount`.
**These cadets must be excluded from automated payment risk scoring until manually verified.**

- C006: outstanding = 461,290 | expected = 451,790
- C023: outstanding = 181,032 | expected = 188,232
- C068: outstanding = 144,227 | expected = 131,227
- C102: outstanding = 215,544 | expected = 220,344

### 2. Safety-Critical: Instructor Qualification Mismatches
4 sorties where instructor's qualified aircraft type ≠ aircraft actually flown:
- **S0044**: Instructor I052 (DA40-qualified) flew a C152 (A005)
- **S0107**: Instructor I017 (DA40-qualified) flew a DA42 (A011)
- **S0184**: Instructor I084 (SR20-qualified) flew a C172 (A004)
- **S0263**: Instructor I088 (C172-qualified) flew a C152 (A001)
> ⚠️ Regulatory compliance risk — DGCA mandates type-specific instructor certification.

### 3. Aircraft Maintenance Data Anomalies
3 aircraft where maintenance_downtime_hours > total_available_hours (physically impossible):
- **A003** (VT-AIR003, DA40): 146 downtime hrs vs 126 available hrs
- **A009** (VT-EAG009, SR20): 220 downtime hrs vs 197 available hrs
- **A016** (VT-EAG016, C152): 192 downtime hrs vs 183 available hrs

### 4. TOGA Study Progress Anomalies
2 records where chapters_completed > total_chapters:
- **C005 / Radio Telephony**: 27 completed out of 24 total
- **C030 / Radio Telephony**: 37 completed out of 36 total

### 5. Duplicate Cadet Names (Data Entry Risk)
3 name pairs found with different cadet_ids:
- 'Sanya Gupta': C002 (CPL/B04), C011 (CPL/B02), C096 (PPL/B02)
- 'Vikram Malhotra': C004 (PPL/B02), C036 (PPL/B03), C114 (CPL/B03), C121 (CPL/B02)
- 'Rahul Patel': C051 (PPL/B03), C127 (CPL/B03), C149 (PPL/B01)

### 6. Cross-Base Instructor Deployments
20 sorties where instructor's home base ≠ sortie operating base.
This may indicate ad-hoc cross-base scheduling not captured in Skynet. Recommend adding a
'temporary_deployment' flag to the scheduling system.

### 7. High-Defect Aircraft
35 aircraft with defect_count ≥ 10: A002, A010, A012, A018, A022, A023, A027, A028, A029, A031, A039, A040, A041, A045, A048, A049, A050, A052, A066, A067, A070, A071, A073, A080, A083, A087, A088, A089, A092, A098, A103, A105, A114, A116, A120
These should be placed under enhanced maintenance monitoring in Skynet.

---
### 8. Negative Sortie Duration (Data Entry Error — CRITICAL for Utilization)
1 sortie where `actual_end < actual_start` (negative computed duration):
- **S0259** (aircraft A032, DA42, base B03): actual_end is earlier than actual_start — physically impossible.
  This sortie caused A032 to show **-716.5 flown hours** and **-389.4% utilization rate** in initial calculations.
> ⚠️ This is almost certainly a data entry error (timestamps swapped or entered incorrectly).
> Action: Sortie S0259 has been **excluded** from aircraft utilization calculations. A032's true flown hours are now 0.0 (no valid completed sorties after exclusion). Source system should be audited to correct the timestamp pair.

---
*Report generated by AIRMAN Data Science Assessment pipeline*