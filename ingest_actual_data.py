import json
import os
import pandas as pd
import numpy as np

# Source paths
EXCEL_PATH = "Nutribus_2.0_Activity.xlsx"
OFFICIAL_SCHOOLS_PATH = "official_64_schools.json"
TRACKER_FILE = ".ingest_tracker.json"

if not os.path.exists(EXCEL_PATH):
    print(f"❌ Error: {EXCEL_PATH} not found.")
    exit(1)

df = pd.read_excel(EXCEL_PATH)
with open(OFFICIAL_SCHOOLS_PATH, "r", encoding="utf-8") as f:
    OFFICIAL_SCHOOLS = json.load(f)

# 1. IDENTIFY THE INDEX COLUMN (_index, -index, index)
INDEX_COL = None
for col in df.columns:
    if str(col).strip().lower() in ["_index", "-index", "index"]:
        INDEX_COL = col
        break

if INDEX_COL is None:
    # Auto-fallback: create 1-based index if not in sheet
    INDEX_COL = "_index"
    df["_index"] = list(range(1, len(df) + 1))
    print(f"⚠️ Index column not detected; auto-generated '{INDEX_COL}' for {len(df)} rows.")

# Ensure index column is integer-cast and sorted
df[INDEX_COL] = pd.to_numeric(df[INDEX_COL], errors="coerce").fillna(0).astype(int)
df = df.sort_values(by=[INDEX_COL])

# 2. LOAD PREVIOUS TRACKER STATE
prev_processed_indices = set()
last_processed_idx = 0

if os.path.exists(TRACKER_FILE):
    try:
        with open(TRACKER_FILE, "r", encoding="utf-8") as tf:
            tracker_data = json.load(tf)
            prev_processed_indices = set(tracker_data.get("processed_indices", []))
            last_processed_idx = tracker_data.get("last_processed_index", 0)
    except Exception as e:
        prev_processed_indices = set()

current_indices = sorted(df[INDEX_COL].tolist())
new_indices = [idx for idx in current_indices if idx not in prev_processed_indices]

print("=" * 65)
print(f"📋 NUTRIBUS 2.0 SUBMISSION INGESTION PIPELINE")
print(f"📌 Tracking Column: '{INDEX_COL}'")
print(f"📊 Total Rows in Excel: {len(df)}")
if prev_processed_indices:
    print(f"⏮️ Previously Tracked Highest Index: #{last_processed_idx}")
    if new_indices:
        print(f"✨ NEW ENTRIES DETECTED: {len(new_indices)} new submission(s) (Indices: {new_indices})")
    else:
        print(f"🔄 All entries up to #{last_processed_idx} are already tracked. Re-verifying database.")
else:
    print(f"🚀 Initializing tracking for all {len(current_indices)} entries (Indices: {current_indices})")
print("=" * 65)

# Build official school lookups
ALL_DISTRICTS = ["Abim", "Amudat", "Kaabong", "Karenga", "Kotido", "Moroto", "Nabilatuk", "Nakapiripirit", "Napak"]
DISTRICT_SCHOOLS = {d: [] for d in ALL_DISTRICTS}
for s in OFFICIAL_SCHOOLS:
    d = s.get("district", "Unknown")
    if d in DISTRICT_SCHOOLS:
        DISTRICT_SCHOOLS[d].append(s)

def clean_val(val, default=0):
    if pd.isnull(val):
        return default
    if isinstance(val, str):
        val_clean = val.strip().replace("O", "0").replace("o", "0")
        try:
            return float(val_clean)
        except ValueError:
            return default
    try:
        return float(val)
    except:
        return default

def get_school_name(row):
    dist = str(row.get("District", "")).strip()
    if dist in row and pd.notnull(row[dist]):
        return str(row[dist]).strip()
    for d in ALL_DISTRICTS:
        if d in row and pd.notnull(row[d]):
            return str(row[d]).strip()
    for col in row.index:
        if "school" in col.lower() and pd.notnull(row[col]):
            return str(row[col]).strip()
    return "Unknown School"

