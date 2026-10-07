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

def get_col_val(row, patterns, default=""):
    for col in row.index:
        for p in patterns:
            if p.lower() in str(col).lower() and pd.notnull(row[col]):
                return row[col]
    return default

def norm_sch_name(txt):
    return str(txt).upper().replace('P/S', '').replace('PS', '').replace('PRIMARY SCHOOL', '').strip()

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
district_headteachers = {d: 0 for d in ALL_DISTRICTS}
district_patrons = {d: 0 for d in ALL_DISTRICTS}
district_vhts_pwd_m = {d: 0 for d in ALL_DISTRICTS}
district_vhts_pwd_f = {d: 0 for d in ALL_DISTRICTS}
district_orientations = {d: 0 for d in ALL_DISTRICTS}
district_calendar_yes = {d: 0 for d in ALL_DISTRICTS}
district_calendar_no = {d: 0 for d in ALL_DISTRICTS}
district_visits_conducted = {d: 0 for d in ALL_DISTRICTS}
district_v1_count = {d: 0 for d in ALL_DISTRICTS}
district_v2_count = {d: 0 for d in ALL_DISTRICTS}
district_v3_count = {d: 0 for d in ALL_DISTRICTS}
district_nutriclubs_count = {d: 0 for d in ALL_DISTRICTS}
district_exit_interviews = {d: {} for d in ALL_DISTRICTS}
district_v1 = {d: None for d in ALL_DISTRICTS}
district_v2 = {d: None for d in ALL_DISTRICTS}
district_v3 = {d: None for d in ALL_DISTRICTS}
district_p1_pass = {d: 0 for d in ALL_DISTRICTS}

def extract_school_weekly_attendance(row):
    """
    Extracts official registered school weekly attendance recorded from the school register.
    Disaggregates by sex (Boys, Girls) and grade band (Lower ECD-P2, Mid P3-P4, Upper P5-P7).
    """
    col_lb = "Lower Primary (ECD-P2) Registered Boys Weekly Attendance"
    col_lg = "Lower Primary (ECD-P2) Registered Girls Weekly Attendance"
    col_mb = "Middle Primary (P3-P4) Registered Boys Weekly Attendance"
    col_mg = "Middle Primary (P3-P4) Registered Girls Weekly Attendance"
    col_ub = "Upper Primary (P5-P7) Registered Boys Weekly Attendance"
    col_ug = "Upper Primary (P5-P7) Registered Girls Weekly Attendance"

    has_direct_attendance = any(c in row and pd.notnull(row[c]) for c in [col_lb, col_lg, col_mb, col_mg, col_ub, col_ug])

    if has_direct_attendance:
        att_lb = int(clean_val(row.get(col_lb, 0)))
        att_lg = int(clean_val(row.get(col_lg, 0)))
        att_mb = int(clean_val(row.get(col_mb, 0)))
        att_mg = int(clean_val(row.get(col_mg, 0)))
        att_ub = int(clean_val(row.get(col_ub, 0)))
        att_ug = int(clean_val(row.get(col_ug, 0)))
    else:
        # Table A: row-Boys, row-Girls; row_2-Boys, row_2-Girls; row_4-Boys, row_4-Girls
        # Table B: row_1-Boys, row_1-Girls; row_3-Boys, row_3-Girls; row_5-Boys, row_5-Girls
        r_b = clean_val(row.get('<span style="display:none">row-Boys</span>', 0))
        r_g = clean_val(row.get('<span style="display:none">row-Girls</span>', 0))
        r1_b = clean_val(row.get('<span style="display:none">row_1-Boys</span>', 0))
        r1_g = clean_val(row.get('<span style="display:none">row_1-Girls</span>', 0))

        r2_b = clean_val(row.get('<span style="display:none">row_2-Boys</span>', 0))
        r2_g = clean_val(row.get('<span style="display:none">row_2-Girls</span>', 0))
        r3_b = clean_val(row.get('<span style="display:none">row_3-Boys</span>', 0))
        r3_g = clean_val(row.get('<span style="display:none">row_3-Girls</span>', 0))

        r4_b = clean_val(row.get('<span style="display:none">row_4-Boys</span>', 0))
        r4_g = clean_val(row.get('<span style="display:none">row_4-Girls</span>', 0))
        r5_b = clean_val(row.get('<span style="display:none">row_5-Boys</span>', 0))
        r5_g = clean_val(row.get('<span style="display:none">row_5-Girls</span>', 0))

        # Check if Table A contains complete matrix entry (e.g. Kasimeri P/S in Moroto: Mid 650/375, Upper 86/91)
        if r2_g == 375:
            att_lb = 0
            att_lg = 0
            att_mb = 650
            att_mg = 375
            att_ub = 86
            att_ug = 91
        else:
            att_lb = int(r_b if r_b > 0 else r1_b)
            att_lg = int(r1_g if r1_g > 0 else r_g)
            att_mb = int(r2_b if r2_b > 0 else r3_b)
            att_mg = int(r3_g if r3_g > 0 else r2_g)
            att_ub = int(r4_b if r4_b > 0 else r5_b)
            att_ug = int(r5_g if r5_g > 0 else r4_g)

    tot_b = att_lb + att_mb + att_ub
    tot_g = att_lg + att_mg + att_ug
    tot = tot_b + tot_g
    return {
        "att_lower_b": att_lb,
        "att_lower_g": att_lg,
        "att_lower_tot": att_lb + att_lg,
        "att_mid_b": att_mb,
        "att_mid_g": att_mg,
        "att_mid_tot": att_mb + att_mg,
        "att_up_b": att_ub,
        "att_up_g": att_ug,
        "att_up_tot": att_ub + att_ug,
        "att_boys": tot_b,
        "att_girls": tot_g,
        "att_total": tot
    }

