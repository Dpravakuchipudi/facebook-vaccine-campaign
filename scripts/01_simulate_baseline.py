# ----------------------------------------
# 01_simulate_baseline.py
# Step 1: Simulate Baseline Survey Data
# ----------------------------------------

import pandas as pd
import numpy as np
import os

# ----------------------------------------
# Setup
# ----------------------------------------

# Create 'data/' folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Total number of participants to simulate
N_PARTICIPANTS = 5000
participant_ids = [f"P{i:05d}" for i in range(1, N_PARTICIPANTS + 1)]

# ----------------------------------------
# Simulate Demographic Attributes
# ----------------------------------------

age = np.clip(
    np.random.normal(loc=40, scale=12, size=N_PARTICIPANTS).astype(int),
    18, 85  # constrain age between 18 and 85
)

gender = np.random.choice(
    ['Male', 'Female', 'Other'],
    p=[0.48, 0.50, 0.02],
    size=N_PARTICIPANTS
)

race_ethnicity = np.random.choice(
    ['White', 'Black', 'Asian', 'Hispanic', 'Other'],
    p=[0.60, 0.13, 0.06, 0.18, 0.03],
    size=N_PARTICIPANTS
)

education_level = np.random.choice(
    ['High School', 'Bachelor', 'Master', 'PhD', 'Not Applicable'],
    p=[0.38, 0.33, 0.18, 0.05, 0.06],
    size=N_PARTICIPANTS
)

political_affiliation = np.random.choice(
    ['Liberal', 'Moderate', 'Conservative'],
    p=[0.4, 0.3, 0.3],
    size=N_PARTICIPANTS
)

# ----------------------------------------
# Simulate Baseline Attitudes & Engagement
# ----------------------------------------

vaccine_hesitancy = np.random.randint(1, 6, size=N_PARTICIPANTS)
trust_in_science = np.random.randint(1, 6, size=N_PARTICIPANTS)
trust_in_government = np.random.randint(1, 6, size=N_PARTICIPANTS)

# Engagement score: normally distributed, clipped to 1-5
ad_engagement_score = np.clip(
    np.round(np.random.normal(loc=3.0, scale=1.0, size=N_PARTICIPANTS), 1),
    1.0, 5.0
)

# Used later to calculate change in attitude post-campaign
baseline_attitude_score = np.random.randint(1, 6, size=N_PARTICIPANTS)

# ----------------------------------------
# Create DataFrame
# ----------------------------------------

baseline_df = pd.DataFrame({
    'participant_id': participant_ids,
    'age': age,
    'gender': gender,
    'race_ethnicity': race_ethnicity,
    'education_level': education_level,
    'political_affiliation': political_affiliation,
    'vaccine_hesitancy': vaccine_hesitancy,
    'trust_in_science': trust_in_science,
    'trust_in_government': trust_in_government,
    'ad_engagement_score': ad_engagement_score,
    'baseline_attitude_score': baseline_attitude_score
})

# ----------------------------------------
# Save to CSV
# ----------------------------------------

baseline_df.to_csv("data/baseline_data.csv", index=False)
print("✅ Baseline data generated and saved to data/baseline_data.csv")
