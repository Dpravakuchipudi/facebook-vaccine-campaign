# ----------------------------------------
# 02_assign_ad_groups.py
# Step 2: Randomly Assign Ad Groups to Participants
# ----------------------------------------

import pandas as pd
import numpy as np
import os

# ----------------------------------------
# Setup
# ----------------------------------------

# Ensure the 'data/' directory exists
os.makedirs("data", exist_ok=True)

# Set seed for reproducibility
np.random.seed(42)

# ----------------------------------------
# Load Baseline Participant Data
# ----------------------------------------

# Load the baseline data generated in step 1
baseline_df = pd.read_csv("data/baseline_data.csv")

# Ensure clean participant IDs (no whitespace)
baseline_df["participant_id"] = baseline_df["participant_id"].str.strip()

# ----------------------------------------
# Random Assignment to Experimental Groups
# ----------------------------------------

# Define 3 groups: reasoning-based ad, emotional ad, and no ad (control)
ad_groups = ['Ad_Reason', 'Ad_Emotion', 'Control']

# Randomly assign each participant to one group (equal probability)
assigned_groups = np.random.choice(ad_groups, size=len(baseline_df), replace=True)

# ----------------------------------------
# Build Assignment DataFrame
# ----------------------------------------

assignment_df = pd.DataFrame({
    'participant_id': baseline_df['participant_id'],
    'ad_group': assigned_groups
})

# ----------------------------------------
# Save Assigned Groups to File
# ----------------------------------------

assignment_df.to_csv("data/assignment_data.csv", index=False)
print("✅ Ad group assignment complete. Saved to data/assignment_data.csv")