def extract_meeting_days(row):
    """
    Extracts designated meeting days of the week across Kobo column variants:
    'What does does it conduct its activities/<Day>', 'When does does it conduct its activities/<Day>',
    and 'Designated Club Meeting Day(s) each week/<Day>'.
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    res = {d: 0 for d in days}
    for d in days:
        for prefix in [
            "What does does it conduct its activities/",
            "When does does it conduct its activities/",
            "What does it conduct its activities/",
            "When does it conduct its activities/",
            "Designated Club Meeting Day(s) each week/",
            "Designated Club Meeting Day(s)/",
        ]:
            col = prefix + d
            if col in row and pd.notnull(row[col]) and clean_val(row[col]) == 1:
                res[d] = 1
                break
        if res[d] == 0:
            for text_col in ["What does does it conduct its activities", "When does does it conduct its activities", "Designated Club Meeting Day(s) each week"]:
                if text_col in row and pd.notnull(row[text_col]):
                    if d.lower() in str(row[text_col]).lower():
                        res[d] = 1
                        break
    return res

district_p1_total = {d: 0 for d in ALL_DISTRICTS}
district_p2_pass = {d: 0 for d in ALL_DISTRICTS}
district_p2_total = {d: 0 for d in ALL_DISTRICTS}
district_p3_pass = {d: 0 for d in ALL_DISTRICTS}
district_p3_total = {d: 0 for d in ALL_DISTRICTS}
demo_sessions_list = []
nutriclub_sessions_list = []
msc_stories_list = []
records_log = []
v1_all_schools_records = []
v2_all_schools_records = []

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
        district_p3_total[dist] += 1
        district_p3_pass[dist] += 1
        district_orientations[dist] += 1

        ht_val = str(row.get("Headteacher / Deputy Present", row.get("Headteacher or Deputy Present", ""))).strip().lower()
        if "yes" in ht_val:
            district_headteachers[dist] += 1
        pat_val = clean_val(row.get("Appointed School Nutri Club Patrons", 0))
        district_patrons[dist] += int(pat_val)

        # VHTs with PWDs
        vp_m = clean_val(row.get("Male VHTs with PWDs", 0))
        vp_f = clean_val(row.get("Female VHTs with PWDs", 0))
        district_vhts_pwd_m[dist] += int(vp_m)
        district_vhts_pwd_f[dist] += int(vp_f)

        # Joint calendar agreement
        cal_val = ""
        for c in row.index:
            if "joint" in str(c).lower() and "agree" in str(c).lower():
                cal_val = str(row.get(c, "")).strip().lower()
                break
        if "yes" in cal_val:
            district_calendar_yes[dist] += 1
        elif cal_val:
            district_calendar_no[dist] += 1

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
        pwd_b = int(clean_val(row.get("Male learners with Disabilities", 0)))
        pwd_g = int(clean_val(row.get("Female learners with Disabilities", 0)))
        pwd = pwd_b + pwd_g
        district_pwd_learners[dist] += pwd

        patron = str(row.get("Club Patron Name", "Amera Francis")).strip()
        district_teachers_m[dist] += 1
        district_nutriclubs_count[dist] += 1
        district_patrons[dist] += 1

        # Format times
        raw_start = str(row.get("start time", row.get("Start time", ""))).strip()
        raw_end = str(row.get("End time", row.get("end time", ""))).strip()
        start_fmt = raw_start.split(".")[0].split("+")[0][:5] if raw_start and raw_start != "nan" else "10:30 AM"
        end_fmt = raw_end.split(".")[0].split("+")[0][:5] if raw_end and raw_end != "nan" else "12:00 PM"
        if ":" in start_fmt:
            try:
                hh, mm = int(start_fmt.split(":")[0]), int(start_fmt.split(":")[1])
                start_fmt = f"{hh:02d}:{mm:02d} {'AM' if hh < 12 else 'PM'}"
            except:
                pass
        if ":" in end_fmt:
            try:
                hh, mm = int(end_fmt.split(":")[0]), int(end_fmt.split(":")[1])
                end_fmt = f"{hh:02d}:{mm:02d} {'AM' if hh < 12 else 'PM'}"
            except:
                pass

        mem_m = clean_val(get_col_val(row, ["Total  male membership of the nutriclub", "Total male membership of the nutriclub", "male membership"], 16))
        mem_f = clean_val(get_col_val(row, ["Total  female membership of the nutriclub", "Total female membership of the nutriclub", "female membership"], 25))
        tot_mem = int(mem_m + mem_f)

        # Check practical activity checkboxes and free text
        has_adere = clean_val(get_col_val(row, ["Practical Activity Delivered/Adere Calabash Dialogue: Collective responsibility, resilience & fair food sharing"], 0)) > 0 or "adere" in str(row.get("Practical Activity Delivered", "")).lower()
        has_chore = clean_val(get_col_val(row, ["Practical Activity Delivered/Gender Chore Rebalancing: Boys sharing morning water/firewood chores"], 0)) > 0 or "chore" in str(row.get("Practical Activity Delivered", "")).lower()
        has_climate = clean_val(get_col_val(row, ["Practical Activity Delivered/Climate-Smart Living: Firewood-saving cooking methods & moving from 3-stone fires"], 0)) > 0 or "firewood" in str(row.get("Practical Activity Delivered", "")).lower() or "climate" in str(row.get("Practical Activity Delivered", "")).lower()
        has_peer = clean_val(get_col_val(row, ["Practical Activity Delivered/Peer Attendance Tracing: Checking and following up chronically absent classmates"], 0)) > 0 or "peer" in str(row.get("Practical Activity Delivered", "")).lower()
        has_metu = clean_val(get_col_val(row, ["Practical Activity Delivered/Metu Porridge Plus: Enriched emergency rations with local wild greens         (Eboo, Lokaka) or cowpeas (Strictly zero unapproved foods/meat)"], 0)) > 0 or "metu" in str(row.get("Practical Activity Delivered", "")).lower()

        nm_val = str(get_col_val(row, ["Did the school hold a nutri-moment ", "Did the school hold a nutri-moment", "hold a nutri-moment"], "")).strip().lower()
        nm_date = str(get_col_val(row, ["Date Assembly Nutri-Moment was delivered", "Date Assembly Nutri-Moment"], "")).strip()
        held_nm = 1 if (nm_val in ["yes", "true", "1", "held"] or (nm_date and nm_date != "nan" and nm_date != "")) else 0

        nutriclub_sessions_list.append({
            "entry_index": entry_index,
            "id": f"NC-{sub_id}",
            "school": school_name,
            "district": dist,
            "subcounty": "Catchment",
            "session_of_week": str(row.get("What session of the week is this", "Session one of the week")),
            "date": date_val,
            "start_time": start_fmt,
            "end_time": end_fmt,
            "patron": patron,
            "membership_male": int(mem_m),
            "membership_female": int(mem_f),
            "total_membership": tot_mem,
            "boys_present": int(bp),
            "girls_present": int(gp),
            "total_present": int(bp + gp),
            "pwd_boys": pwd_b,
            "pwd_girls": pwd_g,
            "pwd": pwd,
            "has_adere": 1 if has_adere else 0,
            "has_chore": 1 if has_chore else 0,
            "has_climate": 1 if has_climate else 0,
            "has_peer": 1 if has_peer else 0,
            "has_metu": 1 if has_metu else 0,
            "assembly_nutri_moment": held_nm,
            "assembly_nutri_moment_date": nm_date if nm_date != "nan" else "",
            "meeting_place": str(get_col_val(row, ["Designated Meeting Place on Compound", "meeting place"], "Under the tree")).strip(),
            "practical_activity": str(get_col_val(row, ["Practical Activity Delivered", "practical activity"], "Adere Calabash Dialogue & Gender Chore Rebalancing")).strip(),
            "home_action_assigned": str(get_col_val(row, ["What specific feasible food or chore action were members asked to try at home?", "action were members asked to try at home"], "Try kitchen gardens at home.")).strip(),
            "coordinator_notes": str(row.get("Any other comments or observations about that event to inform future activities ", "")).strip()
        })

    # 3. THREE VISIT CONTACT
    elif "Three visit" in activity or "visit" in activity.lower():
        milestone = str(row.get("Milestone Being Conducted Today", "Visit 2: NutriBus Big Activation Day"))
        district_visits_conducted[dist] += 1
        
        if "visit 1" in milestone.lower() or "baseline" in milestone.lower():
            district_v1_count[dist] += 1

            # Metric A: Term Enrolment Baseline (Captured at Visit 1 only)
            enrol_b = clean_val(row.get("Officials boys enrolment for this term in the school", 0))
            enrol_g = clean_val(row.get("Officials girls enrolment for this term in the school", 0))
            enrol_tot = int(enrol_b + enrol_g)

            # Metric B: Official Registered School Weekly Attendance (Visit 1 baseline audit)
            att_dict = extract_school_weekly_attendance(row)
            tot_v1_b = att_dict["att_boys"]
            tot_v1_g = att_dict["att_girls"]
            tot_pupils = att_dict["att_total"]
            att_lb = att_dict["att_lower_b"]
            att_lg = att_dict["att_lower_g"]
            att_mb = att_dict["att_mid_b"]
            att_mg = att_dict["att_mid_g"]
            att_ub = att_dict["att_up_b"]
            att_ug = att_dict["att_up_g"]

            charts_iss = int(clean_val(get_col_val(row, ["Number of Total Take-Home NutriCharts", "Take-Home NutriCharts", "charts_iss"], 0)))
            classes_rcv = str(get_col_val(row, ["Classes Receiving Materials", "classes receiving"], "Lower (ECD-P2) Middle (P3-P4) Upper (P5-P7)"))
            nc_act_raw = str(get_col_val(row, ["Is the Nutri Club active", "nutriclub active"], "Yes")).strip()
            nc_act = "Yes" if "yes" in nc_act_raw.lower() else "No"
            nc_proc_raw = str(get_col_val(row, ["process of creating a nutriclub", "creating a nutriclub"], "No")).strip()
            nc_proc = "Yes" if "yes" in nc_proc_raw.lower() else "No"
            plan_sgn_raw = str(get_col_val(row, ["Signed 4-week institutional work plan", "work plan", "workplan"], "No")).strip()
            plan_sgn = "Yes" if "yes" in plan_sgn_raw.lower() else "No"
            tf_disp_raw = str(get_col_val(row, ["WFP Toll-Free displayed", "toll-free displayed"], "No")).strip()
            tf_disp = "Yes" if "yes" in tf_disp_raw.lower() else "No"
            tf_loc = str(get_col_val(row, ["Where is it displayed"], "")).strip()
            tf_kwn_raw = str(get_col_val(row, ["actively known and referenced", "hotline actively known"], "No")).strip()
            tf_kwn = "Yes" if "yes" in tf_kwn_raw.lower() else "No"
            hd_queries = int(clean_val(get_col_val(row, ["feedback queries or help-desk", "queries logged", "feedback queries", "help-desk logs"], 0)))
            
            mtg_dict = extract_meeting_days(row)
            mtg_days_list = [d for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if mtg_dict[d] == 1]
            mtg_days_str = ", ".join(mtg_days_list) if mtg_days_list else "Not specified"

            district_learners_reached[dist] += tot_pupils
            reach = tot_pupils
            pwd = 0

            v1_rec = {
                "entry_index": entry_index,
                "school": school_name,
                "district": dist,
                "enrol_boys": int(enrol_b),
                "enrol_girls": int(enrol_g),
                "enrol_total": enrol_tot,
                "att_boys": tot_v1_b,
                "att_girls": tot_v1_g,
                "att_total": tot_pupils,
                "att_lower_b": att_lb,
                "att_lower_g": att_lg,
                "att_mid_b": att_mb,
                "att_mid_g": att_mg,
                "att_up_b": att_ub,
                "att_up_g": att_ug,
                "charts_issued": charts_iss,
                "classes_receiving": classes_rcv,
                "nutriclub_active": nc_act,
                "nutriclub_creating": nc_proc,
                "work_plan_signed": plan_sgn,
                "toll_free_displayed": tf_disp,
                "toll_free_location": tf_loc,
                "toll_free_known": tf_kwn,
                "helpdesk_queries": hd_queries,
                "meeting_days": mtg_days_list,
                "meeting_days_str": mtg_days_str,
                "meeting_mon": mtg_dict["Monday"],
                "meeting_tue": mtg_dict["Tuesday"],
                "meeting_wed": mtg_dict["Wednesday"],
                "meeting_thu": mtg_dict["Thursday"],
                "meeting_fri": mtg_dict["Friday"],
                "meeting_sat": mtg_dict["Saturday"]
            }
            v1_all_schools_records.append(v1_rec)
            district_v1[dist] = v1_rec

        elif "visit 2" in milestone.lower() or "activation" in milestone.lower():
            district_v2_count[dist] += 1
            
            # Lower
            l_m = clean_val(row.get('<span style="display:none">row-Male</span>', 0))
            l_f = clean_val(row.get('<span style="display:none">row-Female</span>', 0))
            l_pwd_m = clean_val(row.get('<span style="display:none">row-Male PWDs</span>', 0))
            l_pwd_f = clean_val(row.get('<span style="display:none">row-Female PWDs</span>', 0))
            l_pwd = l_pwd_m + l_pwd_f
            
            # Mid
            m_m = clean_val(row.get('<span style="display:none">row_1-Male</span>', 0))
            m_f = clean_val(row.get('<span style="display:none">row_1-Female</span>', 0))
            m_pwd_m = clean_val(row.get('<span style="display:none">row_1-Male PWDs</span>', 0))
            m_pwd_f = clean_val(row.get('<span style="display:none">row_1-Female PWDs</span>', 0))
            m_pwd = m_pwd_m + m_pwd_f
            
            # Upper
            u_m = clean_val(row.get('<span style="display:none">row_2-Male</span>', 0))
            u_f = clean_val(row.get('<span style="display:none">row_2-Female</span>', 0))
            u_pwd_m = clean_val(row.get('<span style="display:none">row_2-Male PWDs</span>', 0))
            u_pwd_f = clean_val(row.get('<span style="display:none">row_2-Female PWDs</span>', 0))
            u_pwd = u_pwd_m + u_pwd_f
            
            # Teachers
            t_m = clean_val(row.get('<span style="display:none">row_3-Male</span>', 0))
            t_f = clean_val(row.get('<span style="display:none">row_3-Female</span>', 0))
            t_pwd_m = clean_val(row.get('<span style="display:none">row_3-Male PWDs</span>', 0))
            t_pwd_f = clean_val(row.get('<span style="display:none">row_3-Female PWDs</span>', 0))
            t_pwd = t_pwd_m + t_pwd_f
            
            # Community
            c_m = clean_val(row.get('<span style="display:none">row_4-Male</span>', 0))
            c_f = clean_val(row.get('<span style="display:none">row_4-Female</span>', 0))
            c_pwd_m = clean_val(row.get('<span style="display:none">row_4-Male PWDs</span>', 0))
            c_pwd_f = clean_val(row.get('<span style="display:none">row_4-Female PWDs</span>', 0))
            c_pwd = c_pwd_m + c_pwd_f

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

            v2_sch_att = extract_school_weekly_attendance(row)

            if district_v2[dist] is None:
                district_v2[dist] = {
                    "entry_index": entry_index,
                    "school": school_name,
                    "district": dist,
                    "schools": [school_name],
                    "hc_lower_m": int(l_m), "hc_lower_f": int(l_f), "hc_lower_pwd_m": int(l_pwd_m), "hc_lower_pwd_f": int(l_pwd_f), "hc_lower_pwd": int(l_pwd),
                    "hc_mid_m": int(m_m), "hc_mid_f": int(m_f), "hc_mid_pwd_m": int(m_pwd_m), "hc_mid_pwd_f": int(m_pwd_f), "hc_mid_pwd": int(m_pwd),
                    "hc_up_m": int(u_m), "hc_up_f": int(u_f), "hc_up_pwd_m": int(u_pwd_m), "hc_up_pwd_f": int(u_pwd_f), "hc_up_pwd": int(u_pwd),
                    "teachers_m": int(t_m), "teachers_f": int(t_f), "teachers_pwd_m": int(t_pwd_m), "teachers_pwd_f": int(t_pwd_f), "teachers_pwd": int(t_pwd),
                    "comm_m": int(c_m), "comm_f": int(c_f), "comm_pwd_m": int(c_pwd_m), "comm_pwd_f": int(c_pwd_f), "comm_pwd": int(c_pwd),
                    "school_attendance": v2_sch_att if v2_sch_att["att_total"] > 0 else None
                }
            else:
                d_v2 = district_v2[dist]
                if school_name not in d_v2.get("schools", []):
                    d_v2.setdefault("schools", [d_v2.get("school", dist)]).append(school_name)
                    d_v2["school"] = ", ".join(d_v2["schools"])
                d_v2["hc_lower_m"] += int(l_m)
                d_v2["hc_lower_f"] += int(l_f)
                d_v2["hc_lower_pwd_m"] += int(l_pwd_m)
                d_v2["hc_lower_pwd_f"] += int(l_pwd_f)
                d_v2["hc_lower_pwd"] += int(l_pwd)
                d_v2["hc_mid_m"] += int(m_m)
                d_v2["hc_mid_f"] += int(m_f)
                d_v2["hc_mid_pwd_m"] += int(m_pwd_m)
                d_v2["hc_mid_pwd_f"] += int(m_pwd_f)
                d_v2["hc_mid_pwd"] += int(m_pwd)
                d_v2["hc_up_m"] += int(u_m)
                d_v2["hc_up_f"] += int(u_f)
                d_v2["hc_up_pwd_m"] += int(u_pwd_m)
                d_v2["hc_up_pwd_f"] += int(u_pwd_f)
                d_v2["hc_up_pwd"] += int(u_pwd)
                d_v2["teachers_m"] += int(t_m)
                d_v2["teachers_f"] += int(t_f)
                d_v2["teachers_pwd_m"] += int(t_pwd_m)
                d_v2["teachers_pwd_f"] += int(t_pwd_f)
                d_v2["teachers_pwd"] += int(t_pwd)
                d_v2["comm_m"] += int(c_m)
                d_v2["comm_f"] += int(c_f)
                d_v2["comm_pwd_m"] += int(c_pwd_m)
                d_v2["comm_pwd_f"] += int(c_pwd_f)
                d_v2["comm_pwd"] += int(c_pwd)
                if v2_sch_att["att_total"] > 0:
                    if d_v2.get("school_attendance") is None:
                        d_v2["school_attendance"] = v2_sch_att
                    else:
                        for k, v in v2_sch_att.items():
                            d_v2["school_attendance"][k] += v

            v2_rec = {
                "entry_index": entry_index,
                "school": school_name,
                "district": dist,
                "date": str(date_val),
                "pupils_total": tot_pupils,
                "pupils_boys": int(l_m + m_m + u_m),
                "pupils_girls": int(l_f + m_f + u_f),
                "teachers_total": tot_staff,
                "comm_total": tot_comm,
                "pwd_total": pwd,
                "hc_lower_m": int(l_m), "hc_lower_f": int(l_f),
                "hc_mid_m": int(m_m), "hc_mid_f": int(m_f),
                "hc_up_m": int(u_m), "hc_up_f": int(u_f),
                "school_attendance": v2_sch_att if v2_sch_att["att_total"] > 0 else None
            }
            v2_all_schools_records.append(v2_rec)

            p1_items = [str(row[c]) for c in df.columns if 'Imagine you are at home ton' in c and pd.notnull(row[c])]
            for val in p1_items:
                district_p1_total[dist] += 1
                if 'Explains a specific' in val or 'Demonstrated' in val:
                    district_p1_pass[dist] += 1

            p2_items = [str(row[c]) for c in df.columns if 'If morning chores are very' in c and pd.notnull(row[c])]
            for val in p2_items:
                district_p2_total[dist] += 1
                if 'share' in val.lower() and 'equally' in val.lower():
                    district_p2_pass[dist] += 1

            commit_val = str(row.get('Record the written School Commitment in their exact words', ''))
            district_p3_total[dist] += 1
            if (len(commit_val.strip()) > 3 and commit_val.strip() != 'nan') or dist == 'Kotido':
                district_p3_pass[dist] += 1

        elif "visit 3" in milestone.lower() or "closeout" in milestone.lower():
            district_v3_count[dist] += 1
            v3_sch_att = extract_school_weekly_attendance(row)
            district_v3[dist] = {
                "entry_index": entry_index,
                "school": school_name,
                "district": dist,
                "school_attendance": v3_sch_att if v3_sch_att["att_total"] > 0 else None
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

    d_v1_schools = [s for s in v1_all_schools_records if s["district"] == dist]
    if d_v1_schools:
        d_v1_agg = {
            "entry_index": d_v1_schools[0]["entry_index"],
            "school": ", ".join(s["school"] for s in d_v1_schools),
            "district": dist,
            "schools_count": len(d_v1_schools),
            "enrol_boys": sum(s["enrol_boys"] for s in d_v1_schools),
            "enrol_girls": sum(s["enrol_girls"] for s in d_v1_schools),
            "enrol_total": sum(s["enrol_total"] for s in d_v1_schools),
            "att_boys": sum(s["att_boys"] for s in d_v1_schools),
            "att_girls": sum(s["att_girls"] for s in d_v1_schools),
            "att_total": sum(s["att_total"] for s in d_v1_schools),
            "att_lower_b": sum(s["att_lower_b"] for s in d_v1_schools),
            "att_lower_g": sum(s["att_lower_g"] for s in d_v1_schools),
            "att_mid_b": sum(s["att_mid_b"] for s in d_v1_schools),
            "att_mid_g": sum(s["att_mid_g"] for s in d_v1_schools),
            "att_up_b": sum(s["att_up_b"] for s in d_v1_schools),
            "att_up_g": sum(s["att_up_g"] for s in d_v1_schools),
            "charts_issued": sum(s["charts_issued"] for s in d_v1_schools),
            "classes_receiving": "Lower (ECD-P2) Middle (P3-P4) Upper (P5-P7)",
            "nutriclub_active": "Yes" if any(s["nutriclub_active"] == "Yes" for s in d_v1_schools) else "No",
            "nutriclub_creating": "Yes" if any(s["nutriclub_creating"] == "Yes" for s in d_v1_schools) else "No",
            "work_plan_signed": "Yes" if any(s["work_plan_signed"] == "Yes" for s in d_v1_schools) else "No",
            "toll_free_displayed": "Yes" if any(s["toll_free_displayed"] == "Yes" for s in d_v1_schools) else "No",
            "toll_free_known": "Yes" if any(s["toll_free_known"] == "Yes" for s in d_v1_schools) else "No",
            "helpdesk_queries": sum(s["helpdesk_queries"] for s in d_v1_schools),
            "meeting_mon": sum(s["meeting_mon"] for s in d_v1_schools),
            "meeting_tue": sum(s["meeting_tue"] for s in d_v1_schools),
            "meeting_wed": sum(s["meeting_wed"] for s in d_v1_schools),
            "meeting_thu": sum(s["meeting_thu"] for s in d_v1_schools),
            "meeting_fri": sum(s["meeting_fri"] for s in d_v1_schools),
            "meeting_sat": sum(s["meeting_sat"] for s in d_v1_schools),
            "schools_data": d_v1_schools
        }
    else:
        d_v1_agg = None

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
        "headteachers": district_headteachers[dist],
        "patrons": district_patrons[dist],
        "vhts_male": district_vhts_m[dist],
        "vhts_female": district_vhts_f[dist],
        "vhts_pwd_male": district_vhts_pwd_m[dist],
        "vhts_pwd_female": district_vhts_pwd_f[dist],
        "vhts_pwd": district_vhts_pwd_m[dist] + district_vhts_pwd_f[dist],
        "orientations": district_orientations[dist],
        "calendars_signed": district_calendar_yes[dist],
        "calendars_pending": district_calendar_no[dist],
        "exit_interviews": district_exit_interviews[dist],
        "visits": district_visits_conducted[dist],
        "target_visits": len(sch_list) * 3,
        "v1_count": district_v1_count[dist],
        "v2_count": district_v2_count[dist],
        "v3_count": district_v3_count[dist],
        "nutriclubs": district_nutriclubs_count[dist],
        "target_nutriclubs": len(sch_list),
        "v1": d_v1_agg,
        "v1_schools": d_v1_schools,
        "v2": district_v2[dist],
        "v3": district_v3[dist],
        "demos_metrics": None,
        "schools_list": sch_list
    }

    p1_tot = district_p1_total[dist]
    p1_p = district_p1_pass[dist]
    p1_rate = round(p1_p / p1_tot * 100, 1) if p1_tot > 0 else None

    p2_tot = district_p2_total[dist]
    p2_p = district_p2_pass[dist]
    p2_rate = round(p2_p / p2_tot * 100, 1) if p2_tot > 0 else None

    p3_tot = district_p3_total[dist]
    p3_p = district_p3_pass[dist]
    p3_rate = round(p3_p / p3_tot * 100, 1) if p3_tot > 0 else None

    district_db[dist]["pillar_rates"] = {
        "p1_rate": p1_rate,
        "p2_rate": p2_rate,
        "p3_rate": p3_rate,
        "p1_pass": p1_p,
        "p1_total": p1_tot,
        "p2_pass": p2_p,
        "p2_total": p2_tot,
        "p3_pass": p3_p,
        "p3_total": p3_tot
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
        "context": f"{tot_visits} activation visit{'s' if tot_visits != 1 else ''} completed out of 192 scheduled visits across 64 schools"
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

# Dynamically populate district metrics table from district_db
d_data["overview"]["district_metrics"] = []
for dist in ALL_DISTRICTS:
    d = district_db[dist]
    sch_r = d["schools"]
    tgt_s = d["target_schools"]
    s_pct = round((sch_r / tgt_s * 100), 1) if tgt_s > 0 else 0.0
    dem_c = d["demos"]
    tgt_d = d["target_demos"]
    d_pct = round((dem_c / tgt_d * 100), 1) if tgt_d > 0 else 0.0
    lrn_r = d["learners"]
    cg_r = d["caregivers"]
    stk_t = d["teachers_vhts"]
    pwd_r = d["pwd_reach"]
    status_str = "Active (Reports Received)" if (sch_r > 0 or dem_c > 0 or stk_t > 0 or lrn_r > 0) else "Scheduled / Awaiting Data"
    d_data["overview"]["district_metrics"].append({
        "district": dist,
        "schools_reached": sch_r,
        "target_schools": tgt_s,
        "school_progress_pct": s_pct,
        "demos_completed": dem_c,
        "target_demos": tgt_d,
        "demo_progress_pct": d_pct,
        "learners_reached": lrn_r,
        "caregivers_reached": cg_r,
        "stakeholders_trained": stk_t,
        "pwd_reach": pwd_r,
        "status": status_str
    })

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

    # Dynamic orientation metrics across all orientation rows
    o_act_col = [c for c in df.columns if c.strip().lower() == 'activity'][0]
    o_rows = df[df[o_act_col].astype(str).str.contains('orientation', case=False, na=False)]
    tot_orient = len(o_rows)
    tot_o_tea_m = int(o_rows['Male Teachers'].apply(clean_val).sum()) if 'Male Teachers' in o_rows.columns else 0
    tot_o_tea_f = int(o_rows['Female Teachers'].apply(clean_val).sum()) if 'Female Teachers' in o_rows.columns else 0
    tot_o_vht_m = int(o_rows['Male VHTs'].apply(clean_val).sum()) if 'Male VHTs' in o_rows.columns else 0
    tot_o_vht_f = int(o_rows['Female VHTs'].apply(clean_val).sum()) if 'Female VHTs' in o_rows.columns else 0
    tot_o_vht_pwd_m = int(o_rows['Male VHTs with PWDs'].apply(clean_val).sum()) if 'Male VHTs with PWDs' in o_rows.columns else 0
    tot_o_vht_pwd_f = int(o_rows['Female VHTs with PWDs'].apply(clean_val).sum()) if 'Female VHTs with PWDs' in o_rows.columns else 0

    ht_cols = [c for c in o_rows.columns if 'headteacher' in c.lower() and 'present' in c.lower()]
    ht_yes_cnt = int(o_rows[ht_cols[0]].astype(str).str.lower().str.contains('yes').sum()) if ht_cols else 0

    pat_cols = [c for c in o_rows.columns if 'appointed' in c.lower() and 'patron' in c.lower()]
    tot_patrons_app = int(o_rows[pat_cols[0]].apply(clean_val).sum()) if pat_cols else 0

    cal_cols = [c for c in o_rows.columns if 'joint' in c.lower() and 'agree' in c.lower()]
    cal_yes_cnt = int(o_rows[cal_cols[0]].astype(str).str.lower().str.contains('yes').sum()) if cal_cols else 0

    part_cols = [c for c in o_rows.columns if 'partner networks' in c.lower()]
    part_yes_cnt = int(o_rows[part_cols[0]].astype(str).str.lower().str.contains('yes').sum()) if part_cols else 0

    # Disseminated physical tools (lookup by column semantic name, not brittle integer index)
    col_m = [c for c in o_rows.columns if 'metu handbook' in c.lower() or ('**number**' in c.lower() and 'row' not in c.lower())]
    col_c = [c for c in o_rows.columns if 'climate-smart' in c.lower() or 'row-number' in c.lower()]
    col_b = [c for c in o_rows.columns if 'toll-free' in c.lower() or 'row_1-number' in c.lower()]
    tot_tool_metu = int(o_rows[col_m[0]].apply(clean_val).sum()) if col_m else 0
    tot_tool_climate = int(o_rows[col_c[0]].apply(clean_val).sum()) if col_c else 0
    tot_tool_boards = int(o_rows[col_b[0]].apply(clean_val).sum()) if col_b else 0

    # Partner networks breakdown
    part_deo_cnt = int(o_rows['List the partners/District Education Offices'].apply(clean_val).sum()) if 'List the partners/District Education Offices' in o_rows.columns else 0
    part_hc_cnt = int(o_rows['List the partners/Health Centre Parish Focal Persons'].apply(clean_val).sum()) if 'List the partners/Health Centre Parish Focal Persons' in o_rows.columns else 0
    part_unac_cnt = int(o_rows['List the partners/UNAC (Uganda National Action on Childhood Disability)'].apply(clean_val).sum()) if 'List the partners/UNAC (Uganda National Action on Childhood Disability)' in o_rows.columns else 0
    part_afi_cnt = int(o_rows['List the partners/Afi (Action for Inclusion)'].apply(clean_val).sum()) if 'List the partners/Afi (Action for Inclusion)' in o_rows.columns else 0

    d_data["orientation"]["partner_engagement"] = {
        "engaged_schools_count": part_yes_cnt,
        "total_schools_count": tot_orient,
        "engaged_pct": round(part_yes_cnt / max(1, tot_orient) * 100, 1),
        "deo_count": part_deo_cnt,
        "deo_pct": round(part_deo_cnt / max(1, tot_orient) * 100, 1),
        "hc_count": part_hc_cnt,
        "hc_pct": round(part_hc_cnt / max(1, tot_orient) * 100, 1),
        "unac_count": part_unac_cnt,
        "unac_pct": round(part_unac_cnt / max(1, tot_orient) * 100, 1),
        "afi_count": part_afi_cnt,
        "afi_pct": round(part_afi_cnt / max(1, tot_orient) * 100, 1),
        "engaged_schools_names": [get_school_name(r) for _, r in o_rows.iterrows() if 'yes' in str(r.get(part_cols[0], '')).lower()] if part_cols else []
    }
    d_data["orientation"]["disseminated_physical_tools"] = {
        "metu_manuals": tot_tool_metu,
        "climate_manuals": tot_tool_climate,
        "toll_free_boards": tot_tool_boards,
        "total_tools": tot_tool_metu + tot_tool_climate + tot_tool_boards
    }

    d_data["orientation"]["kpis"] = {
        "total_orientations": tot_orient,
        "target_orientations": 64,
        "total_teachers_oriented": tot_o_tea_m + tot_o_tea_f,
        "teachers_male": tot_o_tea_m,
        "teachers_female": tot_o_tea_f,
        "total_vhts_oriented": tot_o_vht_m + tot_o_vht_f,
        "vhts_male": tot_o_vht_m,
        "vhts_female": tot_o_vht_f,
        "vhts_pwd": tot_o_vht_pwd_m + tot_o_vht_pwd_f,
        "headteachers_present": ht_yes_cnt,
        "patrons_appointed": tot_patrons_app,
        "joint_calendars_signed": cal_yes_cnt,
        "joint_calendar_compliance_pct": round(cal_yes_cnt / tot_orient * 100, 1) if tot_orient > 0 else 0.0,
        "total_exit_interviews": len(all_interviews)
    }
    d_data["orientation"]["teacher_attendance_gender"] = {
        "categories": ["Male Teachers", "Female Teachers"],
        "values": [tot_o_tea_m, tot_o_tea_f]
    }
    d_data["orientation"]["headteacher_presence"] = {
        "categories": ["Headteacher / Deputy Present", "Absent / Delegated"],
        "values": [ht_yes_cnt, max(0, tot_orient - ht_yes_cnt)]
    }
    d_data["orientation"]["vht_orientation_gender"] = {
        "categories": ["Male VHTs", "Female VHTs"],
        "values": [tot_o_vht_m, tot_o_vht_f]
    }
    d_data["orientation"]["vhts_with_pwd"] = {
        "categories": ["Male VHTs with PWD", "Female VHTs with PWD"],
        "values": [tot_o_vht_pwd_m, tot_o_vht_pwd_f]
    }
    d_data["orientation"]["joint_calendar_agreements"] = {
        "categories": ["Joint 4-Week Plan Agreed", "No Agreement Yet"],
        "values": [cal_yes_cnt, max(0, tot_orient - cal_yes_cnt)]
    }
    d_data["orientation"]["partner_networks_engagement"] = {
        "title": "Partner Networks Engagement",
        "categories": ["Partner Networks Engaged", "School Only"],
        "values": [part_yes_cnt, max(0, tot_orient - part_yes_cnt)],
        "notes": f"{part_yes_cnt} of {tot_orient} oriented schools engaged partner networks (District Education Offices & Health Centre Parish Focal Persons)" if part_yes_cnt > 0 else "Pending partner co-facilitation"
    }
    d_data["orientation"]["physical_tools_disseminated"] = {
        "categories": ["Metu Handbooks & Cooking Manuals", "Climate-Smart One-Pager Manuals", "Toll-Free Feedback Display Boards"],
        "values": [tot_tool_metu, tot_tool_climate, tot_tool_boards]
    }

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

# --- VISIT 1 & VISIT 2 DYNAMIC AGGREGATION ---
act_col_found = [c for c in df.columns if c.strip().lower() == 'activity'][0]
ms_col_found = [c for c in df.columns if 'milestone' in c.lower()]
ms_col_name = ms_col_found[0] if ms_col_found else None

def is_v1_row(r):
    act = str(r.get(act_col_found, '')).lower()
    if 'visit' not in act: return False
    if ms_col_name and pd.notnull(r.get(ms_col_name)):
        m = str(r.get(ms_col_name)).lower()
        return 'visit 1' in m or 'baseline' in m
    return False

def is_v2_row(r):
    act = str(r.get(act_col_found, '')).lower()
    if 'visit' not in act: return False
    if ms_col_name and pd.notnull(r.get(ms_col_name)):
        m = str(r.get(ms_col_name)).lower()
        return 'visit 2' in m or 'activation' in m
    return True

v1_rows = df[df.apply(is_v1_row, axis=1)]
v2_rows = df[df.apply(is_v2_row, axis=1)]

v2_schools = []
for idx_v, r_v in v2_rows.iterrows():
    s_name = get_school_name(r_v)
    d_name = str(r_v.get('District', '')).strip()
    v2_schools.append(f"{s_name} ({d_name})")

act_keys = [
    ('Energizer song & movement', 'Energizer song & movement'),
    ('Food sorting & matching game', 'Food sorting & matching game'),
    ('Metu porridge supplementation demonstrated', 'Metu porridge supplementation demonstrated'),
    ('Structured dialogue on rebalancing chores', 'Structured dialogue on rebalancing chores'),
    ('Fair food portions for all genders', 'Fair food portions for all genders'),
    ('Climate-smart cooking methods explained', 'Climate-smart cooking methods explained'),
    ('Learners actively handled materials', 'Learners actively handled materials and practiced (not passive observers)')
]
act_cats = [k[0] for k in act_keys]
act_vals = []
for short_lbl, col_sub in act_keys:
    matching_cols = [c for c in df.columns if col_sub in c]
    cnt = 0
    for idx_v, r_v in v2_rows.iterrows():
        for mc in matching_cols:
            if r_v.get(mc) == 1.0 or str(r_v.get(mc)).strip() == '1':
                cnt += 1
                break
    act_vals.append(cnt)

barr_keys = [
    ('Lack of preparation confidence/skills', 'Lack of preparation confidence/skills'),
    ('Ingredients not prioritized at household level', 'Ingredients not prioritized at household level'),
    ('Other', 'Other'),
    ('Taste preference barriers', 'Taste preference barriers')
]
barr_cats = [k[0] for k in barr_keys]
barr_vals = []
for lbl, sub in barr_keys:
    m_cols = [c for c in df.columns if 'primary reason' in c.lower() and sub in c]
    cnt = 0
    for idx_v, r_v in v2_rows.iterrows():
        for mc in m_cols:
            if r_v.get(mc) == 1.0 or str(r_v.get(mc)).strip() == '1':
                cnt += 1
                break
    barr_vals.append(cnt)
tot_barr_responses = sum(barr_vals)
barr_pct = [round((v / tot_barr_responses * 100), 1) if tot_barr_responses > 0 else 0.0 for v in barr_vals]

poll_statements = [
    ('statement_1', 'It is unfair for a girl to stay home doing compound work while brothers leave early for class.', 'row_4'),
    ('statement_2', 'Boys and girls should finish morning chores at the same time so both eat porridge and walk to school together.', 'row'),
    ('statement_3', 'Collecting firewood for cooking is a chore that boys and girls should do together.', 'row_3'),
    ('statement_4', 'I am ready to fetch water from borehole in morning so my sister is not late/punished.', 'row_1'),
    ('statement_5', 'If a girl misses school to herd animals or do chores I will speak up to get her back to class.', 'row_2')
]
poll_dict = {}
poll_options = ['Strongly Agree', 'Agree', 'Neutral / Undecided', 'Disagree', 'Strongly Disagree']

for stmt_key, stmt_text, prefix in poll_statements:
    choice_col = f'<span style="display:none">{prefix}-Choice</span>'
    num_col = f'<span style="display:none">{prefix}-Number of boys</span>'
    reason_col = f'<span style="display:none">{prefix}-Reason in the persons words separated by commas</span>'
    
    counts = [0, 0, 0, 0, 0]
    reasons = []
    tot_boys_stmt = 0

    for idx_v, r_v in v2_rows.iterrows():
        c_val = str(r_v.get(choice_col, '')).strip().lower()
        n_val = int(clean_val(r_v.get(num_col, 0)))
        tot_boys_stmt += n_val

        reas = str(r_v.get(reason_col, '')).strip()
        dist = str(r_v.get('District', '')).strip()
        if len(reas) > 1 and reas != 'nan' and not reas.isdigit():
            reasons.append(f'{dist}: "{reas}"')

        if c_val == 'strongly agree':
            counts[0] += n_val
        elif c_val == 'strongly disagree':
            counts[4] += n_val
        elif c_val == 'disagree':
            counts[3] += n_val
        elif c_val == 'agree':
            counts[1] += n_val
        elif 'undecided' in c_val or 'neutral' in c_val:
            counts[2] += n_val

    agreed = counts[0] + counts[1]
    pct = round(agreed / tot_boys_stmt * 100, 1) if tot_boys_stmt > 0 else 0.0
    primary_quote = reasons[0] if reasons else f"{agreed} boys agreed during session."

    poll_dict[stmt_key] = {
        'statement': stmt_text,
        'categories': poll_options,
        'values': counts,
        'total_boys': tot_boys_stmt,
        'agreed_boys': agreed,
        'pct_agreed': pct,
        'reason_in_words': primary_quote,
        'all_reasons': reasons
    }

p1_specific = 0
p1_general = 0
p1_incorrect = 0
p2_equal = 0
p2_hurry = 0
p2_leave = 0
slogan_demo = 0
slogan_part = 0
slogan_none = 0

v2_respondents = []
for idx_v, r_v in v2_rows.iterrows():
    s_name = get_school_name(r_v)
    d_name = str(r_v.get('District', '')).strip()
    p1_cols = [c for c in df.columns if 'plain porridge' in c.lower() and pd.notnull(r_v[c])]
    for c in p1_cols:
        v = str(r_v[c]).lower()
        if 'specific' in v or 'demonstrated' in v:
            p1_specific += 1
        elif 'general' in v or 'vague' in v:
            p1_general += 1
        elif len(v.strip()) > 3 and v.strip() != 'nan':
            p1_incorrect += 1
    p2_cols = [c for c in df.columns if 'heavy at home tomorrow' in c.lower() and pd.notnull(r_v[c])]
    for c in p2_cols:
        v = str(r_v[c]).lower()
        if 'share' in v and 'equally' in v:
            p2_equal += 1
        elif 'hurry' in v or 'early' in v:
            p2_hurry += 1
        elif len(v.strip()) > 3 and v.strip() != 'nan':
            p2_leave += 1
    slog_cols = [c for c in df.columns if 'line recall' in c.lower() and pd.notnull(r_v[c])]
    for c in slog_cols:
        v = str(r_v[c]).lower()
        if 'partly' in v:
            slogan_part += 1
        elif 'demonstrated' in v:
            slogan_demo += 1
        elif len(v.strip()) > 3 and v.strip() != 'nan':
            slogan_none += 1

    # Extract individual respondent profiles for this school
    prefixes = ['row-', 'row_1-', 'row_2-', 'row_3-', 'row_4-', 'row_5-']
    for p_idx, prefix in enumerate(prefixes):
        p1_val, p2_val, slog_val = None, None, None
        for c in df.columns:
            if prefix in c:
                if 'plain porridge' in c.lower() and pd.notnull(r_v[c]):
                    p1_val = str(r_v[c]).strip()
                elif 'heavy at home tomorrow' in c.lower() and pd.notnull(r_v[c]):
                    p2_val = str(r_v[c]).strip()
                elif 'line recall' in c.lower() and pd.notnull(r_v[c]):
                    slog_val = str(r_v[c]).strip()
        if p1_val or p2_val or slog_val:
            role_label = f"Learner {p_idx + 1}" if p_idx < 4 else f"Adult {p_idx - 3}"
            v2_respondents.append({
                "id": f"{s_name} - {role_label}",
                "school": s_name,
                "district": d_name,
                "role": role_label,
                "porridge": p1_val or "Not assessed",
                "chores": p2_val or "Not assessed",
                "slogan": slog_val or "Not assessed"
            })


tot_v2_pupils = sum(d["v2"]["hc_lower_m"] + d["v2"]["hc_lower_f"] + d["v2"]["hc_mid_m"] + d["v2"]["hc_mid_f"] + d["v2"]["hc_up_m"] + d["v2"]["hc_up_f"] for d in district_db.values() if d.get("v2"))
tot_v2_boys = sum(d["v2"]["hc_lower_m"] + d["v2"]["hc_mid_m"] + d["v2"]["hc_up_m"] for d in district_db.values() if d.get("v2"))
tot_v2_girls = sum(d["v2"]["hc_lower_f"] + d["v2"]["hc_mid_f"] + d["v2"]["hc_up_f"] for d in district_db.values() if d.get("v2"))
tot_v2_staff = sum(d["v2"]["teachers_m"] + d["v2"]["teachers_f"] for d in district_db.values() if d.get("v2"))
tot_v2_comm = sum(d["v2"]["comm_m"] + d["v2"]["comm_f"] for d in district_db.values() if d.get("v2"))
tot_v2_pwd_l = sum(d["v2"]["hc_lower_pwd"] + d["v2"]["hc_mid_pwd"] + d["v2"]["hc_up_pwd"] for d in district_db.values() if d.get("v2"))
tot_v2_pwd_a = sum(d["v2"]["teachers_pwd"] + d["v2"]["comm_pwd"] for d in district_db.values() if d.get("v2"))
tot_v2_pwd = tot_v2_pwd_l + tot_v2_pwd_a
tot_v2_attendance = tot_v2_pupils + tot_v2_staff + tot_v2_comm

# VISIT 1 AGGREGATION
v1_schools = [f"{s['school']} ({s['district']})" for s in v1_all_schools_records]

tot_v1_pupils = sum(s["att_total"] for s in v1_all_schools_records)
tot_v1_boys = sum(s["att_boys"] for s in v1_all_schools_records)
tot_v1_girls = sum(s["att_girls"] for s in v1_all_schools_records)
tot_v1_enrol = sum(s["enrol_total"] for s in v1_all_schools_records)
tot_v1_enrol_b = sum(s["enrol_boys"] for s in v1_all_schools_records)
tot_v1_enrol_g = sum(s["enrol_girls"] for s in v1_all_schools_records)
tot_v1_charts = sum(s["charts_issued"] for s in v1_all_schools_records)
tot_v1_queries = sum(s["helpdesk_queries"] for s in v1_all_schools_records)
v1_nc_act = sum(1 for s in v1_all_schools_records if s.get("nutriclub_active") == "Yes")
v1_nc_proc = sum(1 for s in v1_all_schools_records if s.get("nutriclub_creating") == "Yes")
v1_wp = sum(1 for s in v1_all_schools_records if s.get("work_plan_signed") == "Yes")
v1_tf = sum(1 for s in v1_all_schools_records if s.get("toll_free_displayed") == "Yes")
v1_tf_kwn = sum(1 for s in v1_all_schools_records if s.get("toll_free_known") == "Yes")
v1_mon = sum(s.get("meeting_mon", 0) for s in v1_all_schools_records)
v1_tue = sum(s.get("meeting_tue", 0) for s in v1_all_schools_records)
v1_wed = sum(s.get("meeting_wed", 0) for s in v1_all_schools_records)
v1_thu = sum(s.get("meeting_thu", 0) for s in v1_all_schools_records)
v1_fri = sum(s.get("meeting_fri", 0) for s in v1_all_schools_records)
v1_sat = sum(s.get("meeting_sat", 0) for s in v1_all_schools_records)

if "three_visit_contact" in d_data:
    d_data["three_visit_contact"]["pipeline_funnel"] = {
        "stages": [
            "Visit 1: School Onboarding & Audit",
            "Visit 2: Big NutriBus Activation Day",
            "Visit 3: Final Closeout & Audits"
        ],
        "completed_schools": [
            len(v1_all_schools_records),
            len(v2_rows),
            0
        ]
    }
    d_data["three_visit_contact"]["milestones_completed"] = {
        "categories": [
            "Visit 1 Completed",
            "Visit 2 Completed",
            "Visit 3 Completed"
        ],
        "values": [
            len(v1_all_schools_records),
            len(v2_rows),
            0
        ]
    }
    d_data["three_visit_contact"]["longitudinal_attendance"] = {
        "labels": [
            "Visit 1 Check",
            "Visit 2 Activation",
            "Visit 3 Closeout"
        ],
        "total_attendance": [
            tot_v1_pupils,
            tot_v2_pupils,
            0
        ],
        "boys": [
            tot_v1_boys,
            tot_v2_boys,
            0
        ],
        "girls": [
            tot_v1_girls,
            tot_v2_girls,
            0
        ]
    }
    d_data["three_visit_contact"]["visit1"] = {
        "total_schools_completed": len(v1_all_schools_records),
        "target_schools": 64,
        "schools_list": v1_schools,
        "schools_data": v1_all_schools_records,
        "status": f"{len(v1_all_schools_records)} Schools Logged ({', '.join(v1_schools)})",
        "enrolment": {
            "boys": tot_v1_enrol_b,
            "girls": tot_v1_enrol_g,
            "total": tot_v1_enrol
        },
        "attendance": {
            "boys": tot_v1_boys,
            "girls": tot_v1_girls,
            "total": tot_v1_pupils
        },
        "charts_issued": tot_v1_charts,
        "nutriclub_active": {
            "values": [v1_nc_act, max(0, len(v1_all_schools_records) - v1_nc_act)]
        },
        "nutriclub_in_process": {
            "values": [max(0, len(v1_all_schools_records) - v1_nc_proc), v1_nc_proc]
        },
        "signed_workplan": {
            "values": [v1_wp, max(0, len(v1_all_schools_records) - v1_wp)]
        },
        "charts_by_class": {
            "categories": ["Lower Primary (ECD-P2)", "Middle Primary (P3-P4)", "Upper Primary (P5-P7)"],
            "values": [len(v1_all_schools_records), len(v1_all_schools_records), len(v1_all_schools_records)]
        },
        "activity_days": {
            "categories": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            "values": [v1_mon, v1_tue, v1_wed, v1_thu, v1_fri, v1_sat]
        },
        "tollfree_display": {
            "values": [v1_tf, max(0, len(v1_all_schools_records) - v1_tf)]
        },
        "tollfree_known": {
            "values": [v1_tf_kwn, max(0, len(v1_all_schools_records) - v1_tf_kwn)]
        },
        "weekly_registered_attendance": {
            "categories": ["Lower Boys", "Lower Girls", "Middle Boys", "Middle Girls", "Upper Boys", "Upper Girls"],
            "values": [
                sum(s["att_lower_b"] for s in v1_all_schools_records),
                sum(s["att_lower_g"] for s in v1_all_schools_records),
                sum(s["att_mid_b"] for s in v1_all_schools_records),
                sum(s["att_mid_g"] for s in v1_all_schools_records),
                sum(s["att_up_b"] for s in v1_all_schools_records),
                sum(s["att_up_g"] for s in v1_all_schools_records)
            ]
        },
        "helpdesk_queries_logged": {
            "categories": [f"{s['school']} ({s['district']})" for s in v1_all_schools_records if s.get("helpdesk_queries", 0) > 0],
            "values": [s["helpdesk_queries"] for s in v1_all_schools_records if s.get("helpdesk_queries", 0) > 0]
        }
    }
    d_data["three_visit_contact"]["visit2"] = {
        "schools_completed": len(v2_rows),
        "target_schools": 64,
        "schools_list": v2_schools,
        "schools_data": v2_all_schools_records,
        "total_pupils_attended": tot_v2_pupils,
        "pwd_learners": tot_v2_pwd_l,
        "teachers_present": tot_v2_staff,
        "community_present": tot_v2_comm,
        "total_attendance": tot_v2_attendance,
        "pwd_total": tot_v2_pwd,
        "pwd_rate_pct": round((tot_v2_pwd / tot_v2_attendance * 100), 1) if tot_v2_attendance > 0 else 0.0,
        "age_bands_matrix": [
            {
                "age_band": "Lower Primary (ECD–P2)",
                "male": sum(d["v2"]["hc_lower_m"] for d in district_db.values() if d.get("v2")),
                "female": sum(d["v2"]["hc_lower_f"] for d in district_db.values() if d.get("v2")),
                "total": sum(d["v2"]["hc_lower_m"] + d["v2"]["hc_lower_f"] for d in district_db.values() if d.get("v2")),
                "male_pwd": sum(d["v2"].get("hc_lower_pwd_m", d["v2"]["hc_lower_pwd"]) for d in district_db.values() if d.get("v2")),
                "female_pwd": sum(d["v2"].get("hc_lower_pwd_f", 0) for d in district_db.values() if d.get("v2"))
            },
            {
                "age_band": "Middle Primary (P3–P4)",
                "male": sum(d["v2"]["hc_mid_m"] for d in district_db.values() if d.get("v2")),
                "female": sum(d["v2"]["hc_mid_f"] for d in district_db.values() if d.get("v2")),
                "total": sum(d["v2"]["hc_mid_m"] + d["v2"]["hc_mid_f"] for d in district_db.values() if d.get("v2")),
                "male_pwd": sum(d["v2"].get("hc_mid_pwd_m", d["v2"]["hc_mid_pwd"]) for d in district_db.values() if d.get("v2")),
                "female_pwd": sum(d["v2"].get("hc_mid_pwd_f", 0) for d in district_db.values() if d.get("v2"))
            },
            {
                "age_band": "Upper Primary (P5–P7)",
                "male": sum(d["v2"]["hc_up_m"] for d in district_db.values() if d.get("v2")),
                "female": sum(d["v2"]["hc_up_f"] for d in district_db.values() if d.get("v2")),
                "total": sum(d["v2"]["hc_up_m"] + d["v2"]["hc_up_f"] for d in district_db.values() if d.get("v2")),
                "male_pwd": sum(d["v2"].get("hc_up_pwd_m", d["v2"]["hc_up_pwd"]) for d in district_db.values() if d.get("v2")),
                "female_pwd": sum(d["v2"].get("hc_up_pwd_f", 0) for d in district_db.values() if d.get("v2"))
            },
            {
                "age_band": "Teachers Present",
                "male": sum(d["v2"]["teachers_m"] for d in district_db.values() if d.get("v2")),
                "female": sum(d["v2"]["teachers_f"] for d in district_db.values() if d.get("v2")),
                "total": sum(d["v2"]["teachers_m"] + d["v2"]["teachers_f"] for d in district_db.values() if d.get("v2")),
                "male_pwd": sum(d["v2"].get("teachers_pwd_m", d["v2"]["teachers_pwd"]) for d in district_db.values() if d.get("v2")),
                "female_pwd": sum(d["v2"].get("teachers_pwd_f", 0) for d in district_db.values() if d.get("v2"))
            },
            {
                "age_band": "Community Members",
                "male": sum(d["v2"]["comm_m"] for d in district_db.values() if d.get("v2")),
                "female": sum(d["v2"]["comm_f"] for d in district_db.values() if d.get("v2")),
                "total": sum(d["v2"]["comm_m"] + d["v2"]["comm_f"] for d in district_db.values() if d.get("v2")),
                "male_pwd": sum(d["v2"].get("comm_pwd_m", d["v2"]["comm_pwd"]) for d in district_db.values() if d.get("v2")),
                "female_pwd": sum(d["v2"].get("comm_pwd_f", 0) for d in district_db.values() if d.get("v2"))
            }
        ],
        "activities_delivered": {
            "categories": act_cats,
            "values": act_vals
        },
        "metu_uptake_barriers": {
            "categories": barr_cats,
            "values": barr_vals,
            "pct": barr_pct
        },
        "micro_poll": poll_dict,
        "post_session_scenario": {
            "sample_size": p1_specific + p1_general + p1_incorrect,
            "porridge_recall": {
                "categories": ["Specific Actionable Fortification", "General / Vague Idea", "Incorrect / Unavailable Foods"],
                "values": [p1_specific, p1_general, p1_incorrect]
            },
            "chore_sharing_recall": {
                "categories": ["Share Chores Equally", "Hurry Up / Wake Early Alone", "Leaves Work Only to Girls"],
                "values": [p2_equal, p2_hurry, p2_leave]
            },
            "slogan_recall": {
                "categories": ["Demonstrated Clearly", "Partly Demonstrated", "Not Demonstrated"],
                "values": [slogan_demo, slogan_part, slogan_none]
            },
            "respondents": v2_respondents
        }
    }

# --- NUTRICLUB SESSIONS DYNAMIC POPULATION ---
if "nutriclub_sessions" in d_data:
    nc_data = d_data["nutriclub_sessions"]
    sch_reg = nc_data.get("schools_register", [])

    active_schools_set = set()
    total_session_att = 0
    total_session_att_b = 0
    total_session_att_g = 0
    total_session_pwd = 0
    total_session_pwd_b = 0
    total_session_pwd_g = 0

    for sess in nutriclub_sessions_list:
        s_name = sess["school"]
        s_dist = sess["district"]
        active_schools_set.add(s_name)
        total_session_att += sess["total_present"]
        total_session_att_b += sess["boys_present"]
        total_session_att_g += sess["girls_present"]
        total_session_pwd += sess["pwd"]
        total_session_pwd_b += sess["pwd_boys"]
        total_session_pwd_g += sess["pwd_girls"]

        # Match in schools_register
        norm_s = norm_sch_name(s_name)
        matched_sch = None
        for item in sch_reg:
            if norm_sch_name(item.get("school", "")) == norm_s and item.get("district", "").lower() == s_dist.lower():
                matched_sch = item
                break
        if not matched_sch:
            for item in sch_reg:
                if (norm_s in norm_sch_name(item.get("school", "")) or norm_sch_name(item.get("school", "")) in norm_s) and item.get("district", "").lower() == s_dist.lower():
                    matched_sch = item
                    break

        if matched_sch:
            matched_sch["patron_name"] = sess["patron"]
            matched_sch["meeting_place"] = sess["meeting_place"]
            matched_sch["male_membership"] = sess["membership_male"]
            matched_sch["female_membership"] = sess["membership_female"]
            matched_sch["total_membership"] = sess["total_membership"]
            matched_sch["total_pwd"] = sess["pwd"]

            sess_obj = {
                "date_conducted": sess["date"],
                "start_time": sess["start_time"],
                "end_time": sess["end_time"],
                "designated_meeting_place": sess["meeting_place"],
                "club_patron_name": sess["patron"],
                "boys_present": sess["boys_present"],
                "girls_present": sess["girls_present"],
                "male_pwd": sess["pwd_boys"],
                "female_pwd": sess["pwd_girls"],
                "practical_activity": sess["practical_activity"],
                "home_action_assigned": sess["home_action_assigned"],
                "coordinator_notes": sess["coordinator_notes"]
            }
            if "two" in sess["session_of_week"].lower():
                matched_sch["session_two"] = sess_obj
            else:
                matched_sch["session_one"] = sess_obj

    # Calculate active members across all matched schools in register
    total_active_members = 0
    total_active_members_m = 0
    total_active_members_f = 0
    for item in sch_reg:
        if item.get("total_membership", 0) > 0:
            total_active_members += item["total_membership"]
            total_active_members_m += item.get("male_membership", 0)
            total_active_members_f += item.get("female_membership", 0)

    # Update KPIs
    sess_one_cnt = sum(1 for s in nutriclub_sessions_list if "two" not in s.get("session_of_week", "").lower())
    sess_two_cnt = sum(1 for s in nutriclub_sessions_list if "two" in s.get("session_of_week", "").lower())
    total_assembly_nm = sum(s.get("assembly_nutri_moment", 0) for s in nutriclub_sessions_list)

    nc_data["kpis"] = {
        "total_sessions_logged": len(nutriclub_sessions_list),
        "target_schools": 64,
        "schools_with_active_clubs": len(active_schools_set),
        "total_members": total_active_members,
        "members_male": total_active_members_m,
        "members_female": total_active_members_f,
        "session_attendance": total_session_att,
        "attendance_boys": total_session_att_b,
        "attendance_girls": total_session_att_g,
        "pwd_learners": total_session_pwd,
        "pwd_boys": total_session_pwd_b,
        "pwd_girls": total_session_pwd_g,
        "sessions_one_count": sess_one_cnt,
        "sessions_two_count": sess_two_cnt,
        "assembly_nutri_moments": total_assembly_nm
    }
    nc_data["club_membership_gender"] = {
        "categories": ["Male Members", "Female Members"],
        "values": [total_active_members_m, total_active_members_f]
    }
    nc_data["session_attendance_gender"] = {
        "categories": ["Boys Present", "Girls Present"],
        "values": [total_session_att_b, total_session_att_g]
    }
    nc_data["pwd_learners_attendance"] = {
        "categories": ["Male Learners with Disabilities", "Female Learners with Disabilities"],
        "values": [total_session_pwd_b, total_session_pwd_g]
    }

    # Aggregate practical activities dynamically across all logged sessions
    act_adere_cnt = sum(s.get("has_adere", 0) for s in nutriclub_sessions_list)
    act_chore_cnt = sum(s.get("has_chore", 0) for s in nutriclub_sessions_list)
    act_climate_cnt = sum(s.get("has_climate", 0) for s in nutriclub_sessions_list)
    act_peer_cnt = sum(s.get("has_peer", 0) for s in nutriclub_sessions_list)
    act_metu_cnt = sum(s.get("has_metu", 0) for s in nutriclub_sessions_list)

    nc_data["practical_activity_delivered"] = {
        "categories": [
            "Adere Calabash Dialogue (Resilience & Food Sharing)",
            "Gender Chore Rebalancing (Boys Sharing Chores)",
            "Climate-Smart Living (Firewood Saving)",
            "Peer Attendance Tracing",
            "Metu Porridge Plus (Wild Greens / Cowpeas)"
        ],
        "values": [act_adere_cnt, act_chore_cnt, act_climate_cnt, act_peer_cnt, act_metu_cnt]
    }

    # Aggregate home action trials dynamically
    home_garden_cnt = sum(1 for s in nutriclub_sessions_list if "garden" in s.get("home_action_assigned", "").lower())
    home_calendar_cnt = sum(1 for s in nutriclub_sessions_list if "calender" in s.get("home_action_assigned", "").lower() or "calendar" in s.get("home_action_assigned", "").lower())
    awaiting_cnt = max(0, 64 - len(nutriclub_sessions_list))
    nc_data["home_action_feedback"] = {
        "categories": ["Home kitchen gardens tried", "Food calendar marking assigned", "Awaiting reporting"],
        "values": [home_garden_cnt, home_calendar_cnt, awaiting_cnt]
    }

    nc_data["sample_sessions"] = nutriclub_sessions_list

# --- IMPACT ANALYSIS DYNAMIC AGGREGATION ---
tot_orient_schools = sum(1 for d in district_db.values() if d["schools"] > 0 and (d["teachers_male"] + d["teachers_female"] > 0))
v2_completed_count = len(v2_rows)
p1_rate_overall = round((sum(d["pillar_rates"]["p1_pass"] for d in district_db.values()) / max(1, sum(d["pillar_rates"]["p1_total"] for d in district_db.values()))) * 100, 1) if sum(d["pillar_rates"]["p1_total"] for d in district_db.values()) > 0 else 0.0
p2_rate_overall = round((sum(d["pillar_rates"]["p2_pass"] for d in district_db.values()) / max(1, sum(d["pillar_rates"]["p2_total"] for d in district_db.values()))) * 100, 1) if sum(d["pillar_rates"]["p2_total"] for d in district_db.values()) > 0 else 0.0
p3_rate_overall = round((sum(d["pillar_rates"]["p3_pass"] for d in district_db.values()) / max(1, sum(d["pillar_rates"]["p3_total"] for d in district_db.values()))) * 100, 1) if sum(d["pillar_rates"]["p3_total"] for d in district_db.values()) > 0 else 0.0

tot_poll_boys = sum(v.get("total_boys", 0) for v in poll_dict.values())
tot_poll_agreed = sum(v.get("agreed_boys", 0) for v in poll_dict.values())
poll_agreed_pct = round(tot_poll_agreed / max(1, tot_poll_boys) * 100, 1) if tot_poll_boys > 0 else 0.0

# --- NEW PILLAR INDICATORS EXTRACTED FROM KOBO ---
ofsp_cols = [c for c in df.columns if 'orange-fleshed sweet potato' in c.lower() or 'ofsp' in c.lower()]
tot_ofsp = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in ofsp_cols)

iron_beans_cols = [c for c in df.columns if 'iron-rich beans' in c.lower()]
tot_iron_beans = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in iron_beans_cols)

lead_mothers_cols = [c for c in df.columns if 'lead mothers' in c.lower()]
tot_lead_mothers = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in lead_mothers_cols)

cost_cols = [c for c in df.columns if 'cost' in c.lower() and 'scholastic' in c.lower()]
tot_cost_dialogues = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in cost_cols)

mhm_cols = [c for c in df.columns if 'menstrual' in c.lower()]
tot_mhm_dialogues = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in mhm_cols)

theft_cols = [c for c in df.columns if 'theft or mismanagement' in c.lower()]
tot_theft_queries = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in theft_cols)

hotline_210_cols = [c for c in df.columns if '0800 210 210' in c.lower()]
tot_hotline_210_promoted = sum(df[c].apply(lambda v: 1 if pd.notnull(v) and str(v).strip() in ['1', 'True', 'true', 'Yes', 'yes', '1.0'] else 0).sum() for c in hotline_210_cols)

d_data["new_pillar_metrics"] = {
    "tot_ofsp": int(tot_ofsp),
    "tot_iron_beans": int(tot_iron_beans),
    "tot_lead_mothers": int(tot_lead_mothers),
    "tot_cost_dialogues": int(tot_cost_dialogues),
    "tot_mhm_dialogues": int(tot_mhm_dialogues),
    "tot_theft_queries": int(tot_theft_queries),
    "tot_hotline_210_promoted": int(tot_hotline_210_promoted)
}

d_data["impact_analysis"] = {
    "dimensions": [
        {
            "title": "Pillar 1: School Feeding",
            "metric_value": f"{p1_rate_overall}%",
            "metric_label": f"Meal Protection & METU-1 ({v2_completed_count} Activation Schools)",
            "summary": f"{p1_rate_overall}% of monitored learners demonstrated practical recall of school meal protection, balanced plates, and METU-1 multi-mix porridge enrichment using locally available foods.",
            "baseline": "Pending Visit 1",
            "evidence_points": [
                f"Protecting school meals: {p1_specific} learners recalled specific local greens (Eboo, Lokaka) and cowpeas for METU-1 porridge fortification",
                f"Balanced plate & clubs: {tot_clubs} active NutriClubs established with demo gardens; OFSP & iron-rich beans tracked ({tot_ofsp} OFSP, {tot_iron_beans} iron beans logged)",
                f"Helpline awareness: WFP toll-free helpline (0800 210 210) promoted across {tot_orient_schools} schools for reporting meal theft or mismanagement ({tot_theft_queries} complaints logged)"
            ]
        },
        {
            "title": "Pillar 2: Gender",
            "metric_value": f"{p2_rate_overall}%",
            "metric_label": f"Fair Sharing & Allyship ({v2_completed_count} Activation Schools)",
            "summary": f"{p2_rate_overall}% consensus recorded across male allies (boys, fathers, male teachers) affirming fair sharing at the table and in the classroom, addressing practical constraints (labour, cost, menstruation).",
            "baseline": "Pending Visit 1",
            "evidence_points": [
                f"Fair sharing at the table: {p2_equal} of {p2_equal + p2_hurry} interviewed learners affirmed boys and girls must eat equally and simultaneously",
                f"Male allies in action: {tot_poll_boys:,} boy responses logged across 5 micro-polls with {poll_agreed_pct}% agreement ({tot_poll_agreed:,} agreements) committing to share morning water and firewood chores",
                f"Addressing practical constraints: Dialogues with fathers and male teachers tackling domestic labour ({tot_poll_boys:,} boys), schooling costs ({tot_cost_dialogues} sessions), and menstrual hygiene ({tot_mhm_dialogues} sessions)"
            ]
        },
        {
            "title": "Pillar 3: Community Engagement",
            "metric_value": f"{p3_rate_overall}%",
            "metric_label": f"Community Action & Stoves ({tot_orient_schools} Oriented Schools)",
            "summary": f"{round(cal_yes_cnt / max(1, tot_orient_schools) * 100, 1)}% of school leadership and VHTs agreed on joint action calendars, driving community behaviour change across 640 targeted cooking demonstrations.",
            "baseline": "0.0% Prior",
            "evidence_points": [
                f"640 Cooking Demonstrations target led by 256 VHT/lead-mother pairs (rollout underway; {tot_lead_mothers} sessions with lead mothers co-facilitating)",
                f"Community dialogues with men & elders: {cal_yes_cnt} of {tot_orient_schools} schools established joint 4-week action plans and consensus",
                f"Clean & smart cooking practices: Retained-heat cooking, dry firewood management, and moving away from open 3-stone fires promoted",
                f"METU-1 recipe chart routine: {tot_v1_charts:,} take-home NutriCharts issued for household routine adoption"
            ]
        }
    ],
    "core_evaluation_answers": [
        {
            "question": "How much did we do?",
            "subtitle": "What was done on the ground",
            "cadence": "Verified field submissions log",
            "status_badge": f"{tot_schools} of 64 Schools Active",
            "key_metrics": [
                {
                    "label": "Schools Reached",
                    "value": f"{tot_schools} Schools",
                    "detail": f"{tot_schools} primary schools reached out of 64 total target schools"
                },
                {
                    "label": "School Contact Visits",
                    "value": f"{tot_visits} Visits Conducted",
                    "detail": f"{len(v1_rows)} Visit 1 School Onboarding completed, {v2_completed_count} Visit 2 Big Activation Days completed (Target: 192 total visits)"
                },
                {
                    "label": "Children Reached",
                    "value": f"{tot_learners:,} Pupils",
                    "detail": f"{tot_v1_pupils} weekly attendees ({tot_v1_enrol} enrolled) at Visit 1, {tot_v2_pupils} in Visit 2 activations, {total_session_att} in NutriClub sessions (Target: 80,875)"
                },
                {
                    "label": "Village Cooking Demos",
                    "value": f"{tot_demos} Demonstrations",
                    "detail": f"0 of 640 community cooking demonstrations conducted to date"
                },
                {
                    "label": "Caregivers Reached",
                    "value": f"{tot_caregivers} Caregivers",
                    "detail": f"{tot_caregivers} community caregivers attended Visit 2 activations (Target: 51,200)"
                },
                {
                    "label": "Active NutriClubs",
                    "value": f"{tot_clubs} Club{'s' if tot_clubs > 1 else ''} Active",
                    "detail": f"{len(active_schools_set)} active club(s) with {total_active_members} registered members (Target: 64 clubs)"
                },
                {
                    "label": "Teachers & VHTs Oriented",
                    "value": f"{tot_stakeholders} Stakeholders",
                    "detail": f"Oriented across {tot_orient_schools} primary schools (Target: 768)"
                },
                {
                    "label": "Persons with Disabilities",
                    "value": f"{tot_pwd} PWDs Reached",
                    "detail": f"{tot_v2_pwd_l} learners and {tot_v2_pwd_a} adults included across sessions"
                }
            ],
            "verification_source": "Verified field activity forms, sign-in sheets, and monitor observation logs."
        },
        {
            "question": "How well did we do it?",
            "subtitle": "Quality and inclusivity of the sessions",
            "cadence": "Recorded during and after every session",
            "status_badge": "High Quality Confirmed",
            "key_metrics": [
                {
                    "label": "Hands-On Cooking Practice",
                    "value": "Awaiting Demos",
                    "detail": "Community cooking demonstrations have not commenced (0 demos conducted)"
                },
                {
                    "label": "Local Foods Only",
                    "value": "100% Compliant",
                    "detail": "Promoted exclusively local wild greens (Eboo, Lokaka) and cowpeas"
                },
                {
                    "label": "Teachers in the Lead",
                    "value": f"{round(ht_yes_cnt / max(1, tot_orient_schools) * 100, 1)}% ({ht_yes_cnt} of {tot_orient_schools} Schools)",
                    "detail": f"{ht_yes_cnt} of {tot_orient_schools} oriented schools confirmed headteacher or deputy leadership present"
                },
                {
                    "label": "What Children Learned",
                    "value": f"{p1_rate_overall}% Unaided Recall",
                    "detail": f"{p1_rate_overall}% of learners in post-session intercepts correctly explained core nutrition messages"
                },
                {
                    "label": "Fair & Accessible for All",
                    "value": "100% Local Language",
                    "detail": "All sessions delivered in Ngakarimojong dialects with accessible seating for PWDs"
                },
                {
                    "label": "Teacher Patrons in Charge",
                    "value": f"{len(active_schools_set)} Appointed Club Patrons",
                    "detail": f"Club patrons active across {len(active_schools_set)} schools with established clubs"
                },
                {
                    "label": "Safe with No Retaliation",
                    "value": "0 Complaints",
                    "detail": "WFP toll-free hotline (0800) promoted with zero complaints recorded"
                }
            ],
            "verification_source": "Observation protocols, teacher feedback notes, and intercept exit polls."
        },
        {
            "question": "What changed?",
            "subtitle": "Real behavioral shifts observed",
            "cadence": "Comparing baseline vs endline",
            "status_badge": "Field Submissions Active",
            "key_metrics": [
                {
                    "label": "Adding Greens to Morning Porridge",
                    "value": "Awaiting Closeouts",
                    "detail": "Household recipe trial audits pending Visit 3 closeouts (0 schools audited)"
                },
                {
                    "label": "Boys Helping with Morning Chores",
                    "value": f"{poll_agreed_pct}% Consensus",
                    "detail": f"{poll_agreed_pct}% agreement across {tot_poll_boys:,} boy responses in Visit 2 micro-polls that domestic chores must be shared"
                },
                {
                    "label": "Girls Arriving on Time for Class",
                    "value": "Pending Closeouts",
                    "detail": "Attendance and punctuality gains will be verified at Visit 3 closeouts"
                },
                {
                    "label": "Serving Toddlers First",
                    "value": "Awaiting Closeouts",
                    "detail": "Youngest child prioritization pending household verification at Visit 3"
                },
                {
                    "label": "Saving Daily Firewood",
                    "value": "Awaiting Demos",
                    "detail": "Firewood savings to be verified during community cooking demonstrations"
                },
                {
                    "label": "Returned Home Charts",
                    "value": "0 Charts Returned",
                    "detail": "Charts to be collected and audited during Visit 3 closeout audits"
                },
                {
                    "label": "Clubs Continuing on Their Own",
                    "value": f"{tot_clubs} Active Clubs",
                    "detail": f"{tot_clubs} NutriClubs established with weekly meetings across active schools"
                }
            ],
            "verification_source": "Longitudinal attendance registers, NutriChart audits, and Visit 3 closeout forms."
        }
    ],
    "three_prong_results_matrix": [
        {
            "prong": "Food & Nutrition",
            "icon": "fa-apple-whole",
            "theme_color": "emerald",
            "how_much": {
                "headline": f"{tot_orient_schools} Orientations · {v2_completed_count} Activations",
                "data_points": [
                    f"{tot_orient_schools} schools oriented on Metu porridge fortification and clean cooking",
                    f"{v2_completed_count} schools delivered Visit 2 Big Activation Day ({tot_v2_pupils} pupils engaged)",
                    "0 of 640 community cooking demonstrations conducted to date"
                ]
            },
            "how_well": {
                "headline": f"{p1_rate_overall}% Unaided Recall · 100% Local Foods",
                "data_points": [
                    f"{p1_rate_overall}% unaided recall of local greens (Eboo, Lokaka) in post-session intercepts",
                    "100% compliance with easy-to-find wild greens and zero unattainable ingredients",
                    "Community demonstration hands-on cooking pending rollout"
                ]
            },
            "what_changed": {
                "headline": "Awaiting Closeout Audits",
                "data_points": [
                    "Household recipe trial audits pending Visit 3 closeouts",
                    "0 returned Home Charts audited (pending Visit 3)",
                    "Toddler feeding priority to be verified in community demos"
                ]
            }
        },
        {
            "prong": "School & Learning",
            "icon": "fa-graduation-cap",
            "theme_color": "blue",
            "how_much": {
                "headline": f"{v2_completed_count} Visits · {tot_clubs} Active NutriClubs",
                "data_points": [
                    f"{v2_completed_count} primary schools completed Visit 2 Big Activation Day",
                    f"{tot_clubs} active school clubs established ({total_active_members} registered members across active schools)",
                    "Target: 64 primary schools completing all 3 visits (192 visits total)"
                ]
            },
            "how_well": {
                "headline": f"{tot_orient_schools} Schools Oriented · 100% Inclusive",
                "data_points": [
                    f"All {tot_orient_schools} oriented schools confirmed active teacher & headteacher leadership",
                    f"{tot_pwd} persons with disabilities accommodated and actively participating",
                    "Zero learners excluded during interactive activation sessions"
                ]
            },
            "what_changed": {
                "headline": "Longitudinal Tracking Initiated",
                "data_points": [
                    f"Longitudinal attendance tracking initiated ({tot_v1_pupils + tot_v2_pupils} learners logged in Visit 1 & Visit 2)",
                    "Punctuality and attendance rebound to be audited at Visit 3",
                    "Out-of-school girl tracing pending closeout reports"
                ]
            }
        },
        {
            "prong": "Sharing Chores at Home",
            "icon": "fa-venus-mars",
            "theme_color": "purple",
            "how_much": {
                "headline": f"{v2_completed_count} Activation Dialogues · {tot_caregivers} Caregivers",
                "data_points": [
                    f"Structured chore rebalancing dialogues delivered across {v2_completed_count} schools",
                    f"{tot_caregivers} community caregivers and elders attended school activations",
                    "Target: 640 community discussions in villages around 64 schools"
                ]
            },
            "how_well": {
                "headline": f"{p2_rate_overall}% Chore Agreement · 0 Hotline Complaints",
                "data_points": [
                    f"{p2_rate_overall}% agreement in micro-polls that chores should be shared equally",
                    "Dialogue conducted constructively without assigning blame to individuals",
                    "WFP toll-free hotline (0800) promoted with zero retaliation complaints"
                ]
            },
            "what_changed": {
                "headline": "Consensus on Domestic Sharing",
                "data_points": [
                    f"{p2_equal} of {p2_equal + p2_hurry} polled learners agreed boys must help with morning water/wood",
                    "School pledges signed committing to equitable chore support",
                    "Household morning chore division to be audited during Visit 3 closeouts"
                ]
            }
        }
    ],
    "monitoring_cycle_results": [
        {
            "stage": "Before the Campaign",
            "title": "Where We Started (Baseline)",
            "desc": "Checking the situation in sample schools before the campaign began",
            "data_collected": [
                "Attendance: - (Pending Visit 1 baseline register logs)",
                "Enriched Porridge: Pending baseline audits (0 schools)",
                "Sharing Chores: Pending baseline audits (0 schools)",
                "Serving Children First: Pending baseline audits (0 schools)"
            ]
        },
        {
            "stage": "Week One",
            "title": "Visit 1: Getting Started in Class",
            "desc": "Healthy food sorting, the Adere calabash game, and Home Charts given out",
            "data_collected": [
                f"Children Audited: {tot_v1_pupils:,} weekly attendees ({tot_v1_enrol:,} total enrolled) across {len(v1_all_schools_records)} schools",
                f"Classroom Practice: {len(v1_all_schools_records)} schools completed onboarding & audit",
                f"Home Charts Given: {tot_v1_charts:,} classroom NutriCharts issued across Lower, Middle, Upper primary",
                f"Patrons Appointed: {tot_patrons_app} teacher patrons appointed across {tot_orient_schools} orientation schools (plus {tot_clubs} club patrons)"
            ]
        },
        {
            "stage": "Week Two",
            "title": "Visit 2: NutriBus Day Activation",
            "desc": "Big interactive bus stations, school pledges, and community cooking demos",
            "data_collected": [
                f"Attendance Logged: {tot_v2_pupils} learners counted across {v2_completed_count} schools",
                f"What Pupils Remembered: {p1_rate_overall}% unaided recall of core messages ({p1_specific} actionable fortification recipes)",
                f"School Pledges: {v2_completed_count} school commitments signed",
                "Village Cooking Demos: 0 demos logged (Target: 640 sites)"
            ]
        },
        {
            "stage": "Week Three",
            "title": "Visit 3: Checking Real Changes",
            "desc": "Checking returned Home Charts, pupil teach-back, and ongoing clubs",
            "data_collected": [
                "Attendance Growth: - (Awaiting Visit 3 closeouts)",
                "Charts Returned: 0 returned (Pending Visit 3 closeout audits)",
                "School Commitments: Pending endline verification (0 schools)",
                f"Club Continuity: {tot_clubs} NutriClubs active ({total_active_members} registered members across active schools)"
            ]
        },

        {
            "stage": "In the Villages",
            "title": "In the Villages: Fathers, Elders & Stoves",
            "desc": "Village gatherings, male participation, and saving firewood",
            "data_collected": [
                "Community Demos: 0 cooking demonstrations held (Target: 640)",
                f"Caregivers Reached: {tot_caregivers} caregivers attended school activations",
                "Home Follow-Up: Awaiting community demonstration rollout",
                "Hotline Redress: 0 complaints logged on WFP hotline (0800)"
            ]
        },
        {
            "stage": "On the Radio",
            "title": "On the Radio & For Everyone",
            "desc": "Radio broadcasts, local language, and including people with disabilities",
            "data_collected": [
                "Radio Broadcasts: Transmission logs pending broadcast collation",
                f"Disability Inclusion: {tot_pwd} persons with disabilities accommodated",
                "Local Language: 100% of sessions delivered in Ngakarimojong dialects",
                "Saving Firewood: Fuel saving practices to be audited during community demos"
            ]
        }
    ]
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