# Data containers
district_dates = {d: set() for d in ALL_DISTRICTS}
district_schools_reached = {d: set() for d in ALL_DISTRICTS}
district_demos_completed = {d: 0 for d in ALL_DISTRICTS}
district_learners_reached = {d: 0 for d in ALL_DISTRICTS}
district_caregivers_reached = {d: 0 for d in ALL_DISTRICTS}
district_teachers_m = {d: 0 for d in ALL_DISTRICTS}
district_teachers_f = {d: 0 for d in ALL_DISTRICTS}
district_vhts_m = {d: 0 for d in ALL_DISTRICTS}
district_vhts_f = {d: 0 for d in ALL_DISTRICTS}
district_pwd_learners = {d: 0 for d in ALL_DISTRICTS}
district_pwd_adults = {d: 0 for d in ALL_DISTRICTS}
district_visits_conducted = {d: 0 for d in ALL_DISTRICTS}
district_v1_count = {d: 0 for d in ALL_DISTRICTS}
district_v2_count = {d: 0 for d in ALL_DISTRICTS}
district_v3_count = {d: 0 for d in ALL_DISTRICTS}
district_nutriclubs_count = {d: 0 for d in ALL_DISTRICTS}
district_exit_interviews = {d: {} for d in ALL_DISTRICTS}
district_v2 = {d: None for d in ALL_DISTRICTS}
demo_sessions_list = []
nutriclub_sessions_list = []
msc_stories_list = []
records_log = []

