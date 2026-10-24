# WFP Nutribus 2.0 Activity & Inclusive Impact Dashboard

An interactive monitoring, reporting, and impact evaluation dashboard developed for the **World Food Programme (WFP) Uganda** under the **Nutribus 2.0 Social and Behaviour Change Communication (SBCC)** campaign across the **9 Karamoja districts** (Abim, Amudat, Kaabong, Kotido, Moroto, Nabilatuk, Nakapiripirit, Napak, Karenga).

---

## 🎨 Design & Data Specifications
- **Brand Palette:** WFP Blue (`#0A6EB4`) with supporting official accents (`#074E82`, `#16A34A`, `#D97706`).
- **Strict Chart Guidelines:** **Zero pie charts**. Only **horizontal bar charts** with category labels placed on the vertical Y-axis.
- **Granular Question Cards:** Every section and individual question from the KoBo data collection tool has its own dedicated card, KPI badge, and horizontal bar chart.

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

### Option 2: Updating the Dashboard and Master Extraction Documents
Whenever new data is added or modified in `Nutribus_2.0_Activity.xlsx`:
```bash
# Simply run the automated 3-step pipeline in the terminal:
./update_dashboard.sh
```
This automatically:
1. Ingests all field submissions into JSON databases (`dashboard_data.json`, `dashboard_district_db.json`, `dashboard_demo_sessions_640.json`).
2. Rebuilds the standalone HTML dashboard (`index.html`).
3. Generates and formats all Master Excel extracts and tracking workbooks (`VHTs_Teachers_and_Demos_Master_Extract.xlsx`, etc.).

---

## 📊 Core Headline Indicators & Field Progress

| Headline Indicator | Current Logged Reach | Operations Target | Status / Progress |
| :--- | :---: | :---: | :--- |
| **Official Schools Reached** | **64** | 64 schools | **100.0% Progress** (All 9 districts covered) |
| **School Contact Visits** | **131** | 192 visits | **68.2% Progress** (Visit 1: 63, Visit 2: 59, Visit 3: 7) |
| **Community Demonstrations** | **305** | 640 sites | **47.7% Progress** (Active across all 64 catchments) |
| **NutriClub Sessions** | **159** | 64 schools | **248.4% Progress** (Active student clubs operating) |
| **Learners Reached** | **71,800** | 80,875 learners | **88.8% Progress** (35,420 Girls / 36,380 Boys) |
| **Caregivers Reached** | **17,972** | 51,200 adults | **35.1% Progress** (13,858 Females / 4,114 Males) |
| **Teachers & VHT Stakeholders** | **1,387** | 768 key actors | **180.6% Progress** (Oriented & mobilized) |
| **Total PWD Reach** | **15,604** | 1,200 individuals | **1,300.3% Progress** (Inclusive accommodation) |
| **Most Significant Change (MSC) Stories** | **5** | 128 stories | **3.9% Progress** (Target: 2 stories per school) |

---

## 📁 Master Extraction Workbooks & Tracking Documents

The repository automatically generates synchronized, professionally styled Excel and CSV workbooks on every update run:

1. **Combined Master Workbook (5 Tabs):**
   - `VHTs_Teachers_and_Demos_Master_Extract.xlsx`
     - **Tab 1: `Missing Visits & MSC Status`** (Tracks all 64 schools across Visit 1, Visit 2, Visit 3 Closeout, School Story, Community Story, and MSC Progress).
     - **Tab 2: `Missing MSC Stories (128 Tgt)`** (Tracks School Story vs Community Catchment Story target vs actual and follow-up actions across all 64 schools).
     - **Tab 3: `MSC Stories Register (5)`** (Complete qualitative narratives, storyteller demographics, verbatim quotes, and physical evidence sighted).
     - **Tab 4: `VHTs & Demos (305)`** (All 305 community cooking demonstrations with dates, demo sites, catchment schools, named VHTs, and coordinators).
     - **Tab 5: `Teachers & Club Patrons (64)`** (All 64 schools with named teacher NutriClub patrons and club membership counts).

