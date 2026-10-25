import json
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def apply_professional_styles(ws):
    header_fill = PatternFill(start_color="0A6EB4", end_color="0A6EB4", fill_type="solid")
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Arial", size=10, color="1E293B")
    
    thin_border_side = Side(border_style="thin", color="CBD5E1")
    border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    
    # Status fills
    missing_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    missing_font = Font(name="Arial", size=10, bold=True, color="991B1B")
    
    success_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    success_font = Font(name="Arial", size=10, bold=True, color="166534")
    
    pending_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    pending_font = Font(name="Arial", size=10, bold=True, color="92400E")
    
    # Freeze top row
    ws.freeze_panes = "A2"
    
    # Format header row
    ws.row_dimensions[1].height = 28
    for col_idx in range(1, ws.max_column + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
        
    # Format data rows
    for row_idx in range(2, ws.max_row + 1):
        ws.row_dimensions[row_idx].height = 20
        for col_idx in range(1, ws.max_column + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border
            val_str = str(cell.value or "").strip()
            
            # Text alignment
            if isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif any(w in val_str.lower() for w in ["yes", "no", "logged", "missing", "pending"]):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                
            # Conditional coloring
            if "missing" in val_str.lower():
                cell.fill = missing_fill
                cell.font = missing_font
            elif any(w in val_str.lower() for w in ["yes", "logged", "completed", "target achieved"]):
                cell.fill = success_fill
                cell.font = success_font
            elif any(w in val_str.lower() for w in ["pending", "partial"]):
                cell.fill = pending_fill
                cell.font = pending_font
            elif "total" in val_str.lower() and (row_idx == ws.max_row or col_idx == 1):
                cell.fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
                cell.font = Font(name="Arial", size=10, bold=True, color="0F172A")

    # Set column widths with maximum wrap cap
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val = str(cell.value or "")
            if len(val) > max_len:
                max_len = len(val)
        col_width = min(max(max_len + 4, 12), 48)
        ws.column_dimensions[col_letter].width = col_width

    # Enable autofilter
    ws.auto_filter.ref = ws.dimensions

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

    # Detailed MSC Stories Register (5 stories)
    msc_detailed_rows = []
    for s in msc_stories:
        msc_detailed_rows.append({
            "Story ID": s.get("id", ""),
            "Entry Index": s.get("entry_index", ""),
            "Date": s.get("date", ""),
            "District": s.get("district", ""),
            "School": s.get("school", ""),
            "Storyteller Name & Age": s.get("name_and_age", ""),
            "Storyteller Role": s.get("role", ""),
            "Story Type": s.get("story_type", ""),
            "Triggering Campaign Event": s.get("event", ""),
            "Practical Action Done Differently": s.get("action_done", ""),
            "Why Significant (Verbatim Quote)": s.get("why_significant", ""),
            "Verifiable Physical Evidence Sighted": s.get("evidence", ""),
            "Collector Observations / Notes": s.get("collector_notes", ""),
            "Situation Before Campaign": s.get("situation_before", ""),
            "Field Coordinator": s.get("collector", "")
        })
    df_msc_detailed = pd.DataFrame(msc_detailed_rows)

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

    # District Coordinators & Entries Per Activity
    def normalize_coordinator_name(raw_c, raw_s):
        val = raw_s if str(raw_c).strip().lower() in ("other", "nan", "none", "") and pd.notnull(raw_s) else raw_c
        val = str(val).strip() if pd.notnull(val) else ""
        vl = val.lower()
        if "lopeyok" in vl or "martin" in vl:
            return "Lopeyok Martin"
        elif "priscilla" in vl:
            return "Priscilla"
        elif "cheparen" in vl or "pauline" in vl:
            return "Cheparen Pauline"
        elif "evaline" in vl or "evalyne" in vl:
            return "Evaline"
        elif "amoo" in vl or "sofia" in vl:
            return "Amoo Sofia"
        elif "ngole" in vl or "paula" in vl:
            return "Ngole Paula"
        elif "lobu" in vl or "stephen" in vl:
            return "Lobur Stephen"
        elif "awas" in vl:
            return "Awas Francis"
        elif "ochen" in vl and "ogwang" in vl:
            return "Ochen Moses Tom & Ogwang Sam"
        elif "ochen" in vl:
            return "Ochen Moses Tom"
        elif "ogwang" in vl:
            return "Ogwang Sam"
        elif "opio" in vl and "okello" in vl:
            return "Opio John Fred & Okello Daniel Nimaro"
        elif "opio" in vl:
            return "Opio John Fred"
        elif "okello" in vl and "abia" not in vl and "vincent" not in vl:
            return "Okello Daniel Nimaro"
        elif "abia" in vl or "vincent" in vl:
            return "Abia Francis & Okello Vincent"
        elif "emma" in vl or "semakula" in vl:
            return "Ngole Paula"
        return val if val else "Unspecified"

    def classify_activity(act_raw, milestone_raw):
        act = str(act_raw).strip()
        m = str(milestone_raw).strip() if pd.notnull(milestone_raw) else ""
        if "Orientation" in act:
            return "Teacher & VHT Orientation"
        elif "Three visit" in act or "visit" in act.lower():
            if "Visit 1" in m:
                return "School Visit 1 (Follow-up)"
            elif "Visit 2" in m:
                return "School Visit 2 (Big Activation)"
            elif "Visit 3" in m:
                return "School Visit 3 (Closing Audit)"
            return "Three Visit (Other)"
        elif "Nutriclub" in act:
            return "NutriClub Sessions"
        elif "Community" in act or "demo" in act.lower():
            return "Community Cooking Demos"
        elif "change" in act.lower() or "msc" in act.lower() or "stories" in act.lower():
            return "MSC Stories"
        return act if act else "Other Activity"

    def get_school_location(row, dist):
        raw = None
        if dist in row and pd.notnull(row[dist]):
            raw = str(row[dist]).strip()
        if not raw:
            for d in ["Abim", "Amudat", "Kaabong", "Karenga", "Kotido", "Moroto", "Nabilatuk", "Nakapiripirit", "Napak"]:
                if d in row and pd.notnull(row[d]):
                    raw = str(row[d]).strip()
                    break
        if not raw:
            for col in row.index:
                if "school" in str(col).lower() and pd.notnull(row[col]):
                    raw = str(row[col]).strip()
                    break
        if not raw and pd.notnull(row.get("Village / Catchment Demo Site")):
            raw = str(row.get("Village / Catchment Demo Site")).strip()
        return raw if raw else "Catchment Area"

    coord_col = [c for c in df.columns if "coordinator name" in c.lower()][0]
    spec_col = [c for c in df.columns if c.strip().lower() == "specify"][0]
    dist_col = [c for c in df.columns if c.strip().lower() == "district"][0]
    m_col = [c for c in df.columns if "milestone being conducted" in c.lower()][0]

    from collections import defaultdict
    matrix = defaultdict(lambda: defaultdict(int))
    rows_log = []

    for _, r in df.iterrows():
        idx = int(r["_index"])
        dt = str(r.get("Date", "")).split(" ")[0]
        dist = str(r.get(dist_col, "")).strip()
        coord = normalize_coordinator_name(r.get(coord_col), r.get(spec_col))
        act_type = classify_activity(r.get(act_col), r.get(m_col))
        loc = get_school_location(r, dist)

        matrix[(dist, coord)][act_type] += 1
        matrix[(dist, coord)]["Total"] += 1

        rows_log.append({
            "Entry Index": idx,
            "Date": dt,
            "District": dist,
            "District Coordinator": coord,
            "Activity Category": str(r.get(act_col, "")).strip(),
            "Activity / Milestone": act_type,
            "School / Demo Site": loc,
            "Submission Status": "Logged & Verified"
        })

    activity_cols = [
        "Teacher & VHT Orientation",
        "School Visit 1 (Follow-up)",
        "School Visit 2 (Big Activation)",
        "School Visit 3 (Closing Audit)",
        "NutriClub Sessions",
        "Community Cooking Demos",
        "MSC Stories"
    ]

    summary_rows = []
    for (dist, coord), acts in sorted(matrix.items()):
        row_data = {
            "District": dist,
            "District Coordinator": coord
        }
        for ac in activity_cols:
            row_data[ac] = acts.get(ac, 0)
        row_data["Total Entries Logged"] = acts["Total"]
        summary_rows.append(row_data)

    total_row = {
        "District": "TOTAL (Karamoja Region)",
        "District Coordinator": "All District Coordinators"
    }
    for ac in activity_cols:
        total_row[ac] = sum(r[ac] for r in summary_rows)
    total_row["Total Entries Logged"] = sum(r["Total Entries Logged"] for r in summary_rows)
    summary_rows.append(total_row)

    df_coord_summary = pd.DataFrame(summary_rows)
    df_coord_log = pd.DataFrame(rows_log).sort_values(["District", "District Coordinator", "Entry Index"])

    # Master Workbook (7 Tabs)
    master_file = "VHTs_Teachers_and_Demos_Master_Extract.xlsx"
    with pd.ExcelWriter(master_file, engine="openpyxl") as writer:
        df_coord_summary.to_excel(writer, sheet_name="Coordinator Activity Summary", index=False)
        df_coord_log.to_excel(writer, sheet_name=f"Coordinator Entries Log ({len(df_coord_log)})", index=False)
        df_visits.to_excel(writer, sheet_name="Missing Visits & MSC Status", index=False)
        df_msc.to_excel(writer, sheet_name="Missing MSC Stories (128 Tgt)", index=False)
        df_msc_detailed.to_excel(writer, sheet_name="MSC Stories Register (5)", index=False)
        df_vhts.to_excel(writer, sheet_name=f"VHTs & Demos ({len(df_vhts)})", index=False)
        df_teachers.to_excel(writer, sheet_name="Teachers & Club Patrons (64)", index=False)

    # Apply professional styling to Master Workbook
    wb_master = openpyxl.load_workbook(master_file)
    for sheet_name in wb_master.sheetnames:
        apply_professional_styles(wb_master[sheet_name])
    wb_master.save(master_file)

    print(f"✅ Combined Master Workbook updated: {master_file} ({len(df_coord_summary)} Coordinator Rows | {len(df_vhts)} Demos | {len(df_teachers)} Teachers | {len(df_visits)} Schools | {len(df_msc_detailed)} MSC Stories).")

if __name__ == "__main__":
    update_all_extracts()
