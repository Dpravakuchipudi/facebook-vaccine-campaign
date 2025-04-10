# ----------------------------------------
# 04_analyze_effectiveness.py
# Analyze Facebook Ad Campaign Effectiveness
# ----------------------------------------

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.formula.api as smf
import numpy as np
import os

# ----------------------------------------
# Setup & Constants
# ----------------------------------------

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Exposure probability settings per group
EXPOSURE_RATES = {
    "Ad_Emotion": 0.7,
    "Ad_Reason": 0.65,
    "Control": 0.0
}

# Set style
sns.set(style="whitegrid")
np.random.seed(42)

# ----------------------------------------
# Load and Merge Data
# ----------------------------------------

try:
    baseline = pd.read_csv("data/baseline_data.csv")
    assignment = pd.read_csv("data/assignment_data.csv")
    endline = pd.read_csv("data/endline_data.csv")
except FileNotFoundError as e:
    print(f"❌ Missing file: {e}")
    exit(1)

# Clean IDs
# Clean IDs
for df in [baseline, assignment, endline]:
    df["participant_id"] = df["participant_id"].astype(str).str.strip()

# Merge all data
merged = baseline.merge(assignment, on="participant_id").merge(endline, on="participant_id")

# Rename the correct ad_group column from assignment_data
merged = merged.rename(columns={"ad_group_x": "ad_group"})

# Save merged data
merged.to_csv("outputs/merged_full_data.csv", index=False)


# ----------------------------------------
# Simulate Campaign Exposure (Reach)
# ----------------------------------------

merged["ad_exposed"] = merged["ad_group"].apply(lambda g: np.random.binomial(1, EXPOSURE_RATES[g]))

# ----------------------------------------
# ITT & TOT Summary
# ----------------------------------------

# ITT: everyone assigned
summary_itt = merged.groupby("ad_group")["vaccine_uptake"].agg(["count", "sum", "mean"]).reset_index()
summary_itt.columns = ["ad_group", "total", "vaccinated", "vaccination_rate"]
summary_itt["type"] = "ITT"
summary_itt.to_csv("outputs/vaccination_summary_itt.csv", index=False)

# TOT: only exposed participants
tot_df = merged[merged["ad_exposed"] == 1]
summary_tot = tot_df.groupby("ad_group")["vaccine_uptake"].agg(["count", "sum", "mean"]).reset_index()
summary_tot.columns = ["ad_group", "exposed_total", "vaccinated", "vaccination_rate"]
summary_tot["type"] = "TOT"
summary_tot.to_csv("outputs/vaccination_summary_tot.csv", index=False)

# Combine for plotting
compare_df = pd.concat([
    summary_itt[["ad_group", "vaccination_rate", "type"]],
    summary_tot[["ad_group", "vaccination_rate", "type"]]
])

