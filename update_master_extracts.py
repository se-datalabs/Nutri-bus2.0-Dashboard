import json
import pandas as pd

def update_all_extracts():
    print("📑 Updating Master Extraction Spreadsheets and CSVs...")
    d = json.load(open("dashboard_data.json"))
    demos_json = {x["entry_index"]: x for x in json.load(open("dashboard_demo_sessions_640.json"))}
    df = pd.read_excel("Nutribus_2.0_Activity.xlsx")

    nc_reg = d["nutriclub_sessions"]["schools_register"]
    v1_schools = d["three_visit_contact"]["visit1"]["schools_data"]
    v2_schools = d["three_visit_contact"]["visit2"]["schools_data"]
    v3_schools = d["three_visit_contact"]["visit3"]["schools_data"]

    v1_set = {(s["district"], s["school"]) for s in v1_schools}
    v2_set = {(s["district"], s["school"]) for s in v2_schools}
    v3_set = {(s["district"], s["school"]) for s in v3_schools}

    # MSC Stories from dashboard_data
    msc_stories = d.get("msc_stories", {}).get("stories_register", [])
    school_stories = {}
    for s in msc_stories:
        key = (s["district"], s["school"])
        if key not in school_stories:
            school_stories[key] = {"school_story": 0, "community_story": 0}
        if s.get("story_type") == "School Story":
            school_stories[key]["school_story"] += 1
        else:
            school_stories[key]["community_story"] += 1

    visit_matrix = []
    msc_tracking = []

    for s in sorted(nc_reg, key=lambda x: (x["district"], x["school"])):
        dist = s["district"]
        sch = s["school"]
        sub = s.get("subcounty", "")
        has_v1 = (dist, sch) in v1_set
        has_v2 = (dist, sch) in v2_set
        has_v3 = (dist, sch) in v3_set
        
        st_info = school_stories.get((dist, sch), {"school_story": 0, "community_story": 0})
        sch_st = st_info["school_story"]
        comm_st = st_info["community_story"]
        tot_st = sch_st + comm_st
        
        if tot_st == 0:
            msc_status = "MISSING (0 of 2)"
            follow_up = "Collect 1 School Story + 1 Community Story"
        elif tot_st == 1:
            if sch_st > 0:
                msc_status = "PARTIAL (1 of 2: School done, Community missing)"
                follow_up = "Collect Community Catchment Story"
            else:
                msc_status = "PARTIAL (1 of 2: Community done, School missing)"
                follow_up = "Collect School Story"
        else:
            msc_status = f"COMPLETED ({tot_st} of 2)"
            follow_up = "Target Achieved"
        
        visit_matrix.append({
            "District": dist,
            "Subcounty": sub,
            "School": sch,
            "Visit 1 Baseline": "Yes" if has_v1 else "MISSING",
            "Visit 2 Activation": "Yes" if has_v2 else "MISSING",
            "Visit 3 Closeout": "Yes" if has_v3 else "Pending",
            "School Story (1 Target)": "Logged" if sch_st > 0 else "MISSING",
            "Community Story (1 Target)": "Logged" if comm_st > 0 else "MISSING",
            "MSC Total Progress": f"{tot_st} of 2 ({msc_status})"
        })
        
        msc_tracking.append({
            "District": dist,
            "Subcounty": sub,
            "School": sch,
            "Total Target Stories": 2,
            "School Story Target": 1,
            "School Story Logged": sch_st,
            "Community Catchment Story Target": 1,
            "Community Catchment Story Logged": comm_st,
            "Total Stories Logged": tot_st,
            "Remaining Stories Needed": max(0, 2 - tot_st),
            "Status": msc_status,
            "Follow-Up Action Required": follow_up
        })

    df_visits = pd.DataFrame(visit_matrix)
    df_msc = pd.DataFrame(msc_tracking)

    # VHTs & Community Demos (305)
    act_col = [c for c in df.columns if c.strip().lower() == "activity"][0]
    demos_df = df[df[act_col].astype(str).str.contains("Community demonstration|demonstration|demo", case=False, na=False)].copy()
    vht_rows = []
    for _, r in demos_df.iterrows():
        idx = int(r["_index"])
        dj = demos_json.get(idx, {})
        vht_raw = str(r.get("Name of VHT", "")).strip() if pd.notnull(r.get("Name of VHT")) else ""
        who_raw = str(r.get("Who was on ground when this demo happened", "")).strip() if pd.notnull(r.get("Who was on ground when this demo happened")) else ""
        vht_rows.append({
            "Entry Index": idx,
            "Date": dj.get("date", str(r.get("Date", "")).split(" ")[0]),
            "District": str(r.get("District", dj.get("district", ""))).strip(),
            "Subcounty": dj.get("subcounty", "Catchment"),
            "Catchment School": dj.get("school", ""),
            "Community Demo Site / Village": str(r.get("Village / Catchment Demo Site", "")).strip() if pd.notnull(r.get("Village / Catchment Demo Site")) else dj.get("site", ""),
            "Who Was On Ground": who_raw,
            "Name of VHT": vht_raw if vht_raw else "Not specified (Coordinator led)",
            "Field Coordinator": dj.get("facilitator", str(r.get("Coordinator Name", ""))),
            "Total Attendees": dj.get("total", 0)
        })
    df_vhts = pd.DataFrame(vht_rows).sort_values(["District", "Catchment School", "Entry Index"])

    # Teachers & Club Patrons (64)
    nc_sess = d["nutriclub_sessions"]["sample_sessions"]
    patron_map = {}
    for s in nc_sess:
        key = (s["district"], s["school"])
        p = str(s.get("patron", "")).strip()
        if p and p.lower() not in ("nan", "none", "to be appointed"):
            if key not in patron_map:
                patron_map[key] = []
            if p not in patron_map[key]:
                patron_map[key].append(p)

    teacher_rows = []
    for s in sorted(nc_reg, key=lambda x: (x["district"], x["school"])):
        dist = s["district"]
        sch = s["school"]
        p_reg = str(s.get("patron_name", "")).strip()
        p_list = patron_map.get((dist, sch), [])
        if p_list:
            patron_str = " / ".join(p_list)
        elif p_reg and p_reg.lower() not in ("nan", "none"):
            patron_str = p_reg
        else:
            patron_str = "Not yet logged (Session 2 only / Pending)"
        teacher_rows.append({
            "District": dist,
            "Subcounty": s.get("subcounty", ""),
            "School": sch,
            "Teacher / Club Patron Name(s)": patron_str,
            "Club Membership": s.get("total_membership", 0),
            "Session 1 Logged": "Yes" if s.get("session_one") else "No",
            "Session 2 Logged": "Yes" if s.get("session_two") else "No"
        })
    df_teachers = pd.DataFrame(teacher_rows)

    # Master Workbook
    with pd.ExcelWriter("VHTs_Teachers_and_Demos_Master_Extract.xlsx", engine="openpyxl") as writer:
        df_visits.to_excel(writer, sheet_name="Missing Visits & MSC Status", index=False)
        df_msc.to_excel(writer, sheet_name="Missing MSC Stories (128 Tgt)", index=False)
        df_vhts.to_excel(writer, sheet_name=f"VHTs & Demos ({len(df_vhts)})", index=False)
        df_teachers.to_excel(writer, sheet_name="Teachers & Club Patrons (64)", index=False)

    # Standalone Extracts
    df_vhts.to_excel("VHTs_and_Community_Demos_Extract.xlsx", index=False)
    df_vhts.to_csv("VHTs_and_Community_Demos_Extract.csv", index=False)
    df_teachers.to_excel("Teachers_and_School_Patrons_Extract.xlsx", index=False)
    df_teachers.to_csv("Teachers_and_School_Patrons_Extract.csv", index=False)
    df_msc.to_excel("Missing_MSC_Stories_Tracking.xlsx", index=False)
    df_msc.to_csv("Missing_MSC_Stories_Tracking.csv", index=False)

    print(f"✅ Master extraction complete: {len(df_vhts)} Demos | {len(df_teachers)} Teachers | {len(df_visits)} Schools tracked.")

if __name__ == "__main__":
    update_all_extracts()
