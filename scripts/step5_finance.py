"""
STEP 5 — Finance & Operational Risk
Payment risk scores, outstanding amounts, finance report
"""
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA = os.path.join(BASE, "data")
REPORTS = os.path.join(BASE, "reports")
REF_DATE = pd.Timestamp('2026-05-15')

cadets   = pd.read_csv(os.path.join(DATA, "cadets.csv"))
payments = pd.read_csv(os.path.join(DATA, "payments.csv"))
payments['last_payment_date'] = pd.to_datetime(payments['last_payment_date'])

# ── FLAG DATA ERRORS FIRST ────────────────────────────────────────────────────
payments['expected_outstanding'] = payments['invoiced_amount'] - payments['paid_amount']
payments['calc_error'] = payments['outstanding_amount'] != payments['expected_outstanding']
error_cadets = {'C006','C023','C068','C102'}

# ── PAYMENT METRICS ───────────────────────────────────────────────────────────
payments['payment_completion_pct'] = (payments['paid_amount'] / payments['invoiced_amount'] * 100).round(2)
payments['outstanding_ratio']      = (payments['outstanding_amount'] / payments['invoiced_amount']).round(4)
payments['days_since_payment']     = (REF_DATE - payments['last_payment_date']).dt.days

# ── PAYMENT RISK SCORE (skip error cadets for accurate scoring) ───────────────
def payment_risk(row):
    score = (
        0.50 * row['outstanding_ratio'] * 100 +
        0.30 * min(row['days_since_payment'] / 60, 1.0) * 100 +
        0.20 * (1 - row['payment_completion_pct'] / 100) * 100
    )
    return round(score, 2)

payments['payment_risk_score'] = payments.apply(payment_risk, axis=1)
payments.loc[payments['cadet_id'].isin(error_cadets), 'payment_risk_score'] = np.nan  # exclude errors

def risk_level(score):
    if pd.isna(score): return "DATA ERROR"
    if score < 40:    return "Low"
    if score < 70:    return "Medium"
    return "High"

payments['risk_level'] = payments['payment_risk_score'].apply(risk_level)

def risk_reason(row):
    if row['cadet_id'] in error_cadets: return "Data integrity error — manual review required"
    reasons = []
    if row['outstanding_ratio'] > 0.7:   reasons.append(f"High outstanding ratio {row['outstanding_ratio']:.0%}")
    if row['days_since_payment'] > 45:   reasons.append(f"{row['days_since_payment']}d since last payment")
    if row['payment_completion_pct'] < 40: reasons.append(f"Only {row['payment_completion_pct']:.0f}% fees paid")
    return "; ".join(reasons) if reasons else "Within acceptable range"

payments['reason'] = payments.apply(risk_reason, axis=1)

# Merge cadet names
payments = payments.merge(cadets[['cadet_id','name','course']], on='cadet_id', how='left')

# ── TOTALS ────────────────────────────────────────────────────────────────────
total_invoiced    = payments['invoiced_amount'].sum()
total_paid        = payments['paid_amount'].sum()
total_outstanding = payments['outstanding_amount'].sum()
collection_rate   = total_paid / total_invoiced * 100

high_risk = payments[payments['risk_level'] == 'High']
medium_risk = payments[payments['risk_level'] == 'Medium']

# ── WRITE REPORT ──────────────────────────────────────────────────────────────
lines = [
    "# Finance & Operational Risk Report",
    f"*Reference Date: {REF_DATE.date()} | Analysis Period: May–June 2026*\n",
    "---\n## 1. Portfolio Summary\n",
    f"| Metric | Value |",
    f"|--------|-------|",
    f"| Total Invoiced | ₹{total_invoiced:,.0f} |",
    f"| Total Paid | ₹{total_paid:,.0f} |",
    f"| Total Outstanding | ₹{total_outstanding:,.0f} |",
    f"| Collection Rate | {collection_rate:.1f}% |",
    f"| High Risk Cadets | {len(high_risk)} |",
    f"| Medium Risk Cadets | {len(medium_risk)} |",
    f"| Cadets with Data Errors | 4 (C006, C023, C068, C102) |\n",
    "---\n## 2. Data Integrity Alerts — Manual Review Required\n",
    "> **WARNING:** The following 4 cadets have outstanding_amount ≠ invoiced_amount − paid_amount.",
    "> These records have been EXCLUDED from automated risk scoring until finance team verification.\n",
    "| Cadet ID | Name | Invoiced | Paid | Recorded Outstanding | Correct Outstanding | Difference |",
    "|----------|------|---------|------|---------------------|--------------------| -----------|",
]
for cid in ['C006','C023','C068','C102']:
    row = payments[payments['cadet_id']==cid].iloc[0]
    diff = row['outstanding_amount'] - row['expected_outstanding']
    lines.append(f"| {cid} | {row['name']} | ₹{row['invoiced_amount']:,.0f} | ₹{row['paid_amount']:,.0f} | "
                 f"₹{row['outstanding_amount']:,.0f} | ₹{row['expected_outstanding']:,.0f} | ₹{diff:,.0f} |")

lines += [
    "\n---\n## 3. Payment Risk Table (All Cadets)\n",
    "| cadet_id | Name | Course | Outstanding (₹) | Payment Completion% | Days Since Payment | Risk Score | Risk Level | Reason |",
    "|----------|------|--------|----------------|--------------------|--------------------|------------|------------|--------|",
]
for _, row in payments.sort_values('payment_risk_score', ascending=False, na_position='last').iterrows():
    score_str = f"{row['payment_risk_score']:.1f}" if not pd.isna(row['payment_risk_score']) else "N/A"
    lines.append(
        f"| {row['cadet_id']} | {row['name']} | {row['course']} | "
        f"₹{row['outstanding_amount']:,.0f} | {row['payment_completion_pct']:.1f}% | "
        f"{int(row['days_since_payment'])} | {score_str} | {row['risk_level']} | {row['reason']} |"
    )

lines += [
    "\n---\n## 4. High Risk Cadets — Immediate Action Required\n",
]
for _, row in high_risk.sort_values('payment_risk_score', ascending=False).head(10).iterrows():
    lines.append(f"- **{row['cadet_id']} — {row['name']} ({row['course']}):** "
                 f"₹{row['outstanding_amount']:,.0f} outstanding | Risk Score: {row['payment_risk_score']:.1f} | "
                 f"{row['reason']}")

lines += [
    "\n---\n## 5. Recommendations\n",
    "1. **Immediate collections action** on all High Risk cadets — training continuity at risk if fees remain unpaid.",
    "2. **Finance team manual review** of C006, C023, C068, C102 — correct outstanding amounts in Skynet before next billing cycle.",
    "3. **Skynet billing module** should auto-compute outstanding as invoiced − paid and flag discrepancies at record save time.",
    f"4. **Revenue at risk:** ₹{high_risk['outstanding_amount'].sum():,.0f} across {len(high_risk)} high-risk cadets.",
    "5. **Payment plan option:** Offer structured EMI plan to medium-risk cadets to prevent them escalating to high risk.",
]

with open(os.path.join(REPORTS, "finance_risk_analysis.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# Save for downstream
payments.to_csv(os.path.join(DATA, "payments_enriched.csv"), index=False)
print("DONE: finance_risk_analysis.md")
print(f"Total outstanding: INR {total_outstanding:,.0f}")
print(f"Collection rate: {collection_rate:.1f}%")
print(f"High risk: {len(high_risk)} | Medium: {len(medium_risk)}")