# Plot ITT vs TOT comparison
plt.figure(figsize=(8, 5))
sns.barplot(data=compare_df, x="ad_group", y="vaccination_rate", hue="type", palette="Set2")
plt.title("Intention-to-Treat vs Treatment-on-the-Treated")
plt.ylabel("Vaccination Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("outputs/itt_vs_tot_comparison.png")
plt.close()

print("\n✅ ITT and TOT analysis complete.")

# ----------------------------------------
# Vaccine Uptake Summary Table (General)
# ----------------------------------------

summary = merged.groupby("ad_group")["vaccine_uptake"].agg(["count", "sum", "mean"]).reset_index()
summary.columns = ["ad_group", "total", "vaccinated", "vaccination_rate"]
summary.to_csv("outputs/vaccination_summary.csv", index=False)

print("\n📊 Vaccination Rates by Ad Group:")
print(summary)

# Plot vaccine uptake
plt.figure(figsize=(8, 5))
sns.barplot(data=summary, x="ad_group", y="vaccination_rate", palette="Set3")
plt.title("Vaccine Uptake by Ad Group")
plt.ylabel("Vaccination Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("outputs/vaccine_uptake_by_ad_group.png")
plt.close()

# ----------------------------------------
# Attitude Change Analysis
# ----------------------------------------

attitude_summary = None

if "baseline_attitude_score" in merged.columns and "post_attitude_score" in merged.columns:
    merged["attitude_change"] = merged["post_attitude_score"] - merged["baseline_attitude_score"]

    attitude_summary = merged.groupby("ad_group")["attitude_change"].mean().reset_index()
    attitude_summary.columns = ["ad_group", "avg_attitude_change"]
    print("\n📊 Average Attitude Change by Ad Group:")
    print(attitude_summary)
    attitude_summary.to_csv("outputs/attitude_change_summary.csv", index=False)

    # Boxplot
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=merged, x="ad_group", y="attitude_change", palette="coolwarm")
    plt.title("Attitude Change by Ad Group")
    plt.ylabel("Post - Baseline Attitude Score")
    plt.tight_layout()
    plt.savefig("outputs/attitude_change_by_group.png")
    plt.close()
else:
    print("\n⚠️ Skipping attitude change analysis — columns missing.")

# ----------------------------------------
# Chi-Square Test
# ----------------------------------------

contingency = pd.crosstab(merged["ad_group"], merged["vaccine_uptake"])
chi2, p, dof, _ = stats.chi2_contingency(contingency)
print("\n📊 Chi-Square Test Results:")
print(f"Chi2 = {chi2:.2f}, p-value = {p:.4f}, dof = {dof}")

# Save chi-square result
with open("outputs/chi_square_results.txt", "w") as f:
    f.write(f"Chi2 = {chi2:.2f}, p = {p:.4f}, dof = {dof}\n")

# ----------------------------------------
# Hesitancy vs. Uptake Plot
# ----------------------------------------

merged["hesitancy_group"] = pd.cut(merged["vaccine_hesitancy"], bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], labels=["1", "2", "3", "4", "5"])
hesitancy_summary = merged.groupby(["ad_group", "hesitancy_group"])["vaccine_uptake"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.lineplot(data=hesitancy_summary, x="hesitancy_group", y="vaccine_uptake", hue="ad_group", marker="o")
plt.title("Uptake by Hesitancy Score and Ad Group")
plt.xlabel("Hesitancy Score")
plt.ylabel("Vaccination Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("outputs/uptake_by_hesitancy_adgroup.png")
plt.close()

# ----------------------------------------
# Trust in Science vs Uptake Boxplot
# ----------------------------------------

plt.figure(figsize=(6, 4))
sns.boxplot(data=merged, x="vaccine_uptake", y="trust_in_science")
plt.title("Trust in Science vs Vaccine Uptake")
plt.xlabel("Vaccine Uptake (0 = No, 1 = Yes)")
plt.ylabel("Trust in Science")
plt.tight_layout()
plt.savefig("outputs/trust_vs_uptake_boxplot.png")
plt.close()

# ----------------------------------------
# Political Affiliation Stacked Bar
# ----------------------------------------

political_uptake = pd.crosstab(merged["political_affiliation"], merged["vaccine_uptake"], normalize='index')
political_uptake.plot(kind='bar', stacked=True, color=["salmon", "skyblue"], figsize=(7, 5))
plt.title("Vaccine Uptake by Political Affiliation")
plt.ylabel("Proportion")
plt.xlabel("Political Affiliation")
plt.legend(["Did Not Vaccinate", "Vaccinated"])
plt.tight_layout()
plt.savefig("outputs/uptake_by_political_affiliation.png")
plt.close()

# ----------------------------------------
# Logistic Regression
# ----------------------------------------

print("\n Logistic Regression: Ad Group + Hesitancy + Trust in Science")
logit_model = smf.logit("vaccine_uptake ~ C(ad_group) + vaccine_hesitancy + trust_in_science", data=merged).fit()
print(logit_model.summary())
pseudo_r2 = 1 - logit_model.llf / logit_model.llnull
print(f"Pseudo R²: {pseudo_r2:.4f}")

with open("outputs/logistic_summary.txt", "w") as f:
    f.write(logit_model.summary().as_text())
    f.write(f"\n\nPseudo R²: {pseudo_r2:.4f}")

# ----------------------------------------
# Summary Report
# ----------------------------------------

with open("outputs/summary_report.txt", "w") as f:
    f.write("=== Vaccination Summary ===\n")
    f.write(summary.to_string(index=False))
    f.write("\n\n=== Attitude Change Summary ===\n")
    if attitude_summary is not None:
        f.write(attitude_summary.to_string(index=False))
    else:
        f.write("Skipped — baseline or post-campaign scores missing.\n")
    f.write(f"\n\n=== Chi-Square Test ===\nChi2 = {chi2:.2f}, p = {p:.4f}, dof = {dof}\n")
    f.write(f"\n\n=== Logistic Regression Pseudo R² ===\nPseudo R² = {pseudo_r2:.4f}\n")

# ----------------------------------------
# Combined Summary Visualization (2x2)
# ----------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Effectiveness of Facebook Ads on Vaccine Uptake", fontsize=16)

# Bar
sns.barplot(ax=axes[0, 0], data=summary, x="ad_group", y="vaccination_rate", palette="Set3")
axes[0, 0].set_title("Vaccination Rate by Ad Group")
axes[0, 0].set_ylim(0, 1)

# Line
sns.lineplot(ax=axes[0, 1], data=hesitancy_summary, x="hesitancy_group", y="vaccine_uptake", hue="ad_group", marker="o")
axes[0, 1].set_title("Uptake by Hesitancy Score")
axes[0, 1].set_ylim(0, 1)

# Box
sns.boxplot(ax=axes[1, 0], data=merged, x="vaccine_uptake", y="trust_in_science")
axes[1, 0].set_title("Trust in Science vs Uptake")

# Stacked Bar
political_uptake.plot(kind="bar", stacked=True, ax=axes[1, 1], color=["salmon", "skyblue"], legend=False)
axes[1, 1].set_title("Uptake by Political Affiliation")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("outputs/summary_visuals_combined.png")
plt.show()

print("\n✅ All analysis complete. Check the 'outputs/' folder.")
