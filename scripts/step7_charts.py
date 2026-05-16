"""
STEP 7 — All 7 Charts
Saves PNG files at 300 DPI to charts/ directory
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

BASE   = r"c:\Users\Ayan2\OneDrive\Desktop\AIRMAN_Assessment-"
DATA   = os.path.join(BASE, "data")
CHARTS = os.path.join(BASE, "charts")
os.makedirs(CHARTS, exist_ok=True)

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
PALETTE = ['#1A3557','#2E86AB','#A23B72','#F18F01','#C73E1D','#44BBA4','#E94F37']

ac_util  = pd.read_csv(os.path.join(DATA, "ac_util.csv"))
sorties  = pd.read_csv(os.path.join(DATA, "sorties.csv"))
cadets_e = pd.read_csv(os.path.join(DATA, "cadets_enriched.csv"))
toga_e   = pd.read_csv(os.path.join(DATA, "toga_enriched.csv"))
pay_e    = pd.read_csv(os.path.join(DATA, "payments_enriched.csv"))
risk     = pd.read_csv(os.path.join(DATA, "risk_full.csv"))

# ── CHART 1: Aircraft Utilisation ────────────────────────────────────────────
print("Generating Chart 1...")
ac_valid = ac_util[~ac_util['data_error_flag']].copy()
# Show top 20 by utilization rate (descending) for executive readability
ac_plot = ac_valid.sort_values('utilization_rate', ascending=False).head(20).sort_values('utilization_rate')
colors = ['#C73E1D' if x < 40 else '#F18F01' if x <= 70 else '#44BBA4' for x in ac_plot['utilization_rate']]

fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(ac_plot['aircraft_id'], ac_plot['utilization_rate'], color=colors, height=0.7, edgecolor='white', linewidth=0.3)
ax.axvline(x=40, color='#C73E1D', linestyle='--', linewidth=1.5, label='Under-utilised threshold (40%)')
ax.axvline(x=70, color='#44BBA4', linestyle='--', linewidth=1.5, label='Optimal threshold (70%)')
for bar, val in zip(bars, ac_plot['utilization_rate']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', ha='left', fontsize=8, fontweight='bold')
ax.set_xlabel('Utilisation Rate (%)', fontsize=11, fontweight='bold')
ax.set_title('Top 20 Aircraft by Utilisation Rate\n'
             f'(Fleet avg: {ac_valid["utilization_rate"].mean():.1f}% | '
             f'3 data-error aircraft excluded: A003, A009, A016)',
             fontsize=12, fontweight='bold', pad=12)
ax.set_xlim(0, 120)
patches = [mpatches.Patch(color='#C73E1D', label='Under-utilised (<40%)'),
           mpatches.Patch(color='#F18F01', label='Optimal (40-70%)'),
           mpatches.Patch(color='#44BBA4', label='High (>70%)')]
ax.legend(handles=patches + [
    plt.Line2D([0],[0],color='#C73E1D',linestyle='--',label='40% threshold'),
    plt.Line2D([0],[0],color='#44BBA4',linestyle='--',label='70% threshold')
], loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "aircraft_utilization.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved aircraft_utilization.png")


# ── CHART 2: Cancellation Reasons ────────────────────────────────────────────
print("Generating Chart 2...")
cancelled = sorties[sorties['status']=='cancelled']
cancel_counts = cancelled['cancel_reason'].value_counts()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Sortie Cancellation Analysis\nMay–June 2026', fontsize=13, fontweight='bold')

wedge_colors = PALETTE[:len(cancel_counts)]
wedges, texts, autotexts = ax1.pie(cancel_counts.values, labels=cancel_counts.index,
    autopct='%1.1f%%', colors=wedge_colors, startangle=90,
    wedgeprops={'edgecolor':'white','linewidth':1.5})
for at in autotexts: at.set_fontsize(9)
ax1.set_title('Proportion by Reason', fontsize=11, fontweight='bold')

bars2 = ax2.bar(cancel_counts.index, cancel_counts.values, color=wedge_colors, edgecolor='white', linewidth=1.5)
ax2.set_xlabel('Cancellation Reason', fontsize=10, fontweight='bold')
ax2.set_ylabel('Number of Sorties', fontsize=10, fontweight='bold')
ax2.set_title('Count by Reason', fontsize=11, fontweight='bold')
for bar, val in zip(bars2, cancel_counts.values):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height()+0.2, str(val),
             ha='center', va='bottom', fontweight='bold', fontsize=10)
plt.setp(ax2.get_xticklabels(), rotation=30, ha='right', fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "cancellation_reasons.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved cancellation_reasons.png")

# ── CHART 3: Cadet Progress ───────────────────────────────────────────────────
print("Generating Chart 3...")
cplot = cadets_e.sort_values('progress_pct').head(60).copy()  # show top 60 for readability
fig, ax = plt.subplots(figsize=(14, 16))
y = np.arange(len(cplot))
ppl_mask = cplot['course'] == 'PPL'
ax.barh(y[ppl_mask],  cplot[ppl_mask]['total_required_hours'], height=0.7,
        color='#E8F4FD', edgecolor='#2E86AB', linewidth=1, label='PPL Required')
ax.barh(y[ppl_mask],  cplot[ppl_mask]['total_flown_hours'], height=0.7,
        color='#2E86AB', label='PPL Flown')
ax.barh(y[~ppl_mask], cplot[~ppl_mask]['total_required_hours'], height=0.7,
        color='#FDEEE0', edgecolor='#F18F01', linewidth=1, label='CPL Required')
ax.barh(y[~ppl_mask], cplot[~ppl_mask]['total_flown_hours'], height=0.7,
        color='#F18F01', label='CPL Flown')
ax.set_yticks(y)
ax.set_yticklabels([f"{r['cadet_id']} {r['name'][:12]}" for _, r in cplot.iterrows()], fontsize=6)
ax.set_xlabel('Flight Hours', fontsize=11, fontweight='bold')
ax.set_title('Cadet Flight Progress\n(Flown vs Required Hours — sorted by progress %)', fontsize=12, fontweight='bold')
ax.legend(loc='lower right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "cadet_progress.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved cadet_progress.png")

# ── CHART 4: Study Readiness ──────────────────────────────────────────────────
print("Generating Chart 4...")
tr = toga_e.merge(cadets_e[['cadet_id','name']], on='cadet_id', how='left').sort_values('study_readiness')
colors4 = ['#C73E1D' if s < 40 else '#F18F01' if s < 70 else '#44BBA4' for s in tr['study_readiness']]
fig, ax = plt.subplots(figsize=(14, 10))
ax.bar(range(len(tr)), tr['study_readiness'], color=colors4, width=0.8, edgecolor='white', linewidth=0.3)
ax.axhline(y=40, color='#C73E1D', linestyle='--', linewidth=1.5, label='Low threshold (40)')
ax.axhline(y=70, color='#44BBA4', linestyle='--', linewidth=1.5, label='High threshold (70)')
ax.set_xlabel('Cadets (sorted by score)', fontsize=11, fontweight='bold')
ax.set_ylabel('Study Readiness Score (0–100)', fontsize=11, fontweight='bold')
ax.set_title('TOGA Study Readiness Score by Cadet\n(Red <40 | Amber 40–70 | Green >70)',
             fontsize=12, fontweight='bold')
ax.set_xticks([])
patches4 = [mpatches.Patch(color='#C73E1D', label=f"Low (<40): {sum(s<40 for s in tr['study_readiness'])} cadets"),
            mpatches.Patch(color='#F18F01', label=f"Medium (40-70): {sum(40<=s<70 for s in tr['study_readiness'])} cadets"),
            mpatches.Patch(color='#44BBA4', label=f"High (>70): {sum(s>=70 for s in tr['study_readiness'])} cadets")]
ax.legend(handles=patches4, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "study_readiness.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved study_readiness.png")

# ── CHART 5: Payment Risk ─────────────────────────────────────────────────────
print("Generating Chart 5...")
pay_plot = pay_e[~pay_e['cadet_id'].isin(['C006','C023','C068','C102'])].sort_values('outstanding_amount', ascending=False).head(50)
color_map5 = {'Low':'#44BBA4','Medium':'#F18F01','High':'#C73E1D','DATA ERROR':'#888888'}
colors5 = [color_map5.get(r, '#888888') for r in pay_plot['risk_level']]
fig, ax = plt.subplots(figsize=(14, 8))
bars5 = ax.bar(range(len(pay_plot)), pay_plot['outstanding_amount']/1000, color=colors5, edgecolor='white', linewidth=0.5)
ax.set_xticks(range(len(pay_plot)))
ax.set_xticklabels(pay_plot['cadet_id'], rotation=45, ha='right', fontsize=6)
ax.set_ylabel('Outstanding Amount (₹ thousands)', fontsize=11, fontweight='bold')
ax.set_title('Top 50 Cadets by Outstanding Payment\n(Coloured by Payment Risk Level)',
             fontsize=12, fontweight='bold')
patches5 = [mpatches.Patch(color='#C73E1D', label='High Risk'),
            mpatches.Patch(color='#F18F01', label='Medium Risk'),
            mpatches.Patch(color='#44BBA4', label='Low Risk')]
ax.legend(handles=patches5, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "payment_risk.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved payment_risk.png")

# ── CHART 6: Cadet Risk Scores ────────────────────────────────────────────────
print("Generating Chart 6...")
risk_plot = risk.sort_values('risk_score', ascending=False).head(50)
color_map6 = {'Low':'#44BBA4','Medium':'#F18F01','High':'#C73E1D'}
colors6 = [color_map6.get(r,'#888') for r in risk_plot['risk_level']]
fig, ax = plt.subplots(figsize=(14, 12))
y6 = np.arange(len(risk_plot))
bars6 = ax.barh(y6, risk_plot['risk_score'], color=colors6, height=0.7, edgecolor='white', linewidth=0.5)
ax.axvline(x=40, color='#F18F01', linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvline(x=70, color='#C73E1D', linestyle='--', linewidth=1.5, alpha=0.7)
ax.set_yticks(y6)
ax.set_yticklabels([f"{r['cadet_id']} — {r['name'][:15]}" for _, r in risk_plot.iterrows()], fontsize=7)
for i, (score, level) in enumerate(zip(risk_plot['risk_score'], risk_plot['risk_level'])):
    ax.text(score + 0.5, i, f" {level}", va='center', fontsize=6, color='#333')
ax.set_xlabel('Composite Risk Score (0–100)', fontsize=11, fontweight='bold')
ax.set_title('Cadet Composite Risk Score (Top 50)\nLower is better | Weighted formula: flight + study + finance + TOGA',
             fontsize=12, fontweight='bold')
patches6 = [mpatches.Patch(color='#44BBA4', label='Low Risk (0-39)'),
            mpatches.Patch(color='#F18F01', label='Medium Risk (40-69)'),
            mpatches.Patch(color='#C73E1D', label='High Risk (70-100)')]
ax.legend(handles=patches6, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "cadet_risk_scores.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved cadet_risk_scores.png")

# ── CHART 7: Flight vs Study Scatter ─────────────────────────────────────────
print("Generating Chart 7...")
scatter_df = risk[['cadet_id','name','risk_level','flight_progress_norm','study_readiness','payment_risk_score']].copy()
scatter_df['flight_pct'] = scatter_df['flight_progress_norm'] * 100
scatter_df['payment_size'] = (scatter_df['payment_risk_score'].fillna(50) / 100 * 200 + 30)

color_map7 = {'Low':'#44BBA4','Medium':'#F18F01','High':'#C73E1D'}
colors7 = [color_map7.get(r,'#888') for r in scatter_df['risk_level']]

fig, ax = plt.subplots(figsize=(12, 9))
scatter = ax.scatter(scatter_df['flight_pct'], scatter_df['study_readiness'],
                     c=colors7, s=scatter_df['payment_size'], alpha=0.75, edgecolors='white', linewidth=0.8)
ax.axvline(x=50, color='#aaa', linestyle='--', linewidth=1)
ax.axhline(y=60, color='#aaa', linestyle='--', linewidth=1)

ax.text(75, 80, 'On Track', fontsize=10, color='#44BBA4', fontweight='bold', ha='center')
ax.text(25, 80, 'Studying but\nnot flying', fontsize=10, color='#2E86AB', fontweight='bold', ha='center')
ax.text(75, 25, 'Flying but\nnot studying', fontsize=10, color='#F18F01', fontweight='bold', ha='center')
ax.text(25, 25, 'High Risk', fontsize=10, color='#C73E1D', fontweight='bold', ha='center')

ax.set_xlabel('Flight Progress (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('TOGA Study Readiness Score', fontsize=12, fontweight='bold')
ax.set_title('Flight Progress vs Study Readiness\n(Point size = payment risk | Colour = overall risk level)',
             fontsize=13, fontweight='bold')
ax.set_xlim(-5, 105)
ax.set_ylim(-5, 105)
patches7 = [mpatches.Patch(color='#44BBA4', label='Low Risk'),
            mpatches.Patch(color='#F18F01', label='Medium Risk'),
            mpatches.Patch(color='#C73E1D', label='High Risk')]
ax.legend(handles=patches7, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "flight_vs_study_progress.png"), dpi=300, bbox_inches='tight')
plt.close()
print("  Saved flight_vs_study_progress.png")

print("\nAll 7 charts generated successfully!")