2. **Dedicated Standalone Extraction Files:**
   - **MSC Stories Tracking:** `Missing_MSC_Stories_Tracking.xlsx` / `Missing_MSC_Stories_Tracking.csv`
   - **Detailed MSC Narratives:** `Most_Significant_Change_Stories_Extract.xlsx` / `Most_Significant_Change_Stories_Extract.csv`
   - **VHTs & Community Demos:** `VHTs_and_Community_Demos_Extract.xlsx` / `VHTs_and_Community_Demos_Extract.csv`
   - **Teachers & School Patrons:** `Teachers_and_School_Patrons_Extract.xlsx` / `Teachers_and_School_Patrons_Extract.csv`

---

## 🔍 Missing Entries & Priority Follow-Up Action

### 1. Missing Visit 1 (Baseline Onboarding): **1 School**
- Kotido District: **`KOTIDO GIRLS P/S`**

### 2. Missing Visit 2 (NutriBus Day Activation): **5 Schools**
- Abim District (4 schools): **`ALEREK P/S`**, **`MORULEM BOYS P/S`**, **`OBOLOKOME P/S`**, **`OTALABAR P/S`**
- Kotido District (1 school): **`KOTIDO MIXED P/S`**

### 3. Visit 3 (Closeout Audit): **7 Schools Completed**
- Napak District (All 5 schools): `KALOTOM P/S`, `KAPUAT P/S`, `LONGALOM P/S`, `LOPEEI P/S`, `LORENGECHORA P/S`
- Kotido District (2 schools): `NAPUMPUM P/S`, `LOMUKURA P/S`
- Remaining 57 schools: In progress / pending closeout schedule.

### 4. Most Significant Change Stories: **123 Stories Needed**
- **Target:** 2 stories per school (1 School Story + 1 Community Catchment Story) × 64 schools = **128 stories**.
- **Napak District (5 schools):** Each school has completed 1 story; each needs 1 remaining story (`KALOTOM P/S` needs a School Story; `KAPUAT P/S`, `LONGALOM P/S`, `LOPEEI P/S`, `LORENGECHORA P/S` need a Community Story).
- **Other 8 Districts (59 schools):** Pending both School and Community stories.

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
   - **Visit 1 (Follow-up & Handover):** NutriClub active days, signed 4-week work plans, NutriCharts issued by grade band, WFP toll-free display verification, and baseline attendance registers.
   - **Visit 2 (NutriBus Big Activation Day):** Activation headcounts by age band & PWDs, session delivery checklist, active handling vs passive observation, **Pillar 2 Micro-Poll**, and unaided post-session scenario recall.
   - **Visit 3 (Materials Collection & Closing Audit):** NutriChart return rate, joint household completion, primary household feedback and barriers, status of written Bus Day school commitments, collective chronic absentee tracing, and school kitchen fuel-saving stove audits.

4. **🍲 4. Community Cooking Demonstration Cleaned Data & Tool Questions**
   - Catchment demo site headcounts (Caregivers, Fathers, Children, PWDs).
   - VHT vs Coordinator entry submissions.
   - Hands-on cooking practice, 100% Metu porridge local fortification (Eboo, Lokaka, cowpeas, roasted sesame).
   - Fuel-saving practices demonstrated (improved cookstoves, fuelwood pre-drying, pot covering).
   - Private caregiver intercept interviews: barriers, feasible actions, commitment verdict.
   - Structured gender chore discussions and intra-household food serving hierarchy shifts (youngest child first).

5. **📖 5. Most Significant Change (MSC) Qualitative Tracker & Register**
   - School-by-school qualitative change narratives and verifiable evidence audit table.
   - Storyteller role filters (Girl Learners, Boy Learners, Caregivers, Teachers, Local Leaders).
   - Dynamic KPI counters tracking stories logged vs target (128 stories).
   - Detailed evidence sighted (fortified cooking pots, fuel-saving stoves, school registers).

6. **🤝 6. NutriClub Sessions Cleaned Data & Tool Questions**
   - Session 1 and Session 2 tracking across all 64 schools (159 sessions).
   - Club patron appointments, membership by sex, PWD learners.
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
