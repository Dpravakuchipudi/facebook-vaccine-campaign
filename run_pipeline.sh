#!/bin/bash

set -e  # Exit the script if any command fails

echo "🚀 Starting Facebook Vaccine Campaign Simulation Pipeline..."
echo ""

# Optional: Show Python version
echo "🔍 Using Python version:"
python --version
echo ""

# Step 1: Baseline data simulation
echo " Step 1: Simulating baseline data..."
python scripts/01_simulate_baseline.py

# Step 2: Ad group assignment
echo " Step 2: Randomly assigning ad groups..."
python scripts/02_assign_ad_groups.py

# Step 3: Endline survey simulation
echo " Step 3: Simulating endline survey responses..."
python scripts/03_simulate_endline.py

# Step 4: Effectiveness analysis (vaccine uptake, attitude, regression)
echo " Step 4: Running effectiveness analysis..."
python scripts/04_analyze_effectiveness.py

# Step 5: Centrality analysis (optional enhancement)
echo "Step 5: Running centrality analysis (optional)..."
python scripts/05_network_analysis.py

# Step 6: Network-based community insights
echo " Step 6: Running full network & community analysis..."
python scripts/06_network_deepdive.py

echo ""
echo " All steps complete! Check the outputs/ folder for results and visualizations."
