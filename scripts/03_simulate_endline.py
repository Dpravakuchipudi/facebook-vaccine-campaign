# ----------------------------------------
# 03_simulate_endline.py
# Step 3: Simulate Endline Survey Data
# ----------------------------------------

import pandas as pd
import numpy as np
import os

# ----------------------------------------
# Setup
# ----------------------------------------

# Ensure the 'data/' folder exists
os.makedirs("data", exist_ok=True)

# Set seed for reproducibility
np.random.seed(42)

# ----------------------------------------
# Load Assigned Groups from Previous Step
# ----------------------------------------

assignment_df = pd.read_csv("data/assignment_data.csv")
assignment_df["participant_id"] = assignment_df["participant_id"].str.strip()

# ----------------------------------------
# Simulate Survey Dropout
# ----------------------------------------

# Only 4,500 out of 5,000 participants respond to the endline survey
respondents = assignment_df.sample(n=4500, random_state=42).copy()

# ----------------------------------------
# Simulate Vaccine Uptake by Ad Group
# ----------------------------------------

def simulate_vaccine_uptake(group: str) -> int:
    """
    Simulates vaccine uptake using group-specific probabilities.
    """
    uptake_probs = {
        'Control': 0.50,
        'Ad_Reason': 0.58,
        'Ad_Emotion': 0.67
    }
    return np.random.binomial(1, uptake_probs[group])

respondents["vaccine_uptake"] = respondents["ad_group"].apply(simulate_vaccine_uptake)

# ----------------------------------------
# Simulate Post-Campaign Attitude Score
# ----------------------------------------

def simulate_post_attitude(group: str) -> int:
    """
    Simulates post-campaign attitude scores using group-specific means.
    Returns integer values on a 1–5 Likert scale.
    """
    mean_scores = {
        'Control': 3.0,
        'Ad_Reason': 3.3,
        'Ad_Emotion': 3.6
    }
    score = np.random.normal(loc=mean_scores[group], scale=1.0)
    return int(round(np.clip(score, 1, 5)))

respondents["post_attitude_score"] = respondents["ad_group"].apply(simulate_post_attitude)

# ----------------------------------------
# Save Simulated Endline Data
# ----------------------------------------

endline_df = respondents[["participant_id", "vaccine_uptake", "post_attitude_score"]]
endline_df.to_csv("data/endline_data.csv", index=False)

print("✅ Endline data simulated and saved to data/endline_data.csv")