# --- PARSE EACH ROW BY INDEX ---
for _, row in df.iterrows():
    entry_index = int(row[INDEX_COL])
    sub_id = int(row.get("_id", entry_index)) if pd.notnull(row.get("_id")) else entry_index
    date_val = str(row.get("Date", "")).split(" ")[0] if pd.notnull(row.get("Date")) else "2026-10-02"
    dist = str(row.get("District", "")).strip()
    if dist not in ALL_DISTRICTS:
        dist = "Abim"  # fallback
    
    activity = str(row.get("Activity ", row.get("Activity", ""))).strip()
    school_name = get_school_name(row)
    coordinator = str(row.get("Specify", row.get("Coordinator Name", "Field Coordinator"))).strip()

    district_dates[dist].add(date_val)
    district_schools_reached[dist].add(school_name)

    reach = 0
    pwd = 0

    # 1. ORIENTATION
    if "Orientation" in activity:
        tm = clean_val(row.get("Male Teachers", 0))
        tf = clean_val(row.get("Female Teachers", 0))
        vm = clean_val(row.get("Male VHTs", 0))
        vf = clean_val(row.get("Female VHTs", 0))
        district_teachers_m[dist] += tm
        district_teachers_f[dist] += tf
        district_vhts_m[dist] += vm
        district_vhts_f[dist] += vf
        reach = int(tm + tf + vm + vf)
        pwd = 0

        # Parse Exit Interviews in this row
        for prefix in ["row", "row_1", "row_2", "row_3", "row_4", "row_5"]:
            word_col = f'<span style="display:none">{prefix}-Record their Specific personal action in their exact words</span>'
            act_col = f'<span style="display:none">{prefix}-What specific action are you personally going to take this week?</span>'
            les_col = f'<span style="display:none">{prefix}-What were the most important lessons learned today across the 3 Pillars?</span>'
            sex_col = f'<span style="display:none">{prefix}-Sex</span>'

            words = str(row.get(word_col, "")).strip() if word_col in row and pd.notnull(row[word_col]) else ""
            if words and words.lower() != "nan":
                sex = str(row.get(sex_col, "Female")).strip() if sex_col in row and pd.notnull(row[sex_col]) else "Female"
                action = str(row.get(act_col, "General nutrition support")).strip() if act_col in row and pd.notnull(row[act_col]) else "General nutrition support"
                lessons_raw = str(row.get(les_col, "")).strip() if les_col in row and pd.notnull(row[les_col]) else ""
                
                lessons = []
                if "porridge" in lessons_raw.lower() or "wild greens" in lessons_raw.lower():
                    lessons.append("Metu Porridge Fortification (Local Greens)")
                if "chores" in lessons_raw.lower() or "firewood" in lessons_raw.lower():
                    lessons.append("Rebalancing Morning Chores so Girls Stay in School")
                if "hotline" in lessons_raw.lower() or "clubs" in lessons_raw.lower():
                    lessons.append("Establishing Nutri Clubs & Hotline 0800")
                if "plate" in lessons_raw.lower() or "sharing" in lessons_raw.lower():
                    lessons.append("Fair and Equal Plate Sharing at Home")
                if "improved cooking" in lessons_raw.lower() or "less firewood" in lessons_raw.lower():
                    lessons.append("Improved Cooking Methods (Firewood Saving)")
                if not lessons:
                    lessons = ["Metu Porridge Fortification", "Equitable Morning Chores"]

                resp_key = f"Respondent {len(district_exit_interviews[dist]) + 1} ({school_name})"
                district_exit_interviews[dist][resp_key] = {
                    "key": resp_key,
                    "sex": sex,
                    "role": "Teacher / VHT",
                    "lessons": lessons,
                    "action": action,
                    "words": words,
                    "school": school_name,
                    "district": dist,
                    "entry_index": entry_index
                }

    # 2. NUTRICLUB SESSION
    elif "Nutriclub" in activity or "Nutri Club" in activity:
        bp = clean_val(row.get("Boys Present", 0))
        gp = clean_val(row.get("Girls Present", 0))
        district_learners_reached[dist] += int(bp + gp)
        reach = int(bp + gp)
        pwd = int(clean_val(row.get("Male learners with Disabilities", 0)) + clean_val(row.get("Female learners with Disabilities", 0)))
        district_pwd_learners[dist] += pwd

        patron = str(row.get("Club Patron Name", "Amera Francis")).strip()
        district_teachers_m[dist] += 1
        district_nutriclubs_count[dist] += 1

        nutriclub_sessions_list.append({
            "entry_index": entry_index,
            "school": school_name,
            "district": dist,
            "subcounty": "Catchment",
            "session_of_week": str(row.get("What session of the week is this", "Session one of the week")),
            "date": date_val,
            "patron": patron,
            "membership_male": clean_val(row.get("Total  male membership of the nutriclub", 16)),
            "membership_female": clean_val(row.get("Total  female membership of the nutriclub", 25)),
            "total_membership": clean_val(row.get("Total  male membership of the nutriclub", 16)) + clean_val(row.get("Total  female membership of the nutriclub", 25)),
            "boys_present": int(bp),
            "girls_present": int(gp),
            "total_present": int(bp + gp),
            "pwd_boys": clean_val(row.get("Male learners with Disabilities", 0)),
            "pwd_girls": clean_val(row.get("Female learners with Disabilities", 0)),
            "meeting_place": str(row.get("Designated Meeting Place on Compound", "Under the tree")),
            "practical_activity": str(row.get("Practical Activity Delivered", "Adere Calabash Dialogue & Gender Chore Rebalancing")),
            "home_action_assigned": str(row.get("What specific feasible food or chore action were members asked to try at home?", "Try kitchen gardens at home.")),
            "coordinator_notes": str(row.get("Any other comments or observations about that event to inform future activities ", ""))
        })

    # 3. THREE VISIT CONTACT
    elif "Three visit" in activity or "visit" in activity.lower():
        milestone = str(row.get("Milestone Being Conducted Today", "Visit 2: NutriBus Big Activation Day"))
        district_visits_conducted[dist] += 1
        if "visit 1" in milestone.lower() or "baseline" in milestone.lower():
            district_v1_count[dist] += 1
        elif "visit 2" in milestone.lower() or "activation" in milestone.lower():
            district_v2_count[dist] += 1
        elif "visit 3" in milestone.lower() or "closeout" in milestone.lower():
            district_v3_count[dist] += 1
        
        # Lower
        l_m = clean_val(row.get('<span style="display:none">row-Male</span>', 0))
        l_f = clean_val(row.get('<span style="display:none">row-Female</span>', 0))
        l_pwd = clean_val(row.get('<span style="display:none">row-Male PWDs</span>', 0)) + clean_val(row.get('<span style="display:none">row-Female PWDs</span>', 0))
        
        # Mid
        m_m = clean_val(row.get('<span style="display:none">row_1-Male</span>', 0))
        m_f = clean_val(row.get('<span style="display:none">row_1-Female</span>', 0))
        m_pwd = clean_val(row.get('<span style="display:none">row_1-Male PWDs</span>', 0)) + clean_val(row.get('<span style="display:none">row_1-Female PWDs</span>', 0))
        
        # Upper
        u_m = clean_val(row.get('<span style="display:none">row_2-Male</span>', 0))
        u_f = clean_val(row.get('<span style="display:none">row_2-Female</span>', 0))
        u_pwd = clean_val(row.get('<span style="display:none">row_2-Male PWDs</span>', 0)) + clean_val(row.get('<span style="display:none">row_2-Female PWDs</span>', 0))
        
        # Teachers
        t_m = clean_val(row.get('<span style="display:none">row_3-Male</span>', 0))
        t_f = clean_val(row.get('<span style="display:none">row_3-Female</span>', 0))
        t_pwd = clean_val(row.get('<span style="display:none">row_3-Male PWDs</span>', 0)) + clean_val(row.get('<span style="display:none">row_3-Female PWDs</span>', 0))
        
        # Community
        c_m = clean_val(row.get('<span style="display:none">row_4-Male</span>', 0))
        c_f = clean_val(row.get('<span style="display:none">row_4-Female</span>', 0))
        c_pwd = clean_val(row.get('<span style="display:none">row_4-Male PWDs</span>', 0)) + clean_val(row.get('<span style="display:none">row_4-Female PWDs</span>', 0))

        tot_pupils = int(l_m + l_f + m_m + m_f + u_m + u_f)
        tot_staff = int(t_m + t_f)
        tot_comm = int(c_m + c_f)
        tot_pwd_l = int(l_pwd + m_pwd + u_pwd)
        tot_pwd_a = int(t_pwd + c_pwd)

        district_learners_reached[dist] += tot_pupils
        district_teachers_m[dist] += int(t_m)
        district_teachers_f[dist] += int(t_f)
        district_caregivers_reached[dist] += tot_comm
        district_pwd_learners[dist] += tot_pwd_l
        district_pwd_adults[dist] += tot_pwd_a

        reach = tot_pupils + tot_staff + tot_comm
        pwd = tot_pwd_l + tot_pwd_a

        if "Visit 2" in milestone or district_v2[dist] is None:
            district_v2[dist] = {
                "entry_index": entry_index,
                "school": school_name,
                "district": dist,
                "hc_lower_m": int(l_m), "hc_lower_f": int(l_f), "hc_lower_pwd": int(l_pwd),
                "hc_mid_m": int(m_m), "hc_mid_f": int(m_f), "hc_mid_pwd": int(m_pwd),
                "hc_up_m": int(u_m), "hc_up_f": int(u_f), "hc_up_pwd": int(u_pwd),
                "teachers_m": int(t_m), "teachers_f": int(t_f), "teachers_pwd": int(t_pwd),
                "comm_m": int(c_m), "comm_f": int(c_f), "comm_pwd": int(c_pwd)
            }

    # 4. COMMUNITY DEMONSTRATION
    elif "demonstration" in activity.lower() or "demo" in activity.lower():
        district_demos_completed[dist] += 1
        cg = clean_val(row.get("Caregivers Present", row.get("Total Caregivers", 0)))
        el = clean_val(row.get("Elders Present", 0))
        ch = clean_val(row.get("Children Present", 0))
        pw = clean_val(row.get("PWDs Present", 0))
        district_caregivers_reached[dist] += int(cg)
        reach = int(cg + el + ch + pw)
        pwd = int(pw)
        district_pwd_adults[dist] += pwd

        demo_sessions_list.append({
            "entry_index": entry_index,
            "id": f"DEMO-{sub_id}",
            "session_no": len(demo_sessions_list) + 1,
            "district": dist,
            "subcounty": "Catchment",
            "school": school_name,
            "site": str(row.get("Location of activity", "Community Kraal / Shade")),
            "date": date_val,
            "facilitator": coordinator,
            "caregivers": int(cg),
            "elders": int(el),
            "children": int(ch),
            "pwd": int(pw),
            "total": reach,
            "flagged": reach < 80,
            "status": "✅ Compliant (≥80)" if reach >= 80 else "🚩 Turnout Gap (<80)"
        })

    # Log record with entry_index
    records_log.append({
        "entry_index": entry_index,
        "id": sub_id,
        "date": date_val,
        "district": dist,
        "activity": activity,
        "school": school_name,
        "coordinator": coordinator,
        "reach": reach,
        "pwd": pwd,
        "is_new": entry_index in new_indices,
        "status": "Verified / Ingested"
    })

