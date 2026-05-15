"""
STEP 6 — Explainable Cadet Risk Score
Builds risk_scores.csv using transparent weighted formula — NO ML
"""
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

BASE = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA = os.path.join(BASE, "data")
REF_DATE = pd.Timestamp('2026-05-15')

cadets   = pd.read_csv(os.path.join(DATA, "cadets_enriched.csv"))
toga_e   = pd.read_csv(os.path.join(DATA, "toga_enriched.csv"))
pay_e    = pd.read_csv(os.path.join(DATA, "payments_enriched.csv"))
sorties  = pd.read_csv(os.path.join(DATA, "sorties.csv"))

# ── ASSEMBLE FEATURES ─────────────────────────────────────────────────────────
df = cadets[['cadet_id','name','course','progress_pct','cancel_rate']].copy()

# Study readiness
df = df.merge(toga_e[['cadet_id','study_readiness','mean_quiz','days_since_active']], on='cadet_id', how='left')

# Payment risk
df = df.merge(pay_e[['cadet_id','payment_risk_score','risk_level']], on='cadet_id', how='left')

# Fill missing
df['study_readiness']    = df['study_readiness'].fillna(50)
df['mean_quiz']          = df['mean_quiz'].fillna(50)
df['days_since_active']  = df['days_since_active'].fillna(30)
df['payment_risk_score'] = df['payment_risk_score'].fillna(50)  # neutral for error cadets
df['cancel_rate']        = df['cancel_rate'].fillna(0)

# ── FORMULA ───────────────────────────────────────────────────────────────────
# All components normalized 0-1, then weighted
df['flight_progress_norm'] = (df['progress_pct'] / 100).clip(0, 1)
df['study_readiness_norm'] = (df['study_readiness'] / 100).clip(0, 1)
df['quiz_norm']            = (df['mean_quiz'] / 100).clip(0, 1)
df['payment_risk_norm']    = (df['payment_risk_score'] / 100).clip(0, 1)
df['inactivity_score']     = (df['days_since_active'] / 30).clip(0, 1)
df['cancel_rate_norm']     = df['cancel_rate'].clip(0, 1)

df['risk_score'] = (
    0.25 * (1 - df['flight_progress_norm'])   +
    0.20 * (1 - df['study_readiness_norm'])   +
    0.15 * (1 - df['quiz_norm'])              +
    0.15 * df['payment_risk_norm']            +
    0.15 * df['inactivity_score']             +
    0.10 * df['cancel_rate_norm']
) * 100
df['risk_score'] = df['risk_score'].round(2)

def risk_level(s):
    if s < 40:  return "Low"
    if s < 70:  return "Medium"
    return "High"
df['risk_level'] = df['risk_score'].apply(risk_level)

# ── MAIN RISK REASON ──────────────────────────────────────────────────────────
def main_reason(row):
    components = {
        'Low flight progress':  0.25 * (1 - row['flight_progress_norm']),
        'Low study readiness':  0.20 * (1 - row['study_readiness_norm']),
        'Low quiz scores':      0.15 * (1 - row['quiz_norm']),
        'Payment risk':         0.15 * row['payment_risk_norm'],
        'TOGA inactivity':      0.15 * row['inactivity_score'],
        'Sortie cancellations': 0.10 * row['cancel_rate_norm'],
    }
    top2 = sorted(components, key=components.get, reverse=True)[:2]
    return " + ".join(top2)

df['main_risk_reason'] = df.apply(main_reason, axis=1)

# ── SAVE ──────────────────────────────────────────────────────────────────────
out_cols = ['cadet_id','name','course','risk_score','risk_level',
            'flight_progress_norm','study_readiness','mean_quiz',
            'payment_risk_score','days_since_active','cancel_rate','main_risk_reason']
df[out_cols].rename(columns={
    'flight_progress_norm': 'flight_progress',
    'mean_quiz': 'avg_quiz_score',
    'days_since_active': 'days_inactive',
}).to_csv(os.path.join(DATA, "risk_scores.csv"), index=False)

print("DONE: risk_scores.csv saved")
print(f"Risk distribution: Low={( df.risk_level=='Low').sum()} | Medium={(df.risk_level=='Medium').sum()} | High={(df.risk_level=='High').sum()}")
print(f"\nTop 10 highest risk cadets:")
for _, r in df.nlargest(10,'risk_score').iterrows():
    print(f"  {r['cadet_id']} {r['name']:30s} Score={r['risk_score']:.1f} [{r['risk_level']}] — {r['main_risk_reason']}")

# Also save full enriched df for charts
df.to_csv(os.path.join(DATA, "risk_full.csv"), index=False)
