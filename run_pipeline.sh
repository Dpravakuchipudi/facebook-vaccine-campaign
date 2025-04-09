#!/bin/bash

echo "🚀 Running Facebook Vaccine Campaign Simulation"

python scripts/01_simulate_baseline.py
python scripts/02_assign_ad_groups.py
python scripts/03_simulate_endline.py
python scripts/04_analyze_effectiveness.py
python scripts/05_network_analysis.py
python scripts/06_network_deepdive.py

echo "✅ All steps complete! Check the outputs/ folder."