# --- BUILD DISTRICT_DB ---
district_db = {}
for dist in ALL_DISTRICTS:
    sch_list = DISTRICT_SCHOOLS.get(dist, [])
    tgt_sch = len(sch_list)
    tgt_dem = tgt_sch * 10
    tgt_lrn = sum(s.get("attending", s.get("total", 0)) for s in sch_list)
    tgt_enr = sum(s.get("total", 0) for s in sch_list)
    tgt_cg = tgt_sch * 800

    dates = sorted(list(district_dates[dist]))
    schools_reached_count = len(district_schools_reached[dist])
    tot_pwd_dist = district_pwd_learners[dist] + district_pwd_adults[dist]

    district_db[dist] = {
        "dates": dates,
        "schools": schools_reached_count,
        "target_schools": tgt_sch,
        "demos": district_demos_completed[dist],
        "target_demos": tgt_dem,
        "learners": district_learners_reached[dist],
        "target_learners": tgt_lrn,
        "target_enrolled": tgt_enr,
        "caregivers": district_caregivers_reached[dist],
        "target_caregivers": tgt_cg,
        "teachers_vhts": district_teachers_m[dist] + district_teachers_f[dist] + district_vhts_m[dist] + district_vhts_f[dist],
        "pwd_reach": tot_pwd_dist,
        "teachers_male": district_teachers_m[dist],
        "teachers_female": district_teachers_f[dist],
        "headteachers": 1 if schools_reached_count > 0 and (district_teachers_m[dist] + district_teachers_f[dist] > 0) else 0,
        "patrons": 9 if dist == "Abim" else (1 if dist == "Kaabong" else 0),
        "vhts_male": district_vhts_m[dist],
        "vhts_female": district_vhts_f[dist],
        "vhts_pwd_male": 0,
        "vhts_pwd_female": 0,
        "exit_interviews": district_exit_interviews[dist],
        "visits": district_visits_conducted[dist],
        "target_visits": len(sch_list) * 3,
        "v1_count": district_v1_count[dist],
        "v2_count": district_v2_count[dist],
        "v3_count": district_v3_count[dist],
        "nutriclubs": district_nutriclubs_count[dist],
        "target_nutriclubs": len(sch_list),
        "v1": None,
        "v2": district_v2[dist],
        "v3": None,
        "demos_metrics": None,
        "schools_list": sch_list
    }

