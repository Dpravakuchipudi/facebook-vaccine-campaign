
# Facebook Vaccine Ad Campaign Simulation

This repository presents a complete pipeline for a **simulated field experiment** examining the impact of different Facebook ad campaigns on COVID-19 vaccine uptake. It includes:

- End-to-end **data simulation**
- A full **experimental design workflow**
- **Causal inference** using intention-to-treat (ITT) and treatment-on-the-treated (TOT)
- **Attitude shift analysis**
- **Network-based modeling** and community-level behavioral insights

---

##  Objective

To simulate a realistic public health experiment and evaluate the **effectiveness of behavior-change messaging** delivered through social media ads — comparing appeals to **reason** vs **emotion** — in increasing vaccine adoption.

This experiment mirrors the logic and methodology used in academic and policy research and is especially inspired by randomized controlled trials (RCTs) used in **development economics, public health, and behavioral science**.

---

##  Summary of Experimental Design

- **Participants:** 5,000 individuals
- **Random Assignment:**
  - 1/3 receive a **reason-based** ad
  - 1/3 receive an **emotion-based** ad
  - 1/3 are **control group**
- **Surveys:** All complete a **baseline survey**, and 4,500 complete an **endline survey**
- **Reach simulation:** Only ~65–70% in treatment groups are assumed to be exposed to the ad

---

##  Analytical Methods

###  Descriptive & Inferential Stats:
- Vaccine uptake % by ad group
- Attitude change (pre vs post)
- Chi-square test for group differences
- T-test on network centrality

### Causal Modeling:
- **ITT vs TOT** estimation
- **Logistic regression** on uptake using:
  - Ad group
  - Trust in science
  - Vaccine hesitancy

### Network Science (Optional Enhancements):
- Randomly generated social network (Erdős–Rényi model)
- Community detection via **modularity optimization**
- Centrality vs uptake correlation
- Community-level uptake variance

---

##  Folder Structure

```
facebook-vaccine-campaign/
├── data/                    # Simulated CSV datasets
├── outputs/                 # All visualizations & result tables
├── scripts/                 # All modular steps (see below)
├── requirements.txt         # Python dependencies
└── README.md                # You're reading it!
```

---

##  How to Run This Pipeline

Each step is modular and can be executed independently:

```bash
# STEP 1: Simulate baseline survey
python scripts/01_baseline_only.py

# STEP 2: Randomly assign ad groups
python scripts/02_assign_groups.py

# STEP 3: Simulate endline responses
python scripts/03_simulate_endline.py

# STEP 4: Analyze ITT, TOT, regression, visualizations
python scripts/04_analyze_effectiveness.py

# STEP 5: Optional — Centrality and uptake boxplot
python scripts/05_network_analysis.py

# STEP 6: Optional — Community structure, t-test, subgraph visuals
python scripts/06_network_deepdive.py
```

---

##  Sample Output Files

| Output                        | Description                                 |
|------------------------------|---------------------------------------------|
| `vaccination_summary.csv`    | Uptake rates by ad group (ITT)              |
| `attitude_change_by_group.png` | Visualization of average attitude change   |
| `logistic_summary.txt`       | Logistic regression summary                 |
| `itt_vs_tot_comparison.png`  | Uptake rates: ITT vs TOT                    |
| `network_centrality_vs_uptake.png` | Centrality vs vaccine uptake          |
| `vaccine_uptake_by_community.png` | Community-level uptake variance       |
| `network_graph_sample.png`   | Network visualization (subgraph of 100)     |

---

##  Dependencies

This project requires:

```txt
pandas
numpy
matplotlib
seaborn
networkx
scipy
statsmodels
```

Install via:

```bash
pip install -r requirements.txt
```

---

##  Interpretation Highlights

- **Ad_Emotion group** had the highest vaccine uptake and greatest attitude improvement
- **Statistically significant** differences in uptake were observed (Chi2 test)
- **Central participants** (in simulated network) were more likely to vaccinate
- **Community-level clustering** revealed uptake varies across subgroups even in randomized contexts

---

##  Why This Project Matters

This project showcases how **experimental design**, **data simulation**, and **causal analysis** can work hand-in-hand. It demonstrates:

- Strong skills in **data generation, cleaning, and merging**
- Application of **statistical modeling** and **inference**
- Integration of **network science** with behavioral analytics
- Clean, reproducible code structure suitable for academic, policy, or product evaluation use cases

---

##  Author

**Durga Pravallika Kuchipudi**  
Graduate Researcher & Data Scientist  
📍 Indiana University – M.S. in Applied Data Science  
🔗 [LinkedIn](https://www.linkedin.com/in/your-link) | 🌐 [Portfolio](https://your-portfolio.com)

---

##  License

MIT License – For educational and research use.
