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
3. Generates and formats the Master Excel workbook (`VHTs_Teachers_and_Demos_Master_Extract.xlsx`).

---

## 📊 Core Headline Indicators & Field Progress (811 Submissions Ingested)

| Headline Indicator | Current Cleaned Reach | Operations Target | Status / Progress |
| :--- | :---: | :---: | :--- |
| **Official Schools Reached** | **64** | 64 schools | **100.0% Progress** (All 9 districts covered) |
| **School Contact Visits** | **141** | 192 visits | **73.4% Progress** (Visit 1: 65, Visit 2: 63, Visit 3: 13) |
| **Community Demonstrations** | **438** | 640 sites | **68.4% Progress** (Active across all 64 catchments) |
| **NutriClub Sessions** | **207** | 64 schools | **323.4% Progress** (Active student clubs operating) |
| **Learners Reached** | **79,102** | 80,875 learners | **97.8% Progress** |
| **Caregivers Reached** | **24,949** | 51,200 adults | **48.7% Progress** |
| **Teachers & VHT Stakeholders** | **1,522** | 768 key actors | **198.2% Progress** (Oriented & mobilized) |
| **Total PWD Reach** | **21,577** | 1,200 individuals | **1,798.1% Progress** (Inclusive accommodation) |
| **Most Significant Change (MSC) Stories** | **9** | 128 stories | **7.0% Progress** (Target: 2 stories per school) |

---

## 📁 Consolidated Master Extraction Workbook

All verification, monitoring audit, and partner reporting is unified in a single multi-tab workbook:

👉 **`VHTs_Teachers_and_Demos_Master_Extract.xlsx`** (7 Formatted Tabs)
1. **Tab 1: `Coordinator Activity Summary`** (Executive summary matrix of total submissions logged by each District Coordinator broken down by activity type).
2. **Tab 2: `Coordinator Entries Log (811)`** (Full registry of all 811 submissions with entry index, date, district, coordinator, activity type, and school/site).
3. **Tab 3: `Missing Visits & MSC Status`** (Tracks all 64 schools across Visit 1, Visit 2, Visit 3 Closeout, School Story, Community Story, and MSC Progress).
4. **Tab 4: `Missing MSC Stories (128 Tgt)`** (Tracks School Story vs Community Catchment Story target vs actual and follow-up actions across all 64 schools).
5. **Tab 5: `MSC Stories Register (9)`** (Complete qualitative narratives, storyteller demographics, verbatim quotes, and physical evidence sighted).
6. **Tab 6: `VHTs & Demos (438)`** (All 438 community cooking demonstrations with dates, demo sites, catchment schools, named VHTs, and coordinators).
7. **Tab 7: `Teachers & Club Patrons (64)`** (All 64 schools with named teacher NutriClub patrons and club membership counts).

---

## 🔍 Missing Entries & Priority Follow-Up Action

### 1. Missing Visit 1 (Baseline Onboarding): **1 School**
- Kotido District: **`KOTIDO GIRLS P/S`**

### 2. Missing Visit 2 (NutriBus Day Activation): **2 Schools**
- Abim District (2 schools remaining): **`OBOLOKOME P/S`**, **`OTALABAR P/S`** (`MORULEM BOYS P/S` completed in entry #768; `ALEREK P/S` completed in entry #696)

### 3. Visit 3 (Closeout Audit): **13 Schools Completed**
- **Napak District (5 of 5 schools completed - 100%):** `KALOTOM P/S`, `KAPUAT P/S`, `LONGALOM P/S`, `LOPEEI P/S`, `LORENGECHORA P/S`
- **Karenga District (5 of 5 schools completed - 100%):** `KARENGA BOYS P/S`, `KARENGA GIRLS P/S`, `KAWALAKOL P/S`, `LOBALANGIT P/S`, `NALAKAS P/S`
- **Kotido District (2 schools completed):** `NAPUMPUM P/S`, `LOMUKURA P/S`
- **Abim District (1 school completed):** `ROGOM P/S` (Entry #806)
- Remaining 51 schools: In progress / pending closeout schedule.

### 4. Most Significant Change Stories: **119 Stories Needed**
- **Target:** 2 stories per school (1 School Story + 1 Community Catchment Story) × 64 schools = **128 stories**.
- **Completed Target Schools (2 schools completed 100%):**
  - **Kaabong District:** `KAKAMAR P/S` (2 of 2: Lokol Lokodo & Lobwal Joseph) and `KAMACHARIKOL P/S` (2 of 2: Piramoe John Leo & Nakong Hellen).
- **Partial Target Schools (5 schools):**
  - **Napak District:** `KALOTOM P/S` (needs School Story); `KAPUAT P/S`, `LONGALOM P/S`, `LOPEEI P/S`, `LORENGECHORA P/S` (each needs 1 Community Story).
- **Other 7 Districts (57 schools):** Pending both School and Community stories.

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
   - Session 1 and Session 2 tracking across all 64 schools (175 sessions).
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