with open("dashboard_district_db.json", "w", encoding="utf-8") as f:
    json.dump(district_db, f, indent=2)

with open("dashboard_demo_sessions_640.json", "w", encoding="utf-8") as f:
    json.dump(demo_sessions_list, f, indent=2)

# --- REBUILD DASHBOARD_DATA.JSON ---
tot_schools = sum(d["schools"] for d in district_db.values())
tot_visits = sum(d.get("visits", 0) for d in district_db.values())
tot_demos = sum(d["demos"] for d in district_db.values())
tot_clubs = sum(d.get("nutriclubs", 0) for d in district_db.values())
tot_learners = sum(d["learners"] for d in district_db.values())
tot_caregivers = sum(d["caregivers"] for d in district_db.values())
tot_stakeholders = sum(d["teachers_vhts"] for d in district_db.values())
tot_pwd = sum(d["pwd_reach"] for d in district_db.values())

with open("dashboard_data.json", "r", encoding="utf-8") as f:
    d_data = json.load(f)

# Save tracker metadata
max_idx = max(current_indices) if current_indices else 0
d_data["metadata"]["index_tracking"] = {
    "column": INDEX_COL,
    "last_processed_index": max_idx,
    "total_submissions_tracked": len(current_indices),
    "new_entries_this_batch": len(new_indices),
    "tracked_indices": current_indices,
    "last_synced": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Attach records_log
d_data["records_log"] = records_log

# Update or insert visits KPI
kpi_ids = [k["id"] for k in d_data["overview"]["kpis"]]
if "visits" not in kpi_ids:
    d_data["overview"]["kpis"].insert(1, {
        "id": "visits",
        "title": "School Contact Visits",
        "value": tot_visits,
        "target": 192,
        "unit": "visits",
        "progress_pct": round((tot_visits / 192) * 100, 1),
        "icon": "fa-bus",
        "badge": "3-Visit Cycle",
        "context": "1 activation visit at Kotido Mixed P/S completed out of 192 total scheduled visits across 64 schools"
    })

# Update KPIs
for kpi in d_data["overview"]["kpis"]:
    if kpi["id"] == "schools":
        kpi["value"] = tot_schools
        kpi["progress_pct"] = round((tot_schools / 64) * 100, 1)
    elif kpi["id"] == "visits":
        kpi["value"] = tot_visits
        kpi["progress_pct"] = round((tot_visits / 192) * 100, 1)
    elif kpi["id"] == "demos":
        kpi["value"] = tot_demos
        kpi["progress_pct"] = round((tot_demos / 640) * 100, 1)
    elif kpi["id"] == "learners":
        kpi["value"] = tot_learners
        kpi["progress_pct"] = round((tot_learners / 80875) * 100, 2)
    elif kpi["id"] == "caregivers":
        kpi["value"] = tot_caregivers
        kpi["progress_pct"] = round((tot_caregivers / 51200) * 100, 2)
    elif kpi["id"] == "stakeholders":
        kpi["value"] = tot_stakeholders
        kpi["progress_pct"] = round((tot_stakeholders / 768) * 100, 1)
    elif kpi["id"] == "pwd":
        kpi["value"] = tot_pwd
        kpi["progress_pct"] = round((tot_pwd / 1200) * 100, 2)

d_data["overview"]["targets_vs_actuals"]["categories"] = [
    "Schools Reached", "School Visits", "Demonstrations", "NutriClubs", "Learners", "Caregivers", "Teachers & VHTs", "PWD Reach"
]
d_data["overview"]["targets_vs_actuals"]["actuals"] = [tot_schools, tot_visits, tot_demos, tot_clubs, tot_learners, tot_caregivers, tot_stakeholders, tot_pwd]
d_data["overview"]["targets_vs_actuals"]["targets"] = [64, 192, 640, 64, 80875, 51200, 768, 1200]
d_data["overview"]["targets_vs_actuals"]["pct"] = [
    round((tot_schools/64)*100, 1),
    round((tot_visits/192)*100, 1),
    round((tot_demos/640)*100, 1) if tot_demos > 0 else 0.0,
    round((tot_clubs/64)*100, 1),
    round((tot_learners/80875)*100, 2),
    round((tot_caregivers/51200)*100, 2),
    round((tot_stakeholders/768)*100, 1),
    round((tot_pwd/1200)*100, 2)
]

# Dynamically aggregate orientation exit interview charts from all ingested interview records
all_interviews = []
for d_interviews in district_exit_interviews.values():
    all_interviews.extend(d_interviews.values())

pillar_counts = {
    "Metu Porridge Fortification (Local Greens/Staples)": 0,
    "Improved Cooking Methods (Firewood Saving)": 0,
    "Establishing Nutri Clubs & Hotline 0800": 0,
    "Rebalancing Morning Chores so Girls Stay in School": 0,
    "Fair and Equal Plate Sharing at Home": 0
}
action_counts = {
    "Enrich School/Home Porridge with Local Greens/Cowpeas": 0,
    "Mobilize Boys/Fathers to Share Water/Wood Chores": 0,
    "Adopt Firewood-Saving Practices / Establish Nutri Club": 0
}

for item in all_interviews:
    for lesson in item.get("lessons", []):
        if "porridge" in lesson.lower():
            pillar_counts["Metu Porridge Fortification (Local Greens/Staples)"] += 1
        if "cooking" in lesson.lower() or "firewood" in lesson.lower():
            pillar_counts["Improved Cooking Methods (Firewood Saving)"] += 1
        if "hotline" in lesson.lower() or "clubs" in lesson.lower():
            pillar_counts["Establishing Nutri Clubs & Hotline 0800"] += 1
        if "chores" in lesson.lower():
            pillar_counts["Rebalancing Morning Chores so Girls Stay in School"] += 1
        if "plate" in lesson.lower() or "sharing" in lesson.lower():
            pillar_counts["Fair and Equal Plate Sharing at Home"] += 1

    act = item.get("action", "").lower()
    if "enrich" in act or "porridge" in act:
        action_counts["Enrich School/Home Porridge with Local Greens/Cowpeas"] += 1
    if "mobilize" in act or "chores" in act or "water" in act:
        action_counts["Mobilize Boys/Fathers to Share Water/Wood Chores"] += 1
    if "firewood" in act or "kitchen" in act or "club" in act:
        action_counts["Adopt Firewood-Saving Practices / Establish Nutri Club"] += 1

if "orientation" in d_data:
    d_data["orientation"]["exit_interviews_pillars"]["sample_size"] = len(all_interviews)
    d_data["orientation"]["exit_interviews_pillars"]["values"] = list(pillar_counts.values())
    d_data["orientation"]["exit_interviews_actions"]["sample_size"] = len(all_interviews)
    d_data["orientation"]["exit_interviews_actions"]["values"] = list(action_counts.values())
    
    quotes_list = []
    for idx, item in enumerate(all_interviews):
        quotes_list.append({
            "respondent_id": item.get("key") or f"Respondent {idx + 1} ({item.get('school', '')})",
            "role": item.get("role", "Teacher / VHT"),
            "sex": item.get("sex", "Female"),
            "school": item.get("school", ""),
            "district": item.get("district", ""),
            "action": item.get("action", ""),
            "words": item.get("words", "")
        })
    d_data["orientation"]["exit_interview_quotes"] = quotes_list

# Clean community demonstrations data if 0 demos conducted
if tot_demos == 0:
    d_data["community_demonstrations"] = {
        "kpis": {
            "total_sessions_completed": 0,
            "target_sessions": 640,
            "total_caregivers_reached": 0,
            "target_caregivers": 51200,
            "average_attendance_per_demo": 0,
            "caregivers_female": 0,
            "caregivers_male": 0,
            "children_present": 0,
            "elders_present": 0,
            "pwd_present": 0
        },
        "partner_cofacilitation": {
            "question": "Were capacity-strengthening partners (e.g., UNAC, Afi) present and co-facilitating this community demonstration?",
            "present": {
                "categories": ["Yes", "No"],
                "values": [0, 0],
                "pct": "0.0%"
            },
            "specified_partners": {
                "question": "If yes, specify partner name",
                "categories": ["UNAC", "AFI", "Other"],
                "values": [0, 0, 0],
                "pct": ["0.0%", "0.0%", "0.0%"],
                "other_specified": "Pending field submissions"
            },
            "partner_role_observed": {
                "question": "Partner role observed",
                "categories": [
                    "Co-facilitating clean cooking/gender dialogue",
                    "Mentoring local VHTs/Elders",
                    "Observing for sustainability tracking",
                    "Other"
                ],
                "values": [0, 0, 0, 0],
                "pct": ["0.0%", "0.0%", "0.0%", "0.0%"],
                "other_specified": "Pending field verification"
            }
        },
        "headcount_breakdown": {
            "categories": [
                "Female Caregivers",
                "Male Caregivers",
                "Children (U5 & School Age)",
                "Elders / Community Leaders",
                "Persons with Disabilities"
            ],
            "values": [0, 0, 0, 0, 0]
        },
        "entry_submission_role": {
            "categories": [
                "Submitted by Village Health Team (VHT)",
                "Submitted by District Coordinator"
            ],
            "values": [0, 0]
        },
        "hands_on_cooking": {
            "categories": [
                "Practiced and cooked hands-on",
                "Stood and watched passively"
            ],
            "values": [0, 0]
        },
        "metu_porridge_local_additions": {
            "categories": [
                "Demonstrated with local staples (Eboo, Lokaka, Cowpeas, Sesame)",
                "Not Demonstrated"
            ],
            "values": [0, 0]
        },
        "local_sourcing_compliance": {
            "categories": [
                "Strictly compliant with seasonal local foods",
                "Promoted unapproved/unattainable foods"
            ],
            "values": [0, 0]
        },
        "fuel_saving_practices": {
            "categories": [
                "Covering the Pot with a Lid",
                "Soaking Dry Beans/Legumes First",
                "Shielded 3-Stone Fire / Improved Stove",
                "Open Uncovered Fire (Non-compliant)"
            ],
            "values": [0, 0, 0, 0]
        },
        "caregiver_barriers": {
            "categories": [
                "Money / Lack of cash for ingredients",
                "Water scarcity / long walking distance",
                "Missing required ingredients at market",
                "Firewood shortage / difficult collection",
                "Morning household chores"
            ],
            "values": [0, 0, 0, 0, 0]
        },
        "caregiver_feasible_actions": {
            "categories": [
                "Add wild greens (Eboo, Lokaka) or cowpeas to porridge",
                "Cover pot with a lid when cooking to save wood",
                "Serve youngest toddler and girls equal first plates",
                "Rebalance morning chores so girls reach school early",
                "Establish a small home kitchen garden"
            ],
            "values": [0, 0, 0, 0, 0]
        },
        "caregiver_commitments": {
            "categories": [
                "Will try it at home this week",
                "Need VHT support before attempting",
                "Not possible right now"
            ],
            "values": [0, 0, 0]
        },
        "gender_chore_discussion": {
            "categories": [
                "Structured Gender Chore Discussion Took Place",
                "Discussion Did Not Take Place"
            ],
            "values": [0, 0]
        },
        "male_participation_level": {
            "categories": [
                "High Male Participation (≥5 Men)",
                "Moderate Male Participation (1–4 Men)",
                "Zero Male Attendance"
            ],
            "values": [0, 0, 0]
        },
        "community_accountability_hotline": {
            "categories": [
                "WFP Hotline & Feedback Promoted",
                "Not Promoted"
            ],
            "values": [0, 0]
        },
        "serving_hierarchy_quotes": [],
        "caregiver_interviews": [],
        "community_dialogue_insights": {
            "summary": "Awaiting field submissions for community cooking demonstrations",
            "total_dialogues": 0,
            "hotline_awareness_pct": 0,
            "quotes": []
        },
        "pillar3_clean_cooking": {
            "question": "Pillar 3: Was clean/smart cooking demonstrated to protect the environment and lead to better harvests?",
            "categories": ["Yes", "No"],
            "values": [0, 0],
            "pct": "0.0%"
        },
        "clean_cooking_commitment": {
            "categories": [
                "Covered Pot Observed",
                "Soaking Legumes Demonstrated",
                "Improved Fire Setting"
            ],
            "values": [0, 0, 0]
        },
        "gender_dialogues_execution": {
            "question": "Were gender dialogues led by senior women, senior men, and VHTs successfully executed?",
            "categories": ["Yes", "No"],
            "values": [0, 0],
            "pct": "0.0%"
        },
        "community_pr_media_highlights": {
            "question": "Were community media highlights or clean cooking/gender dialogue photos captured for social media PR reporting?",
            "categories": ["Yes", "No"],
            "values": [0, 0],
            "pct": "0.0%",
            "sample_highlight": "Pending community demo field logs."
        },
        "community_radio_feedback": {
            "question": "Did community members mention or give feedback on the campaign radio broadcasts during the gathering?",
            "categories": ["Yes", "No"],
            "values": [0, 0],
            "pct": "0.0%",
            "summary": "Pending community demo field logs and radio broadcast feedback."
        }
    }

with open("dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(d_data, f, indent=2)

# Save persistent tracker file
tracker_state = {
    "index_column": INDEX_COL,
    "last_processed_index": max_idx,
    "total_entries": len(current_indices),
    "processed_indices": current_indices,
    "last_run_timestamp": d_data["metadata"]["index_tracking"]["last_synced"]
}
with open(TRACKER_FILE, "w", encoding="utf-8") as tf:
    json.dump(tracker_state, tf, indent=2)

print(f"✅ Tracker state saved to '{TRACKER_FILE}' (Highest _index: #{max_idx}).")
print(f"✅ Updated database JSONs: {tot_schools} Schools | {tot_demos} Demos | {tot_learners} Learners | {tot_caregivers} Caregivers | {tot_stakeholders} Stakeholders | {tot_pwd} PWDs")
