# WFP Nutribus 2.0 Activity & Inclusive Impact Dashboard

An interactive monitoring and impact evaluation dashboard developed for the **World Food Programme (WFP) Uganda** under the **Nutribus 2.0 Social and Behaviour Change Communication (SBCC)** campaign across the **9 Karamoja districts** (Abim, Amudat, Kaabong, Kotido, Moroto, Nabilatuk, Nakapiripirit, Napak, Karenga).

---

## 🎨 Design & Data Specifications
- **Brand Palette:** WFP Blue (`#0A6EB4`) with supporting official accents (`#074E82`, `#16A34A`, `#D97706`).
- **Strict Chart Guidelines:** **Zero pie charts**. Only **horizontal bar charts** with category labels placed on the vertical Y-axis.
- **Granular Question Cards:** Every section and individual question from the 36-page KoBo data collection tool has its own dedicated card, KPI badge, and horizontal bar chart.

---

## 🚀 How to Run the Dashboard

### Option 1: Standalone Web Dashboard (Recommended for Instant Access)
The standalone web application is located in `index.html`. It runs directly in any modern browser without requiring any server setup:
```bash
# On macOS:
open index.html

# Or start a lightweight local HTTP server:
python3 -m http.server 8080
# Open http://localhost:8080 in your browser
```

### Option 2: Updating the Dashboard with New Data
Whenever new data is added or modified in `Nutribus_2.0_Activity.xlsx`:
```bash
# Simply run the update script in the terminal:
./update_dashboard.sh

# Or on macOS, double-click:
Update_Dashboard.command
```
This automatically ingests the latest Excel data, updates `dashboard_data.json` and `dashboard_district_db.json`, and rebuilds the standalone `index.html`.

---

## 📊 Core Headline Indicators & Targets

| Headline Indicator | Current Cleaned Reach | Operations Target | Status |
| :--- | :---: | :---: | :--- |
| **Schools Reached** | **6** | 64 schools | 9.4% Progress |
| **Demonstrations** | **60** | 640 sites | 9.4% Progress |
| **Learners Reached** | **5,840** | 80,875 learners | 7.2% Progress |
| **Caregivers Reached** | **165** | 51,200 adults | Catchment Active |
| **Teachers & VHTs** | **143** | Key stakeholders | 48 Teachers \| 95 VHTs |
| **Total PWD Reach** | **248** | Inclusive Reach | 78 M / 68 F Learners, 36 VHTs, 66 Adults |

---

## 📑 Dashboard Architecture & Tabs

1. **📊 1. Campaign Overview, Reach & PWD Inclusion (Summary & Reach)**
   - Operational progress against targets across all 9 Karamoja districts.
   - Comprehensive PWD inclusion disaggregation (Learners, VHTs, Caregivers).
   - District-by-district reach data table and comparative horizontal bar chart.

2. **🏫 2. Teacher & VHT Orientation (Cleaned Data & Tool Questions)**
   - Teacher attendance by sex, Headteacher/Deputy presence (100%), Appointed NutriClub patrons.
   - VHTs oriented by sex, VHTs with disabilities (PWDs).
   - Signed 4-week joint calendar agreements (100% compliance).
   - Exit interviews across the 3 Pillars: most important lessons and personal action commitments.
   - Campaign collateral handover compliance (forms, posters, manuals, WFP 0800 boards).

3. **🚌 3. Three-Visit School Contact Data & Tool Questions**
   - **Visit 1 (Follow-up & Handover):** NutriClub active days, signed 4-week work plans, 1,840 NutriCharts issued by grade band, WFP toll-free display verification, and baseline attendance registers.
   - **Visit 2 (NutriBus Big Activation Day):** Activation headcounts by age band & PWDs, session delivery checklist, active handling vs passive observation, **Pillar 2 Micro-Poll (5 statements with 180 boys sampled)**, and unaided post-session scenario recall.
   - **Visit 3 (Materials Collection & Closing Audit):** 86.2% NutriChart return rate, 89.0% joint household completion, primary household feedback and barriers, status of written Bus Day school commitments, collective chronic absentee tracing, and school kitchen fuel-saving stove audits.

4. **🍲 4. Community Cooking Demonstration Cleaned Data & Tool Questions**
   - Catchment demo site headcounts (Caregivers, Fathers, Children, PWDs).
   - VHT vs Coordinator entry submissions.
   - 90% hands-on cooking practice, 100% Metu porridge local fortification (Eboo, Lokaka, cowpeas, roasted sesame).
   - Fuel-saving practices demonstrated (improved cookstoves, fuelwood pre-drying, pot covering).
   - Private caregiver intercept interviews (150 interviewed): barriers, feasible actions, commitment verdict.
   - Structured gender chore discussions and intra-household food serving hierarchy shifts (youngest child first).

5. **📖 5. Most Significant Change (MSC) Qualitative Tracker**
   - Storyteller roles (Caregivers, Girls, Boys, Fathers, Teachers, Leaders) and ages.
   - Triggering campaign events and observed physical behavioral shifts.
   - Verifiable physical evidence sighted on-site by collector (100% verified).
   - Featured case stories with verbatim transcripts.

6. **🤝 6. NutriClub Sessions Cleaned Data & Tool Questions**
   - Session 1 and Session 2 tracking across 6 schools (12 sessions).
   - Club patron appointments, membership by sex (312 members), PWD learners (38 learners).
   - Practical activity delivered checklist and home action feedback from parents.
   - Whole-School Assembly Nutri-Moments: core nutrition and gender messages shared.

7. **📈 7. Impact Analysis (Based on Entered Data)**
   - Cross-cutting synthesis across 6 impact dimensions:
     1. Gender chore rebalancing & girl on-time school arrival.
     2. Metu Porridge Plus local fortification adoption rate.
     3. Climate-smart cooking & firewood conservation.
     4. Intra-household food equity & child prioritization.
     5. PWD accessibility & active community participation.
     6. Institutional sustainability scorecard.

8. **📋 8. Cleaned KoBo Data Records & Interactive Entry**
   - Searchable, filterable table of field records.
   - Direct modal data entry to input new submissions and recalculate metrics in real-time.
   - CSV export functionality.
