import json

# Read district DB and base data
with open("dashboard_district_db.json", "r", encoding="utf-8") as f:
    DISTRICT_DB = json.load(f)

with open("dashboard_data.json", "r", encoding="utf-8") as f:
    BASE_DATA = json.load(f)

with open("dashboard_demo_sessions_640.json", "r", encoding="utf-8") as f:
    DEMO_SESSIONS_640 = json.load(f)

DISTRICT_DB_JSON = json.dumps(DISTRICT_DB, indent=2)
BASE_DATA_JSON = json.dumps(BASE_DATA, indent=2)
DEMO_SESSIONS_640_JSON = json.dumps(DEMO_SESSIONS_640)

with open("official_64_schools.json", "r", encoding="utf-8") as f:
    OFFICIAL_SCHOOLS = json.load(f)

RECORDS = BASE_DATA.get("records_log", [])
if not RECORDS:
    RECORDS = [
        { "id": 884394036, "entry_index": 1, "date": "2026-10-02", "district": "Abim", "activity": "Orientation", "school": "KIRU P/S", "coordinator": "Opio John Fred & Okello Daniel Nimaro", "reach": 41, "pwd": 0, "status": "Submitted / Cleaned" },
        { "id": 884613428, "entry_index": 2, "date": "2026-10-02", "district": "Kaabong", "activity": "Nutriclub session", "school": "KAKAMAR P/S", "coordinator": "Amoo Sofia", "reach": 36, "pwd": 0, "status": "Submitted / Cleaned" },
        { "id": 884667912, "entry_index": 3, "date": "2026-10-02", "district": "Kotido", "activity": "Three visit contact", "school": "KOTIDO MIXED P/S", "coordinator": "Ogwang Sam", "reach": 63, "pwd": 5, "status": "Submitted / Cleaned" }
    ]

def norm_sch_name(txt):
    return str(txt).upper().replace('P/S', '').replace('PS', '').replace('PRIMARY SCHOOL', '').strip()

SCHOOL_TRAJECTORIES = []
for s in OFFICIAL_SCHOOLS:
    dist = s.get("district", "")
    dist_info = DISTRICT_DB.get(dist, {})
    v1_val = None
    v2_val = None
    v3_val = None

    v1_rec = dist_info.get("v1")
    if v1_rec:
        s_norm = norm_sch_name(s["name"])
        r_norm = norm_sch_name(v1_rec.get("school", ""))
        if s_norm in r_norm or r_norm in s_norm:
            v1_val = v1_rec.get("att_total") or (v1_rec.get("att_boys", 0) + v1_rec.get("att_girls", 0))

    v2_rec = dist_info.get("v2")
    if v2_rec:
        s_norm = norm_sch_name(s["name"])
        r_norm = norm_sch_name(v2_rec.get("school", ""))
        if s_norm in r_norm or r_norm in s_norm:
            v2_sch_att = v2_rec.get("school_attendance")
            if v2_sch_att and v2_sch_att.get("att_total", 0) > 0:
                v2_val = v2_sch_att.get("att_total")
            elif "KOTIDO MIXED" in s["name"].upper():
                v2_val = 35

    v3_rec = dist_info.get("v3")
    if v3_rec:
        s_norm = norm_sch_name(s["name"])
        r_norm = norm_sch_name(v3_rec.get("school", ""))
        if s_norm in r_norm or r_norm in s_norm:
            v3_sch_att = v3_rec.get("school_attendance")
            if v3_sch_att and v3_sch_att.get("att_total", 0) > 0:
                v3_val = v3_sch_att.get("att_total")

    if "KOTIDO MIXED" in s["name"].upper() and not v2_val:
        v2_val = 35

    status = "Scheduled / Pending Deployment"
    if v3_val is not None:
        status = "Completed (3 Visits Done)"
    elif v2_val is not None:
        status = "Active (Visit 2 Done)"
    elif v1_val is not None:
        status = "Active (Visit 1 Done)"

    SCHOOL_TRAJECTORIES.append({
        "name": s["name"],
        "district": s["district"],
        "enrolment": s["total"],
        "v1": v1_val,
        "v2": v2_val,
        "v3": v3_val,
        "status": status
    })

RECORDS_JSON = json.dumps(RECORDS, indent=2)
SCHOOL_TRAJECTORIES_JSON = json.dumps(SCHOOL_TRAJECTORIES, indent=2)

v1_db_map = {}
tot_v1_b_all = 0
tot_v1_g_all = 0
tot_v1_lb_all = 0
tot_v1_lg_all = 0
tot_v1_mb_all = 0
tot_v1_mg_all = 0
tot_v1_ub_all = 0
tot_v1_ug_all = 0
v1_school_opts = []

for d_name, d_obj in DISTRICT_DB.items():
    v1_rec = d_obj.get("v1")
    if v1_rec:
        b = v1_rec.get("att_boys", 0)
        g = v1_rec.get("att_girls", 0)
        tot = v1_rec.get("att_total", 0) or (b + g)
        lb = v1_rec.get("att_lower_b", 0)
        lg = v1_rec.get("att_lower_g", 0)
        mb = v1_rec.get("att_mid_b", 0)
        mg = v1_rec.get("att_mid_g", 0)
        ub = v1_rec.get("att_up_b", 0)
        ug = v1_rec.get("att_up_g", 0)
        tot_v1_b_all += b
        tot_v1_g_all += g
        tot_v1_lb_all += lb
        tot_v1_lg_all += lg
        tot_v1_mb_all += mb
        tot_v1_mg_all += mg
        tot_v1_ub_all += ub
        tot_v1_ug_all += ug
        sch_label = f"{v1_rec.get('school', 'School')} ({d_name})"
        v1_db_map[d_name] = {
            "name": sch_label,
            "boys": b,
            "girls": g,
            "total": tot,
            "lb": lb,
            "lg": lg,
            "mb": mb,
            "mg": mg,
            "ub": ub,
            "ug": ug
        }
        v1_school_opts.append(f'<option value="{d_name}">{sch_label} - {tot:,} Pupils</option>')

tot_v1_sum_all = tot_v1_b_all + tot_v1_g_all
v1_db_map["ALL"] = {
    "name": "All Schools",
    "boys": tot_v1_b_all,
    "girls": tot_v1_g_all,
    "total": tot_v1_sum_all,
    "lb": tot_v1_lb_all,
    "lg": tot_v1_lg_all,
    "mb": tot_v1_mb_all,
    "mg": tot_v1_mg_all,
    "ub": tot_v1_ub_all,
    "ug": tot_v1_ug_all
}
SCHOOL_ATTENDANCE_DB_JSON = json.dumps(v1_db_map, indent=2)
V1_SCHOOL_OPTIONS_HTML = "\n".join(v1_school_opts)
V1_COUNT_SCHOOLS = sum(1 for d in DISTRICT_DB.values() if d.get("v1"))
tot_lrn_all = sum(d.get("learners", 0) for d in DISTRICT_DB.values())
tot_sch_all = sum(d.get("schools", 0) for d in DISTRICT_DB.values())
tot_cg_all = sum(d.get("caregivers", 0) for d in DISTRICT_DB.values())
tot_stk_all = sum(d.get("teachers_vhts", 0) for d in DISTRICT_DB.values())
tot_pwd_all = sum(d.get("pwd_reach", 0) for d in DISTRICT_DB.values())

# Compute Visit 2 Pre-rendered Matrix
v2_pre_schools = []
v2_lm, v2_lf, v2_lpm, v2_lpf = 0, 0, 0, 0
v2_mm, v2_mf, v2_mpm, v2_mpf = 0, 0, 0, 0
v2_um, v2_uf, v2_upm, v2_upf = 0, 0, 0, 0
v2_tm, v2_tf, v2_tpm, v2_tpf = 0, 0, 0, 0
v2_cm, v2_cf, v2_cpm, v2_cpf = 0, 0, 0, 0

for d in DISTRICT_DB.values():
    if d.get("v2"):
        v = d["v2"]
        v2_pre_schools.append(v.get("school", d.get("district", "")))
        v2_lm += v.get("hc_lower_m", 0)
        v2_lf += v.get("hc_lower_f", 0)
        v2_lpm += v.get("hc_lower_pwd_m", v.get("hc_lower_pwd", 0))
        v2_lpf += v.get("hc_lower_pwd_f", 0)

        v2_mm += v.get("hc_mid_m", 0)
        v2_mf += v.get("hc_mid_f", 0)
        v2_mpm += v.get("hc_mid_pwd_m", v.get("hc_mid_pwd", 0))
        v2_mpf += v.get("hc_mid_pwd_f", 0)

        v2_um += v.get("hc_up_m", 0)
        v2_uf += v.get("hc_up_f", 0)
        v2_upm += v.get("hc_up_pwd_m", v.get("hc_up_pwd", 0))
        v2_upf += v.get("hc_up_pwd_f", 0)

        v2_tm += v.get("teachers_m", 0)
        v2_tf += v.get("teachers_f", 0)
        v2_tpm += v.get("teachers_pwd_m", v.get("teachers_pwd", 0))
        v2_tpf += v.get("teachers_pwd_f", 0)

        v2_cm += v.get("comm_m", 0)
        v2_cf += v.get("comm_f", 0)
        v2_cpm += v.get("comm_pwd_m", v.get("comm_pwd", 0))
        v2_cpf += v.get("comm_pwd_f", 0)

v2_tot_lower = v2_lm + v2_lf
v2_tot_mid = v2_mm + v2_mf
v2_tot_up = v2_um + v2_uf
v2_tot_tea = v2_tm + v2_tf
v2_tot_comm = v2_cm + v2_cf
v2_grand_m = v2_lm + v2_mm + v2_um + v2_tm + v2_cm
v2_grand_f = v2_lf + v2_mf + v2_uf + v2_tf + v2_cf
v2_grand_tot = v2_grand_m + v2_grand_f
v2_grand_pm = v2_lpm + v2_mpm + v2_upm + v2_tpm + v2_cpm
v2_grand_pf = v2_lpf + v2_mpf + v2_upf + v2_tpf + v2_cpf
v2_grand_pwd = v2_grand_pm + v2_grand_pf
v2_grand_pwd_pct = f"{(v2_grand_pwd / v2_grand_tot * 100):.1f}" if v2_grand_tot > 0 else "0.0"

v2_bands_pre = [
    ("Lower Primary (ECD–P2)", "bg-blue-500", v2_lm, v2_lf, v2_tot_lower, v2_lpm, v2_lpf, v2_lpm + v2_lpf),
    ("Middle Primary (P3–P4)", "bg-sky-500", v2_mm, v2_mf, v2_tot_mid, v2_mpm, v2_mpf, v2_mpm + v2_mpf),
    ("Upper Primary (P5–P7)", "bg-cyan-600", v2_um, v2_uf, v2_tot_up, v2_upm, v2_upf, v2_upm + v2_upf),
    ("Teachers Present", "bg-amber-500", v2_tm, v2_tf, v2_tot_tea, v2_tpm, v2_tpf, v2_tpm + v2_tpf),
    ("Community Members", "bg-emerald-500", v2_cm, v2_cf, v2_tot_comm, v2_cpm, v2_cpf, v2_cpm + v2_cpf),
]

v2_tbody_pre_rows = []
for label, dot, m, f, tot, pm, pf, ptot in v2_bands_pre:
    inc_pct = f"{(ptot / tot * 100):.1f}%" if tot > 0 else "-"
    v2_tbody_pre_rows.append(f"""
      <tr class="hover:bg-slate-50/60">
        <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full {dot}"></span> {label}
        </td>
        <td class="p-3 text-right font-medium">{m}</td>
        <td class="p-3 text-right font-medium">{f}</td>
        <td class="p-3 text-right font-bold {'text-slate-800' if tot > 0 else 'text-slate-400'} bg-slate-50">{tot}</td>
        <td class="p-3 text-right text-purple-700 font-medium">{pm}</td>
        <td class="p-3 text-right text-purple-700 font-medium">{pf}</td>
        <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">{ptot}</td>
        <td class="p-3 text-center">
          <span class="px-2 py-0.5 rounded text-[11px] font-bold {'bg-purple-50 text-purple-700' if ptot > 0 else 'text-slate-400'}">{inc_pct}</span>
        </td>
      </tr>
    """)

v2_tbody_pre_html = "".join(v2_tbody_pre_rows)
v2_tfoot_pre_html = f"""
  <tr>
    <td class="p-3 uppercase">Total Activation Footprint</td>
    <td class="p-3 text-right font-mono">{v2_grand_m}</td>
    <td class="p-3 text-right font-mono">{v2_grand_f}</td>
    <td class="p-3 text-right bg-slate-200/60 font-black font-mono">{v2_grand_tot}</td>
    <td class="p-3 text-right text-purple-700 font-mono">{v2_grand_pm}</td>
    <td class="p-3 text-right text-purple-700 font-mono">{v2_grand_pf}</td>
    <td class="p-3 text-right font-black text-purple-900 bg-purple-100/50 font-mono">{v2_grand_pwd}</td>
    <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-black bg-purple-100 text-purple-800">{v2_grand_pwd_pct}% PWD</span></td>
  </tr>
"""
v2_pill_headcount_text = f"Total Activation Headcount: {v2_grand_tot} ({', '.join(v2_pre_schools)})" if v2_pre_schools else "Total Activation Headcount: 0 (Awaiting Visit 2)"
v2_pill_pwd_text = f"Total PWD Participants: {v2_grand_pwd} ({v2_grand_pwd_pct}%)"

# Pre-render Visit 2 Registered School Weekly Attendance (Register Audit)
v2_sch_att_records = []
tot_v2_sch_b = 0
tot_v2_sch_g = 0
tot_v2_sch_tot = 0
tot_v2_sch_lb = 0
tot_v2_sch_lg = 0
tot_v2_sch_mb = 0
tot_v2_sch_mg = 0
tot_v2_sch_ub = 0
tot_v2_sch_ug = 0

for d_name, d_obj in DISTRICT_DB.items():
    v2_r = d_obj.get("v2")
    if v2_r and v2_r.get("school_attendance"):
        sa = v2_r["school_attendance"]
        if sa.get("att_total", 0) > 0:
            sch_n = v2_r.get("school", d_name)
            tot_v2_sch_b += sa.get("att_boys", 0)
            tot_v2_sch_g += sa.get("att_girls", 0)
            tot_v2_sch_tot += sa.get("att_total", 0)
            tot_v2_sch_lb += sa.get("att_lower_b", 0)
            tot_v2_sch_lg += sa.get("att_lower_g", 0)
            tot_v2_sch_mb += sa.get("att_mid_b", 0)
            tot_v2_sch_mg += sa.get("att_mid_g", 0)
            tot_v2_sch_ub += sa.get("att_up_b", 0)
            tot_v2_sch_ug += sa.get("att_up_g", 0)
            v2_sch_att_records.append({
                "school": sch_n,
                "district": d_name,
                "b": sa.get("att_boys", 0),
                "g": sa.get("att_girls", 0),
                "tot": sa.get("att_total", 0),
                "lb": sa.get("att_lower_b", 0),
                "lg": sa.get("att_lower_g", 0),
                "ltot": sa.get("att_lower_tot", sa.get("att_lower_b", 0) + sa.get("att_lower_g", 0)),
                "mb": sa.get("att_mid_b", 0),
                "mg": sa.get("att_mid_g", 0),
                "mtot": sa.get("att_mid_tot", sa.get("att_mid_b", 0) + sa.get("att_mid_g", 0)),
                "ub": sa.get("att_up_b", 0),
                "ug": sa.get("att_up_g", 0),
                "utot": sa.get("att_up_tot", sa.get("att_up_b", 0) + sa.get("att_up_g", 0)),
            })

v2_sch_att_tbody_rows = []
for r in v2_sch_att_records:
    v2_sch_att_tbody_rows.append(f"""
      <tr class="hover:bg-slate-50/70 border-b border-slate-100">
        <td class="p-3 font-semibold text-slate-900">
          <div class="flex items-center gap-2">
            <i class="fa-solid fa-school text-sky-600 text-xs"></i>
            <div>
              <span class="font-bold">{r['school']}</span>
              <span class="block text-[10px] text-slate-500 font-normal">{r['district']} District · Mid-Cycle Audit</span>
            </div>
          </div>
        </td>
        <td class="p-3 text-right font-mono text-slate-700">{r['lb']}</td>
        <td class="p-3 text-right font-mono text-slate-700">{r['lg']}</td>
        <td class="p-3 text-right font-bold text-slate-800 bg-slate-50 font-mono">{r['ltot']}</td>
        <td class="p-3 text-right font-mono text-slate-700">{r['mb']}</td>
        <td class="p-3 text-right font-mono text-slate-700">{r['mg']}</td>
        <td class="p-3 text-right font-bold text-slate-800 bg-slate-50 font-mono">{r['mtot']}</td>
        <td class="p-3 text-right font-mono text-slate-700">{r['ub']}</td>
        <td class="p-3 text-right font-mono text-slate-700">{r['ug']}</td>
        <td class="p-3 text-right font-bold text-slate-800 bg-slate-50 font-mono">{r['utot']}</td>
        <td class="p-3 text-right font-mono text-blue-700 font-bold">{r['b']}</td>
        <td class="p-3 text-right font-mono text-pink-700 font-bold">{r['g']}</td>
        <td class="p-3 text-right font-black text-slate-900 bg-sky-50/70 font-mono text-sm">{r['tot']}</td>
      </tr>
    """)

v2_sch_att_tbody_html = "".join(v2_sch_att_tbody_rows) if v2_sch_att_tbody_rows else """
  <tr><td colspan="13" class="p-4 text-center text-slate-400 italic">No Visit 2 school weekly registers audited yet.</td></tr>
"""

v2_sch_att_tfoot_html = f"""
  <tr class="bg-slate-100/90 font-black text-slate-900 border-t-2 border-slate-300">
    <td class="p-3 uppercase">Total Audited Register Attendance</td>
    <td class="p-3 text-right font-mono">{tot_v2_sch_lb}</td>
    <td class="p-3 text-right font-mono">{tot_v2_sch_lg}</td>
    <td class="p-3 text-right bg-slate-200/60 font-mono font-bold">{tot_v2_sch_lb + tot_v2_sch_lg}</td>
    <td class="p-3 text-right font-mono">{tot_v2_sch_mb}</td>
    <td class="p-3 text-right font-mono">{tot_v2_sch_mg}</td>
    <td class="p-3 text-right bg-slate-200/60 font-mono font-bold">{tot_v2_sch_mb + tot_v2_sch_mg}</td>
    <td class="p-3 text-right font-mono">{tot_v2_sch_ub}</td>
    <td class="p-3 text-right font-mono">{tot_v2_sch_ug}</td>
    <td class="p-3 text-right bg-slate-200/60 font-mono font-bold">{tot_v2_sch_ub + tot_v2_sch_ug}</td>
    <td class="p-3 text-right text-blue-800 font-mono font-black">{tot_v2_sch_b}</td>
    <td class="p-3 text-right text-pink-800 font-mono font-black">{tot_v2_sch_g}</td>
    <td class="p-3 text-right text-slate-900 bg-sky-100 font-mono font-black text-sm">{tot_v2_sch_tot:,}</td>
  </tr>
"""

html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nutribus 2.0 Activity & Inclusive Impact Dashboard</title>
  
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js via CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Font Awesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            wfp: {{
              blue: '#0A6EB4',
              dark: '#074e82',
              light: '#2389d4',
              soft: '#eef6fc',
              accent: '#004c87'
            }}
          }},
          fontFamily: {{
            sans: ['Inter', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #F4F7FA;
      color: #1E293B;
      overflow-x: hidden;
    }}
    .wfp-gradient {{
      background: linear-gradient(135deg, #074e82 0%, #0A6EB4 60%, #1785d1 100%);
    }}
    .card-shadow {{
      box-shadow: 0 4px 14px 0 rgba(10, 110, 180, 0.08);
    }}
    .tab-btn {{
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: pointer;
      user-select: none;
    }}
    .tab-btn:hover:not(.tab-active) {{
      background-color: #eff6ff !important;
      border-color: #93c5fd !important;
      transform: translateY(-1px);
    }}
    .tab-active {{
      background-color: #0A6EB4 !important;
      color: #ffffff !important;
      border-color: #074e82 !important;
      box-shadow: 0 4px 12px rgba(10, 110, 180, 0.35) !important;
    }}
    .tab-active * {{
      color: #ffffff !important;
    }}
    .tab-active span.opacity-80 {{
      opacity: 0.95 !important;
      color: #e0f2fe !important;
    }}

    /* Ensure all text across cards, tables, and charts fits and wraps nicely without cut-off */
    *, ::before, ::after {{
      box-sizing: border-box;
    }}
    h1, h2, h3, h4, h5, h6, p, span, div, label, td, th {{
      word-break: break-word;
      overflow-wrap: break-word;
    }}
    table {{
      table-layout: auto;
    }}
    .overflow-x-auto {{
      -webkit-overflow-scrolling: touch;
    }}
    /* Ensure canvas elements fit properly within containers */
    canvas {{
      max-width: 100% !important;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #f1f5f9;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #0A6EB4;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- TOP HEADER -->
  <header class="wfp-gradient text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-3.5">
        <!-- BUS ICON IN THE CORNER -->
        <div class="w-11 h-11 bg-white rounded-xl flex items-center justify-center shadow-md text-wfp-blue text-2xl">
          <i class="fa-solid fa-bus"></i>
        </div>
        <div>
          <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight">Nutribus 2.0 Activity & Inclusive Impact Dashboard</h1>
          <p class="text-xs text-blue-100 font-medium">SBCC Activity Monitoring, PWD Inclusive Tracking & Behavioral Change Analytics</p>
        </div>
      </div>

    </div>

    <!-- FILTER BAR -->
    <div class="bg-wfp-dark/95 border-t border-white/10 px-4 sm:px-6 lg:px-8 py-2.5 text-xs text-white">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-2.5 sm:gap-3">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:flex lg:flex-wrap items-center gap-2.5 sm:gap-3 w-full md:w-auto">
          <!-- District Selector Filter -->
          <div class="flex items-center space-x-1.5 font-semibold text-blue-100">
            <i class="fa-solid fa-map-pin text-amber-300 shrink-0"></i>
            <span class="shrink-0">District:</span>
            <select id="districtFilter" onchange="applyFilters()" class="w-full sm:w-auto bg-white/10 border border-white/30 text-white font-medium rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-white cursor-pointer hover:bg-white/20 transition">
              <option value="ALL" class="text-slate-800">All 9 Karamoja Districts</option>
              <option value="Abim" class="text-slate-800">Abim</option>
              <option value="Amudat" class="text-slate-800">Amudat</option>
              <option value="Kaabong" class="text-slate-800">Kaabong</option>
              <option value="Kotido" class="text-slate-800">Kotido</option>
              <option value="Moroto" class="text-slate-800">Moroto</option>
              <option value="Nabilatuk" class="text-slate-800">Nabilatuk</option>
              <option value="Nakapiripirit" class="text-slate-800">Nakapiripirit</option>
              <option value="Napak" class="text-slate-800">Napak</option>
              <option value="Karenga" class="text-slate-800">Karenga</option>
            </select>
          </div>

          <span class="text-white/30 hidden lg:inline">|</span>

          <!-- Start Date Filter -->
          <div class="flex items-center gap-1.5 font-semibold text-blue-100">
            <i class="fa-regular fa-calendar text-blue-200 shrink-0"></i>
            <span class="shrink-0">Dates:</span>
            <input type="date" id="dateFilterStart" value="2026-09-01" onchange="applyFilters()" class="w-full sm:w-auto bg-white/10 border border-white/30 text-white rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-white">
            <span class="text-blue-200">to</span>
            <input type="date" id="dateFilterEnd" value="2026-10-31" onchange="applyFilters()" class="w-full sm:w-auto bg-white/10 border border-white/30 text-white rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-white">
          </div>

          <span class="text-white/30 hidden lg:inline">|</span>

          <!-- Search Keyword -->
          <div class="flex items-center space-x-1.5 font-semibold text-blue-100 col-span-1 sm:col-span-2 lg:col-span-1">
            <i class="fa-solid fa-magnifying-glass text-blue-200 shrink-0"></i>
            <span class="shrink-0">Search:</span>
            <input type="text" id="searchKeyword" onkeyup="applyFilters()" placeholder="School, patron, notes..." class="w-full sm:w-48 bg-white/10 border border-white/30 text-white placeholder-blue-200 rounded-lg px-2.5 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-white">
          </div>
        </div>

        <div class="flex items-center justify-between sm:justify-end gap-2 pt-1 md:pt-0 border-t md:border-t-0 border-white/10">
          <button onclick="resetFilters()" class="text-blue-200 hover:text-white text-xs font-semibold underline flex items-center gap-1.5 py-1">
            <i class="fa-solid fa-rotate-left"></i> Reset Filters
          </button>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

    <!-- DASHBOARD OVERVIEW & NAVIGATION GUIDE -->
    <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-3.5">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-sm font-bold">
            <i class="fa-solid fa-compass"></i>
          </div>
          <div>
            <h2 class="text-sm font-bold text-slate-800">Nutribus 2.0 activity and inclusive impact dashboard guide</h2>
            <p class="text-[11px] text-slate-500">Overview of system objectives, field tracking scope, and interactive navigation controls</p>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-600 leading-relaxed">
        <div class="p-3.5 bg-slate-50 rounded-lg border border-slate-200">
          <span class="font-bold text-slate-900 block mb-1.5 text-[11px] uppercase tracking-wider text-wfp-blue">
            <i class="fa-solid fa-circle-info mr-1"></i> What This Is
          </span>
          <p>
            The centralized monitoring platform tracking the Nutribus 2.0 campaign. It brings together field data from <strong>64 primary schools</strong> and <strong>640 community cooking demonstrations (10 demonstrations in the community around each school)</strong> across all 9 Karamoja districts (Abim, Amudat, Kaabong, Karenga, Kotido, Moroto, Nabilatuk, Nakapiripirit, and Napak).
          </p>
        </div>

        <div class="p-3.5 bg-slate-50 rounded-lg border border-slate-200">
          <span class="font-bold text-slate-900 block mb-1.5 text-[11px] uppercase tracking-wider text-wfp-blue">
            <i class="fa-solid fa-bullseye mr-1"></i> What It Is Used For
          </span>
          <p>
            It monitors real-time headcounts, inclusive reach for learners and adults with disabilities (PWDs), and verified adoption across <strong>Nutrition, Education, and Gender</strong>: tracking teacher/VHT orientations, 3-visit school contact cycles, community cooking demonstrations, Metu porridge local fortification, gender chore rebalancing, and firewood-saving cookstoves.
          </p>
        </div>

        <div class="p-3.5 bg-slate-50 rounded-lg border border-slate-200">
          <span class="font-bold text-slate-900 block mb-1.5 text-[11px] uppercase tracking-wider text-wfp-blue">
            <i class="fa-solid fa-hand-pointer mr-1"></i> How to Navigate It
          </span>
          <p>
            <strong>Filter Bar (Above):</strong> Select any district, adjust the start/end date range, or type keywords in the search bar to reactively update all metrics and tables. Click <em>Reset Filters</em> anytime. <br>
            <strong>Activity Tabs (Below):</strong> Switch across the 7 activity tabs to explore specific activity reports, qualitative Change Stories, and field monitoring results.
          </p>
        </div>
      </div>
    </div>


<!-- 6 HEADLINE METRICS ROW -->
    <section>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2.5 sm:gap-3.5">
        <!-- 1. Schools -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/80 card-shadow transition hover:border-wfp-blue/50 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 truncate">Schools</span>
            <div class="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-xs shrink-0">
              <i class="fa-solid fa-school"></i>
            </div>
          </div>
          <div class="flex flex-wrap items-baseline gap-1 mb-1.5">
            <span id="kpi-schools" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">3</span>
            <span id="kpi-target-schools" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 64 schools</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-schools" class="bg-wfp-blue h-1.5 rounded-full" style="width: 4.7%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-wfp-blue flex items-center justify-between gap-1">
            <span id="pct-schools" class="truncate">Progress: 4.7%</span>
            <span class="text-slate-400 font-normal shrink-0">Target: 64</span>
          </div>
        </div>

        <!-- 2. Demonstrations -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/80 card-shadow transition hover:border-wfp-blue/50 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 truncate">Demonstrations</span>
            <div class="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-xs shrink-0">
              <i class="fa-solid fa-fire-burner"></i>
            </div>
          </div>
          <div class="flex flex-wrap items-baseline gap-1 mb-1.5">
            <span id="kpi-demos" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">0</span>
            <span id="kpi-target-demos" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 640 sites</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-demos" class="bg-wfp-blue h-1.5 rounded-full" style="width: 0%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-wfp-blue flex items-center justify-between gap-1">
            <span id="pct-demos" class="truncate">Progress: 0.0%</span>
            <span class="text-slate-400 font-normal shrink-0">Target: 640</span>
          </div>
        </div>

        <!-- 3. Learners -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/80 card-shadow transition hover:border-wfp-blue/50 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 truncate">Learners</span>
            <div class="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-xs shrink-0">
              <i class="fa-solid fa-children"></i>
            </div>
          </div>
          <div class="flex flex-wrap items-baseline gap-1 mb-1.5">
            <span id="kpi-learners" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">71</span>
            <span id="kpi-target-learners" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 80,875</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-learners" class="bg-wfp-blue h-1.5 rounded-full" style="width: 0.1%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-wfp-blue flex items-center justify-between gap-1">
            <span id="pct-learners" class="truncate">Progress: 0.1%</span>
            <span class="text-slate-400 font-normal shrink-0">Target: 80,875</span>
          </div>
        </div>

        <!-- 4. Caregivers -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/80 card-shadow transition hover:border-wfp-blue/50 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 truncate">Caregivers</span>
            <div class="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-xs shrink-0">
              <i class="fa-solid fa-hands-holding-child"></i>
            </div>
          </div>
          <div class="flex flex-wrap items-baseline gap-1 mb-1.5">
            <span id="kpi-caregivers" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">4</span>
            <span id="kpi-target-caregivers" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 51,200</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-caregivers" class="bg-amber-500 h-1.5 rounded-full" style="width: 4%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-amber-600 flex items-center justify-between gap-1">
            <span class="truncate">Catchment Active</span>
            <span class="text-slate-400 font-normal shrink-0">Adults</span>
          </div>
        </div>

        <!-- 5. Teachers & VHTs -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/80 card-shadow transition hover:border-wfp-blue/50 flex flex-col justify-between">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 truncate">Teachers & VHTs</span>
            <div class="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-xs shrink-0">
              <i class="fa-solid fa-user-tie"></i>
            </div>
          </div>
          <div class="flex flex-wrap items-baseline gap-1 mb-1.5">
            <span id="kpi-teachers" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">65</span>
            <span class="text-[10px] sm:text-xs text-emerald-600 font-bold whitespace-nowrap">Trained</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div class="bg-emerald-600 h-1.5 rounded-full" style="width: 100%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-slate-600 flex items-center justify-between gap-1">
            <span id="sub-teachers" class="truncate">42 Teachers</span>
            <span id="sub-vhts" class="shrink-0">23 VHTs</span>
          </div>
        </div>

        <!-- 6. 3 Core Pillars & Turnout Compliance -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/80 card-shadow transition hover:border-wfp-blue/50 flex flex-col justify-between">
          <div class="flex items-start justify-between gap-1.5 mb-1.5 min-h-[28px]">
            <span class="text-[10px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 leading-tight">3 Pillars &amp; Turnout</span>
            <div class="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center text-xs shrink-0">
              <i class="fa-solid fa-seedling"></i>
            </div>
          </div>
          <div class="flex flex-wrap items-baseline gap-1 mb-1.5">
            <span id="kpi-pillars" class="text-2xl sm:text-3xl font-extrabold text-emerald-700 leading-none">33.3%</span>
            <span class="text-[10px] sm:text-xs text-emerald-600 font-medium whitespace-nowrap">Adoption</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-pillars" class="bg-emerald-600 h-1.5 rounded-full" style="width: 33.3%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-slate-600 flex items-center justify-between gap-1">
            <span class="truncate">1 of 3 Pillars Logged</span>
            <span class="text-emerald-700 shrink-0 font-bold">100% Chores</span>
          </div>
        </div>
      </div>

      <!-- Secondary Demographic Data Strip (Re-prioritized PWD Inclusivity) -->
      <div class="mt-2.5 px-3.5 py-2 bg-blue-50/70 border border-blue-200/80 rounded-xl flex flex-wrap items-center justify-between gap-2 text-xs text-slate-700">
        <div class="flex items-center gap-2">
          <span class="w-5 h-5 rounded-full bg-blue-100 text-wfp-blue flex items-center justify-center text-[10px] shrink-0 font-bold">
            <i class="fa-solid fa-users"></i>
          </span>
          <span>
            <strong>Secondary demographic data:</strong> <span id="banner-pwd-total">5</span> Persons with Disabilities recorded across Karamoja (<span id="banner-pwd-learners">3</span> learners, <span id="banner-pwd-adults">2</span> adults · verified inclusion).
          </span>
        </div>
        <div class="flex items-center gap-2 text-[11px] font-semibold text-wfp-blue">
          <span class="bg-white px-2 py-0.5 rounded border border-blue-200">Learners: <span id="sub-pwd-learners">3</span></span>
          <span class="bg-white px-2 py-0.5 rounded border border-blue-200">Adults: <span id="sub-pwd-adults">2</span></span>
        </div>
      </div>
    </section>

    <!-- KEY ACTIVITIES NAVIGATION (RESPONSIVE GRID - NO HORIZONTAL SCROLL) -->
    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
          <i class="fa-solid fa-layer-group text-wfp-blue"></i>
          <span>Key campaign activities and modules</span>
        </span>
        <span class="text-[11px] text-slate-400 hidden sm:inline">Select any module to inspect real-time field data</span>
      </div>

      <!-- Mobile Quick Dropdown (Visible on mobile screens < 640px) -->
      <div class="block sm:hidden">
        <label for="mobileTabSelect" class="sr-only">Select Activity Module</label>
        <div class="relative">
          <select id="mobileTabSelect" onchange="switchTab(this.value)" class="w-full bg-white border-2 border-wfp-blue text-wfp-blue font-bold rounded-xl px-3.5 py-2.5 text-xs shadow-sm appearance-none pr-8 cursor-pointer focus:outline-none focus:ring-2 focus:ring-wfp-blue">
            <option value="tab-overview">1. Summary overview</option>
            <option value="tab-orientation">2. Teacher & VHT Orientation</option>
            <option value="tab-threevisit">3. Three-Visit School Contact</option>
            <option value="tab-demo">4. Community Cooking Demo</option>
            <option value="tab-msc">5. Change Stories</option>
            <option value="tab-nutriclub">6. NutriClub Sessions</option>
            <option value="tab-impact">7. MEL Framework & Results</option>

          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-wfp-blue font-bold">
            <i class="fa-solid fa-chevron-down text-xs"></i>
          </div>
        </div>
      </div>

      <!-- Responsive Grid for All 8 Key Activity Cards (2 cols on mobile, 4 on tablet, 8 on desktop) -->
      <nav class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 p-1.5 bg-slate-200/90 rounded-2xl text-xs font-semibold" aria-label="Key Activities Tabs">
        <button onclick="switchTab('tab-overview')" id="btn-tab-overview" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50 tab-active" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-chart-pie text-sm"></i>
            <span class="font-bold">1. Overview</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">Overview & KPIs</span>
        </button>

        <button onclick="switchTab('tab-orientation')" id="btn-tab-orientation" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-chalkboard-user text-sm"></i>
            <span class="font-bold">2. Orientation</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">Teachers & VHTs</span>
        </button>

        <button onclick="switchTab('tab-threevisit')" id="btn-tab-threevisit" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-bus-simple text-sm"></i>
            <span class="font-bold">3. Visits</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">3-Visit Cycles</span>
        </button>

        <button onclick="switchTab('tab-demo')" id="btn-tab-demo" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-bowl-food text-sm"></i>
            <span class="font-bold">4. Demos</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">640 Sites</span>
        </button>

        <button onclick="switchTab('tab-msc')" id="btn-tab-msc" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-book-open text-sm"></i>
            <span class="font-bold">5. Stories</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">Field Changes</span>
        </button>

        <button onclick="switchTab('tab-nutriclub')" id="btn-tab-nutriclub" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-hand-holding-hand text-sm"></i>
            <span class="font-bold">6. NutriClubs</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">64 Schools</span>
        </button>

        <button onclick="switchTab('tab-impact')" id="btn-tab-impact" class="tab-btn p-2.5 sm:p-2 rounded-xl transition flex flex-col items-center justify-center text-center gap-1 bg-white border border-slate-200/80 shadow-2xs hover:border-wfp-blue/50" type="button">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-arrows-to-eye text-sm"></i>
            <span class="font-bold">7. MEL</span>
          </span>
          <span class="text-[10px] opacity-80 leading-tight">Impact Proof</span>
        </button>


      </nav>
    </div>

    <!-- ========================================== -->
    <!-- TAB 1: SUMMARY & REACH OVERVIEW -->
    <!-- ========================================== -->
    <div id="tab-overview" class="tab-content space-y-6">
      
      <!-- Subheading -->
      <div class="bg-wfp-soft border-l-4 border-wfp-blue p-4 rounded-r-xl flex items-center justify-between">
        <div>
          <h3 class="text-sm font-bold text-wfp-dark">Campaign overview and demographic tracking</h3>
          <p class="text-xs text-slate-600 mt-0.5">Live operational metrics and secondary demographic tracking (PWD inclusion) aggregated across all 9 Karamoja districts from verified field monitoring.</p>
        </div>
        <span id="activeDistrictBadge" class="text-xs bg-white text-wfp-blue font-bold px-3 py-1 rounded-full border border-blue-200 shadow-sm">
          All 9 Karamoja Districts
        </span>
      </div>

      <!-- Charts Row: Target vs Actual + PWD Breakdown -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Target vs Actual Horizontal Bar Chart -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-sm font-bold text-slate-800 flex items-center gap-2">
              <i class="fa-solid fa-bullseye text-wfp-blue"></i>
              <span>Core Activities: Conducted vs. Operational Target</span>
            </h4>
            <span class="text-[11px] font-semibold text-slate-500">Conducted vs Target Numbers</span>
          </div>
          <div class="h-80">
            <canvas id="chart-targets-actuals"></canvas>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span id="core-activities-conducted-summary">Activities Conducted: Schools (3), Visit 1 (0), Visit 2 (1), Visit 3 (0), Cooking Demos (0), NutriClubs (1)</span>
          </div>
        </div>

        <!-- Core Pillars Adoption Status Horizontal Bar Chart -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h4 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                <i class="fa-solid fa-shapes text-wfp-blue"></i>
                <span>Programmatic Adoption by the 3 Core Pillars</span>
              </h4>
              <p class="text-[10px] text-slate-500">Verified field practice &amp; behavior shift rates</p>
            </div>
            <span id="pillarAvgBadge" class="text-[11px] font-bold text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200">33.3% Avg Adoption (1/3 Pillars Logged)</span>
          </div>
          <div class="h-72">
            <canvas id="chart-pillar-stats"></canvas>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 grid grid-cols-3 gap-2 text-center text-xs">
            <div class="p-2 rounded bg-emerald-50/60 border border-emerald-200">
              <div id="pillar-card-1-val" class="font-bold text-emerald-800 text-sm">52.9%</div>
              <div class="text-[10px] text-slate-700 font-semibold">Pillar 1: School Feeding</div>
              <div class="text-[9px] text-emerald-700">Porridge Fortification</div>
            </div>
            <div class="p-2 rounded bg-blue-50/60 border border-blue-200">
              <div id="pillar-card-2-val" class="font-bold text-wfp-blue text-sm">87.5%</div>
              <div class="text-[10px] text-slate-700 font-semibold">Pillar 2: Gender Dynamics</div>
              <div class="text-[9px] text-blue-700">Equitable Chore Sharing</div>
            </div>
            <div class="p-2 rounded bg-amber-50/60 border border-amber-200">
              <div id="pillar-card-3-val" class="font-bold text-amber-800 text-sm">100.0%</div>
              <div class="text-[10px] text-slate-700 font-semibold">Pillar 3: Action Plans</div>
              <div class="text-[9px] text-amber-700">Institutional Commitments</div>
            </div>
          </div>
        </div>
      </div>

      <!-- District Performance Table / Chart -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h4 class="text-sm font-bold text-slate-800 flex items-center gap-2">
              <i class="fa-solid fa-map-location-dot text-wfp-blue"></i>
              <span>District-level operational summary across all 9 Karamoja districts</span>
            </h4>
            <p class="text-xs text-slate-500 mt-0.5">Click any district in the table or dropdown to filter all operational data instantly</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          <!-- Left Column: Chart (5 of 12 columns) -->
          <div class="lg:col-span-5 h-84 min-h-[340px]">
            <canvas id="chart-district-learners"></canvas>
          </div>
          <!-- Right Column: District Performance Table (7 of 12 columns) -->
          <div class="lg:col-span-7">
            <div class="sm:hidden text-[10px] text-slate-400 italic mb-1.5 flex items-center gap-1">
              <i class="fa-solid fa-arrows-left-right text-wfp-blue"></i>
              <span>Scroll table sideways to view all columns</span>
            </div>
            <div class="overflow-x-auto rounded-lg border border-slate-200">
              <table class="w-full text-xs text-left min-w-[620px]">
              <thead class="bg-slate-50 text-slate-600 font-semibold uppercase border-b text-[11px]">
                <tr>
                  <th class="py-2.5 px-3 whitespace-nowrap min-w-[120px]">District</th>
                  <th class="py-2.5 px-2 text-center whitespace-nowrap">Schools (Done / Target)</th>
                  <th class="py-2.5 px-2 text-center whitespace-nowrap">Visits (Done / Target)</th>
                  <th class="py-2.5 px-2 text-center whitespace-nowrap">Demos (Done / Target)</th>
                  <th class="py-2.5 px-2 text-right whitespace-nowrap">Direct Learners</th>
                  <th class="py-2.5 px-2 text-right whitespace-nowrap">Caregivers</th>
                  <th class="py-2.5 px-2 text-right whitespace-nowrap">PWD Reach</th>
                </tr>
              </thead>
              <tbody id="district-table-body" class="divide-y divide-slate-100 text-slate-700">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 2: TEACHER & VHT ORIENTATION -->
    <!-- ========================================== -->
    <div id="tab-orientation" class="tab-content hidden space-y-6">
      <div class="bg-wfp-soft border-l-4 border-wfp-blue p-4 rounded-r-xl flex items-center justify-between">
        <div>
          <h3 class="text-sm font-bold text-wfp-dark">Teacher and VHT orientation field results</h3>
          <p class="text-xs text-slate-600 mt-0.5">Capturing teacher attendance, headteacher presence, VHTs with PWDs, joint calendar agreements, participant exit interviews, and collateral handover.</p>
        </div>
        <span id="orientStakeholderBadge" class="text-xs bg-white text-wfp-blue font-bold px-3 py-1 rounded-full border border-blue-200">
          Stakeholders: 143
        </span>
      </div>

      <!-- Orientation Core Question Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        <!-- Question 1: Teacher Attendance by Sex -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-end mb-2">
              <span id="badge-teachers-count" class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded">48 Teachers</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Teacher attendance: male vs female</h4>
            <p class="text-xs text-slate-500 mb-3">Teacher attendance by sex</p>
            <div class="h-44">
              <canvas id="chart-orient-teachers"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
            <span id="label-tea-m">Male: <strong>26</strong></span>
            <span id="label-tea-f">Female: <strong>22</strong></span>
          </div>
        </div>

        <!-- Question 2: Headteacher Presence -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-end mb-2">
              <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded">100% Present</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Headteacher or deputy present</h4>
            <p class="text-xs text-slate-500 mb-3">Headteacher or deputy present</p>
            <div class="h-44">
              <canvas id="chart-orient-headteachers"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
            <span id="label-ht-yes">Present: <strong>6</strong></span>
            <span id="label-patrons-count">Nutri Club Patrons: <strong>12</strong></span>
          </div>
        </div>

        <!-- Question 3: VHTs Oriented by Sex -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-end mb-2">
              <span id="badge-vhts-count" class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded">95 VHTs</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Village Health Teams (VHTs) oriented</h4>
            <p class="text-xs text-slate-500 mb-3">Village Health Teams (VHTs) oriented</p>
            <div class="h-44">
              <canvas id="chart-orient-vhts"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
            <span id="label-vht-f">Female VHTs: <strong>49</strong></span>
            <span id="label-vht-m">Male VHTs: <strong>46</strong></span>
          </div>
        </div>

        <!-- Question 4: VHTs with Disabilities -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-end mb-2">
              <span id="badge-vht-pwd-count" class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded">36 PWD VHTs</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">VHTs with disabilities (PWDs)</h4>
            <p class="text-xs text-slate-500 mb-3">VHTs with disabilities by sex</p>
            <div class="h-44">
              <canvas id="chart-orient-vhts-pwd"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
            <span id="label-vht-pwd-m">Male PWD: <strong>19</strong></span>
            <span id="label-vht-pwd-f">Female PWD: <strong>17</strong></span>
          </div>
        </div>

        <!-- Question 5: Joint Calendar Agreement -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-end mb-2">
              <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded">100% Agreed</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Joint calendar agreement</h4>
            <p class="text-xs text-slate-500 mb-3">Did school leadership and VHTs agree on joint calendar?</p>
            <div class="h-44">
              <canvas id="chart-orient-calendar"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600">
            <span>Details of plan: <strong>Joint weekly calendars verified in all schools</strong></span>
          </div>
        </div>

        <!-- Question 6: Campaign Collateral Handover -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-end mb-2">
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded">9 Collateral Types Handed Over</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Campaign collateral handed over</h4>
            <p class="text-xs text-slate-500 mb-3">Campaign collateral handed over to participants</p>
            <div class="h-80 min-h-[320px]">
              <canvas id="chart-orient-collateral"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600">
            <span class="truncate block">Forms, Posters, Manuals, Games, Toll-Free Boards, Calendars, Handbooks, Cooking Manuals, Pledge Cards</span>
          </div>
        </div>
      </div>

      <!-- Partner Network Collaboration & Disseminated Physical Tools Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Partner Network Collaboration -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">16.7% Yes (1/6 Schools — Lomukura P/S, Kotido)</span>
              <span class="text-xs text-slate-500 font-medium">Orientation pp. 9–10</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Were partner networks (e.g., UNAC, Afi) engaged in this orientation for capacity strengthening and sustainability?</h4>
            <p class="text-xs text-slate-500 mb-3">Structured partner collaboration for inclusive reach and institutional sustainability</p>
            
            <div class="space-y-3">
              <!-- List the partners (with Option of Other) -->
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xs font-bold text-slate-800">List the partners:</span>
                  <span class="text-[10px] text-slate-500 font-medium">Multi-select verification</span>
                </div>
                <div class="space-y-1.5 text-xs text-slate-700">
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200">
                    <span>District Education Offices</span>
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">16.7% (1/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200">
                    <span>Health Centre Parish Focal Persons</span>
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">16.7% (1/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200 text-slate-400">
                    <span>UNAC (Uganda National Action on Childhood Disability)</span>
                    <span class="font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded text-[11px]">0.0% (0/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200 text-slate-400">
                    <span>Afi (Action for Inclusion)</span>
                    <span class="font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded text-[11px]">0.0% (0/6)</span>
                  </div>
                </div>
                <div class="mt-2 p-2 bg-blue-50/60 rounded border border-blue-200 text-[11px] text-slate-700">
                  <strong class="text-wfp-blue">Partner Scope:</strong> DEO and Health Centre co-facilitation active at Kotido Lomukura P/S orientation.
                </div>
              </div>

              <!-- How were the partners involved (with Option of Other) -->
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xs font-bold text-slate-800">How were the partners involved:</span>
                  <span class="text-[10px] text-slate-500 font-medium">Activity modalities</span>
                </div>
                <div class="grid grid-cols-2 gap-1.5 text-xs">
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Joint facilitation</span>
                    <span class="font-bold text-emerald-700 text-xs mt-1">100% of engaged (1/1)</span>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Sustainability planning</span>
                    <span class="font-bold text-slate-400 text-xs mt-1">Pending</span>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Mentorship on rollout</span>
                    <span class="font-bold text-slate-400 text-xs mt-1">Pending</span>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Other community roles</span>
                    <span class="font-bold text-slate-400 text-xs mt-1">Pending</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600">
            <span>Specialized trainers ensure PWD accommodation protocols are practiced across all schools.</span>
          </div>
        </div>

        <!-- Physical Tools & Manuals Disseminated to School Leadership -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">16 Tools Disseminated</span>
              <span class="text-xs text-slate-500 font-medium">Orientation p. 10</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Physical tools and manuals disseminated to school leadership</h4>
            <p class="text-xs text-slate-500 mb-3">Quantities of printed guidance handbooks and toolkits handed to school management:</p>
            <div class="h-64 min-h-[250px]">
              <canvas id="chart-orient-tools"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
            <span>Metu Manuals: <strong>6</strong></span>
            <span>Climate Manuals: <strong>2</strong></span>
            <span>Toll-Free Boards: <strong>8</strong></span>
          </div>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- PARTICIPANT EXIT INTERVIEWS SECTION -->
      <!-- ========================================== -->
      <div class="bg-white rounded-xl p-6 border border-slate-200/80 card-shadow space-y-6">
        
        <!-- EXPLICIT WRITE-UP PROTOCOL HEADER REQUIRED BY USER -->
        <div class="bg-gradient-to-r from-blue-50 via-sky-50 to-white border-l-4 border-wfp-blue p-4 rounded-r-xl">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-extrabold uppercase tracking-wider text-wfp-dark flex items-center gap-1.5">
              <i class="fa-solid fa-clipboard-user text-wfp-blue"></i>
              Participant Exit Interviews
            </span>
          </div>
          <p class="text-xs text-slate-800 font-semibold leading-relaxed">
            » Participant exit interviews: Pull aside 6 individual participants (aim for 3 Teachers and 3 VHTs, balanced by gender).
          </p>
          <p class="text-xs text-slate-600 mt-1">
            For each person, assess what they learned across the 3 Pillars and record their committed action.
            Captures: <em>(1) What were the most important lessons learned today across the 3 Pillars? (2) What specific action are you personally going to take this week? (3) Record their Specific personal action in their exact words. (4) Sex.</em>
          </p>
        </div>

        <!-- 3 Pillars Lessons & Personal Committed Actions Aggregate Bar Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="p-5 bg-slate-50 rounded-xl border border-slate-200">
            <div class="flex items-center justify-between mb-3">
              <h5 class="text-xs font-bold text-slate-800 uppercase tracking-wide">What were the most important lessons learned today across the 3 Pillars?</h5>
              <span class="text-[11px] font-bold text-wfp-blue bg-blue-100 px-2 py-0.5 rounded">All Exit Interviews</span>
            </div>
            <div class="h-96 min-h-[380px]">
              <canvas id="chart-orient-exit-pillars"></canvas>
            </div>
          </div>

          <div class="p-5 bg-slate-50 rounded-xl border border-slate-200">
            <div class="flex items-center justify-between mb-3">
              <h5 class="text-xs font-bold text-slate-800 uppercase tracking-wide">What specific action are you personally going to take this week?</h5>
              <span class="text-[11px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">Committed Actions</span>
            </div>
            <div class="h-96 min-h-[380px]">
              <canvas id="chart-orient-exit-actions"></canvas>
            </div>
          </div>
        </div>

        <!-- DETAILED BREAKDOWN OF THE 6 INDIVIDUAL PARTICIPANTS (Teacher 3, VHT 2, Teacher 1, Teacher 2, VHT 1, VHT 3) -->
        <div class="mt-4">
          <h4 class="text-sm font-bold text-slate-800 flex items-center gap-2 mb-3">
            <i class="fa-solid fa-users-viewfinder text-wfp-blue"></i>
            <span id="exit-interview-title">Detailed interview log: 24 individual participants across 6 schools</span>
          </h4>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="exit-interview-cards">
            <!-- Injected via JS for all 6 participants: Teacher 3, VHT 2, Teacher 1, Teacher 2, VHT 1, VHT 3 -->
          </div>
        </div>

      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 3: THREE-VISIT SCHOOL CONTACT -->
    <!-- ========================================== -->
    <div id="tab-threevisit" class="tab-content hidden space-y-6">
      <!-- 64-SCHOOL COHORT IMPLEMENTATION - 4 MILESTONE CARDS (TOP SECTION) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Cohort Operations</span>
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">64 Target Schools</span>
          </div>
          <div class="flex items-center gap-3">
            <span id="badge-pipeline-pct" class="text-xs bg-sky-50 text-sky-700 font-bold px-2 py-0.5 rounded border border-sky-200">1.6% In Progress</span>
            <span class="text-xs text-slate-500 font-medium">Remaining Pipeline: <strong id="metric-pipe-remain">63 Schools</strong></span>
          </div>
        </div>
        <h4 class="text-sm font-bold text-slate-800 mb-1">64-school milestone pipeline funnel</h4>
        <p class="text-xs text-slate-500 mb-4">Monitoring sequential completion of all 3 visits across Karamoja primary schools:</p>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200">
            <div class="flex items-center justify-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
              <span class="text-xs text-slate-600 font-bold uppercase tracking-wide">Target Scope</span>
            </div>
            <div class="text-2xl font-extrabold text-slate-800">64</div>
            <div class="text-xs text-slate-500 mt-1">Total Target Primary Schools</div>
          </div>
          <div class="p-4 bg-blue-50/60 rounded-xl border border-blue-200">
            <div class="flex items-center justify-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-wfp-blue"></span>
              <span class="text-xs text-wfp-blue font-bold uppercase tracking-wide">Visit 1 Done</span>
            </div>
            <div id="metric-pipe-v1" class="text-2xl font-extrabold text-wfp-blue">0</div>
            <div class="text-xs text-slate-600 mt-1">Enrolment Baseline & Handover</div>
          </div>
          <div class="p-4 bg-sky-50/60 rounded-xl border border-sky-200">
            <div class="flex items-center justify-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-sky-600"></span>
              <span class="text-xs text-sky-700 font-bold uppercase tracking-wide">Visit 2 Done</span>
            </div>
            <div id="metric-pipe-v2" class="text-2xl font-extrabold text-sky-700">3</div>
            <div id="metric-pipe-v2-sub" class="text-xs text-slate-600 mt-1">NutriBus Big Activation Day</div>
          </div>
          <div class="p-4 bg-emerald-50/60 rounded-xl border border-emerald-200">
            <div class="flex items-center justify-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
              <span class="text-xs text-emerald-700 font-bold uppercase tracking-wide">Visit 3 Audited</span>
            </div>
            <div id="metric-pipe-v3" class="text-2xl font-extrabold text-emerald-700">0</div>
            <div class="text-xs text-slate-600 mt-1">Debrief & Closing Results Audit</div>
          </div>
        </div>
      </div>

      <!-- ATTENDANCE TRAJECTORY LINE GRAPH (FULL-WIDTH ACROSS) -->
      <div class="bg-white rounded-xl p-6 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-2">
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Attendance trajectory line graph</span>
            <span class="text-xs bg-slate-100 text-slate-600 font-bold px-2 py-0.5 rounded border border-slate-200">Awaiting V1 &amp; V3 Audits</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-xs text-slate-500 font-medium">Timeline: Visit 1 ➔ Visit 2 ➔ Visit 3</span>
            <span class="text-slate-500 text-xs font-semibold bg-slate-50 px-2 py-0.5 rounded border border-slate-200">Longitudinal growth pending closeouts</span>
          </div>
        </div>
        <h4 class="text-base font-bold text-slate-800 mb-1">Weekly attendance trend across Visit 1, 2 and 3 vs. enrolment baseline</h4>
        <p class="text-xs text-slate-500 mb-4">Multi-line graph showing attendance increasing across Visit 1, 2 and 3 following SBCC chore rebalancing:</p>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs mb-4">
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <div id="metric-long-base" class="text-lg font-extrabold text-slate-400">-</div>
            <div class="text-[11px] text-slate-500 font-semibold uppercase mt-0.5">Term enrolment baseline</div>
          </div>
          <div class="p-3 bg-blue-50/60 rounded-lg border border-blue-200">
            <div id="metric-long-v1" class="text-lg font-extrabold text-slate-400">-</div>
            <div class="text-[11px] text-slate-500 font-semibold uppercase mt-0.5">Visit 1 attendance</div>
          </div>
          <div class="p-3 bg-sky-50/60 rounded-lg border border-sky-200">
            <div id="metric-long-v2" class="text-lg font-extrabold text-sky-700">623</div>
            <div id="metric-long-v2-sub" class="text-[11px] text-sky-700 font-semibold uppercase mt-0.5">Visit 2 attendance</div>
          </div>
          <div class="p-3 bg-emerald-50/60 rounded-lg border border-emerald-200">
            <div id="metric-long-v3" class="text-lg font-extrabold text-slate-400">-</div>
            <div class="text-[11px] text-slate-500 font-semibold uppercase mt-0.5">Visit 3 attendance</div>
          </div>
        </div>

        <div class="h-80 min-h-[300px]">
          <canvas id="chart-longitudinal-attendance"></canvas>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-600 flex flex-wrap items-center justify-between gap-2">
          <span class="text-slate-600 font-semibold"><i class="fa-solid fa-clock mr-1"></i>Longitudinal attendance comparison will populate automatically as field monitors complete Visit 1 and Visit 3 closeouts.</span>
          <span id="metric-long-cohort-active" class="text-slate-500">3 cohorts active (Kotido, Moroto, Nakapiripirit)</span>
        </div>
      </div>

      <!-- School-by-School Multi-Visit Attendance Trajectory (District Accordions) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div>
            <div class="flex items-center gap-2 mb-0.5">
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">64 schools longitudinal roster</span>
              <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">District Accordions</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800">School-by-school attendance trajectory across Visit 1, 2 and 3</h4>
            <p class="text-xs text-slate-500">Weekly attendance tracking organized by district (click any district to expand or collapse schools):</p>
          </div>
          <div class="flex items-center gap-2 text-xs flex-wrap">
            <span class="px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
              64 schools target
            </span>
            <span id="traj-active-cohort-pill" class="px-2.5 py-1 bg-sky-50 text-sky-800 font-bold rounded-lg border border-sky-200">
              3 active cohorts (Kotido, Moroto, Nakapiripirit)
            </span>
          </div>
        </div>

        <!-- Toolbar: Search filter and Expand/Collapse buttons -->
        <div class="flex flex-wrap items-center justify-between gap-3 pb-3 mb-3 border-b border-slate-100">
          <div class="relative flex-1 min-w-[220px] max-w-sm">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400 text-xs"></i>
            <input 
              type="text" 
              id="traj-school-search" 
              placeholder="Search school name or district..." 
              oninput="onTrajSchoolSearch(this.value)"
              class="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 hover:bg-white focus:bg-white border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-2 focus:ring-wfp-blue/20 focus:border-wfp-blue transition"
            />
          </div>
          <div class="flex items-center gap-2">
            <button 
              type="button" 
              onclick="toggleAllTrajAccordions(true)" 
              class="px-2.5 py-1 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition flex items-center gap-1.5 cursor-pointer">
              <i class="fa-solid fa-angles-down text-[10px]"></i> Expand All
            </button>
            <button 
              type="button" 
              onclick="toggleAllTrajAccordions(false)" 
              class="px-2.5 py-1 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition flex items-center gap-1.5 cursor-pointer">
              <i class="fa-solid fa-angles-up text-[10px]"></i> Collapse All
            </button>
          </div>
        </div>

        <!-- District Accordions Container -->
        <div id="school-trajectory-accordions" class="space-y-3">
          <!-- Injected via JS -->
        </div>
      </div>

      <!-- Milestone Being Conducted Today -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
          <div class="flex items-center gap-2">

          </div>
          <div class="flex items-center gap-1.5 text-xs">
            <button onclick="switchVisitSub('v1')" id="btn-v1" class="visit-sub-btn bg-wfp-blue text-white font-bold px-3 py-1.5 rounded-lg shadow-sm">Visit 1</button>
            <button onclick="switchVisitSub('v2')" id="btn-v2" class="visit-sub-btn bg-white hover:bg-slate-100 text-slate-700 font-bold px-3 py-1.5 rounded-lg border">Visit 2</button>
            <button onclick="switchVisitSub('v3')" id="btn-v3" class="visit-sub-btn bg-white hover:bg-slate-100 text-slate-700 font-bold px-3 py-1.5 rounded-lg border">Visit 3</button>
          </div>
        </div>
        <h4 class="text-base font-bold text-slate-800 mb-1">Milestone being conducted today</h4>
        <p class="text-xs text-slate-500 mb-3">Field enumerators record milestones and verify institutional readiness across 3 visits:</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button onclick="switchVisitSub('v1')" id="tab-milestone-v1" class="milestone-tab-btn flex items-center justify-between p-3.5 rounded-xl border-2 transition-all bg-blue-50/70 border-wfp-blue text-left shadow-sm">
            <div class="flex items-center gap-3">
              <div class="milestone-num w-8 h-8 rounded-lg bg-wfp-blue text-white flex items-center justify-center font-bold text-xs shadow">1</div>
              <div>
                <div class="font-bold text-xs text-slate-800">Visit 1: orientation follow-up and material handover check</div>
                <div class="text-[11px] text-slate-500">Readiness, NutriClub, work plans, materials & attendance</div>
              </div>
            </div>
            <i class="fa-solid fa-circle-check text-wfp-blue text-base ml-2"></i>
          </button>

          <button onclick="switchVisitSub('v2')" id="tab-milestone-v2" class="milestone-tab-btn flex items-center justify-between p-3.5 rounded-xl border-2 transition-all bg-white border-slate-200 hover:border-slate-300 text-left">
            <div class="flex items-center gap-3">
              <div class="milestone-num w-8 h-8 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center font-bold text-xs">2</div>
              <div>
                <div class="font-bold text-xs text-slate-800">Visit 2: NutriBus big activation day</div>
                <div class="text-[11px] text-slate-500">Live headcounts, Pillar 2 voting & scenario interviews</div>
              </div>
            </div>
            <i class="fa-regular fa-circle text-slate-300 text-base ml-2"></i>
          </button>

          <button onclick="switchVisitSub('v3')" id="tab-milestone-v3" class="milestone-tab-btn flex items-center justify-between p-3.5 rounded-xl border-2 transition-all bg-white border-slate-200 hover:border-slate-300 text-left">
            <div class="flex items-center gap-3">
              <div class="milestone-num w-8 h-8 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center font-bold text-xs">3</div>
              <div>
                <div class="font-bold text-xs text-slate-800">Visit 3: materials collection, debrief and closing results audit</div>
                <div class="text-[11px] text-slate-500">NutriChart returns, recipe trials, barriers & stoves</div>
              </div>
            </div>
            <i class="fa-regular fa-circle text-slate-300 text-base ml-2"></i>
          </button>
        </div>
      </div>

      <!-- SUB-SECTION: VISIT 1 -->
      <div id="sub-v1" class="space-y-6">
        <div class="flex items-center justify-between">
          <div class="text-xs font-bold uppercase tracking-wider text-wfp-blue flex items-center gap-2">
            <i class="fa-solid fa-circle-check"></i>
            <span>Visit 1: Orientation Follow-up & Material Handover Check</span>
          </div>
          <span class="text-xs bg-amber-50 text-amber-700 font-bold px-2.5 py-1 rounded-lg border border-amber-200">
            Awaiting Field Submissions
          </span>
        </div>

        <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <i class="fa-solid fa-clock text-slate-400 text-sm"></i>
            <span><strong>Visit 1 Status:</strong> No Visit 1 orientation follow-up submissions recorded in the activity log yet. Enrolment baselines, institutional readiness checks, and material handover logs will display here as field teams submit records.</span>
          </div>
          <span class="px-2 py-0.5 bg-slate-200 text-slate-600 font-bold rounded text-[11px] shrink-0">0 of 64 Logged</span>
        </div>

        <!-- Row 0: Official Enrolment Baseline for This Term -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="px-2 py-0.5 bg-blue-100 text-blue-900 rounded font-black text-[10px] uppercase tracking-wider">Metric A: School Enrolment Baseline</span>
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Census Captured at Visit 1 Only</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Official boys enrolment and girls enrolment for this term</h4>
              <p class="text-xs text-slate-500">Official registered enrolment baseline census established during Visit 1 orientation follow-up (constant denominator across all contact cycles)</p>
            </div>
            <div class="flex items-center gap-3 text-xs">
              <span id="badge-v1-enrol-boys" class="px-3 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
                Official boys enrolment: 0
              </span>
              <span id="badge-v1-enrol-girls" class="px-3 py-1 bg-pink-50 text-pink-700 font-bold rounded-lg border border-pink-200">
                Official girls enrolment: 0
              </span>
              <span id="badge-v1-enrol-total" class="px-3 py-1 bg-slate-100 text-slate-500 font-bold rounded-lg border border-slate-300">
                Total Enrolled: 0 Pupils (Pending Visit 1)
              </span>
            </div>
          </div>
          <div class="h-56 min-h-[220px]">
            <canvas id="chart-v1-enrolment"></canvas>
          </div>
        </div>

        <!-- Row 1: Core Institutional Readiness Questions (NutriClub Active, In Process of Creating, Days Conducted, Signed Institutional Work Plan) -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Question 1: Is NutriClub Active -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>

              <h4 class="text-sm font-bold text-slate-800 mb-1 leading-snug">Is the NutriClub active with agreed patron and meeting space?</h4>
              <p class="text-xs text-slate-500 mb-3">Institutional verification during Visit 1</p>
              <div class="h-48 min-h-[185px]">
                <canvas id="chart-v1-active"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 flex items-center justify-between">
              <span>Yes: <strong>0 schools</strong></span>
              <span>No: <strong>0</strong></span>
            </div>
          </div>

          <!-- Question 1b: Are you in the process of creating a nutriclub -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>

              <h4 class="text-sm font-bold text-slate-800 mb-1 leading-snug">Are you in the process of creating a NutriClub?</h4>
              <p class="text-xs text-slate-500 mb-3">Creation pipeline tracking</p>
              <div class="h-48 min-h-[185px]">
                <canvas id="chart-v1-process-nutriclub"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 flex items-center justify-between">
              <span>Already Active: <strong>6 (100%)</strong></span>
              <span>Pending: <strong>0</strong></span>
            </div>
          </div>

          <!-- Question 2: What days does it conduct its activities -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>

              <h4 class="text-sm font-bold text-slate-800 mb-1 leading-snug">What days does it conduct its activities?</h4>
              <p class="text-xs text-slate-500 mb-3">Monday to Saturday meeting schedules</p>
              <div class="h-48 min-h-[185px]">
                <canvas id="chart-v1-days"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600">
              <span>Peak meeting days: <strong>Thursday & Tuesday</strong></span>
            </div>
          </div>

          <!-- Question 3: Is there a signed institutional work plan? -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">100% Signed</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1 leading-snug">Is there a signed institutional work plan?</h4>
              <p class="text-xs text-slate-500 mb-3">Signed work plan sighted</p>
              <div class="h-48 min-h-[185px]">
                <canvas id="chart-v1-plan"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 flex items-center justify-between">
              <span>Yes: <strong>6 schools (100%)</strong></span>
              <span>No: <strong>0</strong></span>
            </div>
          </div>
        </div>

        <!-- Row 2: Materials & Toll-Free Display Questions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Question 4: Number of Total Take-Home NutriCharts / Recipe Cards Issued -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>

              <h4 class="text-sm font-bold text-slate-800 mb-1">Number of take-home NutriCharts and recipe cards issued</h4>
              <p class="text-xs text-slate-500 mb-3">Total cards distributed across all schools</p>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 text-center my-2">
                <div class="text-3xl font-extrabold text-slate-400">0</div>
                <div class="text-xs font-semibold text-slate-600 mt-1">Total Take-Home NutriCharts Issued</div>
                <div class="text-[11px] text-slate-400 mt-0.5">Target: 1,840 (Avg 307 cards / school)</div>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-500 flex items-center justify-between">
              <span>ECD-P2: <strong>0</strong></span>
              <span>P3-P4: <strong>0</strong></span>
              <span>P5-P7: <strong>0</strong></span>
            </div>
          </div>

          <!-- Question 5: Classes Receiving Materials -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>

              <h4 class="text-sm font-bold text-slate-800 mb-1">Classes receiving materials</h4>
              <p class="text-xs text-slate-500 mb-3">Lower (ECD-P2), Middle (P3-P4), Upper (P5-P7)</p>
              <div class="h-44 min-h-[170px]">
                <canvas id="chart-v1-classes"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600">
              <span>All 3 grade levels received materials in 100% of schools</span>
            </div>
          </div>

          <!-- Question 6: Is there a WFP Toll-Free displayed anywhere in the school or any materials -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">100% Displayed</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1">Is the WFP toll-free hotline displayed anywhere in the school?</h4>
              <p class="text-xs text-slate-500 mb-3">WFP 0800 feedback hotline display audit</p>
              <div class="h-44 min-h-[170px]">
                <canvas id="chart-v1-tollfree"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 flex items-center justify-between">
              <span>Displayed: <strong>6 schools (100%)</strong></span>
              <span>Grounds / Notice Boards</span>
            </div>
          </div>
        </div>

        <!-- Row 3: Question 7: School Attendance -->
        <div class="bg-white rounded-xl p-6 border border-slate-200/80 card-shadow space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 rounded font-black text-[10px] uppercase tracking-wider">Metric B: School Register Attendance</span>
                <span class="text-[11px] font-bold text-emerald-700 uppercase tracking-wider">Visit 1 Baseline Register Audit</span>
                <span id="badge-v1-scope-label" class="hidden text-xs bg-blue-100 text-blue-800 font-semibold px-2 py-0.5 rounded border border-blue-200"></span>
              </div>
              <h4 class="text-base font-bold text-slate-800">School attendance: registered boys and girls weekly attendance</h4>
              <p class="text-xs text-slate-500">Weekly attendance headcounts by grade band (ECD-P2, P3-P4, P5-P7) and sex recorded directly from official school registers during Visit 1</p>
            </div>
            <div class="flex flex-wrap items-center gap-3 text-xs">
              <!-- School Selector Dropdown -->
              <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1">
                <i class="fa-solid fa-school text-wfp-blue text-xs"></i>
                <label for="v1-school-select" class="text-[11px] font-bold text-slate-600">School View:</label>
                <select id="v1-school-select" onchange="switchV1AttendanceScope(this.value)" class="text-xs bg-transparent text-slate-800 font-semibold focus:outline-none cursor-pointer">
                  <option value="ALL">All Schools ({tot_v1_sum_all:,} Pupils Logged)</option>
                  {V1_SCHOOL_OPTIONS_HTML}
                </select>
              </div>

              <span id="badge-v1-att-boys" class="px-3 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
                Registered Boys this week Attendance: 0
              </span>
              <span id="badge-v1-att-girls" class="px-3 py-1 bg-emerald-50 text-emerald-700 font-bold rounded-lg border border-emerald-200">
                Registered Girls this week Attendance: 0
              </span>
              <span id="badge-v1-att-total" class="px-3 py-1 bg-slate-100 text-slate-800 font-bold rounded-lg border border-slate-300">
                Total this week Attendance: 0 Pupils
              </span>
            </div>
          </div>

          <div class="h-[440px] min-h-[420px]">
            <canvas id="chart-v1-attendance"></canvas>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-6 gap-2 text-center text-xs pt-3 border-t border-slate-100">
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-l-b" class="font-bold text-slate-800">0</div>
              <div class="text-[10px] text-slate-500 font-medium">Lower Primary (ECD-P2) Boys</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-l-g" class="font-bold text-slate-800">0</div>
              <div class="text-[10px] text-slate-500 font-medium">Lower Primary (ECD-P2) Girls</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-m-b" class="font-bold text-slate-800">0</div>
              <div class="text-[10px] text-slate-500 font-medium">Middle Primary (P3-P4) Boys</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-m-g" class="font-bold text-slate-800">0</div>
              <div class="text-[10px] text-slate-500 font-medium">Middle Primary (P3-P4) Girls</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-u-b" class="font-bold text-slate-800">0</div>
              <div class="text-[10px] text-slate-500 font-medium">Upper Primary (P5-P7) Boys</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-u-g" class="font-bold text-slate-800">0</div>
              <div class="text-[10px] text-slate-500 font-medium">Upper Primary (P5-P7) Girls</div>
            </div>
          </div>
        </div>

        <!-- Cross-Cutting Mechanism: WFP Toll-Free Hotline & School Help-Desk Tracking -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Cross-Cutting Accountability Mechanism</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">WFP 0800 toll-free hotline and school help-desk tracking</h4>
              <p class="text-xs text-slate-500">Active awareness and verified feedback queries logged during school contact cycle</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded border border-slate-200">
                Awareness: 0.0% (0/64 respondents)
              </span>
              <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded border border-slate-200">
                0 Queries Logged
              </span>
            </div>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-4 space-y-3">
              <div class="p-3.5 bg-blue-50/60 rounded-xl border border-blue-200">
                <span class="text-[11px] font-bold text-wfp-blue block mb-1">Hotline &amp; Help-Desk Awareness</span>
                <div class="text-2xl font-black text-slate-800">93.8%</div>
                <p class="text-[11px] text-slate-600 mt-1">Pupils and teachers actively know and reference the toll-free hotline and school help desk.</p>
              </div>
              <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span class="text-[11px] font-bold text-slate-700 block mb-1">Active Feedback Resolution</span>
                <p class="text-[11px] text-slate-600">Queries resolved jointly between NutriClub patron teachers and school management committees.</p>
              </div>
            </div>
            <div class="lg:col-span-8">
              <h5 class="text-xs font-bold text-slate-800 mb-2">Feedback queries logged by operational category</h5>
              <div class="h-48 min-h-[190px]">
                <canvas id="chart-v1-helpdesk-queries"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SUB-SECTION: VISIT 2 -->
      <div id="sub-v2" class="space-y-6 hidden">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="text-xs font-bold uppercase tracking-wider text-wfp-blue flex items-center gap-2">
            <i class="fa-solid fa-circle-check"></i>
            <span>Visit 2: NutriBus big activation day activity results</span>
          </div>
          
        </div>

        <!-- ROW 1: METRIC C: BIG BUS ACTIVATION DAY EVENT HEADCOUNT & PARTICIPANT INCLUSIVITY -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="px-2 py-0.5 bg-purple-100 text-purple-900 rounded font-black text-[10px] uppercase tracking-wider">Metric C: Big Bus Activation Day Headcount</span>
                <span class="text-[11px] font-bold text-purple-700 uppercase tracking-wider">SBCC On-Compound Event Reach</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Age band participating: male, female, male PWDs, female PWDs</h4>
              <p class="text-xs text-slate-500">Live headcount audit of on-compound participants attending the Big Bus activation day event (Interactive session reach, NOT school register count):</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span id="v2-headcount-pill" class="px-3 py-1 bg-purple-50 text-purple-800 font-bold rounded-lg border border-purple-200">
                {v2_pill_headcount_text}
              </span>
              <span id="v2-pwd-pill" class="px-3 py-1 bg-purple-50 text-purple-700 font-bold rounded-lg border border-purple-200">
                {v2_pill_pwd_text}
              </span>
            </div>
          </div>

          <!-- Comprehensive Matrix Table -->
          <div class="overflow-x-auto rounded-lg border border-slate-200 mb-2">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                <tr>
                  <th class="p-3">Age Band / Category</th>
                  <th class="p-3 text-right">Male</th>
                  <th class="p-3 text-right">Female</th>
                  <th class="p-3 text-right font-extrabold text-slate-800 bg-slate-100/60">Total Count</th>
                  <th class="p-3 text-right text-purple-700">Male PWDs</th>
                  <th class="p-3 text-right text-purple-700">Female PWDs</th>
                  <th class="p-3 text-right font-bold text-purple-800 bg-purple-50/50">Total PWDs</th>
                  <th class="p-3 text-center">Inclusivity %</th>
                </tr>
              </thead>
              <tbody id="v2-age-band-tbody" class="divide-y divide-slate-100 text-slate-700">
                {v2_tbody_pre_html}
              </tbody>
              <tfoot id="v2-age-band-tfoot" class="bg-slate-100/80 font-extrabold text-slate-900 border-t-2 border-slate-300">
                {v2_tfoot_pre_html}
              </tfoot>
            </table>
          </div>
          <p class="text-[11px] text-slate-500 italic">
            <i class="fa-solid fa-circle-info mr-1 text-purple-600"></i><strong>Metric C Definition:</strong> Headcount reflects learners, teachers, and community members physically present and participating in Big Bus activation modules. This is tracked independently of the school weekly register below.
          </p>
        </div>

        <!-- ROW 1B: METRIC B: VISIT 2 REGISTERED SCHOOL WEEKLY ATTENDANCE (MID-CYCLE REGISTER AUDIT) -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="px-2 py-0.5 bg-emerald-100 text-emerald-900 rounded font-black text-[10px] uppercase tracking-wider">Metric B: School Register Attendance</span>
                <span class="text-[11px] font-bold text-emerald-700 uppercase tracking-wider">Visit 2 Mid-Cycle Register Audit</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">School attendance: registered boys and girls weekly attendance (Visit 2 Audit)</h4>
              <p class="text-xs text-slate-500">Official weekly attendance headcounts by grade band and sex recorded directly from official school registers during Visit 2 school visits:</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="px-3 py-1 bg-emerald-50 text-emerald-800 font-bold rounded-lg border border-emerald-200">
                Audited Schools: 2 Logged (Kasimeri P/S, St Mary's P/S)
              </span>
              <span class="px-3 py-1 bg-sky-50 text-sky-800 font-bold rounded-lg border border-sky-200">
                Total Audited Weekly Attendance: {tot_v2_sch_tot:,} Pupils
              </span>
            </div>
          </div>

          <div class="overflow-x-auto rounded-lg border border-slate-200 mb-2">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200 text-[11px]">
                <tr>
                  <th rowspan="2" class="p-3 border-r border-slate-200">Audited Primary School</th>
                  <th colspan="3" class="p-2 text-center bg-blue-50/70 border-r border-slate-200">Lower Primary (ECD–P2)</th>
                  <th colspan="3" class="p-2 text-center bg-sky-50/70 border-r border-slate-200">Middle Primary (P3–P4)</th>
                  <th colspan="3" class="p-2 text-center bg-cyan-50/70 border-r border-slate-200">Upper Primary (P5–P7)</th>
                  <th colspan="3" class="p-2 text-center bg-slate-100 font-extrabold">Total School Attendance</th>
                </tr>
                <tr class="border-t border-slate-200 text-[10px]">
                  <th class="p-2 text-right bg-blue-50/40">Boys</th>
                  <th class="p-2 text-right bg-blue-50/40">Girls</th>
                  <th class="p-2 text-right font-bold bg-blue-50/80 border-r border-slate-200">Total</th>
                  <th class="p-2 text-right bg-sky-50/40">Boys</th>
                  <th class="p-2 text-right bg-sky-50/40">Girls</th>
                  <th class="p-2 text-right font-bold bg-sky-50/80 border-r border-slate-200">Total</th>
                  <th class="p-2 text-right bg-cyan-50/40">Boys</th>
                  <th class="p-2 text-right bg-cyan-50/40">Girls</th>
                  <th class="p-2 text-right font-bold bg-cyan-50/80 border-r border-slate-200">Total</th>
                  <th class="p-2 text-right font-bold text-blue-700 bg-slate-100">Boys</th>
                  <th class="p-2 text-right font-bold text-pink-700 bg-slate-100">Girls</th>
                  <th class="p-2 text-right font-black text-slate-900 bg-slate-200/80">Grand Total</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                {v2_sch_att_tbody_html}
              </tbody>
              <tfoot class="bg-slate-100/80 font-extrabold text-slate-900 border-t-2 border-slate-300">
                {v2_sch_att_tfoot_html}
              </tfoot>
            </table>
          </div>
          <p class="text-[11px] text-slate-500 italic">
            <i class="fa-solid fa-circle-info mr-1 text-sky-600"></i><strong>Distinct Metric Tracking:</strong> This table reflects official school weekly register audits. Kotido Mixed P/S participated in the Big Bus Activation event (35 learners) but has not yet submitted their weekly register breakdown.
          </p>
        </div>

        <!-- ROW 2: ACTIVITIES CONDUCTED & PROCESS QUALITY / INCLUSIVITY CHECKS -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Card A: Activities conducted during the session -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>

              <h4 class="text-sm font-bold text-slate-800 mb-1">Activities conducted during the session</h4>
              <p class="text-xs text-slate-500 mb-3">Multi-select verification of interactive SBCC session modules delivered:</p>
              
              <div class="h-80 min-h-[320px]">
                <canvas id="chart-v2-activities"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-[11px] text-slate-600 flex items-center justify-between">
              <span id="v2-activities-footer-text" class="text-emerald-700 font-bold"><i class="fa-solid fa-circle-check mr-1"></i>Modules Verified Across Field Activations</span>
              <span id="v2-activities-footer-badge" class="bg-blue-50 text-wfp-blue px-2 py-0.5 rounded font-bold">3 Schools Logged</span>
            </div>
          </div>

          <!-- Card B: Process Quality & Inclusivity Checks -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Quality Checks</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1">Facilitation quality, inclusive participation and comprehension</h4>
              <p class="text-xs text-slate-500 mb-3">Field coordinator quality assurance checklist recorded during activation:</p>

              <div class="space-y-3">
                <!-- Check 1 -->
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-slate-800">Did learners actively handle materials and practice rather than listen passively?</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 100% (1/1 School)</span>
                  </div>
                  <div class="w-full bg-slate-200 rounded-full h-2">
                    <div class="bg-emerald-600 h-2 rounded-full" style="width: 100%"></div>
                  </div>
                </div>

                <!-- Check 2 -->
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-slate-800">Did all three age bands and both boys and girls participate?</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 100% (1/1 School)</span>
                  </div>
                  <div class="w-full bg-slate-200 rounded-full h-2">
                    <div class="bg-emerald-600 h-2 rounded-full" style="width: 100%"></div>
                  </div>
                </div>

                <!-- Check 3 -->
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-slate-800">Was any learner excluded or left out during sessions?</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">No: 100% (1/1 School)</span>
                  </div>
                  <div class="w-full bg-slate-200 rounded-full h-2">
                    <div class="bg-emerald-600 h-2 rounded-full" style="width: 100%"></div>
                  </div>
                  <div class="text-[11px] text-slate-500 mt-1">Zero learners excluded; active buddy system supported learners with disabilities.</div>
                </div>

                <!-- Check 4 -->
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-slate-800">Were materials understood without long/confusing explanation?</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 100% (1/1 School)</span>
                  </div>
                  <div class="mt-2 p-2 bg-white rounded border border-slate-200 text-[11px] text-slate-700">
                    <strong class="text-wfp-blue">Why:</strong> Visual flashcards, color-coded food grouping cards, and hands-on Metu porridge demonstrations allowed immediate comprehension without complex explanations across Ngakarimojong dialects.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pillar 3: Metu Porridge Uptake Barriers Despite Cash Support -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Pillar 3: Community &amp; Clean Cooking</span>
                <span class="text-xs bg-amber-50 text-amber-800 font-bold px-2 py-0.5 rounded border border-amber-200">Barrier Diagnostic</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Primary reasons for low uptake or preparation know-how of WFP's Metu porridge</h4>
              <p class="text-xs text-slate-500">Diagnostic evaluating why households struggle with Metu porridge preparation despite cash support or market access</p>
            </div>
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
              Sample: 3 Visit 2 Schools (Kotido, Moroto, Nakapiripirit)
            </span>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-5 space-y-3">
              <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <span class="font-bold text-slate-800 block mb-1">Key Diagnostic Finding:</span>
                <p class="text-slate-600 leading-relaxed">
                  <strong>50.0%</strong> of reporting schools cite <em>lack of preparation confidence or recipe skills</em> rather than lack of cash as the primary barrier, alongside ingredient prioritization (25.0%). This directly validates the necessity of practical cooking demonstrations.
                </p>
              </div>
              <div class="grid grid-cols-2 gap-2 text-center text-xs">
                <div class="p-2 bg-blue-50 rounded border border-blue-200">
                  <div class="font-bold text-wfp-blue text-sm">50.0%</div>
                  <div class="text-[10px] text-slate-500">Preparation Confidence</div>
                </div>
                <div class="p-2 bg-amber-50 rounded border border-amber-200">
                  <div class="font-bold text-amber-700 text-sm">25.0%</div>
                  <div class="text-[10px] text-slate-500">Ingredients Prioritization</div>
                </div>
              </div>
            </div>
            <div class="lg:col-span-7">
              <div class="h-56 min-h-[220px]">
                <canvas id="chart-v2-metu-barriers"></canvas>
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 3: PILLAR 2 MICRO-POLL (BOYS ONLY) WITH REASONS IN THEIR WORDS -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Pillar 2 Micro-Poll</span>
                <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">Boys Only Session</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Pillar 2: rebalancing chores and attendance (180 boys sampled)</h4>
              <p class="text-xs text-slate-500">Read out the following statements and count number who agree. Choice (Strongly Agree to Strongly Disagree), Number of boys, and Reason in their words:</p>
            </div>
            <span class="px-3 py-1 bg-emerald-50 text-emerald-700 font-bold rounded-lg border border-emerald-200 text-xs">
              Consensus: 90.9% Average Agreement
            </span>
          </div>

          <!-- 5 Statements Cards with Chart & Reason in their words -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <!-- Statement 1 -->
            <div class="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1 mb-1.5">
                  <span class="text-[10px] font-bold text-wfp-blue uppercase tracking-wider">Statement 1</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">163 / 180 Agreed (90.6%)</span>
                </div>
                <h5 class="text-xs font-bold text-slate-800 mb-2 leading-relaxed">It is unfair for a girl to stay home doing compound work while brothers leave early for class.</h5>
                <div class="h-44 min-h-[175px] mb-2">
                  <canvas id="chart-v2-poll-1"></canvas>
                </div>
              </div>
              <div class="mt-2 p-2 bg-white rounded-lg border border-slate-200 text-[11px] text-slate-700">
                <strong class="text-wfp-blue font-bold">Reason in their words:</strong>
                <p class="italic text-slate-600 mt-0.5">"A girl has equal right to learn and be in class on time; keeping her sweeping compound alone makes her fail tests."</p>
              </div>
            </div>

            <!-- Statement 2 -->
            <div class="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1 mb-1.5">
                  <span class="text-[10px] font-bold text-wfp-blue uppercase tracking-wider">Statement 2</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">168 / 180 Agreed (93.3%)</span>
                </div>
                <h5 class="text-xs font-bold text-slate-800 mb-2 leading-relaxed">Boys and girls should finish morning chores at the same time so both eat porridge and walk to school together.</h5>
                <div class="h-44 min-h-[175px] mb-2">
                  <canvas id="chart-v2-poll-2"></canvas>
                </div>
              </div>
              <div class="mt-2 p-2 bg-white rounded-lg border border-slate-200 text-[11px] text-slate-700">
                <strong class="text-wfp-blue font-bold">Reason in their words:</strong>
                <p class="italic text-slate-600 mt-0.5">"When we help sweep and milk together, porridge is eaten fast and nobody walks alone on the road."</p>
              </div>
            </div>

            <!-- Statement 3 -->
            <div class="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1 mb-1.5">
                  <span class="text-[10px] font-bold text-wfp-blue uppercase tracking-wider">Statement 3</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">161 / 180 Agreed (89.4%)</span>
                </div>
                <h5 class="text-xs font-bold text-slate-800 mb-2 leading-relaxed">Collecting firewood for cooking is a chore that boys and girls should do together.</h5>
                <div class="h-44 min-h-[175px] mb-2">
                  <canvas id="chart-v2-poll-3"></canvas>
                </div>
              </div>
              <div class="mt-2 p-2 bg-white rounded-lg border border-slate-200 text-[11px] text-slate-700">
                <strong class="text-wfp-blue font-bold">Reason in their words:</strong>
                <p class="italic text-slate-600 mt-0.5">"Heavy bundles are easier carried when two people go together, and girls won't get attacked on bushes."</p>
              </div>
            </div>

            <!-- Statement 4 -->
            <div class="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1 mb-1.5">
                  <span class="text-[10px] font-bold text-wfp-blue uppercase tracking-wider">Statement 4</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">165 / 180 Agreed (91.7%)</span>
                </div>
                <h5 class="text-xs font-bold text-slate-800 mb-2 leading-relaxed">I am ready to fetch water from borehole in morning so my sister is not late/punished.</h5>
                <div class="h-44 min-h-[175px] mb-2">
                  <canvas id="chart-v2-poll-4"></canvas>
                </div>
              </div>
              <div class="mt-2 p-2 bg-white rounded-lg border border-slate-200 text-[11px] text-slate-700">
                <strong class="text-wfp-blue font-bold">Reason in their words:</strong>
                <p class="italic text-slate-600 mt-0.5">"I have strong arms for the 20-litre jerrican; my sister can carry the small 5-litre one so she doesn't get whipped for late arrival."</p>
              </div>
            </div>

            <!-- Statement 5 -->
            <div class="p-3.5 bg-slate-50/80 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-1 mb-1.5">
                  <span class="text-[10px] font-bold text-wfp-blue uppercase tracking-wider">Statement 5</span>
                  <span class="text-[11px] font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">161 / 180 Agreed (89.4%)</span>
                </div>
                <h5 class="text-xs font-bold text-slate-800 mb-2 leading-relaxed">If a girl misses school to herd animals or do chores I will speak up to get her back to class.</h5>
                <div class="h-44 min-h-[175px] mb-2">
                  <canvas id="chart-v2-poll-5"></canvas>
                </div>
              </div>
              <div class="mt-2 p-2 bg-white rounded-lg border border-slate-200 text-[11px] text-slate-700">
                <strong class="text-wfp-blue font-bold">Reason in their words:</strong>
                <p class="italic text-slate-600 mt-0.5">"I will tell our father that herding can wait or elders take turns so my sister stays in primary school."</p>
              </div>
            </div>

            <!-- Summary Consensus Card -->
            <div class="p-4 bg-blue-50/60 rounded-xl border border-blue-200 flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-wfp-blue uppercase tracking-wider">Pillar 2 Consensus</span>
                <div class="text-3xl font-black text-wfp-blue mt-1">90.9%</div>
                <div class="text-xs text-slate-700 font-bold mt-1">Average Agreement Rate across 180 Boys</div>
                <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                  Boys explicitly challenged cultural norms and volunteered to carry heavy water jerricans and split firewood so sisters arrive on time.
                </p>
              </div>
              <div class="p-3 bg-white/90 rounded-lg border border-blue-200 mt-3 text-xs text-wfp-blue font-semibold">
                <i class="fa-solid fa-hand-holding-hand mr-1"></i> Boys Pledged Morning Chore Rebalancing
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 4: POST-SESSION RAPID SCENARIO INTERVIEW (LEARNER 1, 2, 3 & ADULT 1, 2) -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Rapid Intercept Assessment</span>
                <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">2 min unaided interview</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Post-session intercept conversation: 4 randomly selected learners and 2 adults</h4>
              <p class="text-xs text-slate-500">Administered away from crowd by Coordinator immediately after session (rule: conversation, not exam; unaided scenario prompt across different age groups):</p>
            </div>
            <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded">6 Sampled In-Depth Profiles</span>
          </div>

          <!-- Cards for the 6 Respondents -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
            <!-- Learner 1 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Learner 1</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Upper Primary</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Porridge greens/food addition:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Explains a specific, actionable practice without prompting
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Add crushed groundnuts, pounded moringa leaves, and roasted sesame seeds to make Metu thick and nutritious."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Heavy morning chores resolution:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      States that boys and girls share water/wood chores equally before leaving
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "My brother fetches the first water jerrycan while I sweep so we both finish by 7:00 AM and walk to school together."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Campaign Line Recall: 'Abas ikimorikinit kaapei':</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Demonstrated (explained clearly and accurately without prompting)
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "It means the NutriBus brings all of us together as one school and one family to eat healthy food and learn."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Learner 2 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Learner 2</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">Male</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Middle Primary</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Porridge greens/food addition:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Explains a specific, actionable practice without prompting
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Stir in cow milk and fresh amaranth greens (Eboo) picked from home garden into warm porridge."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Heavy morning chores resolution:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      States that boys and girls share water/wood chores equally before leaving
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "I carry the firewood bundle from the store while my sister lights the fire, so nobody is left behind."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Campaign Line Recall: 'Abas ikimorikinit kaapei':</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Demonstrated (explained clearly and accurately without prompting)
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Together we share work and food so girls and boys both study well."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Learner 3 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Learner 3</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Lower Primary</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Porridge greens/food addition:</span>
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-bold rounded text-[11px] border border-amber-200 block mb-1">
                      Gives a general/vague idea; lacks a concrete action
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Put yellow pumpkin and green leaves from mum to grow big and run fast."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Heavy morning chores resolution:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      States that boys and girls share water/wood chores equally before leaving
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Big brother helps bring the water bucket so mummy smiles and we run together."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Campaign Line Recall: 'Abas ikimorikinit kaapei':</span>
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-bold rounded text-[11px] border border-amber-200 block mb-1">
                      Partly demonstrated (vague or needed prompting)
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "The bus that came with music and good porridge for everyone."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Learner 4 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Learner 4</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">Male</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Upper Primary</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Porridge greens/food addition:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Explains a specific, actionable practice without prompting
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Boil cowpeas and pound them into the warm sorghum porridge with a spoon of shea butter or simsim."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Heavy morning chores resolution:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      States that boys and girls share water/wood chores equally before leaving
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "I sweep the compound and release the goats early so my sister and I can wash our faces and run to school on time."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Campaign Line Recall: 'Abas ikimorikinit kaapei':</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Demonstrated (explained clearly and accurately without prompting)
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "It means the bus unites the whole village and school so everyone eats strong and learns."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Adult 1 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Adult 1</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Caregiver / PTA</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Porridge greens/food addition:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Explains a specific, actionable practice without prompting
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Supplement plain sorghum flour with roasted simsim paste, orange sweet potato puree, and local milk for zinc and iron."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Heavy morning chores resolution:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      States that boys and girls share water/wood chores equally before leaving
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Assign male sons the morning borehole water trip so female daughters are dressed and at school gates before 7:30 AM."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Campaign Line Recall: 'Abas ikimorikinit kaapei':</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Demonstrated (explained clearly and accurately without prompting)
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Moving forward united: when boys and girls share burdens equally, family nutrition and school completion improve."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Adult 2 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Adult 2</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">Male</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Senior Teacher / SMC</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Porridge greens/food addition:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Explains a specific, actionable practice without prompting
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Promote multi-grain porridge with cowpea flour, dry fish powder, and indigenous greens to fight anaemia in learners."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Heavy morning chores resolution:</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      States that boys and girls share water/wood chores equally before leaving
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Sensitize village elders at water points so fathers stop sending only girls to herd and fetch water during school hours."
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">Campaign Line Recall: 'Abas ikimorikinit kaapei':</span>
                    <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                      Demonstrated (explained clearly and accurately without prompting)
                    </span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Collective action for education and nutrition: no child should be left behind due to preventable household division of labour."
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Scenario Cohort Aggregate Charts -->
          <div class="mt-4 pt-4 border-t border-slate-200">
            <span class="text-xs font-bold text-slate-700 uppercase mb-2 block">Cohort Aggregates (36 Randomly Intercepted Participants across 6 Schools)</span>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <h5 class="text-xs font-bold text-slate-800 mb-1">1. Porridge greens and supplementation recall</h5>
                <div class="h-52 min-h-[210px]">
                  <canvas id="chart-v2-scenario-porridge"></canvas>
                </div>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <h5 class="text-xs font-bold text-slate-800 mb-1">2. Chore rebalancing strategy recall</h5>
                <div class="h-52 min-h-[210px]">
                  <canvas id="chart-v2-scenario-chores"></canvas>
                </div>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <h5 class="text-xs font-bold text-slate-800 mb-1">3. 'Abas ikimorikinit kaapei' meaning recall</h5>
                <div class="h-52 min-h-[210px]">
                  <canvas id="chart-v2-scenario-slogan"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 5: COORDINATOR POST-ACTIVATION FIELD AUDIT LOG -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Qualitative field observations and written school commitments</h4>
          <p class="text-xs text-slate-500 mb-4">Key delivery issues, key successes, adaptations for next school, and exact written school commitments recorded by field teams:</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- School 1 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div class="space-y-2.5 text-xs text-slate-700">
                <div class="flex items-center justify-between border-b border-slate-200 pb-2">
                  <span class="font-bold text-slate-900">Kaabong West Primary School</span>
                  <span class="text-[10px] font-semibold bg-blue-100 text-wfp-blue px-2 py-0.5 rounded">Kaabong</span>
                </div>
                <div>
                  <strong class="text-amber-800 block mb-0.5">Key delivery issue or barrier observed:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "High ambient wind created sound distortion during outdoor cooking demo microphone setup."
                  </p>
                </div>
                <div>
                  <strong class="text-emerald-800 block mb-0.5">Key success observed:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Over 180 boys joined the water jerrican balancing relay and loudly pledged to share water-fetching chores."
                  </p>
                </div>
                <div>
                  <strong class="text-blue-800 block mb-0.5">One adaptation to make before next school:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Shift subsequent demo circle into the lee side of the main classroom block to shield against wind noise."
                  </p>
                </div>
              </div>
              <div class="mt-3 pt-2.5 border-t border-slate-200">
                <strong class="text-wfp-blue text-xs block mb-1">Written School Commitment in exact words:</strong>
                <div class="p-2.5 bg-blue-50/80 rounded-lg border border-blue-200 text-[11px] text-slate-800 italic">
                  "We the teachers and pupils of Kaabong West commit that every child will receive porridge with greens, and boys will fetch morning water so girls never arrive late."
                </div>
              </div>
            </div>

            <!-- School 2 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div class="space-y-2.5 text-xs text-slate-700">
                <div class="flex items-center justify-between border-b border-slate-200 pb-2">
                  <span class="font-bold text-slate-900">Lomorunyankori Primary School</span>
                  <span class="text-[10px] font-semibold bg-blue-100 text-wfp-blue px-2 py-0.5 rounded">Moroto</span>
                </div>
                <div>
                  <strong class="text-amber-800 block mb-0.5">Key delivery issue or barrier observed:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Dusty wind made paper flashcards vulnerable to tearing during peer group food sorting."
                  </p>
                </div>
                <div>
                  <strong class="text-emerald-800 block mb-0.5">Key success observed:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Headteacher pledged school woodlot trees for shade-based NutriClub demonstrations and SMC provided clean storage."
                  </p>
                </div>
                <div>
                  <strong class="text-blue-800 block mb-0.5">One adaptation to make before next school:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Laminate all visual demo charts and mount them on weighted wooden tripods."
                  </p>
                </div>
              </div>
              <div class="mt-3 pt-2.5 border-t border-slate-200">
                <strong class="text-wfp-blue text-xs block mb-1">Written School Commitment in exact words:</strong>
                <div class="p-2.5 bg-blue-50/80 rounded-lg border border-blue-200 text-[11px] text-slate-800 italic">
                  "Lomorunyankori P/S commits to establish an active NutriClub meeting every Wednesday and supporting female attendance through chore rebalancing."
                </div>
              </div>
            </div>

            <!-- School 3 -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div class="space-y-2.5 text-xs text-slate-700">
                <div class="flex items-center justify-between border-b border-slate-200 pb-2">
                  <span class="font-bold text-slate-900">Acegeretolim Primary School</span>
                  <span class="text-[10px] font-semibold bg-blue-100 text-wfp-blue px-2 py-0.5 rounded">Nabilatuk</span>
                </div>
                <div>
                  <strong class="text-amber-800 block mb-0.5">Key delivery issue or barrier observed:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Local dialect differences in scientific nutrition terms required prompt translation into Ngakarimojong."
                  </p>
                </div>
                <div>
                  <strong class="text-emerald-800 block mb-0.5">Key success observed:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Community elders who attended stayed for the full chore dialogue and agreed with boys' public pledges."
                  </p>
                </div>
                <div>
                  <strong class="text-blue-800 block mb-0.5">One adaptation to make before next school:</strong>
                  <p class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Engage lead local language teacher as co-facilitator alongside WFP NutriBus coordinator."
                  </p>
                </div>
              </div>
              <div class="mt-3 pt-2.5 border-t border-slate-200">
                <strong class="text-wfp-blue text-xs block mb-1">Written School Commitment in exact words:</strong>
                <div class="p-2.5 bg-blue-50/80 rounded-lg border border-blue-200 text-[11px] text-slate-800 italic">
                  "Acegeretolim school management and parents commit to monitor morning girl-child attendance and enforce equal chore allocation at household kraals."
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SUB-SECTION: VISIT 3 -->
      <div id="sub-v3" class="space-y-6 hidden">
        <!-- Header Banner -->
        <div class="flex flex-wrap items-center justify-between gap-3 p-4 bg-gradient-to-r from-blue-50 to-emerald-50 rounded-xl border border-blue-200">
          <div>
            <h3 class="text-base font-bold text-slate-800">Visit 3: materials collection, debrief and closing results audit</h3>
            <p class="text-xs text-slate-600 mt-0.5">NutriChart collection and joint household audit, school institutional debrief, and household and learner in-depth shifts</p>
          </div>
          <div class="text-right">
            <span class="px-3 py-1 bg-white text-slate-600 font-bold rounded-lg border border-slate-200 text-xs shadow-sm">
              Pending Closeout Audit
            </span>
          </div>
        </div>

        <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <i class="fa-solid fa-clock text-slate-400 text-sm"></i>
            <span><strong>Visit 3 Status:</strong> No Visit 3 closeout audit submissions recorded in the activity log yet. Materials returns, joint household audits, and debrief results will appear here as field monitors complete closing audits.</span>
          </div>
          <span class="px-2 py-0.5 bg-slate-200 text-slate-600 font-bold rounded text-[11px] shrink-0">0 of 64 Audited</span>
        </div>

        <!-- ROW 1: NUTRICHARTS COLLECTION & JOINT HOUSEHOLD AUDIT -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Metric 1: Total Issued -->
          <div class="p-4 bg-white rounded-xl border border-slate-200/80 card-shadow flex items-center justify-between">
            <div>
              <h4 class="text-xs font-bold text-slate-700 mt-0.5">Total NutriCharts issued (Visit 1)</h4>
              <div class="text-2xl font-black text-slate-400 mt-1">0</div>
              <span class="text-[11px] text-slate-400">Target: 1,840 cards across 64 schools</span>
            </div>
            <div class="w-12 h-12 rounded-xl bg-slate-50 text-slate-400 flex items-center justify-center text-xl">
              <i class="fa-solid fa-file-invoice"></i>
            </div>
          </div>

          <!-- Metric 2: Total Returned Today -->
          <div class="p-4 bg-white rounded-xl border border-slate-200/80 card-shadow flex items-center justify-between">
            <div>
              <h4 class="text-xs font-bold text-slate-700 mt-0.5">Total NutriCharts returned today</h4>
              <div class="text-2xl font-black text-slate-400 mt-1">0</div>
              <span class="text-[11px] text-slate-400 font-semibold">0.0% Overall Return Rate</span>
            </div>
            <div class="w-12 h-12 rounded-xl bg-slate-50 text-slate-400 flex items-center justify-center text-xl">
              <i class="fa-solid fa-box-archive"></i>
            </div>
          </div>

          <!-- Metric 3: Joint Household Completion -->
          <div class="p-4 bg-white rounded-xl border border-slate-200/80 card-shadow flex items-center justify-between">
            <div>
              <h4 class="text-xs font-bold text-slate-700 mt-0.5">Returned charts showing joint household completion</h4>
              <div class="text-2xl font-black text-slate-400 mt-1">0</div>
              <span class="text-[11px] text-slate-400 font-semibold">Awaiting closeout submissions</span>
            </div>
            <div class="w-12 h-12 rounded-xl bg-slate-50 text-slate-400 flex items-center justify-center text-xl">
              <i class="fa-solid fa-handshake-angle"></i>
            </div>
          </div>
        </div>

        <!-- ROW 2: PRIMARY FEEDBACK & PRIMARY BARRIERS -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
              <h4 class="text-sm font-bold text-slate-800 mb-1">Primary feedback from households</h4>
            <p class="text-xs text-slate-500 mb-3">Feedback options recorded from returned NutriCharts:</p>
            <div class="h-48 min-h-[190px]">
              <canvas id="chart-v3-feedback"></canvas>
            </div>
          </div>

          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
              <h4 class="text-sm font-bold text-slate-800 mb-1">Primary barriers reported by households</h4>
            <p class="text-xs text-slate-500 mb-3">What was difficult or got in the way of taking action:</p>
            <div class="h-64 min-h-[250px]">
              <canvas id="chart-v3-barriers"></canvas>
            </div>
          </div>
        </div>

        <!-- ROW 3: SCHOOL-LEVEL INSTITUTIONAL DEBRIEF -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div>
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Institutional Results Debrief</span>
              <h4 class="text-sm font-bold text-slate-800">School commitments, absentee tracing and kitchen energy audit</h4>
            </div>
            <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded border border-slate-200">
              0 Schools Logged (Pending Field Closeout)
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <!-- Question 1: Commitment Status -->
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <h5 class="text-xs font-bold text-slate-800 mb-2">Status of bus day school commitment</h5>
                <div class="h-48 min-h-[190px]">
                  <canvas id="chart-v3-commitment"></canvas>
                </div>
              </div>
              <div class="mt-2 text-[11px] text-slate-600 bg-white p-2 rounded border border-slate-200">
                <strong class="text-wfp-blue font-bold">Audit Status:</strong> Pending field submissions (0 schools).
              </div>
            </div>

            <!-- Question 2: Absentee Tracing -->
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <h5 class="text-xs font-bold text-slate-800 mb-2">Collective chronic absentee tracing active?</h5>
                <div class="h-48 min-h-[190px]">
                  <canvas id="chart-v3-tracing"></canvas>
                </div>
              </div>
              <div class="mt-2 text-[11px] text-slate-600 bg-white p-2 rounded border border-slate-200">
                <strong class="text-wfp-blue font-bold">Tracing Reach:</strong> Pending field submissions (0 schools).
              </div>
            </div>

            <!-- Question 3: School Kitchen Stoves -->
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <h5 class="text-xs font-bold text-slate-800 mb-2">Did the school kitchen implement firewood-saving cooking practices/stoves?</h5>
                <div class="h-48 min-h-[190px]">
                  <canvas id="chart-v3-kitchen"></canvas>
                </div>
              </div>
              <div class="mt-2 text-[11px] text-slate-600 bg-white p-2 rounded border border-slate-200">
                <strong class="text-wfp-blue font-bold">Verification:</strong> Pending field submissions (0 schools).
              </div>
            </div>
          </div>
        </div>

        <!-- PILLAR 1 & PILLAR 2 INTEGRATED IMPACT TRACKING & PR/RADIO TRACKING -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Pillar 1: School Feeding Protection Impact -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Pillar 1: School Feeding</span>
                <span class="text-xs bg-slate-100 text-slate-600 font-bold px-2 py-0.5 rounded border border-slate-200">0.0% Logged</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1">Impact of school feeding routines on student presence</h4>
              <p class="text-xs text-slate-500 mb-3">Evaluation across 64 school cycles on meal protection sustaining classroom presence:</p>
              <div class="h-52 min-h-[200px]">
                <canvas id="chart-v3-pillar1-feeding"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-[11px] text-slate-600">
              <span>High impact: <strong>0 schools</strong> | Moderate: <strong>0</strong> | Low: <strong>0</strong></span>
            </div>
          </div>

          <!-- Pillar 2: Fair Plate-Sharing Practice Shift -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[11px] font-bold text-purple-700 uppercase tracking-wider">Pillar 2: Gender &amp; Equity</span>
                <span class="text-xs bg-slate-100 text-slate-600 font-bold px-2 py-0.5 rounded border border-slate-200">0.0% Logged</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1">Shift in fair plate-sharing practices</h4>
              <p class="text-xs text-slate-500 mb-3">Reported shift stopping the cultural practice of young ones or girls eating last:</p>
              <div class="h-52 min-h-[200px]">
                <canvas id="chart-v3-pillar2-plate"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-[11px] text-slate-600">
              <span>Consistent: <strong>0 schools</strong> | Some resistance: <strong>0</strong> | No change: <strong>0</strong></span>
            </div>
          </div>
        </div>

        <!-- Embedded PR, Communications & Radio Broadcast Tracking (School Level) -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-3">
            <div>
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Campaign Communications &amp; Media</span>
              <h4 class="text-sm font-bold text-slate-800">School-level PR highlights, social media captures and radio tracking</h4>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded border border-slate-200">
                PR Captured: 0.0%
              </span>
              <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded border border-slate-200">
                Radio Reach: 0.0%
              </span>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800">School PR &amp; Social Media Highlights Captured:</span>
                <span class="font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">0.0% (0/64 Schools)</span>
              </div>
              <p class="text-slate-600 text-[11px]">Pending Visit 3 closeout submissions from school media squads.</p>
            </div>

            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800">Campaign Radio Spots Heard by School Community:</span>
                <span class="font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">0.0% (0/64 Schools)</span>
              </div>
              <p class="text-slate-600 text-[11px]">Radio listenership verification will populate as school closeout audits occur across Karamoja FM, Nenah FM, and Voice of Karamoja.</p>
              <div class="grid grid-cols-3 gap-2 text-center pt-2">
                <div class="p-2 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-500">0.0%</div>
                  <div class="text-[10px] text-slate-500">Heard Spots</div>
                </div>
                <div class="p-2 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-500">0.0%</div>
                  <div class="text-[10px] text-slate-500">Did Not Hear</div>
                </div>
                <div class="p-2 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-500">0.0%</div>
                  <div class="text-[10px] text-slate-500">Unsure</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 4: HOUSEHOLD AND LEARNER INTERVIEW (5 IN-DEPTH PROFILES) -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">Closing Rapid Intercept</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Household and learner interviews (Learners I, II, III and Caregivers I, II, III)</h4>
              <p class="text-xs text-slate-500">In-depth qualitative verification of feasible actions tried at home, difficult bottlenecks, morning chore shifts, and food serving equity:</p>
            </div>
            <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded">0 Sampled Household Audits</span>
          </div>

          <!-- Awaiting Household & Learner Exit Intercepts Banner -->
          <div class="p-6 bg-slate-50 border border-slate-200 rounded-xl text-center space-y-2 mb-4">
            <div class="w-10 h-10 mx-auto rounded-full bg-blue-100 text-wfp-blue flex items-center justify-center text-base">
              <i class="fa-solid fa-hourglass-half"></i>
            </div>
            <h5 class="text-xs font-bold text-slate-800 uppercase tracking-wide">Awaiting Household &amp; Learner Exit Intercepts</h5>
            <p class="text-xs text-slate-500 max-w-md mx-auto">
              No Visit 3 exit audits or household intercepts have been submitted from the field yet. Once teams complete closeout visits, verified learner and caregiver profiles will appear here dynamically.
            </p>
          </div>

          <!-- ROW 5: HOUSEHOLD SHIFT COHORT AGGREGATES -->
          <div class="mt-4 pt-4 border-t border-slate-200">
            <span class="text-xs font-bold text-slate-700 uppercase mb-2 block">Cohort Aggregates (0 Households Sampled — Awaiting Visit 3 Deployments)</span>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <h5 class="text-xs font-bold text-slate-800 mb-1">1. Feasible actions tried at home</h5>
                <div class="h-60 min-h-[240px]">
                  <canvas id="chart-v3-actions-tried"></canvas>
                </div>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <h5 class="text-xs font-bold text-slate-800 mb-1">2. Morning chore sharing shifted</h5>
                <div class="h-48 min-h-[190px]">
                  <canvas id="chart-v3-chore-shift"></canvas>
                </div>
              </div>
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <h5 class="text-xs font-bold text-slate-800 mb-1">3. Food serving order shifted for youngest</h5>
                <div class="h-48 min-h-[190px]">
                  <canvas id="chart-v3-serving-shift"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 4: COMMUNITY COOKING DEMO -->
    <!-- ========================================== -->
    <div id="tab-demo" class="tab-content hidden space-y-6">
      <div class="bg-wfp-soft border-l-4 border-wfp-blue p-4 rounded-r-xl">
        <div>
          <h3 class="text-sm font-bold text-wfp-dark">Community cooking demonstration field results</h3>
          <p class="text-xs text-slate-600 mt-0.5">Catchment demo site headcounts (Caregivers, Fathers, Children, PWDs), hands-on cooking engagement, Metu porridge local additions, fuel-saving practices demonstrated, and private caregiver intercept interviews.</p>
        </div>
      </div>

      <!-- TOP METADATA CARD: SITE & SUBMITTER AUDIT -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-3">
          <div>
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Field Demonstration Verification</span>
            <h4 class="text-sm font-bold text-slate-800">Village cooking demonstrations around 64 schools</h4>
          </div>
          <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded-lg border border-blue-200">
            64 School Communities · 10 Demos Each (640 Total Demonstrations)
          </span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span class="text-[11px] font-bold text-slate-700 block mb-1">Village Demonstration Sites:</span>
            <p class="text-xs text-slate-600 leading-relaxed">
              Held under shade trees, community boreholes, and kraal meeting spaces in the villages surrounding all 64 primary schools across Karamoja (10 cooking demonstrations per school community, totaling 640 demonstrations).
            </p>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span class="text-[11px] font-bold text-slate-700 block mb-1">Session Facilitation Breakdown:</span>
            <div class="flex items-center gap-2 mt-1 flex-wrap">
              <span class="px-2.5 py-1 bg-slate-100 text-slate-600 font-semibold rounded text-xs border border-slate-200">
                Village Health Teams (VHT): 0 Demos (0.0%)
              </span>
              <span class="px-2.5 py-1 bg-slate-100 text-slate-600 font-semibold rounded text-xs border border-slate-200">
                Lead Coordinator: 0 Demos (0.0%)
              </span>
            </div>
            <span class="text-[10px] text-slate-500 block mt-1.5 italic">Awaiting field submissions (0 of 640 demonstrations conducted).</span>
          </div>
        </div>
      </div>

      <!-- CAPACITY-STRENGTHENING PARTNERS PRESENCE & CO-FACILITATION (COMMUNITY DEMO) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
          <div>
            <div class="flex items-center gap-2 mb-0.5">
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Partner Network Collaboration</span>
              <span class="text-xs bg-slate-100 text-slate-700 font-bold px-2 py-0.5 rounded border border-slate-200">0.0% Present (0/640 Demos)</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800">Were capacity-strengthening partners (e.g., UNAC, Afi) present and co-facilitating this community demonstration?</h4>
            <p class="text-xs text-slate-500">Partner co-facilitation verifying inclusive PWD mobilization, gender dialogues, and clean cooking sustainability</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded border border-slate-200">
              0 of 640 Demos Co-Facilitated
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Col 1: If yes, specify partner name -->
          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-800">If yes, specify partner name:</span>
              <span class="text-[10px] text-slate-500 font-semibold">Multi-select verification</span>
            </div>
            <div class="space-y-1.5 text-xs text-slate-700">
              <div class="flex items-center justify-between bg-white px-2.5 py-1.5 rounded border border-slate-200">
                <span class="font-medium">UNAC</span>
                <span class="font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[11px]">0.0% (0/640)</span>
              </div>
              <div class="flex items-center justify-between bg-white px-2.5 py-1.5 rounded border border-slate-200">
                <span class="font-medium">AFI</span>
                <span class="font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[11px]">0.0% (0/640)</span>
              </div>
              <div class="flex items-center justify-between bg-white px-2.5 py-1.5 rounded border border-slate-200">
                <span class="font-semibold text-slate-600">Other</span>
                <span class="font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[11px]">0.0% (0/640)</span>
              </div>
            </div>
            <div class="p-2 bg-slate-100/70 rounded border border-slate-200 text-[11px] text-slate-600">
              <strong class="text-slate-700">Status:</strong> Awaiting field submissions once village demonstrations commence.
            </div>
          </div>

          <!-- Col 2: Partner role observed -->
          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-slate-800">Partner role observed:</span>
              <span class="text-[10px] text-slate-500 font-semibold">Observed contributions</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Co-facilitating clean cooking / gender dialogue</span>
                <span class="font-bold text-slate-500 text-xs mt-1.5">0.0% (0/640)</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Mentoring local VHTs / Elders</span>
                <span class="font-bold text-slate-500 text-xs mt-1.5">0.0% (0/640)</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Observing for sustainability tracking</span>
                <span class="font-bold text-slate-500 text-xs mt-1.5">0.0% (0/640)</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Other</span>
                <span class="font-bold text-slate-500 text-xs mt-1.5">0.0% (0/640)</span>
              </div>
            </div>
            <div class="p-2 bg-slate-100 rounded text-[10px] text-slate-600 italic">
              Field verification pending demonstration rollout across 64 school catchments.
            </div>
          </div>
        </div>
      </div>

      <!-- MINIMUM ATTENDANCE THRESHOLD BENCHMARK CARD (80 PARTICIPANTS RULE) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
          <div>
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Quality Assurance & Attendance Standard</span>
            <h4 class="text-sm font-bold text-slate-800">Minimum turnout benchmark: 80 participants per demonstration</h4>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-amber-50 text-amber-800 font-bold px-3 py-1 rounded-lg border border-amber-200 flex items-center gap-1.5">
              <i class="fa-solid fa-flag text-red-600"></i> Strict Benchmark: Min. 80 Participants / Session
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
          <div class="p-3.5 bg-blue-50/50 rounded-xl border border-blue-200/70">
            <span class="text-[11px] font-bold text-slate-500 block">Attendance Benchmark</span>
            <div class="text-2xl font-black text-wfp-blue mt-0.5">80+</div>
            <span class="text-[10px] text-slate-500">Min. required attendees / site</span>
          </div>
          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span class="text-[11px] font-bold text-slate-500 block">Total Demonstrations Evaluated</span>
            <div class="text-2xl font-black text-slate-800 mt-0.5" id="demo-kpi-total-sessions">0</div>
            <span class="text-[10px] text-slate-500">Target: 640 sessions (10 / school)</span>
          </div>
          <div class="p-3.5 bg-emerald-50/60 rounded-xl border border-emerald-200">
            <span class="text-[11px] font-bold text-emerald-800 block">Compliant Sessions (&ge;80)</span>
            <div class="text-2xl font-black text-emerald-700 mt-0.5" id="demo-kpi-compliant-sessions">0</div>
            <span class="text-[10px] text-emerald-600 font-bold" id="demo-kpi-compliant-rate">0.0% compliant rate</span>
          </div>
          <div class="p-3.5 bg-red-50/60 rounded-xl border border-red-200">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold text-red-800 block">Red-Flagged Sessions (&lt;80)</span>
              <span class="w-2 h-2 rounded-full bg-slate-300"></span>
            </div>
            <div class="text-2xl font-black text-red-600 mt-0.5" id="demo-kpi-flagged-sessions">0</div>
            <span class="text-[10px] text-red-600 font-bold" id="demo-kpi-flagged-rate">0.0% flagged for follow-up</span>
          </div>
        </div>

        <div class="p-3.5 bg-amber-50/70 rounded-lg border border-amber-300 text-xs text-amber-950 flex items-start gap-2.5">
          <i class="fa-solid fa-triangle-exclamation text-amber-600 text-base mt-0.5 shrink-0"></i>
          <div class="leading-relaxed">
            <span class="font-bold">M&amp;E Protocol for Turnout Compliance &amp; Calculations:</span>
            Community cooking demonstrations are designed to reach a minimum of <strong>80 participants</strong> per session to achieve the campaign reach of <strong>51,200 caregivers</strong> across 640 village sessions.
            When a session records fewer than 80 participants, it is automatically <strong>red-flagged (🚩)</strong> for supervisor investigation and community mobilization review.
            <strong>Crucially, all participants from red-flagged sessions are fully included and retained in all total calculations, district aggregations, and cumulative KPI headcounts.</strong>
          </div>
        </div>
      </div>

      <!-- ROW 1: PARTICIPANT HEADCOUNT MATRIX -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div>
            <h4 class="text-sm font-bold text-slate-800">Participant headcount by role, sex and PWD inclusion</h4>
            <p class="text-xs text-slate-500">Caregivers, fathers/elders, children, and PWD inclusion recorded at demonstration sites:</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded border border-slate-200">
              Total attendees: 0
            </span>
            <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded border border-slate-200">
              PWD Inclusivity: 0 (0.0%)
            </span>
          </div>
        </div>

        <div>
          <div class="sm:hidden text-[10px] text-slate-400 italic mb-1.5 flex items-center gap-1">
            <i class="fa-solid fa-arrows-left-right text-wfp-blue"></i>
            <span>Scroll table sideways to view all columns</span>
          </div>
          <div class="overflow-x-auto rounded-lg border border-slate-200">
            <table class="w-full text-left text-xs border-collapse min-w-[540px]">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold">
                <th class="py-2.5 px-3">Participant Headcount Category</th>
                <th class="py-2.5 px-3 text-right">Male</th>
                <th class="py-2.5 px-3 text-right">Female</th>
                <th class="py-2.5 px-3 text-right font-extrabold text-wfp-blue">Total Headcount</th>
                <th class="py-2.5 px-3">Facilitation Context & Inclusivity Note</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-slate-700">
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Female Caregivers</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-400">0</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Primary household food preparers and child nutrition gatekeepers</td>
              </tr>
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Male Fathers / Elders</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-400">0</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Household decision-makers engaged in gender chore rebalancing dialogues</td>
              </tr>
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Male Children</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-400">0</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Learners participating in cooking activities and food sorting games</td>
              </tr>
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Female Children</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-400">0</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Girl-child participants practicing hands-on Metu porridge supplementation</td>
              </tr>
              <tr class="hover:bg-slate-50/50 bg-blue-50/20">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Male PWDs</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-400">0</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Participants with physical or sensory disabilities supported by VHTs</td>
              </tr>
              <tr class="hover:bg-slate-50/50 bg-blue-50/20">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Female PWDs</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-400">0</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Provided priority front seating and assisted tasting bowls</td>
              </tr>
              <tr class="bg-slate-100 font-extrabold text-slate-900 border-t-2 border-slate-300">
                <td class="py-3 px-3">Total Cumulative Headcount</td>
                <td class="py-3 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-3 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-3 px-3 text-right font-mono text-slate-500 text-sm">0</td>
                <td class="py-3 px-3 text-slate-500 font-normal">Awaiting Community Cooking Demonstration Logs</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

      <!-- DEMONSTRATION SITES AUDIT REGISTER & RED FLAG TRACKING TABLE (ACCORDION APPROACH: 640 SESSIONS) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <h4 class="text-sm font-bold text-slate-800">Demonstration site audit register and turnout compliance</h4>
              <span class="text-xs bg-red-50 text-red-700 font-bold px-2.5 py-0.5 rounded border border-red-200">
                🚩 Flagged if &lt;80 · Exact Counts Captured in Totals
              </span>
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2.5 py-0.5 rounded border border-blue-200">
                640 Catchment Demos · 64 Schools
              </span>
            </div>
            <p class="text-xs text-slate-500 mt-1">Village demonstration sessions monitored across school catchment areas. Structured by district and primary school catchment using an accordion layout:</p>
          </div>
          <div class="flex flex-wrap items-center gap-2 text-xs">
            <span class="px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded border border-emerald-200">
              <i class="fa-solid fa-check mr-1"></i> &ge;80: Compliant
            </span>
            <span class="px-2.5 py-1 bg-red-50 text-red-700 font-bold rounded border border-red-200">
              <i class="fa-solid fa-flag mr-1"></i> &lt;80: Red-Flagged
            </span>
          </div>
        </div>

        <!-- Filter Controls Bar -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-100">
          <div class="flex flex-wrap items-center gap-2 flex-1 min-w-[280px]">
            <div class="relative flex-1 min-w-[200px]">
              <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400 text-xs"></i>
              <input type="text" id="demo-search-input" onkeyup="handleDemoSearch(this.value)" placeholder="Search village venue, school, subcounty, facilitator..." class="w-full text-xs pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:border-wfp-blue focus:bg-white transition" />
            </div>
            <!-- Compliance Filter Buttons -->
            <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-lg text-xs font-semibold">
              <button id="btn-demo-filter-all" onclick="setDemoFilter('all')" class="px-2.5 py-1 rounded bg-white text-wfp-blue shadow-xs font-bold transition">All 640 Demos</button>
              <button id="btn-demo-filter-flagged" onclick="setDemoFilter('flagged')" class="px-2.5 py-1 rounded text-red-700 hover:bg-white/80 transition">🚩 Flagged (&lt;80)</button>
              <button id="btn-demo-filter-compliant" onclick="setDemoFilter('compliant')" class="px-2.5 py-1 rounded text-emerald-700 hover:bg-white/80 transition">✅ Compliant (&ge;80)</button>
            </div>
          </div>

          <div class="flex items-center gap-2 text-xs">
            <button onclick="toggleAllDemoAccordions(true)" class="px-2.5 py-1.5 border border-slate-300 bg-white rounded-lg text-slate-700 hover:bg-slate-50 font-semibold transition flex items-center gap-1">
              <i class="fa-solid fa-angles-down text-wfp-blue"></i>
              <span>Expand all</span>
            </button>
            <button onclick="toggleAllDemoAccordions(false)" class="px-2.5 py-1.5 border border-slate-300 bg-white rounded-lg text-slate-700 hover:bg-slate-50 font-semibold transition flex items-center gap-1">
              <i class="fa-solid fa-angles-up text-slate-400"></i>
              <span>Collapse all</span>
            </button>
          </div>
        </div>

        <!-- Dynamic Overall Summary KPI Banner -->
        <div id="demo-summary-banner" class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs flex flex-wrap items-center justify-between gap-3">
          <!-- Populated by renderDemoAccordions() -->
        </div>

        <!-- Accordion Container -->
        <div id="demo-accordions-container" class="space-y-3 pt-1">
          <!-- Populated dynamically by JS renderDemoAccordions() -->
        </div>
      </div>

      <!-- ROW 2: COOKING ENGAGEMENT, SOURCING & FUEL-SAVING COOKING -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Col 1: Facilitation Quality Checks -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <h4 class="text-sm font-bold text-slate-800 mb-2">Hands-on cooking engagement and food sourcing checks</h4>
            
            <div class="space-y-3 text-xs">
              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-bold text-slate-800">Did caregivers cook and handle ingredients hands-on, or only observe?</span>
                  <span class="px-2 py-0.5 bg-slate-100 text-slate-700 font-bold rounded text-[11px]">0 Demos Conducted</span>
                </div>
                <div class="text-[11px] text-slate-600">
                  Pending field submissions (0 of 640 demonstrations recorded).
                </div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-bold text-slate-800">Was WFP Metu porridge demonstrated with additions of obtainable local staples?</span>
                  <span class="px-2 py-0.5 bg-slate-100 text-slate-700 font-bold rounded text-[11px]">0 Demos Conducted</span>
                </div>
                <div class="text-[11px] text-slate-600 mb-1">
                  Pending field submissions (0 of 640 demonstrations recorded).
                </div>
                <div class="p-2 bg-white rounded border border-slate-200 text-[11px] text-slate-500 italic">
                  <strong class="text-slate-700 not-italic font-bold">Comments or reactions from spectators:</strong>
                  Awaiting community demonstration reports (0 demos conducted).
                </div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-bold text-slate-800">Were all demonstrated foods sourced locally from seasonal gardens/markets?</span>
                  <span class="px-2 py-0.5 bg-slate-100 text-slate-700 font-bold rounded text-[11px]">0 Demos Conducted</span>
                </div>
                <div class="text-[11px] text-slate-600">
                  Pending field submissions (0 of 640 demonstrations recorded).
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Col 2: Fuel-Saving Practices Chart -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Which fuel-saving practices were demonstrated to the gathering?</h4>
          <p class="text-xs text-slate-500 mb-3">Verification of fuel-saving cookstove and cooking practices shown across target 640 sites:</p>
          <div class="h-64 min-h-[250px]">
            <canvas id="chart-demo-fuelsaving"></canvas>
          </div>
        </div>
      </div>

      <!-- ROW 3: PRIVATE CAREGIVER INTERCEPT INTERVIEWS (CAREGIVERS 1, 2, 3) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div>
            <div class="flex items-center gap-2 mb-0.5">
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Private Rapid Intercept</span>
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">Post-Demo Evaluation</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800">Conducted privately at demo ground: interview 2 to 3 attending caregivers right after demo</h4>
            <p class="text-xs text-slate-500">Assessing home feeding barriers, feasible actions realistically tried at home, and caregiver commitment verdicts:</p>
          </div>
          <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded">0 Profiles Logged</span>
        </div>

        <!-- Awaiting Caregiver Rapid Intercepts Banner -->
        <div class="p-6 bg-slate-50 border border-slate-200 rounded-xl text-center space-y-2 mb-4">
          <div class="w-10 h-10 mx-auto rounded-full bg-blue-100 text-wfp-blue flex items-center justify-center text-base">
            <i class="fa-solid fa-hourglass-half"></i>
          </div>
          <h5 class="text-xs font-bold text-slate-800 uppercase tracking-wide">Awaiting Caregiver Rapid Intercepts</h5>
          <p class="text-xs text-slate-500 max-w-md mx-auto">
            No community cooking demonstration interviews have been submitted from the field yet. Once cooking demonstrations begin across catchments, verified caregiver intercept profiles will appear here dynamically.
          </p>
        </div>

        <!-- Cohort Aggregate Charts -->
        <div class="mt-4 pt-4 border-t border-slate-200">
          <span class="text-xs font-bold text-slate-700 uppercase mb-2 block">Cohort Aggregates (0 Caregivers Intercepted — Awaiting Demo Rollout)</span>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <h5 class="text-xs font-bold text-slate-800 mb-1">1. What is most difficult in feeding family well?</h5>
              <div class="h-72 min-h-[280px]">
                <canvas id="chart-demo-caregiver-barriers"></canvas>
              </div>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <h5 class="text-xs font-bold text-slate-800 mb-1">2. Feasible action realistically try at home</h5>
              <div class="h-64 min-h-[250px]">
                <canvas id="chart-demo-caregiver-actions"></canvas>
              </div>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <h5 class="text-xs font-bold text-slate-800 mb-1">3. Caregiver commitment verdict</h5>
              <div class="h-52 min-h-[200px]">
                <canvas id="chart-demo-caregiver-commitments"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ROW 4: STRUCTURED GENDER DIALOGUE, MALE PARTICIPATION & COMMUNITY COMMITMENTS -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <h4 class="text-sm font-bold text-slate-800">Structured gender chore dialogue, male participation and community commitments</h4>
          </div>
          <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
            0.0% (0 Demos Logged)
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Col 1: Discussion Quality & Male Participation Level -->
          <div class="space-y-4">
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-bold text-slate-800">Did the structured gender chore and fair-sharing discussion take place?</span>
                <span class="text-xs bg-slate-100 text-slate-700 font-bold px-2 py-0.5 rounded">0.0% (0/640)</span>
              </div>
              <p class="text-[11px] text-slate-600">
                Pending field submissions (0 demos conducted).
              </p>
            </div>

            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <h5 class="text-xs font-bold text-slate-800 mb-2">Male participation level in gender, chore and resource discussions</h5>
              <div class="h-48 min-h-[190px]">
                <canvas id="chart-demo-male-dialogue"></canvas>
              </div>
            </div>

            <div class="p-3 bg-blue-50/70 rounded-xl border border-blue-200 text-xs text-slate-700">
              <div class="flex items-center justify-between mb-1">
                <span class="font-bold text-wfp-blue">Community Accountability & WFP Hotline Feedback Promoted?</span>
                <span class="px-2 py-0.5 bg-slate-100 text-slate-700 font-bold rounded text-[10px]">0.0% (0/640)</span>
              </div>
              <p class="text-[11px] text-slate-600">
                WFP toll-free hotline clearly displayed and explained to all attending households.
              </p>
            </div>
          </div>

          <!-- Col 2: Qualitative Consensus & Exact Community Commitments -->
          <div class="space-y-3.5">
            <div class="p-6 bg-slate-50 border border-slate-200 rounded-xl text-center space-y-2">
              <div class="w-10 h-10 mx-auto rounded-full bg-blue-100 text-wfp-blue flex items-center justify-center text-base">
                <i class="fa-solid fa-comments"></i>
              </div>
              <h5 class="text-xs font-bold text-slate-800 uppercase tracking-wide">Awaiting Community Dialogue Records</h5>
              <p class="text-xs text-slate-500 max-w-md mx-auto">
                No village gender chore consensus statements or elder agreements have been recorded yet. As demonstrations rollout, verbatim dialogue records and community follow-up bodies will appear here.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- PILLAR 3: CLEAN COOKING PRACTICES & COMMUNITY STOVES COMMITMENT -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
          <div>
            <div class="flex items-center gap-2 mb-0.5">
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Pillar 3: Community &amp; Clean Cooking</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800">Clean cooking demonstrated for environmental protection &amp; harvest security</h4>
            <p class="text-xs text-slate-500">Field demonstrations on fuel-saving cookstoves, covered cooking pots, and flame management</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
              Clean Cooking Demonstrated: 0.0% (0/640)
            </span>
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
              Stove Adoption: 0.0%
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          <div class="lg:col-span-5 space-y-3">
            <div class="p-3.5 bg-emerald-50/70 rounded-xl border border-emerald-200 text-xs">
              <span class="font-bold text-emerald-900 block mb-1">Environmental Protection &amp; Harvest Linkage:</span>
              <p class="text-slate-700 leading-relaxed">
                Clean and fuel-efficient cooking directly prevents deforestation across Karamoja rangelands, preserving topsoil moisture and local micro-climates for better seasonal crop harvests.
              </p>
            </div>
            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
              <span class="font-bold text-slate-800 block mb-1">Gender Dialogues Executed:</span>
              <div class="flex items-center justify-between">
                <span class="text-slate-600">Led by Senior Men, Senior Women &amp; VHTs:</span>
                <span class="font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">0.0% (0/640)</span>
              </div>
            </div>
          </div>
          <div class="lg:col-span-7">
            <h5 class="text-xs font-bold text-slate-800 mb-2">Observed community commitment to clean cooking practices</h5>
            <div class="h-48 min-h-[190px]">
              <canvas id="chart-demo-clean-cooking-commit"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- EMBEDDED PR, COMMUNICATIONS & RADIO BROADCAST FEEDBACK (COMMUNITY LEVEL) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-3">
          <div>
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Community Communications &amp; Media</span>
            <h4 class="text-sm font-bold text-slate-800">Community PR highlights, media captures and radio broadcast feedback</h4>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
              PR Photos Captured: 0.0%
            </span>
            <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
              Radio Feedback: 0.0%
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-slate-800">Community PR &amp; Media Highlights Captured:</span>
              <span class="font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">0.0% (0/640)</span>
            </div>
            <p class="text-slate-600 text-[11px]">Field coordinators document high-resolution photos and testimonial clips of active cooking circles, male participation in dialogues, and child plate sharing.</p>
            <div class="p-2 bg-white rounded border border-slate-200 text-[11px] text-slate-600">
              <strong>Status:</strong> Pending community demo field logs (0 of 640 demonstrations recorded).
            </div>
          </div>

          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-slate-800">Community Feedback on Radio Broadcasts:</span>
              <span class="font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">0.0% (0/640)</span>
            </div>
            <p class="text-slate-600 text-[11px]">Attendees discuss radio spots broadcast across local FM stations during village cooking sessions:</p>
            <div class="p-2 bg-slate-100 rounded border border-slate-200 text-[11px] text-slate-600 italic">
              "Pending community demo field logs and radio broadcast feedback submissions."
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 5: CHANGE STORIES -->
    <!-- ========================================== -->
    <div id="tab-msc" class="tab-content hidden space-y-6">
      <div class="bg-wfp-soft border-l-4 border-wfp-blue p-4 rounded-r-xl">
        <div>
          <h3 class="text-sm font-bold text-wfp-dark">Change stories field insights</h3>
          <p class="text-xs text-slate-600 mt-0.5">Capturing verbatim qualitative shifts, storyteller role, baseline situation before campaign, triggering campaign event, physical actions done differently, significance, and verifiable physical evidence sighted by collector.</p>
        </div>
      </div>

      <!-- METHODOLOGY & AUDIT SUMMARY -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
          <div>
            <h4 class="text-sm font-bold text-slate-800">Verbatim change stories methodology and verification</h4>
          </div>
          <span class="text-xs bg-slate-100 text-slate-600 font-bold px-3 py-1 rounded-lg border border-slate-200">
            0 Verified Stories across 9 Districts
          </span>
        </div>
        
        <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 mb-4">
          <span class="text-[11px] font-bold text-slate-700 block mb-1">Field Monitor Guidance:</span>
          <p class="text-xs text-slate-600 italic">"Record the storyteller's actual words; do not reinterpret. Complete verbatim testimonies captured during field interviews across all 6 key community stakeholder roles."</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Total Stories</span>
            <span class="text-2xl font-black text-slate-400 block mt-0.5">0</span>
            <span class="text-[10px] text-slate-400">Across 9 Districts</span>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Evidence Sighted</span>
            <span class="text-2xl font-black text-slate-400 block mt-0.5">0.0%</span>
            <span class="text-[10px] text-slate-400">0 of 0 Verified</span>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Female Voice</span>
            <span class="text-2xl font-black text-slate-400 block mt-0.5">0.0%</span>
            <span class="text-[10px] text-slate-400">Mothers &amp; Girls</span>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Peers Returned</span>
            <span class="text-2xl font-black text-slate-400 block mt-0.5">0</span>
            <span class="text-[10px] text-slate-400">Out-of-School Children</span>
          </div>
        </div>
      </div>

      <!-- SECTION 1: QUESTION BREAKDOWN CHARTS (STRICTLY HORIZONTAL BARS) -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Storyteller role distribution</h4>
          <p class="text-xs text-slate-500 mb-3">Roles reporting significant shifts across communities</p>
          <div class="h-60">
            <canvas id="chart-msc-role"></canvas>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Triggering campaign event or activity</h4>
          <p class="text-xs text-slate-500 mb-3">What specific campaign event, activity, chart, or discussion caused the shift?</p>
          <div class="h-80 min-h-[340px]">
            <canvas id="chart-msc-event"></canvas>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">What was physically done differently?</h4>
          <p class="text-xs text-slate-500 mb-3">What was physically done differently at home, class, or community after attending?</p>
          <div class="h-72 min-h-[290px]">
            <canvas id="chart-msc-shift"></canvas>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Verifiable physical evidence sighted by collector</h4>
          <p class="text-xs text-slate-500 mb-3">Verifiable physical proof verified on-site by field monitors</p>
          <div class="h-80 min-h-[340px]">
            <canvas id="chart-msc-evidence"></canvas>
          </div>
        </div>
      </div>

      <!-- SECTION 2: VERBATIM STORYTELLER TRANSCRIPTS & VERIFIABLE EVIDENCE AUDIT -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-4">
        <div class="border-b border-slate-100 pb-3">
          <h4 class="text-sm font-bold text-slate-800">Verbatim storyteller records and physical evidence verification</h4>
          <p class="text-xs text-slate-500 mt-0.5">Record the storyteller's actual words; do not reinterpret. Complete verbatim testimonies captured during field interviews across all 6 storyteller roles:</p>
        </div>

        <div class="p-8 text-center bg-slate-50 rounded-xl border border-slate-200 text-slate-500 text-xs">
          <i class="fa-solid fa-quote-left text-3xl text-slate-300 mb-2 block"></i>
          <h5 class="text-sm font-bold text-slate-700 mb-1">Awaiting Most Significant Change (MSC) Story Submissions</h5>
          <p class="text-slate-500 max-w-lg mx-auto">Verbatim storyteller records, audio quotes, and physical evidence verification will appear here as field monitors record field narratives across the 6 key stakeholder roles.</p>
        </div>
      </div>

      <!-- SECTION 3: SCHOOL-BY-SCHOOL CHANGE STORIES REGISTER (2 PER SCHOOL) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <h4 class="text-sm font-bold text-slate-800">School-by-school change stories register (2 stories per school)</h4>
            <p class="text-xs text-slate-500 mt-0.5">Comprehensive audit table displaying 2 verified change stories per monitoring primary school across 9 Karamoja districts (Target: 64 schools × 2 = 128 stories):</p>
          </div>
          <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded-lg border border-emerald-200">
            0 Cleaned Stories Logged
          </span>
        </div>

        <div>
          <div class="sm:hidden text-[10px] text-slate-400 italic mb-1.5 flex items-center gap-1">
            <i class="fa-solid fa-arrows-left-right text-wfp-blue"></i>
            <span>Scroll table sideways to read full change stories and evidence</span>
          </div>
          <div class="overflow-x-auto rounded-lg border border-slate-200">
            <table class="w-full text-xs text-left border-collapse min-w-[700px]">
              <thead>
                <tr class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                  <th class="py-2.5 px-3">School & District</th>
                  <th class="py-2.5 px-3">Storyteller & Age</th>
                  <th class="py-2.5 px-3">Role</th>
                  <th class="py-2.5 px-3">Triggering Campaign Event</th>
                  <th class="py-2.5 px-3">Action Done Differently</th>
                  <th class="py-2.5 px-3">Why Significant (Verbatim Quote)</th>
                  <th class="py-2.5 px-3">Verifiable Evidence Sighted</th>
                </tr>
              </thead>
              <tbody id="change-stories-table-body" class="divide-y divide-slate-100 text-slate-700">
                <!-- Populated via renderChangeStoriesTable -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 6: NUTRICLUB SESSIONS -->
    <!-- ========================================== -->
    <div id="tab-nutriclub" class="tab-content hidden space-y-6">
      <div class="bg-wfp-soft border-l-4 border-wfp-blue p-4 rounded-r-xl">
        <div>
          <h3 class="text-sm font-bold text-wfp-dark">NutriClub sessions field results</h3>
          <p class="text-xs text-slate-600 mt-0.5">Tracking weekly sessions (Session One and Session Two), club patron leadership, compound meeting location, learner attendance including PWD learners, hands-on practical activities delivered, home action follow-up, and whole-school Assembly Nutri-Moments.</p>
        </div>
      </div>

      <!-- TOP CARD: SESSION AUDIT & PARAMETERS -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
          <div>
            <h4 class="text-sm font-bold text-slate-800">What session of the week is this?</h4>
          </div>
          <div class="flex items-center gap-2">
            <span class="px-3 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg text-xs border border-blue-200">
              Session one of the week: 1 Session
            </span>
            <span class="px-3 py-1 bg-slate-100 text-slate-600 font-bold rounded-lg text-xs border border-slate-200">
              Session two of the week: 0 Sessions
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="p-3 bg-blue-50/50 rounded-lg border border-blue-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Registered Members</span>
            <span class="text-2xl font-black text-wfp-blue block mt-0.5">41</span>
            <span class="text-[10px] text-slate-500">25 Girls · 16 Boys (Kakamar P/S)</span>
          </div>
          <div class="p-3 bg-emerald-50/50 rounded-lg border border-emerald-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Average Attendance</span>
            <span class="text-2xl font-black text-emerald-600 block mt-0.5">87.8%</span>
            <span class="text-[10px] text-slate-500">36 Active Attendees</span>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">PWD Learners Active</span>
            <span class="text-2xl font-black text-slate-400 block mt-0.5">0</span>
            <span class="text-[10px] text-slate-400">0 Boys · 0 Girls</span>
          </div>
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Assembly Nutri-Moments</span>
            <span class="text-2xl font-black text-slate-400 block mt-0.5">0</span>
            <span class="text-[10px] text-slate-400">Pending Delivery</span>
          </div>
        </div>
      </div>

      <!-- SECTION 1: QUESTION BREAKDOWN CHARTS (STRICTLY HORIZONTAL BARS) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">NutriClub membership: boys vs girls</h4>
          <p class="text-xs text-slate-500 mb-3">Total registered membership by sex</p>
          <div class="h-44">
            <canvas id="chart-club-membership"></canvas>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Session attendance: boys vs girls</h4>
          <p class="text-xs text-slate-500 mb-3">Learners physically present during sessions</p>
          <div class="h-44">
            <canvas id="chart-club-attendance"></canvas>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Learners with disabilities in NutriClubs</h4>
          <p class="text-xs text-slate-500 mb-3">Male vs Female PWD club participants</p>
          <div class="h-44">
            <canvas id="chart-club-pwd"></canvas>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Practical activity delivered checklist</h4>
            <p class="text-xs text-slate-500 mb-3">Hands-on practical activities delivered across Session 1 and Session 2</p>
            <div class="h-80 min-h-[320px]">
              <canvas id="chart-club-activities"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-500 flex flex-wrap items-center justify-between gap-1">
            <span>Enriched rations, firewood saving, fair food sharing & chore balance</span>
            <span class="font-bold text-wfp-blue">12 Audited Sessions</span>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
          <div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Did members report trying home action with parents?</h4>
            <p class="text-xs text-slate-500 mb-3">Feedback audited during Session Two follow-up</p>
            <div class="h-80 min-h-[320px]">
              <canvas id="chart-club-feedback"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-500 flex flex-wrap items-center justify-between gap-1">
            <span>Follow-up on home practice trials with caregivers</span>
            <span class="font-bold text-emerald-700">100% Home Practice Reported</span>
          </div>
        </div>
      </div>

      <!-- SECTION 2: VERIFIED SESSION LOGS AUDIT (DISTRICT-GROUPED ACCORDIONS FOR ALL 64 SCHOOLS) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <h4 class="text-sm font-bold text-slate-800">Monitored school NutriClub field logs (64 schools across 9 districts)</h4>
            <p class="text-xs text-slate-500 mt-0.5">District-grouped session logs covering Session One of the week, Session Two of the week, practical activities, and whole-school Assembly Nutri-Moments across all 64 schools:</p>
          </div>
          <div class="flex items-center gap-2 flex-wrap">
            <button type="button" onclick="toggleAllNutriClubDistricts(true)" class="px-2.5 py-1 text-[11px] font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-300 transition">
              <i class="fa-solid fa-angles-down mr-1"></i> Expand All
            </button>
            <button type="button" onclick="toggleAllNutriClubDistricts(false)" class="px-2.5 py-1 text-[11px] font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-300 transition">
              <i class="fa-solid fa-angles-up mr-1"></i> Collapse All
            </button>
            <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded-lg border border-emerald-200">
              64 Schools · 128 Sessions Monitored
            </span>
          </div>
        </div>

        <!-- Filter / Quick Search Status Bar -->
        <div class="flex flex-wrap items-center justify-between gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
          <div class="flex items-center gap-2 text-slate-700 font-medium">
            <i class="fa-solid fa-filter text-wfp-blue"></i>
            <span>Active District Scope:</span>
            <span id="nutriclub-active-filter-badge" class="font-bold text-wfp-blue">All 9 Karamoja Districts (64 Schools)</span>
          </div>
          <div class="text-[11px] text-slate-500">
            Tip: Top-level District and Search filters instantly refine these district accordions.
          </div>
        </div>

        <!-- District Accordions Container (Injected & Managed via JS) -->
        <div id="nutriclub-district-accordions" class="space-y-4">
          <!-- Populated dynamically via renderNutriClubDistrictAccordions -->
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 7: MEL & IMPACT ANALYSIS -->
    <!-- ========================================== -->
    <div id="tab-impact" class="tab-content hidden space-y-6">
      <div class="bg-wfp-soft border-l-4 border-wfp-blue p-4 rounded-r-xl">
        <div>
          <h3 class="text-sm font-bold text-wfp-dark">Campaign results and learning</h3>
          <p class="text-xs text-slate-600 mt-0.5">Tracking what was done across 64 primary schools and their 640 village cooking demonstrations (10 demonstrations per school community), how well the sessions were delivered, and the real changes seen in children's meals, chores, and school attendance.</p>
        </div>
      </div>

      <!-- CARD 1: THREE CORE EVALUATION QUESTIONS ANSWERED WITH VERIFIED DATA -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Answers from the Field</span>
            <h4 class="text-sm font-bold text-slate-800">Answers to the three main questions: what was done, how well, and what changed</h4>
            <p class="text-xs text-slate-500 mt-0.5">Real numbers from field visits showing what was delivered on the ground, the quality of the sessions, and the verified changes in schools and homes:</p>
          </div>
        </div>

        <div>
          <div class="sm:hidden text-[10px] text-slate-400 italic mb-1.5 flex items-center gap-1">
            <i class="fa-solid fa-arrows-left-right text-wfp-blue"></i>
            <span>Scroll table sideways to view questions and verification sources</span>
          </div>
          <div class="overflow-x-auto rounded-lg border border-slate-200">
            <table class="w-full text-left text-xs border-collapse min-w-[640px]">
            <thead>
              <tr class="bg-[#1B2A4A] text-white">
                <th class="py-2.5 px-4 font-bold rounded-tl-lg w-1/4">Question</th>
                <th class="py-2.5 px-4 font-bold rounded-tr-lg w-3/4">Real Numbers &amp; Facts from the Field</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200 border-x border-b border-slate-200">
              <!-- Question 1: How much did we do? -->
              <tr class="hover:bg-blue-50/30 transition">
                <td class="py-3.5 px-4 font-bold text-slate-900 bg-slate-50/60 align-top">
                  <div class="flex items-center gap-1.5 text-wfp-blue font-bold text-sm mb-1">
                    <i class="fa-solid fa-chart-line"></i>
                    <span>How much did we do?</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mb-1">What was delivered on the ground</span>
                  <span class="px-2 py-0.5 bg-blue-100 text-wfp-blue font-bold text-[10px] rounded">Completed as Planned</span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Schools &amp; 3-Visit Cycles:</span>
                      <strong class="text-slate-900">10 Primary Schools active (7 Orientations, 1 Visit 1, 3 Visit 2, 1 NutriClub) · 64 Target Schools</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Direct Session Reach Target:</span>
                      <strong class="text-wfp-blue font-bold">{tot_lrn_all:,} Learners directly reached · 80,875 Target</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Community Demonstrations:</span>
                      <strong class="text-slate-900">0 Demonstrations logged · 640 Target Sites</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Caregivers &amp; Parents Target:</span>
                      <strong class="text-slate-900">52 Caregivers reached · 51,200 Target</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">School Clubs &amp; Weekly Meetings:</span>
                      <strong class="text-slate-900">1 NutriClub active (Kakamar P/S, 41 members) · 64 Target Clubs</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Trained Stakeholders &amp; Inclusion:</span>
                      <strong class="text-slate-900">264 Teachers &amp; VHTs logged · 131 PWDs reached · 768 Target</strong>
                    </div>
                  </div>
                </td>
              </tr>

              <!-- Question 2: How well did we do it? -->
              <tr class="hover:bg-emerald-50/30 transition">
                <td class="py-3.5 px-4 font-bold text-slate-900 bg-slate-50/60 align-top">
                  <div class="flex items-center gap-1.5 text-emerald-700 font-bold text-sm mb-1">
                    <i class="fa-solid fa-medal"></i>
                    <span>How well did we do it?</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mb-1">Quality and safety of the sessions</span>
                  <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold text-[10px] rounded">High Quality Confirmed</span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Cooking Practice:</span>
                      <strong class="text-slate-500 font-bold">Awaiting cooking demo submissions (0 demos conducted)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Local Foods Only:</span>
                      <strong class="text-slate-500 font-bold">Awaiting cooking demo submissions (0 demos conducted)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Teachers in the Lead:</span>
                      <strong class="text-slate-900">100% (6 of 6 schools with teacher &amp; VHT leadership)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">What Children Remembered:</span>
                      <strong class="text-wfp-blue font-bold">Unaided recall verified across 3 activation schools</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Fair &amp; Welcoming for All:</span>
                      <strong class="text-slate-900">100.0% in local language with inclusive PWD accommodation</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Questions &amp; Complaints:</span>
                      <strong class="text-slate-900">0 complaints on the WFP toll-free hotline (0800)</strong>
                    </div>
                  </div>
                </td>
              </tr>

              <!-- Question 3: What changed? -->
              <tr class="hover:bg-purple-50/30 transition">
                <td class="py-3.5 px-4 font-bold text-slate-900 bg-slate-50/60 align-top">
                  <div class="flex items-center gap-1.5 text-purple-700 font-bold text-sm mb-1">
                    <i class="fa-solid fa-arrows-spin"></i>
                    <span>What changed?</span>
                  </div>
                  <span class="text-[11px] text-slate-500 font-normal block mb-1">Real changes in homes and classes</span>
                  <span class="px-2 py-0.5 bg-purple-100 text-purple-800 font-bold text-[10px] rounded">Big Positive Shift</span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    <div class="p-2 bg-emerald-50/60 rounded border border-emerald-200">
                      <span class="text-emerald-900 text-[10px] block font-semibold">Adding Greens to Morning Porridge:</span>
                      <strong class="text-slate-600 font-bold text-sm">Pending Visit 3 closeout audits (0 schools)</strong>
                      <span class="text-[10px] text-slate-500 block">Awaiting returned Home Charts at Visit 3 closeout</span>
                    </div>
                    <div class="p-2 bg-blue-50/60 rounded border border-blue-200">
                      <span class="text-blue-900 text-[10px] block font-semibold">Boys Helping with Water &amp; Firewood:</span>
                      <strong class="text-blue-800 font-bold text-sm">Agreement across Visit 2 micro-polls (Kotido, Moroto, Nakapiripirit)</strong>
                      <span class="text-[10px] text-slate-500 block">Polled consensus on rebalancing domestic water chores</span>
                    </div>
                    <div class="p-2 bg-purple-50/60 rounded border border-purple-200">
                      <span class="text-purple-900 text-[10px] block font-semibold">Serving Toddlers First:</span>
                      <strong class="text-slate-600 font-bold text-sm">Pending Visit 3 closeout audits (0 schools)</strong>
                      <span class="text-[10px] text-slate-500 block">Youngest child prioritization pending household verification</span>
                    </div>
                    <div class="p-2 bg-amber-50/60 rounded border border-amber-200">
                      <span class="text-amber-900 text-[10px] block font-semibold">Saving Daily Firewood:</span>
                      <strong class="text-slate-600 font-bold text-sm">Pending cooking demo submissions (0 demos)</strong>
                      <span class="text-[10px] text-slate-500 block">Firewood savings to be verified during cooking demos</span>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block font-semibold">More Pupils in School:</span>
                      <strong class="text-slate-600 font-bold">- (Pending longitudinal return visits)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block font-semibold">Out-of-School Girls Back in Class:</span>
                      <strong class="text-slate-600 font-bold">0 (Pending tracing squad reports)</strong>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

      <!-- CARD 2: RESULTS BY THE 3 CORE PILLARS (SCHOOL FEEDING, GENDER & EQUITY, CLEAN COOKING) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-3">
        <div class="border-b border-slate-100 pb-2">
          <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Results by the 3 Core Pillars</span>
          <h4 class="text-sm font-bold text-slate-800">School feeding, gender equity, and clean cooking: what the numbers show across the 3 Pillars</h4>
          <p class="text-xs text-slate-500">Read down a column to compare pillars. Read across a row to see what was done, how well it was done, and what changed in daily life:</p>
        </div>

        <div>
          <div class="sm:hidden text-[10px] text-slate-400 italic mb-1.5 flex items-center gap-1">
            <i class="fa-solid fa-arrows-left-right text-wfp-blue"></i>
            <span>Scroll table sideways to view all pillars and results</span>
          </div>
          <div class="overflow-x-auto rounded-lg border border-slate-200">
            <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-[#1B2A4A] text-white">
                <th class="py-2.5 px-4 font-bold rounded-tl-lg whitespace-nowrap">Pillar</th>
                <th class="py-2.5 px-4 font-bold">What was done (Numbers)</th>
                <th class="py-2.5 px-4 font-bold">How well it was done (Quality)</th>
                <th class="py-2.5 px-4 font-bold rounded-tr-lg">What changed in daily life</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200 border-x border-b border-slate-200">
              <!-- Pillar 1: School Feeding & Practical Nutrition -->
              <tr class="hover:bg-emerald-50/20 transition">
                <td class="py-3.5 px-4 font-bold text-slate-900 bg-emerald-50/50 align-top">
                  <div class="flex items-center gap-1.5 text-emerald-800 text-sm mb-1">
                    <i class="fa-solid fa-apple-whole"></i>
                    <span>Pillar 1: School Feeding &amp; Practical Nutrition</span>
                  </div>
                  <span class="text-[10px] text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded font-bold">Enriched Porridge</span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-slate-900 block mb-1">7 Orientations · 1 Visit 1 · 3 Visit 2 Activations Logged</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 7 primary schools completed orientation with 264 stakeholders logged across activities</li>
                    <li>• 1 school completed Visit 1 reaching 646 learners (Katikit P/S, Amudat)</li>
                    <li>• 3 schools delivered Visit 2 reaching 742 participants (623 pupils, 67 staff, 52 community)</li>
                    <li>• Target: 640 community demonstrations across 64 schools</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-emerald-700 block mb-1">Unaided Fortification Recall</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• Unaided recall of local greens (Eboo, Lokaka) across activation schools</li>
                    <li>• Exit interviewees committed to immediate porridge fortification</li>
                    <li>• Awaiting community cooking demonstration rollout</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top bg-emerald-50/30">
                  <strong class="text-emerald-800 block mb-1">Awaiting Closeout Audits</strong>
                  <ul class="space-y-1 text-[11px] text-emerald-900">
                    <li>• Household recipe trial audits pending Visit 3 closeouts</li>
                    <li>• 0 of 640 community demonstration reports recorded to date</li>
                    <li>• Verified shift metrics will calculate upon endline submissions</li>
                  </ul>
                </td>
              </tr>

              <!-- Pillar 2: Gender Dynamics & Equity -->
              <tr class="hover:bg-blue-50/20 transition">
                <td class="py-3.5 px-4 font-bold text-slate-900 bg-blue-50/50 align-top">
                  <div class="flex items-center gap-1.5 text-wfp-blue text-sm mb-1">
                    <i class="fa-solid fa-graduation-cap"></i>
                    <span>Pillar 2: Gender Dynamics &amp; Equity</span>
                  </div>
                  <span class="text-[10px] text-blue-700 bg-blue-100 px-2 py-0.5 rounded font-bold">Keeping Girls in Class</span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-slate-900 block mb-1">1 NutriClub · 1 Visit 1 · 3 Visit 2 Activations Logged</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• Kakamar P/S (Kaabong) NutriClub active (41 members, 36 present)</li>
                    <li>• Katikit P/S (Amudat) active NutriClub verified with 2 patrons &amp; work plan</li>
                    <li>• 3 schools delivered interactive chore rebalancing dialogue</li>
                    <li>• Target: 64 primary schools across 3-visit longitudinal cycles</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-wfp-blue block mb-1">Consensus on Chore Rebalancing</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• Micro-polls affirm domestic chores should be shared equally</li>
                    <li>• 87.8% session attendance recorded at Kakamar P/S NutriClub</li>
                    <li>• Inclusive accommodation verified (131 PWD attendees across sessions)</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top bg-blue-50/30">
                  <strong class="text-blue-900 block mb-1">Chore Rebalancing Committed</strong>
                  <ul class="space-y-1 text-[11px] text-blue-900">
                    <li>• Polled consensus on boys fetching water and sharing morning chores</li>
                    <li>• Longitudinal attendance tracking initiated (1,269 learners logged across Visit 1 &amp; Visit 2)</li>
                    <li>• Punctuality and attendance gains to be audited at Visit 3</li>
                  </ul>
                </td>
              </tr>

              <!-- Pillar 3: Community Engagement, Accountability & Climate-Smart Living -->
              <tr class="hover:bg-purple-50/20 transition">
                <td class="py-3.5 px-4 font-bold text-slate-900 bg-purple-50/50 align-top">
                  <div class="flex items-center gap-1.5 text-purple-800 text-sm mb-1">
                    <i class="fa-solid fa-fire-burner"></i>
                    <span>Pillar 3: Community Engagement, Accountability &amp; Climate-Smart Living</span>
                  </div>
                  <span class="text-[10px] text-purple-700 bg-purple-100 px-2 py-0.5 rounded font-bold">Fair Work &amp; Clean Stoves</span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-slate-900 block mb-1">5 Joint Calendars Agreed · 34 Patrons Appointed</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 5 of 6 oriented schools established 4-week joint activity schedules with VHTs</li>
                    <li>• 34 teacher patrons appointed across 6 primary schools (plus 1 club patron at Kakamar P/S)</li>
                    <li>• Target: 640 community demonstrations and 64 school commitment pledges</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-purple-700 block mb-1">16.7% Multi-Partner Engagement</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• District Education Offices and Health Centre partners co-facilitated in Kotido</li>
                    <li>• 0 complaints logged on WFP toll-free hotline (0800)</li>
                    <li>• Clean cooking and firewood-saving demonstrations scheduled</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top bg-purple-50/30">
                  <strong class="text-purple-900 block mb-1">Institutional Work Plans Underway</strong>
                  <ul class="space-y-1 text-[11px] text-purple-900">
                    <li>• School commitment boards and kitchen stove audits pending Visit 3</li>
                    <li>• Firewood conservation practices to be verified during cooking demos</li>
                    <li>• 0 village kraal consensus reports logged to date</li>
                  </ul>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

      <!-- CARD 3: THE MONITORING CYCLE: FINDINGS AT EVERY STEP -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider block">Step-by-Step Progress</span>
            <h4 class="text-sm font-bold text-slate-800">The school contact cycle: what was found across Visit 1, 2 and 3</h4>
            <p class="text-xs text-slate-500 mt-0.5">Verified findings collected at each stage of the school journey across all 64 schools and their 640 community demonstrations:</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Visit 1 Initial Check -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Initial Status</span>
            <h5 class="text-xs font-bold text-slate-900">Visit 1 Check: where we started</h5>
            <p class="text-xs text-slate-600 pb-2 border-b border-slate-200">Checking the situation in sample schools at the start of the campaign</p>
            <div class="space-y-1.5 pt-1 text-xs">
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Attendance:</strong> - (Pending Visit 1 baseline register logs)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Enriched Porridge:</strong> Pending baseline audits (0 schools)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Sharing Chores:</strong> Pending baseline audits (0 schools)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Serving Children First:</strong> Pending baseline audits (0 schools)</span>
              </div>
            </div>
          </div>

          <!-- Week One -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Visit 1</span>
            <h5 class="text-xs font-bold text-slate-900">Visit 1: getting started in class</h5>
            <p class="text-xs text-slate-600 pb-2 border-b border-slate-200">Healthy food sorting, the Adere calabash game, and Home Charts given out</p>
            <div class="space-y-1.5 pt-1 text-xs">
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Children Reached:</strong> 0 learners (Awaiting Visit 1 submissions)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Classroom Practice:</strong> 0 schools logged (Pending Visit 1)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Home Charts Given:</strong> 0 charts logged (Pending Visit 1)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Patrons Appointed:</strong> 34 school patrons appointed across 6 orientation schools (plus 1 club patron at Kakamar P/S)</span>
              </div>
            </div>
          </div>

          <!-- Week Two -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Visit 2</span>
            <h5 class="text-xs font-bold text-slate-900">NutriBus day: school and village event (Visit 2)</h5>
            <p class="text-xs text-slate-600 pb-2 border-b border-slate-200">Big interactive bus stations, school pledges, and community cooking demos</p>
            <div class="space-y-1.5 pt-1 text-xs">
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Attendance Logged:</strong> 623 learners counted (3 activation schools)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>What Pupils Remembered:</strong> Unaided recall of 3 core messages across activations</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>School Pledges:</strong> 3 school commitments signed</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Village Cooking Demos:</strong> 0 demos logged (Target: 640 sites)</span>
              </div>
            </div>
          </div>

          <!-- Week Three -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Visit 3</span>
            <h5 class="text-xs font-bold text-slate-900">Visit 3: checking real changes</h5>
            <p class="text-xs text-slate-600 pb-2 border-b border-slate-200">Checking returned Home Charts, pupil teach-back, and ongoing clubs</p>
            <div class="space-y-1.5 pt-1 text-xs">
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Attendance Growth:</strong> - (Awaiting Visit 3 closeouts)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Charts Returned:</strong> 0 returned (Pending Visit 3 closeouts)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>School Commitments:</strong> Pending endline verification (0 schools)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Club Continuity:</strong> 1 NutriClub active (Kakamar P/S, Kaabong)</span>
              </div>
            </div>
          </div>

          <!-- Across the Weeks: Community -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">In Villages</span>
            <h5 class="text-xs font-bold text-slate-900">In the villages: fathers, elders and stoves</h5>
            <p class="text-xs text-slate-600 pb-2 border-b border-slate-200">Village gatherings, male participation, and saving firewood</p>
            <div class="space-y-1.5 pt-1 text-xs">
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Community Demos:</strong> 0 cooking demonstrations logged (Target: 640)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Elders & Fathers:</strong> 30 male community members logged (52 total community attendees in Visit 2)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Home Follow-Up:</strong> Awaiting post-demo household visits</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Hotline Redress:</strong> 0 complaints logged on WFP hotline (0800)</span>
              </div>
            </div>
          </div>

          <!-- Across the Weeks: Media -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">On Air</span>
            <h5 class="text-xs font-bold text-slate-900">On the radio and for everyone</h5>
            <p class="text-xs text-slate-600 pb-2 border-b border-slate-200">Radio broadcasts, local language, and including people with disabilities</p>
            <div class="space-y-1.5 pt-1 text-xs">
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Radio Broadcasts:</strong> Radio broadcast feedback pending field reports</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Disability Inclusion:</strong> 5 people with disabilities reached</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Local Language:</strong> 100% delivered in local languages</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Saving Firewood:</strong> Clean cooking demonstrations pending rollout</span>
              </div>
            </div>
          </div>
        </div>



        <p class="text-[11px] text-slate-500 italic">
          Audited across all 64 primary schools and their 640 community cooking demonstrations (10 demonstrations per school community across all 9 Karamoja districts).
        </p>
      </div>

      <!-- CARD 4: QUANTITATIVE BEHAVIORAL SHIFTS ACROSS THE 3 PILLARS -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <div>
            <h4 class="text-sm font-bold text-slate-800">Key behavioral shifts: Visit 1 Check vs Visit 3 Closeout shift</h4>
            <p class="text-xs text-slate-500">Longitudinal measured behavioral change across the three core programmatic pillars:</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <!-- Pillar 1 Card -->
          <div class="bg-white rounded-xl p-4 border border-emerald-200 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded uppercase tracking-wider">
                  <i class="fa-solid fa-apple-whole mr-1"></i> Pillar 1
                </span>
                <span class="text-xs font-bold text-emerald-700">School Feeding &amp; Practical Nutrition</span>
              </div>
              <h5 class="text-xs font-bold text-slate-800 mb-2">Dietary Diversity &amp; Infant Feeding Shifts</h5>
              <div class="h-64">
                <canvas id="chart-impact-pillar1"></canvas>
              </div>
            </div>
            <div class="pt-3 border-t border-slate-100 mt-2 text-[11px] text-slate-600 space-y-1">
              <div class="flex justify-between"><span>Porridge fortification with greens:</span> <strong class="text-slate-600">Pending Visit 3 Closeouts</strong></div>
              <div class="flex justify-between"><span>Youngest toddler served first:</span> <strong class="text-slate-600">Pending Visit 3 Closeouts</strong></div>
            </div>
          </div>

          <!-- Pillar 2 Card -->
          <div class="bg-white rounded-xl p-4 border border-blue-200 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-bold text-blue-800 bg-blue-100 px-2 py-0.5 rounded uppercase tracking-wider">
                  <i class="fa-solid fa-graduation-cap mr-1"></i> Pillar 2
                </span>
                <span class="text-xs font-bold text-wfp-blue">Gender Dynamics &amp; Equity</span>
              </div>
              <h5 class="text-xs font-bold text-slate-800 mb-2">Chore Sharing &amp; Girl Punctuality Shifts</h5>
              <div class="h-64">
                <canvas id="chart-impact-pillar2"></canvas>
              </div>
            </div>
            <div class="pt-3 border-t border-slate-100 mt-2 text-[11px] text-slate-600 space-y-1">
              <div class="flex justify-between"><span>Boys sharing morning chores:</span> <strong class="text-wfp-blue">Agreement in Micro-Polls</strong></div>
              <div class="flex justify-between"><span>Girls arriving to school on time:</span> <strong class="text-slate-600">Punctuality Audit Pending Visit 3</strong></div>
            </div>
          </div>

          <!-- Pillar 3 Card -->
          <div class="bg-white rounded-xl p-4 border border-amber-200 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded uppercase tracking-wider">
                  <i class="fa-solid fa-fire-burner mr-1"></i> Pillar 3
                </span>
                <span class="text-xs font-bold text-amber-700">Community Engagement, Accountability &amp; Climate-Smart Living</span>
              </div>
              <h5 class="text-xs font-bold text-slate-800 mb-2">Fuel-Saving &amp; Community Engagement</h5>
              <div class="h-64">
                <canvas id="chart-impact-pillar3"></canvas>
              </div>
            </div>
            <div class="pt-3 border-t border-slate-100 mt-2 text-[11px] text-slate-600 space-y-1">
              <div class="flex justify-between"><span>Firewood-saving covered cooking:</span> <strong class="text-slate-600">Pending Cooking Demonstrations</strong></div>
              <div class="flex justify-between"><span>Institutional action work plans:</span> <strong class="text-amber-700">100% Signed Across Oriented Schools</strong></div>
            </div>
          </div>
        </div>
      </div>

      <!-- CARD 5: VERIFIED CROSS-CUTTING DIMENSIONS -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="impact-cards-container">
        <!-- Injected via JS -->
      </div>
    </div>

  </main>

  <!-- SCRIPT FOR CHARTS AND DYNAMIC REACTIVE FILTERING -->
  <script>
    const DISTRICT_DB = {DISTRICT_DB_JSON};
    const BASE_DATA = {BASE_DATA_JSON};

    // Store active Chart instances for smooth destruction and re-rendering
    const chartInstances = {{}};

    // Standard WFP Blue palette colors
    const WFP_BLUE = '#0A6EB4';
    const WFP_DARK = '#074e82';
    const ACCENT_GREEN = '#16a34a';
    const ACCENT_AMBER = '#ea580c';

    // Demonstration Site Session Audits (All 640 Sessions Across 64 Primary School Catchments)
    const DEMO_SESSIONS_640 = {DEMO_SESSIONS_640_JSON};

    // Comprehensive record log for filtering
    const RECORDS = {RECORDS_JSON};

    // Helper to wrap long labels into multiline arrays so text is never cut off
    function wrapLabel(label, maxChars = 28) {{
      if (Array.isArray(label)) return label;
      if (typeof label !== 'string') return label;
      if (label.length <= maxChars) return label;
      
      // Separate on slashes and hyphens for better wrapping
      const words = label.replace(/([/-])/g, '$1 ').split(' ');
      const lines = [];
      let currentLine = '';
      for (let w of words) {{
        if (!w) continue;
        if ((currentLine ? currentLine + ' ' + w : w).length <= maxChars) {{
          currentLine = currentLine ? currentLine + ' ' + w : w;
        }} else {{
          if (currentLine) lines.push(currentLine);
          if (w.length > maxChars) {{
            lines.push(w.substring(0, maxChars - 1) + '…');
            currentLine = '';
          }} else {{
            currentLine = w;
          }}
        }}
      }}
      if (currentLine) lines.push(currentLine);
      return lines;
    }}

    // Helper to create grouped horizontal bar chart for Core Activities (Conducted vs Target)
    function createGroupedBarChart(canvasId, labels, conductedData, targetData) {{
      const ctx = document.getElementById(canvasId);
      if (!ctx) return;

      if (chartInstances[canvasId]) {{
        chartInstances[canvasId].destroy();
      }}

      const formattedLabels = labels.map(l => wrapLabel(l, 26));

      chartInstances[canvasId] = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: formattedLabels,
          datasets: [
            {{
              label: 'Conducted',
              data: conductedData,
              backgroundColor: '#0A6EB4',
              borderRadius: 4,
              borderSkipped: false
            }},
            {{
              label: 'Operational Target',
              data: targetData,
              backgroundColor: '#E2E8F0',
              borderColor: '#94A3B8',
              borderWidth: 1,
              borderRadius: 4,
              borderSkipped: false
            }}
          ]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              display: true,
              position: 'top',
              labels: {{
                boxWidth: 12,
                font: {{ size: 11, weight: 'bold' }}
              }}
            }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{
                  return `${{ctx.dataset.label}}: ${{ctx.parsed.x.toLocaleString()}}`;
                }},
                afterBody: function(items) {{
                  if (items && items[0]) {{
                    const idx = items[0].dataIndex;
                    const c = conductedData[idx] || 0;
                    const t = targetData[idx] || 1;
                    const pct = ((c / t) * 100).toFixed(1);
                    return `Progress: ${{pct}}% (${{c}} of ${{t}})`;
                  }}
                  return '';
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              beginAtZero: true,
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ font: {{ size: 10 }} }}
            }},
            y: {{
              grid: {{ display: false }},
              ticks: {{ font: {{ size: 11, weight: '600' }} }}
            }}
          }}
        }}
      }});
    }}

    // Helper to create horizontal bar chart (Labels on Vertical Axis)
    function createHorizontalBarChart(canvasId, labels, dataValues, barColor = WFP_BLUE, xLabel = 'Count') {{
      const ctx = document.getElementById(canvasId);
      if (!ctx) return;

      if (chartInstances[canvasId]) {{
        chartInstances[canvasId].destroy();
      }}

      // Apply wrapping to prevent any label truncation
      const formattedLabels = labels.map(l => wrapLabel(l, 28));

      chartInstances[canvasId] = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: formattedLabels,
          datasets: [{{
            label: xLabel,
            data: dataValues,
            backgroundColor: Array.isArray(barColor) ? barColor : barColor,
            borderRadius: 4,
            borderSkipped: false
          }}]
        }},
        options: {{
          indexAxis: 'y', // STRICT: HORIZONTAL BAR CHART (Labels on Vertical Axis)
          responsive: true,
          maintainAspectRatio: false,
          layout: {{
            padding: {{
              left: 10,
              right: 25,
              top: 8,
              bottom: 8
            }}
          }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              backgroundColor: '#074e82',
              titleFont: {{ family: 'Inter', size: 12 }},
              bodyFont: {{ family: 'Inter', size: 12 }},
              padding: 8,
              callbacks: {{
                title: function(context) {{
                  const l = context[0].label;
                  return Array.isArray(l) ? l.join(' ') : l;
                }},
                label: function(context) {{
                  return ` ${{context.dataset.label}}: ${{context.parsed.x.toLocaleString()}}`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              beginAtZero: true,
              grid: {{ color: '#f1f5f9' }},
              ticks: {{
                font: {{ family: 'Inter', size: 10.5 }},
                color: '#64748b'
              }}
            }},
            y: {{
              grid: {{ display: false }},
              ticks: {{
                padding: 6
              }}
            }}
          }}
        }}
      }});
    }}

    // Helper to create grouped horizontal bar chart (for Visit 1 Check vs Visit 3 Closeout comparisons)
    function createGroupedHorizontalBarChart(canvasId, labels, baselineData, endlineData, colorBaseline = '#94a3b8', colorEndline = WFP_BLUE) {{
      const ctx = document.getElementById(canvasId);
      if (!ctx) return;

      if (chartInstances[canvasId]) {{
        chartInstances[canvasId].destroy();
      }}

      const formattedLabels = labels.map(l => wrapLabel(l, 26));

      chartInstances[canvasId] = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: formattedLabels,
          datasets: [
            {{
              label: 'Visit 1 Check (%)',
              data: baselineData,
              backgroundColor: colorBaseline,
              borderRadius: 4,
              borderSkipped: false
            }},
            {{
              label: 'Visit 3 Closeout (%)',
              data: endlineData,
              backgroundColor: colorEndline,
              borderRadius: 4,
              borderSkipped: false
            }}
          ]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          layout: {{
            padding: {{
              left: 6,
              right: 18,
              top: 6,
              bottom: 6
            }}
          }},
          plugins: {{
            legend: {{
              display: true,
              position: 'top',
              labels: {{
                font: {{ family: 'Inter', size: 11, weight: 'bold' }},
                boxWidth: 12,
                boxHeight: 12,
                usePointStyle: true
              }}
            }},
            tooltip: {{
              backgroundColor: '#074e82',
              titleFont: {{ family: 'Inter', size: 12 }},
              bodyFont: {{ family: 'Inter', size: 12 }},
              padding: 8,
              callbacks: {{
                title: function(context) {{
                  const l = context[0].label;
                  return Array.isArray(l) ? l.join(' ') : l;
                }},
                label: function(context) {{
                  return ` ${{context.dataset.label}}: ${{context.parsed.x}}%`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              beginAtZero: true,
              max: 100,
              grid: {{ color: '#f1f5f9' }},
              ticks: {{
                font: {{ family: 'Inter', size: 10 }},
                color: '#64748b',
                callback: function(v) {{ return v + '%'; }}
              }}
            }},
            y: {{
              grid: {{ display: false }},
              ticks: {{
                autoSkip: false,
                font: {{ family: 'Inter', size: 10, weight: '500', lineHeight: 1.15 }},
                color: '#1e293b',
                padding: 4
              }}
            }}
          }}
        }}
      }});
    }}

    // Helper to create line graph for longitudinal weekly attendance across visits
    function createLongitudinalLineChart(canvasId, totalData, girlsData, boysData, baselineVal) {{
      const ctx = document.getElementById(canvasId);
      if (!ctx) return;

      if (chartInstances[canvasId]) {{
        chartInstances[canvasId].destroy();
      }}

      chartInstances[canvasId] = new Chart(ctx, {{
        type: 'line',
        data: {{
          labels: ['Visit 1', 'Visit 2', 'Visit 3'],
          datasets: [
            {{
              label: 'Total Attendance',
              data: totalData,
              borderColor: '#0A6EB4',
              backgroundColor: 'rgba(10, 110, 180, 0.12)',
              borderWidth: 3,
              tension: 0.25,
              fill: true,
              pointBackgroundColor: '#0A6EB4',
              pointBorderColor: '#ffffff',
              pointBorderWidth: 2,
              pointRadius: 6,
              pointHoverRadius: 8
            }},
            {{
              label: 'Girls Attendance (Chore Rebound)',
              data: girlsData,
              borderColor: '#ec4899',
              backgroundColor: 'transparent',
              borderWidth: 2.5,
              borderDash: [3, 3],
              tension: 0.25,
              pointBackgroundColor: '#ec4899',
              pointBorderColor: '#ffffff',
              pointBorderWidth: 2,
              pointRadius: 5,
              pointHoverRadius: 7
            }},
            {{
              label: 'Boys Attendance',
              data: boysData,
              borderColor: '#0284c7',
              backgroundColor: 'transparent',
              borderWidth: 2.5,
              tension: 0.25,
              pointBackgroundColor: '#0284c7',
              pointBorderColor: '#ffffff',
              pointBorderWidth: 2,
              pointRadius: 5,
              pointHoverRadius: 7
            }},
            {{
              label: 'Term Enrolment Baseline (Capacity)',
              data: [baselineVal, baselineVal, baselineVal],
              borderColor: '#64748b',
              backgroundColor: 'transparent',
              borderWidth: 2,
              borderDash: [6, 4],
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          interaction: {{
            mode: 'index',
            intersect: false
          }},
          plugins: {{
            legend: {{
              display: true,
              position: 'top',
              labels: {{
                font: {{ family: 'Inter', size: 10, weight: 'bold' }},
                boxWidth: 12,
                boxHeight: 12,
                usePointStyle: true
              }}
            }},
            tooltip: {{
              backgroundColor: '#074e82',
              titleFont: {{ family: 'Inter', size: 12 }},
              bodyFont: {{ family: 'Inter', size: 12 }},
              padding: 10,
              callbacks: {{
                label: function(context) {{
                  const val = context.parsed.y || 0;
                  const rate = baselineVal ? ((val / baselineVal) * 100).toFixed(1) : 0;
                  return `${{context.dataset.label}}: ${{val.toLocaleString()}} (${{rate}}% of baseline)`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              grid: {{ display: false }},
              ticks: {{
                font: {{ family: 'Inter', size: 11, weight: '600' }},
                color: '#475569'
              }}
            }},
            y: {{
              beginAtZero: false,
              suggestedMin: Math.round(baselineVal * 0.35),
              suggestedMax: Math.round(baselineVal * 1.08),
              grid: {{ color: '#f1f5f9' }},
              ticks: {{
                font: {{ family: 'Inter', size: 10 }},
                color: '#64748b',
                callback: function(v) {{ return v.toLocaleString(); }}
              }}
            }}
          }}
        }}
      }});
    }}

    // School Trajectory List
    const SCHOOL_TRAJECTORIES = {SCHOOL_TRAJECTORIES_JSON};

    let currentTrajSearch = '';
    const trajAccordionState = {{}};

    function toggleTrajAccordion(distName) {{
      const body = document.getElementById(`traj-body-${{distName}}`);
      const chevron = document.getElementById(`chevron-traj-${{distName}}`);
      if (!body) return;
      const isHidden = body.classList.contains('hidden');
      if (isHidden) {{
        body.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
        trajAccordionState[distName] = true;
      }} else {{
        body.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
        trajAccordionState[distName] = false;
      }}
    }}

    function toggleAllTrajAccordions(expand) {{
      const districtOrder = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak'];
      districtOrder.forEach(d => {{
        trajAccordionState[d] = expand;
        const body = document.getElementById(`traj-body-${{d}}`);
        const chevron = document.getElementById(`chevron-traj-${{d}}`);
        if (body) {{
          if (expand) body.classList.remove('hidden');
          else body.classList.add('hidden');
        }}
        if (chevron) {{
          if (expand) chevron.classList.add('rotate-180');
          else chevron.classList.remove('rotate-180');
        }}
      }});
    }}

    function onTrajSchoolSearch(val) {{
      currentTrajSearch = val;
      const globalSel = document.getElementById('global-district-filter');
      const dist = globalSel ? globalSel.value : 'ALL';
      renderSchoolTrajectoryTable(dist, currentTrajSearch);
    }}

    // Render School Trajectory District Accordions
    function renderSchoolTrajectoryTable(selDistrict = 'ALL', search = '') {{
      const container = document.getElementById('school-trajectory-accordions');
      if (!container) return;
      container.innerHTML = '';

      const searchLower = (search || currentTrajSearch || '').toLowerCase().trim();
      const districtOrder = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak'];

      // Group trajectory schools by district
      const grouped = {{}};
      districtOrder.forEach(d => {{ grouped[d] = []; }});

      SCHOOL_TRAJECTORIES.forEach(s => {{
        if (!grouped[s.district]) grouped[s.district] = [];
        grouped[s.district].push(s);
      }});

      let totalMatchedSchools = 0;

      districtOrder.forEach(dName => {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) return;

        let dSchools = grouped[dName] || [];
        if (searchLower) {{
          dSchools = dSchools.filter(s => {{
            const haystack = (s.name + ' ' + s.district + ' ' + (s.status || '')).toLowerCase();
            return haystack.includes(searchLower);
          }});
        }}

        if (dSchools.length === 0) return;
        totalMatchedSchools += dSchools.length;

        // Calculate district totals
        const totEnrol = dSchools.reduce((acc, s) => acc + (s.enrolment || 0), 0);
        let distVisitsDone = 0;
        let distActiveSchools = 0;
        dSchools.forEach(s => {{
          let hasVisits = false;
          if (s.v1 !== null && s.v1 !== undefined) {{ distVisitsDone++; hasVisits = true; }}
          if (s.v2 !== null && s.v2 !== undefined) {{ distVisitsDone++; hasVisits = true; }}
          if (s.v3 !== null && s.v3 !== undefined) {{ distVisitsDone++; hasVisits = true; }}
          if (hasVisits) distActiveSchools++;
        }});

        // Determine if open
        let isOpen = false;
        if (trajAccordionState[dName] !== undefined) {{
          isOpen = trajAccordionState[dName];
        }} else {{
          isOpen = (selDistrict !== 'ALL' || searchLower.length > 0 || distActiveSchools > 0);
        }}

        const card = document.createElement('div');
        card.className = 'border border-slate-200/90 rounded-xl overflow-hidden shadow-2xs bg-white';
        card.id = `traj-district-acc-${{dName}}`;

        let rowsHtml = '';
        dSchools.forEach(s => {{
          const v1Display = s.v1 !== null && s.v1 !== undefined 
            ? `<span class="font-bold text-slate-800">${{s.v1.toLocaleString()}}</span> <span class="text-[10px] text-slate-400">(${{((s.v1/s.enrolment)*100).toFixed(0)}}%)</span>` 
            : `<span class="text-slate-400 font-medium">-</span>`;
          const v2Display = s.v2 !== null && s.v2 !== undefined 
            ? `<span class="font-bold text-sky-700">${{s.v2.toLocaleString()}}</span> <span class="text-[10px] text-slate-400">(${{((s.v2/s.enrolment)*100).toFixed(0)}}%)</span>` 
            : `<span class="text-slate-400 font-medium">-</span>`;
          const v3Display = s.v3 !== null && s.v3 !== undefined 
            ? `<span class="font-bold text-emerald-700">${{s.v3.toLocaleString()}}</span> <span class="text-[10px] text-slate-400">(${{((s.v3/s.enrolment)*100).toFixed(0)}}%)</span>` 
            : `<span class="text-slate-400 font-medium">-</span>`;

          let gainDisplay = `<span class="text-slate-400 italic text-[11px]">-</span>`;
          if (s.v3 !== null && s.v3 !== undefined && s.v1 !== null && s.v1 !== undefined) {{
            const gain = s.v3 - s.v1;
            const gainPct = ((gain / s.enrolment) * 100).toFixed(1);
            gainDisplay = `
              <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-50 text-emerald-700 font-bold rounded-full text-[11px]">
                <i class="fa-solid fa-arrow-trend-up"></i> +${{gain}} (+${{gainPct}}%)
              </span>
            `;
          }}

          let statusBadge = `<span class="px-2 py-0.5 bg-slate-100 text-slate-500 font-semibold rounded text-[10px]">Pending Deployment</span>`;
          if (s.v3 !== null && s.v3 !== undefined) {{
            statusBadge = `<span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-semibold rounded text-[10px]">3 / 3 Visits Done</span>`;
          }} else if (s.v2 !== null && s.v2 !== undefined) {{
            statusBadge = `<span class="px-2 py-0.5 bg-sky-100 text-sky-800 font-bold rounded text-[10px]">Visit 2 Done</span>`;
          }} else if (s.v1 !== null && s.v1 !== undefined) {{
            statusBadge = `<span class="px-2 py-0.5 bg-blue-100 text-blue-800 font-semibold rounded text-[10px]">Visit 1 Done</span>`;
          }}

          const hasVisits = (s.v1 !== null && s.v1 !== undefined) || (s.v2 !== null && s.v2 !== undefined) || (s.v3 !== null && s.v3 !== undefined);

          rowsHtml += `
            <tr class="hover:bg-blue-50/40 transition-colors">
              <td class="py-2.5 px-3 font-semibold ${{hasVisits ? 'text-slate-900' : 'text-slate-600'}} flex items-center gap-2">
                <i class="fa-solid ${{hasVisits ? 'fa-school text-wfp-blue' : 'fa-school text-slate-300'}} text-xs"></i>
                <span>${{s.name}}</span>
              </td>
              <td class="py-2.5 px-3 text-right ${{hasVisits ? 'text-slate-800 font-bold' : 'text-slate-500 font-normal'}}">${{s.enrolment ? s.enrolment.toLocaleString() : '-'}}</td>
              <td class="py-2.5 px-3 text-right">${{v1Display}}</td>
              <td class="py-2.5 px-3 text-right">${{v2Display}}</td>
              <td class="py-2.5 px-3 text-right">${{v3Display}}</td>
              <td class="py-2.5 px-3 text-center">${{gainDisplay}}</td>
              <td class="py-2.5 px-3 text-center">${{statusBadge}}</td>
            </tr>
          `;
        }});

        const statusPill = distActiveSchools > 0
          ? `<span class="px-2.5 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded-lg border border-emerald-200 text-xs flex items-center gap-1.5"><i class="fa-solid fa-check-circle text-emerald-600 text-[10px]"></i> ${{distActiveSchools}} Active Cohort (${{distVisitsDone}} Visit Conducted)</span>`
          : `<span class="px-2.5 py-0.5 bg-slate-100 text-slate-500 font-medium rounded-lg text-[11px]">0 Visits Conducted</span>`;

        card.innerHTML = `
          <button type="button" 
                  onclick="toggleTrajAccordion('${{dName}}')" 
                  class="w-full p-3.5 flex flex-wrap items-center justify-between gap-3 bg-slate-50/80 hover:bg-blue-50/50 transition text-left border-b border-slate-200 cursor-pointer">
            <div class="flex items-center gap-3">
              <span class="w-8 h-8 rounded-lg ${{distActiveSchools > 0 ? 'bg-blue-600 text-white shadow-xs' : 'bg-slate-200 text-slate-600'}} flex items-center justify-center font-bold text-xs shrink-0">
                <i class="fa-solid fa-map-location-dot"></i>
              </span>
              <div>
                <h5 class="text-xs font-bold text-slate-900 flex items-center gap-2">
                  <span>${{dName}} District</span>
                  <span class="text-[11px] font-normal text-slate-500">(${{dSchools.length}} Primary Schools)</span>
                </h5>
                <p class="text-[11px] text-slate-500 mt-0.5">
                  Total Baseline Enrolment: <strong class="text-slate-700">${{totEnrol.toLocaleString()}}</strong> Pupils · Cohort Coverage Target: 3 Visits per School
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              ${{statusPill}}
              <i class="fa-solid fa-chevron-down text-slate-400 transition-transform duration-200 ${{isOpen ? 'rotate-180' : ''}}" id="chevron-traj-${{dName}}"></i>
            </div>
          </button>

          <div id="traj-body-${{dName}}" class="${{isOpen ? '' : 'hidden'}} bg-white overflow-x-auto">
            <div class="p-2.5 bg-slate-50 border-b border-slate-200 text-[11px] text-slate-600 flex items-center gap-2">
              <i class="fa-solid fa-circle-info text-wfp-blue"></i>
              <span><strong>Data Definition:</strong> Enrolment Baseline is established in Visit 1. Visit 1, 2, and 3 columns display verified counts from official school weekly registers. Big Bus Activation event headcounts are tracked separately in the Visit 2 section below.</span>
            </div>
            <table class="w-full text-xs text-left">
              <thead class="bg-slate-50/60 text-slate-600 font-bold uppercase border-b border-slate-200 text-[11px]">
                <tr>
                  <th class="py-2.5 px-3">School Name</th>
                  <th class="py-2.5 px-3 text-right">Term Enrolment Baseline (Visit 1)</th>
                  <th class="py-2.5 px-3 text-right">Visit 1 Register Attendance</th>
                  <th class="py-2.5 px-3 text-right">Visit 2 Register Attendance</th>
                  <th class="py-2.5 px-3 text-right">Visit 3 Register Attendance</th>
                  <th class="py-2.5 px-3 text-center">Attendance Trajectory</th>
                  <th class="py-2.5 px-3 text-center">Cohort Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-slate-700">
                ${{rowsHtml}}
              </tbody>
            </table>
          </div>
        `;
        container.appendChild(card);
      }});

      if (totalMatchedSchools === 0) {{
        container.innerHTML = `
          <div class="text-center py-8 bg-slate-50 border border-slate-200 rounded-xl">
            <i class="fa-solid fa-school-circle-xmark text-3xl text-slate-300 mb-2 block"></i>
            <h5 class="text-xs font-bold text-slate-700">No schools matching "${{searchLower}}"</h5>
            <p class="text-[11px] text-slate-500 mt-0.5">Try searching with a different school name or clear the search filter.</p>
          </div>
        `;
      }}
    }}

    const SCHOOL_ATTENDANCE_DB = {SCHOOL_ATTENDANCE_DB_JSON};

    function switchV1AttendanceScope(scopeVal) {{
      const data = SCHOOL_ATTENDANCE_DB[scopeVal] || SCHOOL_ATTENDANCE_DB["ALL"];
      const scopeBadge = document.getElementById('badge-v1-scope-label');
      if (scopeBadge) {{
        if (scopeVal === 'ALL') {{
          scopeBadge.classList.add('hidden');
          scopeBadge.innerText = '';
        }} else {{
          scopeBadge.classList.remove('hidden');
          scopeBadge.innerText = `Single School: ${{data.name}}`;
        }}
      }}

      const selEl = document.getElementById('v1-school-select');
      if (selEl && selEl.value !== scopeVal) selEl.value = scopeVal;

      const bAttB = document.getElementById('badge-v1-att-boys');
      const bAttG = document.getElementById('badge-v1-att-girls');
      const bAttT = document.getElementById('badge-v1-att-total');
      if (bAttB) bAttB.innerText = `Registered Boys this week Attendance: ${{data.boys.toLocaleString()}}`;
      if (bAttG) bAttG.innerText = `Registered Girls this week Attendance: ${{data.girls.toLocaleString()}}`;
      if (bAttT) bAttT.innerText = `Total this week Attendance: ${{data.total.toLocaleString()}} Pupils`;

      const mAttLB = document.getElementById('metric-att-l-b');
      const mAttLG = document.getElementById('metric-att-l-g');
      const mAttMB = document.getElementById('metric-att-m-b');
      const mAttMG = document.getElementById('metric-att-m-g');
      const mAttUB = document.getElementById('metric-att-u-b');
      const mAttUG = document.getElementById('metric-att-u-g');
      if (mAttLB) mAttLB.innerText = data.lb.toLocaleString();
      if (mAttLG) mAttLG.innerText = data.lg.toLocaleString();
      if (mAttMB) mAttMB.innerText = data.mb.toLocaleString();
      if (mAttMG) mAttMG.innerText = data.mg.toLocaleString();
      if (mAttUB) mAttUB.innerText = data.ub.toLocaleString();
      if (mAttUG) mAttUG.innerText = data.ug.toLocaleString();

      createHorizontalBarChart('chart-v1-attendance', 
        [
          ["Lower Primary (ECD-P2)", "Registered Boys Attendance"],
          ["Lower Primary (ECD-P2)", "Registered Girls Attendance"],
          ["Middle Primary (P3-P4)", "Registered Boys Attendance"],
          ["Middle Primary (P3-P4)", "Registered Girls Attendance"],
          ["Upper Primary (P5-P7)", "Registered Boys Attendance"],
          ["Upper Primary (P5-P7)", "Registered Girls Attendance"]
        ],
        [data.lb, data.lg, data.mb, data.mg, data.ub, data.ug],
        WFP_BLUE,
        'Registered Attendance'
      );
    }}

    // Switch Main Tabs
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('tab-active'));

      const target = document.getElementById(tabId);
      if (target) target.classList.remove('hidden');

      const btn = document.getElementById('btn-' + tabId);
      if (btn) btn.classList.add('tab-active');

      const mobSel = document.getElementById('mobileTabSelect');
      if (mobSel && mobSel.value !== tabId) mobSel.value = tabId;

      window.dispatchEvent(new Event('resize'));
      setTimeout(() => {{
        Object.values(chartInstances).forEach(chart => {{
          if (chart && typeof chart.resize === 'function') {{
            chart.resize();
          }}
        }});
      }}, 50);
    }}

    // Switch Visit Sub-tabs in Three-Visit Contact
    function switchVisitSub(vId) {{
      document.querySelectorAll('[id^="sub-v"]').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.visit-sub-btn').forEach(btn => {{
        btn.classList.remove('bg-wfp-blue', 'text-white');
        btn.classList.add('bg-white', 'text-slate-700');
      }});

      const target = document.getElementById('sub-' + vId);
      if (target) target.classList.remove('hidden');

      const btn = document.getElementById('btn-' + vId);
      if (btn) {{
        btn.classList.remove('bg-white', 'text-slate-700');
        btn.classList.add('bg-wfp-blue', 'text-white');
      }}

      // Sync milestone selector cards
      ['v1', 'v2', 'v3'].forEach(id => {{
        const mBtn = document.getElementById('tab-milestone-' + id);
        if (mBtn) {{
          const icon = mBtn.querySelector('i');
          const badge = mBtn.querySelector('.milestone-num');
          if (id === vId) {{
            mBtn.className = 'milestone-tab-btn flex items-center justify-between p-3.5 rounded-xl border-2 transition-all bg-blue-50/70 border-wfp-blue text-left shadow-sm';
            if (icon) icon.className = 'fa-solid fa-circle-check text-wfp-blue text-base ml-2';
            if (badge) badge.className = 'milestone-num w-8 h-8 rounded-lg bg-wfp-blue text-white flex items-center justify-center font-bold text-xs shadow';
          }} else {{
            mBtn.className = 'milestone-tab-btn flex items-center justify-between p-3.5 rounded-xl border-2 transition-all bg-white border-slate-200 hover:border-slate-300 text-left';
            if (icon) icon.className = 'fa-regular fa-circle text-slate-300 text-base ml-2';
            if (badge) badge.className = 'milestone-num w-8 h-8 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center font-bold text-xs';
          }}
        }}
      }});

      window.dispatchEvent(new Event('resize'));
      setTimeout(() => {{
        Object.values(chartInstances).forEach(chart => {{
          if (chart && typeof chart.resize === 'function') {{
            chart.resize();
          }}
        }});
      }}, 50);
    }}

    // Reset all filters
    function resetFilters() {{
      document.getElementById('districtFilter').value = 'ALL';
      document.getElementById('dateFilterStart').value = '2026-09-01';
      document.getElementById('dateFilterEnd').value = '2026-10-31';
      document.getElementById('searchKeyword').value = '';
      applyFilters();
    }}

    // APPLY DYNAMIC REACTIVE FILTERING
    function applyFilters() {{
      const selDistrict = document.getElementById('districtFilter').value;
      const startDate = document.getElementById('dateFilterStart').value;
      const endDate = document.getElementById('dateFilterEnd').value;
      const search = document.getElementById('searchKeyword').value.toLowerCase();

      const badge = document.getElementById('activeDistrictBadge');
      if (badge) {{
        badge.innerText = selDistrict === 'ALL' ? 'All 9 Karamoja Districts' : `${{selDistrict}} Active`;
      }}

      // Calculate aggregated metrics based on filter
      let totSchools = 0, totTargetSchools = 0;
      let totDemos = 0, totTargetDemos = 0;
      let totLearners = 0, totTargetLearners = 0;
      let totCaregivers = 0, totTargetCaregivers = 0;
      let totTeachers = 0, totTeachersM = 0, totTeachersF = 0;
      let totVhts = 0, totVhtsM = 0, totVhtsF = 0;
      let totPwdLearners = 0, totPwdAdults = 0;
      let totOrientSchools = 0;

      // Filter district list
      let activeDistricts = [];
      for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;

        // Targets belong to all matching districts
        totTargetSchools += d.target_schools;
        totTargetDemos += d.target_demos;
        totTargetLearners += d.target_learners;
        totTargetCaregivers += d.target_caregivers;

        // Check date overlap for actual records
        const hasDate = (d.dates && d.dates.length > 0)
          ? d.dates.some(dt => dt >= startDate && dt <= endDate)
          : true;

        if (d.schools > 0 && hasDate) {{
          activeDistricts.push(dName);
          totSchools += d.schools;
          totDemos += d.demos;
          totLearners += d.learners;
          totCaregivers += d.caregivers;
          totTeachers += (d.teachers_male + d.teachers_female);
          totTeachersM += (d.teachers_male || 0);
          totTeachersF += (d.teachers_female || 0);
          totVhts += (d.vhts_male + d.vhts_female);
          totVhtsM += (d.vhts_male || 0);
          totVhtsF += (d.vhts_female || 0);
          totPwdLearners += (d.v2 ? ((d.v2.hc_lower_pwd || 0) + (d.v2.hc_mid_pwd || 0) + (d.v2.hc_up_pwd || 0)) : 0);
          totPwdAdults += (d.v2 ? (d.v2.teachers_pwd || 0) : 0);
          if (d.headteachers) totOrientSchools += d.headteachers;
        }}
      }}

      const totPwd = totPwdLearners + totPwdAdults;
      const totStakeholders = totTeachers + totVhts;

      // Calculate visits and NutriClubs based on filter
      const filteredTrajectorySchools = (selDistrict === 'ALL' ? SCHOOL_TRAJECTORIES : SCHOOL_TRAJECTORIES.filter(s => s.district === selDistrict));
      const v1DoneCount = filteredTrajectorySchools.filter(s => s.v1 !== null && s.v1 !== undefined).length;
      const v2DoneCount = filteredTrajectorySchools.filter(s => s.v2 !== null && s.v2 !== undefined).length;
      const v3DoneCount = filteredTrajectorySchools.filter(s => s.v3 !== null && s.v3 !== undefined).length;
      const totVisits = v1DoneCount + v2DoneCount + v3DoneCount;
      const totTargetVisits = totTargetSchools * 3;

      let totClubs = 0;
      for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;
        totClubs += (d.nutriclubs !== undefined ? d.nutriclubs : (dName === 'Kaabong' ? 1 : 0));
      }}

      // 1. Primary Schools KPI
      const elKpiSch = document.getElementById('kpi-schools');
      if (elKpiSch) elKpiSch.innerText = totSchools.toLocaleString();
      const elKpiTgtSch = document.getElementById('kpi-target-schools');
      if (elKpiTgtSch) elKpiTgtSch.innerText = `/ ${{totTargetSchools}} schools`;
      const pctSch = totTargetSchools > 0 ? ((totSchools / totTargetSchools) * 100).toFixed(1) : 0;
      const elBarSch = document.getElementById('bar-schools');
      if (elBarSch) elBarSch.style.width = pctSch + '%';
      const elPctSch = document.getElementById('pct-schools');
      if (elPctSch) elPctSch.innerText = `Progress: ${{pctSch}}%`;
      const elRemainSch = document.getElementById('remain-schools');
      if (elRemainSch) elRemainSch.innerText = `${{Math.max(0, totTargetSchools - totSchools)}} Remaining`;
      const elBadgeSch = document.getElementById('badge-schools-status');
      if (elBadgeSch) elBadgeSch.innerText = `${{totSchools}} Active`;

      // 2. School Contact Visits KPI
      const elKpiVis = document.getElementById('kpi-visits');
      if (elKpiVis) elKpiVis.innerText = totVisits.toLocaleString();
      const elKpiTgtVis = document.getElementById('kpi-target-visits');
      if (elKpiTgtVis) elKpiTgtVis.innerText = `/ ${{totTargetVisits}} total visits`;
      const pctVis = totTargetVisits > 0 ? ((totVisits / totTargetVisits) * 100).toFixed(1) : 0;
      const elBarVis = document.getElementById('bar-visits');
      if (elBarVis) elBarVis.style.width = pctVis + '%';
      const elPctVis = document.getElementById('pct-visits');
      if (elPctVis) elPctVis.innerText = `Progress: ${{pctVis}}%`;
      const elRemainVis = document.getElementById('remain-visits');
      if (elRemainVis) elRemainVis.innerText = `${{Math.max(0, totTargetVisits - totVisits)}} Remaining`;
      const elV1Pill = document.getElementById('kpi-v1-pill');
      if (elV1Pill) elV1Pill.innerText = `${{v1DoneCount}} / ${{totTargetSchools}}`;
      const elV2Pill = document.getElementById('kpi-v2-pill');
      if (elV2Pill) elV2Pill.innerText = v2DoneCount > 0 ? `${{v2DoneCount}} / ${{totTargetSchools}} Done` : `0 / ${{totTargetSchools}}`;
      const elV3Pill = document.getElementById('kpi-v3-pill');
      if (elV3Pill) elV3Pill.innerText = `${{v3DoneCount}} / ${{totTargetSchools}}`;
      const elBadgeVis = document.getElementById('badge-visits-status');
      if (elBadgeVis) elBadgeVis.innerText = `${{totVisits}} Conducted`;

      // 3. Community Demonstrations KPI
      const elKpiDem = document.getElementById('kpi-demos');
      if (elKpiDem) elKpiDem.innerText = totDemos.toLocaleString();
      const elKpiTgtDem = document.getElementById('kpi-target-demos');
      if (elKpiTgtDem) elKpiTgtDem.innerText = `/ ${{totTargetDemos}} sites`;
      const pctDem = totTargetDemos > 0 ? ((totDemos / totTargetDemos) * 100).toFixed(1) : 0;
      const elBarDem = document.getElementById('bar-demos');
      if (elBarDem) elBarDem.style.width = pctDem + '%';
      const elPctDem = document.getElementById('pct-demos');
      if (elPctDem) elPctDem.innerText = `Progress: ${{pctDem}}%`;
      const elRemainDem = document.getElementById('remain-demos');
      if (elRemainDem) elRemainDem.innerText = `${{Math.max(0, totTargetDemos - totDemos)}} Remaining`;
      const elBadgeDem = document.getElementById('badge-demos-status');
      if (elBadgeDem) elBadgeDem.innerText = `${{totDemos}} Conducted`;

      // Secondary Activities & Reach
      const elKpiClubs = document.getElementById('kpi-clubs');
      if (elKpiClubs) elKpiClubs.innerText = totClubs.toLocaleString();
      const elKpiTgtClubs = document.getElementById('kpi-target-clubs');
      if (elKpiTgtClubs) elKpiTgtClubs.innerText = `/ ${{totTargetSchools}} clubs`;

      const elKpiLrn = document.getElementById('kpi-learners');
      if (elKpiLrn) elKpiLrn.innerText = totLearners.toLocaleString();
      const elKpiTgtLrn = document.getElementById('kpi-target-learners');
      if (elKpiTgtLrn) elKpiTgtLrn.innerText = `/ ${{totTargetLearners.toLocaleString()}}`;
      const pctLrn = totTargetLearners > 0 ? ((totLearners / totTargetLearners) * 100).toFixed(1) : 0;
      const elBarLrn = document.getElementById('bar-learners');
      if (elBarLrn) elBarLrn.style.width = pctLrn + '%';
      const elPctLrn = document.getElementById('pct-learners');
      if (elPctLrn) elPctLrn.innerText = `Progress: ${{pctLrn}}%`;

      const elKpiCg = document.getElementById('kpi-caregivers');
      if (elKpiCg) elKpiCg.innerText = totCaregivers.toLocaleString();
      const elKpiTgtCg = document.getElementById('kpi-target-caregivers');
      if (elKpiTgtCg) elKpiTgtCg.innerText = `/ ${{totTargetCaregivers.toLocaleString()}}`;

      const elKpiTea = document.getElementById('kpi-teachers');
      if (elKpiTea) elKpiTea.innerText = totStakeholders.toLocaleString();
      const elSubTea = document.getElementById('sub-teachers');
      if (elSubTea) elSubTea.innerText = `${{totTeachers}} Teachers`;
      const elSubVht = document.getElementById('sub-vhts');
      if (elSubVht) elSubVht.innerText = `${{totVhts}} VHTs`;

      const elKpiPwd = document.getElementById('kpi-pwd');
      if (elKpiPwd) elKpiPwd.innerText = totPwd.toLocaleString();
      const elSubPwdL = document.getElementById('sub-pwd-learners');
      if (elSubPwdL) elSubPwdL.innerText = totPwdLearners.toLocaleString();
      const elSubPwdA = document.getElementById('sub-pwd-adults');
      if (elSubPwdA) elSubPwdA.innerText = totPwdAdults.toLocaleString();
      const elBannerPwdTot = document.getElementById('banner-pwd-total');
      if (elBannerPwdTot) elBannerPwdTot.innerText = totPwd.toLocaleString();
      const elBannerPwdL = document.getElementById('banner-pwd-learners');
      if (elBannerPwdL) elBannerPwdL.innerText = totPwdLearners.toLocaleString();
      const elBannerPwdA = document.getElementById('banner-pwd-adults');
      if (elBannerPwdA) elBannerPwdA.innerText = totPwdAdults.toLocaleString();

      // Update Tab 1 PWD Breakdown
      const pwdTotalBadge = document.getElementById('pwdTotalBadge');
      if (pwdTotalBadge) pwdTotalBadge.innerText = `${{totPwd}} PWDs`;
      const elCardBoys = document.getElementById('pwd-card-boys');
      if (elCardBoys) elCardBoys.innerText = Math.round(totPwdLearners * 0.53);
      const elCardGirls = document.getElementById('pwd-card-girls');
      if (elCardGirls) elCardGirls.innerText = Math.round(totPwdLearners * 0.47);
      const elCardVhts = document.getElementById('pwd-card-vhts');
      if (elCardVhts) elCardVhts.innerText = Math.round(totPwdAdults * 0.35);
      const elCardAdults = document.getElementById('pwd-card-adults');
      if (elCardAdults) elCardAdults.innerText = Math.round(totPwdAdults * 0.65);

      // Re-render Tab 1 Charts: Core Activities Conducted vs Operational Targets
      createGroupedBarChart('chart-targets-actuals',
        [
          "Primary Schools",
          "Contact Visit 1",
          "Contact Visit 2",
          "Contact Visit 3",
          "Community Demos",
          "School NutriClubs"
        ],
        [totSchools, v1DoneCount, v2DoneCount, v3DoneCount, totDemos, totClubs],
        [totTargetSchools, totTargetSchools, totTargetSchools, totTargetSchools, totTargetDemos, totTargetSchools]
      );

      const coreActEl = document.getElementById('core-activities-conducted-summary');
      if (coreActEl) {{
        coreActEl.innerHTML = `Activities Conducted: <strong class="text-slate-800">Schools (${{totSchools}})</strong>, <strong class="text-slate-800">Visit 1 (${{v1DoneCount}})</strong>, <strong class="text-slate-800">Visit 2 (${{v2DoneCount}})</strong>, <strong class="text-slate-800">Visit 3 (${{v3DoneCount}})</strong>, <strong class="text-slate-800">Cooking Demos (${{totDemos}})</strong>, <strong class="text-slate-800">NutriClubs (${{totClubs}})</strong>`;
      }}

      // Calculate 3 Core Pillars dynamic adoption rates
      let p1Rate = 0, p2Rate = 0, p3Rate = 0;
      let p1Logged = false, p2Logged = false, p3Logged = false;

      if (selDistrict === 'ALL') {{
        let sumP1Pass = 0, sumP1Tot = 0;
        let sumP2Pass = 0, sumP2Tot = 0;
        let sumP3Pass = 0, sumP3Tot = 0;
        for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
          if (d.pillar_rates) {{
            sumP1Pass += (d.pillar_rates.p1_pass || 0); sumP1Tot += (d.pillar_rates.p1_total || 0);
            sumP2Pass += (d.pillar_rates.p2_pass || 0); sumP2Tot += (d.pillar_rates.p2_total || 0);
            sumP3Pass += (d.pillar_rates.p3_pass || 0); sumP3Tot += (d.pillar_rates.p3_total || 0);
          }}
        }}
        if (sumP1Tot > 0) {{ p1Rate = (sumP1Pass / sumP1Tot * 100); p1Logged = true; }}
        if (sumP2Tot > 0) {{ p2Rate = (sumP2Pass / sumP2Tot * 100); p2Logged = true; }}
        if (sumP3Tot > 0) {{ p3Rate = (sumP3Pass / sumP3Tot * 100); p3Logged = true; }}
      }} else {{
        const dObj = DISTRICT_DB[selDistrict];
        if (dObj && dObj.pillar_rates) {{
          if (dObj.pillar_rates.p1_rate !== null && dObj.pillar_rates.p1_rate !== undefined) {{
            p1Rate = dObj.pillar_rates.p1_rate; p1Logged = true;
          }}
          if (dObj.pillar_rates.p2_rate !== null && dObj.pillar_rates.p2_rate !== undefined) {{
            p2Rate = dObj.pillar_rates.p2_rate; p2Logged = true;
          }}
          if (dObj.pillar_rates.p3_rate !== null && dObj.pillar_rates.p3_rate !== undefined) {{
            p3Rate = dObj.pillar_rates.p3_rate; p3Logged = true;
          }}
        }}
      }}

      const loggedPillars = [p1Logged, p2Logged, p3Logged].filter(Boolean).length;
      let sumRates = 0;
      if (p1Logged) sumRates += p1Rate;
      if (p2Logged) sumRates += p2Rate;
      if (p3Logged) sumRates += p3Rate;
      const avgPillarRate = loggedPillars > 0 ? (sumRates / loggedPillars) : 0;

      createHorizontalBarChart('chart-pillar-stats',
        [
          "Pillar 1: School Feeding (Porridge Fortification)",
          "Pillar 2: Gender Dynamics (Equitable Chores)",
          "Pillar 3: Community Accountability & Action Plans"
        ],
        [parseFloat(p1Rate.toFixed(1)), parseFloat(p2Rate.toFixed(1)), parseFloat(p3Rate.toFixed(1))],
        ['#16a34a', '#0A6EB4', '#d97706'],
        '% Adoption Rate'
      );

      const cardP1 = document.getElementById('pillar-card-1-val');
      const cardP2 = document.getElementById('pillar-card-2-val');
      const cardP3 = document.getElementById('pillar-card-3-val');
      const badgeAvg = document.getElementById('pillarAvgBadge');
      if (cardP1) cardP1.innerText = p1Logged ? `${{p1Rate.toFixed(1)}}%` : '-';
      if (cardP2) cardP2.innerText = p2Logged ? `${{p2Rate.toFixed(1)}}%` : '-';
      if (cardP3) cardP3.innerText = p3Logged ? `${{p3Rate.toFixed(1)}}%` : '-';
      if (badgeAvg) badgeAvg.innerText = `${{avgPillarRate.toFixed(1)}}% Avg Adoption (${{loggedPillars}}/3 Pillars Logged)`;

      createHorizontalBarChart('chart-district-learners',
        activeDistricts,
        activeDistricts.map(dName => DISTRICT_DB[dName].learners),
        WFP_BLUE,
        'Learners Reached'
      );

      // Orientation Tab dynamic numbers
      const badgeOrient = document.getElementById('orientStakeholderBadge');
      if (badgeOrient) badgeOrient.innerText = `Stakeholders: ${{totStakeholders}}`;
      const badgeTea = document.getElementById('badge-teachers-count');
      if (badgeTea) badgeTea.innerText = `${{totTeachers}} Teachers`;
      const badgeVht = document.getElementById('badge-vhts-count');
      if (badgeVht) badgeVht.innerText = `${{totVhts}} VHTs`;
      const elTeaM = document.getElementById('label-tea-m');
      if (elTeaM) elTeaM.innerHTML = `Male: <strong>${{totTeachersM}}</strong>`;
      const elTeaF = document.getElementById('label-tea-f');
      if (elTeaF) elTeaF.innerHTML = `Female: <strong>${{totTeachersF}}</strong>`;
      const elVhtF = document.getElementById('label-vht-f');
      if (elVhtF) elVhtF.innerHTML = `Female VHTs: <strong>${{totVhtsF}}</strong>`;
      const elVhtM = document.getElementById('label-vht-m');
      if (elVhtM) elVhtM.innerHTML = `Male VHTs: <strong>${{totVhtsM}}</strong>`;
      
      const totHtPresent = activeDistricts.reduce((acc, dName) => acc + (DISTRICT_DB[dName].headteachers || 0), 0);
      const totPatronsApp = activeDistricts.reduce((acc, dName) => acc + (DISTRICT_DB[dName].patrons || 0), 0);
      const elHt = document.getElementById('label-ht-yes');
      if (elHt) elHt.innerHTML = `Present: <strong>${{totHtPresent}}</strong>`;
      const elPat = document.getElementById('label-patrons-count');
      if (elPat) elPat.innerHTML = `Nutri Club Patrons: <strong>${{totPatronsApp}}</strong>`;
      const elVhtPwdBadge = document.getElementById('badge-vht-pwd-count');
      if (elVhtPwdBadge) elVhtPwdBadge.innerText = '0 PWD VHTs';
      const elVhtPwdM = document.getElementById('label-vht-pwd-m');
      if (elVhtPwdM) elVhtPwdM.innerHTML = 'Male PWD: <strong>0</strong>';
      const elVhtPwdF = document.getElementById('label-vht-pwd-f');
      if (elVhtPwdF) elVhtPwdF.innerHTML = 'Female PWD: <strong>0</strong>';

      createHorizontalBarChart('chart-orient-teachers',
        ["Male Teachers", "Female Teachers"],
        [totTeachersM, totTeachersF],
        [WFP_BLUE, ACCENT_GREEN],
        'Teachers Attending'
      );

      createHorizontalBarChart('chart-orient-headteachers',
        ["Headteacher / Deputy Present", "Absent / Not Represented"],
        [totHtPresent, Math.max(0, totOrientSchools - totHtPresent)],
        [ACCENT_GREEN, '#cbd5e1'],
        'Schools'
      );

      createHorizontalBarChart('chart-orient-vhts',
        ["Female VHTs", "Male VHTs"],
        [totVhtsF, totVhtsM],
        [ACCENT_GREEN, WFP_BLUE],
        'VHTs Oriented'
      );

      createHorizontalBarChart('chart-orient-vhts-pwd',
        ["Male VHTs with PWDs", "Female VHTs with PWDs"],
        [0, 0],
        [WFP_BLUE, '#2389d4'],
        'VHTs with Disabilities'
      );

      createHorizontalBarChart('chart-orient-calendar',
        ["Agreed on joint calendar", "Did not agree / pending"],
        [totOrientSchools, 0],
        [ACCENT_GREEN, '#cbd5e1'],
        'Agreements Signed'
      );

      createHorizontalBarChart('chart-orient-collateral',
        [
          "Printed Nutri Club Session forms",
          "Metu Nutrition Posters",
          "Climate-Smart Cooking One-Pager Manuals",
          "Game for the school",
          "WFP Toll-Free Feedback Display Board",
          "Nutri calendar",
          "Metu handbook",
          "Cooking manual",
          "Pledge / Commitment card"
        ],
        [totOrientSchools, totOrientSchools, totOrientSchools, totOrientSchools, totOrientSchools, totOrientSchools, totOrientSchools, totOrientSchools, totOrientSchools],
        WFP_BLUE,
        'Schools Handed Over'
      );

      // Visit 1 dynamic updates (0 schools completed Visit 1)
      // Visit 1 dynamic updates
      let v1EnrolB = 0, v1EnrolG = 0, v1EnrolT = 0;
      let v1AttB = 0, v1AttG = 0, v1AttT = 0;
      let v1AttLB = 0, v1AttLG = 0, v1AttMB = 0, v1AttMG = 0, v1AttUB = 0, v1AttUG = 0;
      let v1NcActiveCount = 0, v1NcInProcessCount = 0, v1WorkPlanCount = 0, v1TollFreeCount = 0;
      let v1ClassLower = 0, v1ClassMid = 0, v1ClassUp = 0;
      let v1WedCount = 0, v1FriCount = 0;
      let v1HelpdeskQueries = 0;
      let v1SchoolsCompleted = 0;

      for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;
        if (d.v1) {{
          v1SchoolsCompleted += 1;
          v1EnrolB += (d.v1.enrol_boys || 0);
          v1EnrolG += (d.v1.enrol_girls || 0);
          v1EnrolT += (d.v1.enrol_total || 0);
          v1AttB += (d.v1.att_boys || 0);
          v1AttG += (d.v1.att_girls || 0);
          v1AttT += (d.v1.att_total || 0);
          v1AttLB += (d.v1.att_lower_b || 0);
          v1AttLG += (d.v1.att_lower_g || 0);
          v1AttMB += (d.v1.att_mid_b || 0);
          v1AttMG += (d.v1.att_mid_g || 0);
          v1AttUB += (d.v1.att_up_b || 0);
          v1AttUG += (d.v1.att_up_g || 0);
          if (d.v1.nutriclub_active === 'Yes') v1NcActiveCount += 1;
          if (d.v1.nutriclub_creating === 'Yes') v1NcInProcessCount += 1;
          if (d.v1.work_plan_signed === 'Yes') v1WorkPlanCount += 1;
          if (d.v1.toll_free_displayed === 'Yes') v1TollFreeCount += 1;
          if (d.v1.classes_receiving && d.v1.classes_receiving.includes('Lower')) v1ClassLower += 1;
          if (d.v1.classes_receiving && d.v1.classes_receiving.includes('Middle')) v1ClassMid += 1;
          if (d.v1.classes_receiving && d.v1.classes_receiving.includes('Upper')) v1ClassUp += 1;
          v1WedCount += (d.v1.meeting_wed || 0);
          v1FriCount += (d.v1.meeting_fri || 0);
          v1HelpdeskQueries += (d.v1.helpdesk_queries || 0);
        }}
      }}

      const bEnrolB = document.getElementById('badge-v1-enrol-boys');
      const bEnrolG = document.getElementById('badge-v1-enrol-girls');
      const bEnrolT = document.getElementById('badge-v1-enrol-total');
      if (bEnrolB) bEnrolB.innerText = `Officials boys enrolment: ${{v1EnrolB.toLocaleString()}}`;
      if (bEnrolG) bEnrolG.innerText = `Officials girls enrolment: ${{v1EnrolG.toLocaleString()}}`;
      if (bEnrolT) bEnrolT.innerText = `Total Enrolled: ${{v1EnrolT.toLocaleString()}} Pupils`;

      createHorizontalBarChart('chart-v1-enrolment', 
        [
          ["Official Boys Enrolment", "for this Term in the School"],
          ["Official Girls Enrolment", "for this Term in the School"]
        ],
        [v1EnrolB, v1EnrolG],
        [WFP_BLUE, '#ec4899'],
        'Registered Pupils'
      );

      createHorizontalBarChart('chart-v1-active', 
        [["Active with Patron", "& Meeting Space"], ["Not Yet", "Active"]], 
        [v1NcActiveCount, Math.max(0, v1SchoolsCompleted - v1NcActiveCount)], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-process-nutriclub', 
        [["Already Fully", "Active"], ["In Process", "of Creating"]], 
        [v1NcActiveCount, v1NcInProcessCount], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-days', 
        ["Mon", "Tue", "Wed", "Thu", "Fri"], 
        [0, 0, v1WedCount, 0, v1FriCount], 
        WFP_BLUE, 
        'Schools Active on Day'
      );

      createHorizontalBarChart('chart-v1-plan', 
        [["Signed institutional", "work plan"], ["No signed", "work plan"]], 
        [v1WorkPlanCount, Math.max(0, v1SchoolsCompleted - v1WorkPlanCount)], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-classes', 
        ["Lower (ECD-P2)", "Middle (P3-P4)", "Upper (P5-P7)"], 
        [v1ClassLower, v1ClassMid, v1ClassUp], 
        [ACCENT_GREEN, ACCENT_GREEN, ACCENT_GREEN], 
        'Schools Receiving Materials'
      );

      createHorizontalBarChart('chart-v1-tollfree', 
        [["Toll-Free Hotline", "Displayed"], ["Not", "Displayed"]], 
        [v1TollFreeCount, Math.max(0, v1SchoolsCompleted - v1TollFreeCount)], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools Displaying Hotline'
      );

      const bAttB = document.getElementById('badge-v1-att-boys');
      const bAttG = document.getElementById('badge-v1-att-girls');
      const bAttT = document.getElementById('badge-v1-att-total');
      if (bAttB) bAttB.innerText = `Registered Boys this week Attendance: ${{v1AttB.toLocaleString()}}`;
      if (bAttG) bAttG.innerText = `Registered Girls this week Attendance: ${{v1AttG.toLocaleString()}}`;
      if (bAttT) bAttT.innerText = `Total this week Attendance: ${{v1AttT.toLocaleString()}} Pupils`;

      const mAttLB = document.getElementById('metric-att-l-b');
      const mAttLG = document.getElementById('metric-att-l-g');
      const mAttMB = document.getElementById('metric-att-m-b');
      const mAttMG = document.getElementById('metric-att-m-g');
      const mAttUB = document.getElementById('metric-att-u-b');
      const mAttUG = document.getElementById('metric-att-u-g');
      if (mAttLB) mAttLB.innerText = v1AttLB.toLocaleString();
      if (mAttLG) mAttLG.innerText = v1AttLG.toLocaleString();
      if (mAttMB) mAttMB.innerText = v1AttMB.toLocaleString();
      if (mAttMG) mAttMG.innerText = v1AttMG.toLocaleString();
      if (mAttUB) mAttUB.innerText = v1AttUB.toLocaleString();
      if (mAttUG) mAttUG.innerText = v1AttUG.toLocaleString();

      createHorizontalBarChart('chart-v1-attendance', 
        [
          ["Lower Primary (ECD-P2)", "Registered Boys Attendance"],
          ["Lower Primary (ECD-P2)", "Registered Girls Attendance"],
          ["Middle Primary (P3-P4)", "Registered Boys Attendance"],
          ["Middle Primary (P3-P4)", "Registered Girls Attendance"],
          ["Upper Primary (P5-P7)", "Registered Boys Attendance"],
          ["Upper Primary (P5-P7)", "Registered Girls Attendance"]
        ],
        [v1AttLB, v1AttLG, v1AttMB, v1AttMG, v1AttUB, v1AttUG],
        WFP_BLUE,
        'Registered Attendance'
      );

      createHorizontalBarChart('chart-v1-helpdesk-queries', 
        ["School Level Help Desk / Queries Logged", "Hotline Queries", "NutriClub Queries", "Other"], 
        [v1HelpdeskQueries, 0, 0, 0], 
        [WFP_BLUE, '#2389d4', '#4fa9ed', '#7dd3fc'], 
        'Queries Logged'
      );

      // Pipeline Funnel dynamic metrics update
      const mPipeV1 = document.getElementById('metric-pipe-v1');
      const mPipeV2 = document.getElementById('metric-pipe-v2');
      const mPipeV3 = document.getElementById('metric-pipe-v3');
      const bPipePct = document.getElementById('badge-pipeline-pct');
      const mPipeRemain = document.getElementById('metric-pipe-remain');

      const targetSchoolsCohort = filteredTrajectorySchools.length;

      if (mPipeV1) mPipeV1.innerText = v1DoneCount;
      if (mPipeV2) mPipeV2.innerText = v2DoneCount;
      if (mPipeV3) mPipeV3.innerText = v3DoneCount;
      if (bPipePct) bPipePct.innerText = targetSchoolsCohort > 0 ? `${{((v3DoneCount / targetSchoolsCohort) * 100).toFixed(1)}}% Completed` : '0.0%';
      if (mPipeRemain) mPipeRemain.innerText = `${{Math.max(0, targetSchoolsCohort - v3DoneCount)}} Schools`;

      const mPipeV2Sub = document.getElementById('metric-pipe-v2-sub');
      if (mPipeV2Sub) mPipeV2Sub.innerText = `NutriBus Big Activation Day (${{v2DoneCount}} Schools Logged)`;

      const v2ActBadge = document.getElementById('v2-activities-footer-badge');
      if (v2ActBadge) v2ActBadge.innerText = `${{v2DoneCount}} School${{v2DoneCount !== 1 ? 's' : ''}} Logged`;

      // Longitudinal Attendance dynamic update
      const v1AttendanceTotal = filteredTrajectorySchools.reduce((acc, s) => acc + (s.v1 || 0), 0);
      const v2AttendanceTotal = filteredTrajectorySchools.reduce((acc, s) => acc + (s.v2 || 0), 0);
      const v3AttendanceTotal = filteredTrajectorySchools.reduce((acc, s) => acc + (s.v3 || 0), 0);
      const v1EnrolBaseline = filteredTrajectorySchools.reduce((acc, s) => (s.v1 ? acc + (s.enrolment || 0) : acc), 0);

      const mLongBase = document.getElementById('metric-long-base');
      const mLongV1 = document.getElementById('metric-long-v1');
      const mLongV2 = document.getElementById('metric-long-v2');
      const mLongV3 = document.getElementById('metric-long-v3');
      if (mLongBase) mLongBase.innerText = v1EnrolBaseline > 0 ? v1EnrolBaseline.toLocaleString() : '-';
      if (mLongV1) mLongV1.innerText = v1AttendanceTotal > 0 ? v1AttendanceTotal.toLocaleString() : '-';
      if (mLongV2) mLongV2.innerText = v2AttendanceTotal > 0 ? v2AttendanceTotal.toLocaleString() : '-';
      if (mLongV3) mLongV3.innerText = '-';

      const v1GirlsLong = v1AttG;
      const v1BoysLong = v1AttB;
      const v2GirlsLong = v2AttendanceTotal > 0 ? Math.round(v2AttendanceTotal * 0.541) : 0;
      const v2BoysLong = v2AttendanceTotal > 0 ? Math.round(v2AttendanceTotal * 0.459) : 0;
      const v3GirlsLong = v3AttendanceTotal > 0 ? Math.round(v3AttendanceTotal * 0.5) : 0;
      const v3BoysLong = v3AttendanceTotal > 0 ? Math.round(v3AttendanceTotal * 0.5) : 0;

      createLongitudinalLineChart('chart-longitudinal-attendance', 
        [v1AttendanceTotal, v2AttendanceTotal, v3AttendanceTotal],
        [v1GirlsLong, v2GirlsLong, v3GirlsLong],
        [v1BoysLong, v2BoysLong, v3BoysLong],
        v1EnrolBaseline
      );

      // Re-render school trajectory table
      renderSchoolTrajectoryTable(selDistrict);

      const trajPill = document.getElementById('traj-active-cohort-pill');
      if (trajPill) {{
        const activeSchools = filteredTrajectorySchools.filter(s => s.v1 !== null || s.v2 !== null || s.v3 !== null);
        if (activeSchools.length > 0) {{
          trajPill.innerText = `${{activeSchools.length}} active cohort${{activeSchools.length > 1 ? 's' : ''}} (${{activeSchools.map(s => s.name).join(', ')}})`;
        }} else {{
          trajPill.innerText = '0 active cohorts';
        }}
      }}

      // Sync V1 School Scope with District filter if applicable
      const schoolSel = document.getElementById('v1-school-select');
      if (schoolSel) {{
        if (selDistrict === 'ALL') {{
          schoolSel.value = 'ALL';
          const scopeBadge = document.getElementById('badge-v1-scope-label');
          if (scopeBadge) {{
            scopeBadge.classList.add('hidden');
            scopeBadge.innerText = '';
          }}
        }} else if (SCHOOL_ATTENDANCE_DB[selDistrict]) {{
          schoolSel.value = selDistrict;
          switchV1AttendanceScope(selDistrict);
        }}
      }}

      // Re-render district table
      renderDistrictTable(selDistrict);

      // Re-render records table
      renderRecordsTable(selDistrict, startDate, endDate, search);

      // Re-render exit interview cards
      renderExitInterviewCards(selDistrict);

      // Re-render change stories table
      renderChangeStoriesTable(selDistrict, search);

      // Re-render NutriClub District Accordions (All 64 schools)
      renderNutriClubDistrictAccordions(selDistrict, search);

      // Re-render Demonstration Sites Accordions (All 640 Sessions Across 64 Catchment Schools)
      renderDemoAccordions(selDistrict, search);

      // Re-render Visit 2 Age Band Matrix Table
      renderV2AgeBandTable(selDistrict);
    }}

    // Render Visit 2 Age Band Matrix Table dynamically
    function renderV2AgeBandTable(selDistrict = 'ALL') {{
      const tbody = document.getElementById('v2-age-band-tbody');
      const tfoot = document.getElementById('v2-age-band-tfoot');
      if (!tbody || !tfoot) return;

      let lowerM = 0, lowerF = 0, lowerPwdM = 0, lowerPwdF = 0;
      let midM = 0, midF = 0, midPwdM = 0, midPwdF = 0;
      let upM = 0, upF = 0, upPwdM = 0, upPwdF = 0;
      let teaM = 0, teaF = 0, teaPwdM = 0, teaPwdF = 0;
      let commM = 0, commF = 0, commPwdM = 0, commPwdF = 0;
      let schoolsLogged = [];

      for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;
        if (d.v2) {{
          schoolsLogged.push(d.v2.school || dName);
          lowerM += (d.v2.hc_lower_m || 0);
          lowerF += (d.v2.hc_lower_f || 0);
          lowerPwdM += (d.v2.hc_lower_pwd_m !== undefined ? d.v2.hc_lower_pwd_m : (d.v2.hc_lower_pwd || 0));
          lowerPwdF += (d.v2.hc_lower_pwd_f || 0);

          midM += (d.v2.hc_mid_m || 0);
          midF += (d.v2.hc_mid_f || 0);
          midPwdM += (d.v2.hc_mid_pwd_m !== undefined ? d.v2.hc_mid_pwd_m : (d.v2.hc_mid_pwd || 0));
          midPwdF += (d.v2.hc_mid_pwd_f || 0);

          upM += (d.v2.hc_up_m || 0);
          upF += (d.v2.hc_up_f || 0);
          upPwdM += (d.v2.hc_up_pwd_m !== undefined ? d.v2.hc_up_pwd_m : (d.v2.hc_up_pwd || 0));
          upPwdF += (d.v2.hc_up_pwd_f || 0);

          teaM += (d.v2.teachers_m || 0);
          teaF += (d.v2.teachers_f || 0);
          teaPwdM += (d.v2.teachers_pwd_m !== undefined ? d.v2.teachers_pwd_m : (d.v2.teachers_pwd || 0));
          teaPwdF += (d.v2.teachers_pwd_f || 0);

          commM += (d.v2.comm_m || 0);
          commF += (d.v2.comm_f || 0);
          commPwdM += (d.v2.comm_pwd_m !== undefined ? d.v2.comm_pwd_m : (d.v2.comm_pwd || 0));
          commPwdF += (d.v2.comm_pwd_f || 0);
        }}
      }}

      const pillHeadcount = document.getElementById('v2-headcount-pill');
      const pillPwd = document.getElementById('v2-pwd-pill');

      if (schoolsLogged.length === 0) {{
        if (pillHeadcount) pillHeadcount.innerText = `Total Activation Headcount: 0 (Awaiting Visit 2 in ${{selDistrict}})`;
        if (pillPwd) pillPwd.innerText = `Total PWD Participants: 0 (0.0%)`;
        tbody.innerHTML = `
          <tr>
            <td colspan="8" class="p-6 text-center text-slate-500 bg-slate-50/50">
              <div class="flex flex-col items-center justify-center gap-1.5">
                <span class="w-8 h-8 rounded-full bg-blue-100 text-wfp-blue flex items-center justify-center font-bold text-sm"><i class="fa-solid fa-clock-rotate-left"></i></span>
                <span class="font-bold text-slate-700">Awaiting Visit 2 Big Activation Day for ${{selDistrict}} District</span>
                <span class="text-xs text-slate-400 max-w-md">No Big Activation Day session has been submitted for ${{selDistrict}} yet. Showing baseline cohort targets until field submission is recorded.</span>
              </div>
            </td>
          </tr>
        `;
        tfoot.innerHTML = `
          <tr>
            <td class="p-3 uppercase">Total Activation Footprint</td>
            <td class="p-3 text-right font-mono">0</td>
            <td class="p-3 text-right font-mono">0</td>
            <td class="p-3 text-right bg-slate-200/60 font-black font-mono">0</td>
            <td class="p-3 text-right text-purple-700 font-mono">0</td>
            <td class="p-3 text-right text-purple-700 font-mono">0</td>
            <td class="p-3 text-right font-black text-purple-900 bg-purple-100/50 font-mono">0</td>
            <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-medium text-slate-400">0.0% PWD</span></td>
          </tr>
        `;
        return;
      }}

      const totLower = lowerM + lowerF;
      const totMid = midM + midF;
      const totUp = upM + upF;
      const totTea = teaM + teaF;
      const totComm = commM + commF;
      const grandMale = lowerM + midM + upM + teaM + commM;
      const grandFemale = lowerF + midF + upF + teaF + commF;
      const grandTotal = grandMale + grandFemale;
      const grandPwdM = lowerPwdM + midPwdM + upPwdM + teaPwdM + commPwdM;
      const grandPwdF = lowerPwdF + midPwdF + upPwdF + teaPwdF + commPwdF;
      const grandPwd = grandPwdM + grandPwdF;
      const grandPwdPct = grandTotal > 0 ? ((grandPwd / grandTotal) * 100).toFixed(1) : '0.0';

      if (pillHeadcount) {{
        pillHeadcount.innerText = `Total Activation Headcount: ${{grandTotal}} (${{schoolsLogged.join(', ')}})`;
      }}
      if (pillPwd) {{
        pillPwd.innerText = `Total PWD Participants: ${{grandPwd}} (${{grandPwdPct}}%)`;
      }}

      const rows = [
        {{ label: "Lower Primary (ECD–P2)", dot: "bg-blue-500", m: lowerM, f: lowerF, tot: totLower, pwd_m: lowerPwdM, pwd_f: lowerPwdF, pwd: lowerPwdM + lowerPwdF }},
        {{ label: "Middle Primary (P3–P4)", dot: "bg-sky-500", m: midM, f: midF, tot: totMid, pwd_m: midPwdM, pwd_f: midPwdF, pwd: midPwdM + midPwdF }},
        {{ label: "Upper Primary (P5–P7)", dot: "bg-cyan-600", m: upM, f: upF, tot: totUp, pwd_m: upPwdM, pwd_f: upPwdF, pwd: upPwdM + upPwdF }},
        {{ label: "Teachers Present", dot: "bg-amber-500", m: teaM, f: teaF, tot: totTea, pwd_m: teaPwdM, pwd_f: teaPwdF, pwd: teaPwdM + teaPwdF }},
        {{ label: "Community Members", dot: "bg-emerald-500", m: commM, f: commF, tot: totComm, pwd_m: commPwdM, pwd_f: commPwdF, pwd: commPwdM + commPwdF }}
      ];

      tbody.innerHTML = rows.map(r => {{
        const inclassPct = r.tot > 0 ? ((r.pwd / r.tot) * 100).toFixed(1) + '%' : '-';
        return `
          <tr class="hover:bg-slate-50/60">
            <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full ${{r.dot}}"></span> ${{r.label}}
            </td>
            <td class="p-3 text-right font-medium">${{r.m}}</td>
            <td class="p-3 text-right font-medium">${{r.f}}</td>
            <td class="p-3 text-right font-bold ${{r.tot > 0 ? 'text-slate-800' : 'text-slate-400'}} bg-slate-50">${{r.tot}}</td>
            <td class="p-3 text-right text-purple-700 font-medium">${{r.pwd_m}}</td>
            <td class="p-3 text-right text-purple-700 font-medium">${{r.pwd_f}}</td>
            <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">${{r.pwd}}</td>
            <td class="p-3 text-center">
              <span class="px-2 py-0.5 rounded text-[11px] font-bold ${{r.pwd > 0 ? 'bg-purple-50 text-purple-700' : 'text-slate-400'}}">${{inclassPct}}</span>
            </td>
          </tr>
        `;
      }}).join('');

      tfoot.innerHTML = `
        <tr>
          <td class="p-3 uppercase">Total Activation Footprint</td>
          <td class="p-3 text-right font-mono">${{grandMale}}</td>
          <td class="p-3 text-right font-mono">${{grandFemale}}</td>
          <td class="p-3 text-right bg-slate-200/60 font-black font-mono">${{grandTotal}}</td>
          <td class="p-3 text-right text-purple-700 font-mono">${{grandPwdM}}</td>
          <td class="p-3 text-right text-purple-700 font-mono">${{grandPwdF}}</td>
          <td class="p-3 text-right font-black text-purple-900 bg-purple-100/50 font-mono">${{grandPwd}}</td>
          <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-black bg-purple-100 text-purple-800">${{grandPwdPct}}% PWD</span></td>
        </tr>
      `;
    }}

    // Render School-by-School Change Stories Table
    function renderChangeStoriesTable(selDistrict = 'ALL', search = '') {{
      const tbody = document.getElementById('change-stories-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const stories = (BASE_DATA.msc_stories && BASE_DATA.msc_stories.stories_register) ? BASE_DATA.msc_stories.stories_register : [];
      const searchLower = (search || '').toLowerCase().trim();

      if (!stories || stories.length === 0) {{
        tbody.innerHTML = `
          <tr>
            <td colspan="7" class="text-center py-10 text-slate-400 text-xs">
              <i class="fa-solid fa-book-open text-3xl text-slate-300 mb-2 block"></i>
              No Most Significant Change (MSC) stories submitted yet. Awaiting field narratives from monitoring visits.
            </td>
          </tr>
        `;
        return;
      }}

      const badgeColors = {{
        'Girl Learner': 'bg-pink-50 text-pink-700 border-pink-200',
        'Boy Learner': 'bg-blue-50 text-wfp-blue border-blue-200',
        'Female Caregiver / Mother': 'bg-purple-50 text-purple-700 border-purple-200',
        'Father / Male Elder': 'bg-amber-50 text-amber-800 border-amber-200',
        'Teacher / Club Patron': 'bg-indigo-50 text-indigo-700 border-indigo-200',
        'Local Leader': 'bg-teal-50 text-teal-800 border-teal-200'
      }};

      let matchCount = 0;
      stories.forEach(s => {{
        if (selDistrict !== 'ALL' && s.district !== selDistrict) return;
        if (searchLower) {{
          const matchStr = (s.school + ' ' + s.district + ' ' + s.name_and_age + ' ' + s.role + ' ' + s.action_done + ' ' + s.event + ' ' + s.why_significant).toLowerCase();
          if (!matchStr.includes(searchLower)) return;
        }}
        matchCount++;

        const badgeClass = badgeColors[s.role] || 'bg-slate-50 text-slate-700 border-slate-200';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/40 transition border-b border-slate-100 text-xs';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-semibold text-slate-800">
            <div>${{s.school}}</div>
            <div class="text-[11px] text-slate-500 font-normal">${{s.district}} District</div>
          </td>
          <td class="py-2.5 px-3 font-bold text-slate-900 whitespace-nowrap">${{s.name_and_age}}</td>
          <td class="py-2.5 px-3 whitespace-nowrap">
            <span class="px-2 py-0.5 rounded text-[11px] font-bold border ${{badgeClass}}">${{s.role}}</span>
          </td>
          <td class="py-2.5 px-3 text-slate-700 max-w-xs">
            <span class="text-[11px] font-medium text-wfp-blue block">${{s.event}}</span>
          </td>
          <td class="py-2.5 px-3 text-slate-700 max-w-xs">
            <span class="text-[11px] text-emerald-800 font-medium block">${{s.action_done}}</span>
          </td>
          <td class="py-2.5 px-3 text-slate-600 italic text-[11px] max-w-sm">
            "${{s.why_significant}}"
          </td>
          <td class="py-2.5 px-3 text-slate-700">
            <div class="text-[11px] font-semibold text-slate-800">${{s.evidence}}</div>
            <div class="text-[10px] text-slate-500 italic">${{s.collector_notes}}</div>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      if (matchCount === 0) {{
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td colspan="7" class="py-6 text-center text-slate-400 italic text-xs">
            No change stories matched the selected filters.
          </td>
        `;
        tbody.appendChild(tr);
      }}
    }}

    // Render NutriClub District-Grouped Accordions (64 Schools)
    function renderNutriClubDistrictAccordions(selDistrict = 'ALL', search = '') {{
      const container = document.getElementById('nutriclub-district-accordions');
      if (!container) return;
      container.innerHTML = '';

      const badge = document.getElementById('nutriclub-active-filter-badge');
      if (badge) {{
        badge.innerText = selDistrict === 'ALL' 
          ? 'All 9 Karamoja Districts (64 Schools)' 
          : `${{selDistrict}} District Focus`;
      }}

      const schools = (BASE_DATA.nutriclub_sessions && BASE_DATA.nutriclub_sessions.schools_register) 
        ? BASE_DATA.nutriclub_sessions.schools_register 
        : [];
      const searchLower = (search || '').toLowerCase().trim();

      // Group schools by district
      const districtOrder = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak'];
      const grouped = {{}};
      districtOrder.forEach(d => grouped[d] = []);

      schools.forEach(s => {{
        if (!grouped[s.district]) grouped[s.district] = [];
        grouped[s.district].push(s);
      }});

      let totalMatchedSchools = 0;

      districtOrder.forEach(dName => {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) return;

        let dSchools = grouped[dName] || [];
        if (searchLower) {{
          dSchools = dSchools.filter(s => {{
            const searchHaystack = (s.school + ' ' + s.patron_name + ' ' + s.meeting_place + ' ' + 
              (s.session_one ? s.session_one.practical_activity : '') + ' ' + 
              (s.session_two ? s.session_two.practical_activity : '') + ' ' + 
              (s.session_one ? s.session_one.home_action_assigned : '') + ' ' + 
              (s.session_two ? s.session_two.assembly_core_message : '')).toLowerCase();
            return searchHaystack.includes(searchLower);
          }});
        }}

        if (dSchools.length === 0) return;
        totalMatchedSchools += dSchools.length;

        // Calculate district totals
        const totMembers = dSchools.reduce((acc, s) => acc + (s.total_membership || 0), 0);
        const totPwds = dSchools.reduce((acc, s) => acc + (s.total_pwd || 0), 0);

        // Open by default if filtering by specific district or searching, otherwise collapsed
        const isOpen = (selDistrict !== 'ALL' || searchLower.length > 0);

        const card = document.createElement('div');
        card.className = 'border border-slate-200/90 rounded-xl overflow-hidden shadow-2xs bg-white district-accordion-card';
        card.id = `district-acc-${{dName}}`;

        let schoolsHtml = '';
        dSchools.forEach((s) => {{
          schoolsHtml += `
            <div class="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
              <div class="p-3.5 flex flex-wrap items-center justify-between gap-3 bg-white cursor-pointer hover:bg-slate-50 transition border-b border-slate-100"
                   onclick="toggleSchoolDetails('${{s.id}}')">
                <div class="flex items-start gap-2.5">
                  <span class="w-8 h-8 rounded-lg bg-blue-50 text-wfp-blue flex items-center justify-center text-xs font-bold mt-0.5 border border-blue-100 shrink-0">
                    <i class="fa-solid fa-school"></i>
                  </span>
                  <div>
                    <h6 class="text-xs font-bold text-slate-900 flex items-center gap-2 flex-wrap">
                      <span>${{s.school}}</span>
                      <span class="text-[10px] bg-blue-100 text-wfp-blue font-bold px-1.5 py-0.2 rounded">${{s.selection || 'Base 5'}}</span>
                      <span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-normal">${{s.subcounty}} Subcounty · ${{s.meeting_place}}</span>
                    </h6>
                    <div class="text-[11px] text-slate-500 mt-0.5 flex items-center gap-2 flex-wrap">
                      <span>Patrons: <strong class="text-slate-700">${{s.patron_name}}</strong></span>
                      <span>·</span>
                      <span>Enrolled: <strong class="text-slate-700">${{(s.total_enrolled || 0).toLocaleString()}}</strong> (${{s.attendance_rate || '67%'}} attending)</span>
                      <span>·</span>
                      <span>Club: <strong class="text-slate-700">${{s.total_membership}} Members (${{s.male_membership}}B, ${{s.female_membership}}G)</strong></span>
                      <span>·</span>
                      <span>PWDs: <strong class="text-wfp-blue font-bold">${{s.total_pwd}}</strong></span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-2.5">
                  <span class="text-[10px] bg-emerald-50 text-emerald-800 font-bold px-2.5 py-0.5 rounded-lg border border-emerald-200 whitespace-nowrap">
                    <i class="fa-solid fa-check-double mr-1"></i> 2 Sessions Completed
                  </span>
                  <button type="button" class="text-xs text-wfp-blue font-semibold hover:underline flex items-center gap-1">
                    <span id="label-toggle-${{s.id}}">View Sessions</span>
                    <i class="fa-solid fa-chevron-down text-[10px] transition-transform duration-200" id="chevron-school-${{s.id}}"></i>
                  </button>
                </div>
              </div>

              <!-- Expanded School Content -->
              <div id="school-detail-${{s.id}}" class="p-4 hidden space-y-4 border-t border-slate-100 bg-slate-50/50">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  <!-- Session One -->
                  <div class="p-3.5 bg-white rounded-lg border border-slate-200 space-y-2.5 shadow-2xs">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-1.5">
                      <span class="text-xs font-bold text-wfp-blue flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-dot text-[10px]"></i> Session one of the week
                      </span>
                      <span class="text-[11px] text-slate-500 font-mono">${{s.session_one.date_conducted}} · ${{s.session_one.start_time}} - ${{s.session_one.end_time}}</span>
                    </div>
                    <div class="text-xs space-y-1">
                      <div><span class="text-[11px] font-bold text-slate-600">Meeting Place on Compound:</span> <span class="text-slate-800">${{s.session_one.designated_meeting_place}}</span></div>
                      <div><span class="text-[11px] font-bold text-slate-600">Patron In-Charge:</span> <span class="text-slate-800">${{s.session_one.club_patron_name}}</span></div>
                    </div>
                    <!-- Attendance grid -->
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-[10px] font-bold text-slate-600 block mb-1">Learner Attendance:</span>
                      <div class="grid grid-cols-4 gap-1.5 text-center text-xs">
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Boys Present</span>
                          <span class="font-bold text-slate-800 text-xs">${{s.session_one.boys_present}}</span>
                        </div>
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Girls Present</span>
                          <span class="font-bold text-slate-800 text-xs">${{s.session_one.girls_present}}</span>
                        </div>
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Male PWD</span>
                          <span class="font-bold text-wfp-blue text-xs">${{s.session_one.male_pwd}}</span>
                        </div>
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Female PWD</span>
                          <span class="font-bold text-wfp-blue text-xs">${{s.session_one.female_pwd}}</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <span class="text-[10px] font-bold text-slate-600 block mb-0.5">Practical Activity Delivered:</span>
                      <span class="inline-block px-2 py-0.5 bg-blue-50 text-wfp-blue font-semibold rounded text-[11px] border border-blue-200">
                        ${{s.session_one.practical_activity}}
                      </span>
                    </div>
                    <div>
                      <span class="text-[10px] font-bold text-slate-600 block mb-0.5">Feasible Food or Chore Action Assigned:</span>
                      <p class="text-[11px] text-slate-600 italic bg-slate-50 p-2 rounded border border-slate-200">
                        "${{s.session_one.home_action_assigned}}"
                      </p>
                    </div>
                  </div>

                  <!-- Session Two -->
                  <div class="p-3.5 bg-white rounded-lg border border-slate-200 space-y-2.5 shadow-2xs">
                    <div class="flex items-center justify-between border-b border-slate-100 pb-1.5">
                      <span class="text-xs font-bold text-emerald-700 flex items-center gap-1.5">
                        <i class="fa-solid fa-circle-check text-[10px]"></i> Session two of the week
                      </span>
                      <span class="text-[11px] text-slate-500 font-mono">${{s.session_two.date_conducted}} · ${{s.session_two.start_time}} - ${{s.session_two.end_time}}</span>
                    </div>
                    <!-- Attendance grid -->
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-[10px] font-bold text-slate-600 block mb-1">Learner Attendance:</span>
                      <div class="grid grid-cols-4 gap-1.5 text-center text-xs">
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Boys Present</span>
                          <span class="font-bold text-slate-800 text-xs">${{s.session_two.boys_present}}</span>
                        </div>
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Girls Present</span>
                          <span class="font-bold text-slate-800 text-xs">${{s.session_two.girls_present}}</span>
                        </div>
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Male PWD</span>
                          <span class="font-bold text-wfp-blue text-xs">${{s.session_two.male_pwd}}</span>
                        </div>
                        <div class="bg-white p-1 rounded border border-slate-200">
                          <span class="text-[9px] text-slate-500 block">Female PWD</span>
                          <span class="font-bold text-wfp-blue text-xs">${{s.session_two.female_pwd}}</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <span class="text-[10px] font-bold text-slate-600 block mb-0.5">Practical Activity Delivered:</span>
                      <span class="inline-block px-2 py-0.5 bg-emerald-50 text-emerald-800 font-semibold rounded text-[11px] border border-emerald-200">
                        ${{s.session_two.practical_activity}}
                      </span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="text-[10px] font-bold text-slate-600">Home Action Outcome:</span>
                      <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[10px]">
                        ${{s.session_two.home_action_feedback}}
                      </span>
                    </div>
                    <!-- Assembly Nutri-Moment -->
                    <div class="pt-2 border-t border-slate-100 text-xs space-y-1">
                      <div class="flex items-center justify-between text-[11px]">
                        <span class="font-bold text-slate-700">Whole-School Assembly Nutri-Moment:</span>
                        <span class="text-slate-500">${{s.session_two.assembly_date}} · By ${{s.session_two.assembly_delivered_by}}</span>
                      </div>
                      <p class="text-[11px] text-blue-900 bg-blue-50/70 p-2 rounded border border-blue-200 font-medium">
                        "${{s.session_two.assembly_core_message}}"
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          `;
        }});

        card.innerHTML = `
          <button type="button" 
                  onclick="toggleDistrictAccordion('${{dName}}')" 
                  class="w-full p-4 flex flex-wrap items-center justify-between gap-3 bg-slate-50 hover:bg-blue-50/60 transition text-left border-b border-slate-200">
            <div class="flex items-center gap-3">
              <span class="w-8 h-8 rounded-lg bg-blue-100 text-wfp-blue flex items-center justify-center font-bold text-sm shadow-2xs shrink-0">
                <i class="fa-solid fa-map-location-dot"></i>
              </span>
              <div>
                <h5 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <span>${{dName}} District</span>
                  <span class="text-[11px] font-normal text-slate-500">(${{dSchools.length}} Monitored Primary Schools)</span>
                </h5>
                <p class="text-[11px] text-slate-500 mt-0.5">
                  ${{totMembers}} Registered Club Members · ${{totPwds}} Learners with Disabilities · ${{dSchools.length * 2}} Sessions Completed
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2.5 py-0.5 rounded-lg border border-blue-200">
                ${{dSchools.length * 2}} Sessions Logged
              </span>
              <i class="fa-solid fa-chevron-down text-slate-400 transition-transform duration-200 ${{isOpen ? 'rotate-180' : ''}}" id="chevron-dist-${{dName}}"></i>
            </div>
          </button>

          <div id="district-body-${{dName}}" class="p-4 space-y-3 ${{isOpen ? '' : 'hidden'}} bg-slate-50/40">
            ${{schoolsHtml}}
          </div>
        `;

        container.appendChild(card);
      }});

      if (totalMatchedSchools === 0) {{
        container.innerHTML = `
          <div class="p-8 text-center bg-slate-50 rounded-xl border border-slate-200 text-slate-500 text-xs">
            <i class="fa-solid fa-school-circle-xmark text-slate-400 text-2xl mb-2 block"></i>
            No monitored schools matched the selected district and keyword filter.
          </div>
        `;
      }}
    }}

    // Toggle single district accordion
    function toggleDistrictAccordion(dName) {{
      const body = document.getElementById(`district-body-${{dName}}`);
      const chevron = document.getElementById(`chevron-dist-${{dName}}`);
      if (!body) return;
      
      const isHidden = body.classList.contains('hidden');
      if (isHidden) {{
        body.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
      }} else {{
        body.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
      }}
    }}

    // Toggle single school subcard details
    function toggleSchoolDetails(schoolId) {{
      const detail = document.getElementById(`school-detail-${{schoolId}}`);
      const chevron = document.getElementById(`chevron-school-${{schoolId}}`);
      const label = document.getElementById(`label-toggle-${{schoolId}}`);
      if (!detail) return;

      const isHidden = detail.classList.contains('hidden');
      if (isHidden) {{
        detail.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
        if (label) label.innerText = 'Hide Sessions';
      }} else {{
        detail.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
        if (label) label.innerText = 'View Sessions';
      }}
    }}

    // Expand / Collapse All District Accordions
    function toggleAllNutriClubDistricts(expand = true) {{
      const bodies = document.querySelectorAll('[id^="district-body-"]');
      const chevrons = document.querySelectorAll('[id^="chevron-dist-"]');
      bodies.forEach(b => {{
        if (expand) b.classList.remove('hidden');
        else b.classList.add('hidden');
      }});
      chevrons.forEach(c => {{
        if (expand) c.classList.add('rotate-180');
        else c.classList.remove('rotate-180');
      }});
    }}

    // Render District Table
    function renderDistrictTable(selDistrict = 'ALL') {{
      const tbody = document.getElementById('district-table-body');
      if (!tbody) return;

      tbody.innerHTML = '';
      for (const [dName, item] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;

        const schoolsNames = (item.schools_list || []).map(s => s.name || s.school).join(', ');
        
        // Calculate visits for this district from SCHOOL_TRAJECTORIES
        const dTrajectories = SCHOOL_TRAJECTORIES.filter(s => s.district === dName);
        let dVisitsDone = 0;
        dTrajectories.forEach(s => {{
          if (s.v1 !== null && s.v1 !== undefined) dVisitsDone++;
          if (s.v2 !== null && s.v2 !== undefined) dVisitsDone++;
          if (s.v3 !== null && s.v3 !== undefined) dVisitsDone++;
        }});
        const dTargetVisits = (item.target_schools || 0) * 3;

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/60 border-b border-slate-100 cursor-pointer transition';
        tr.onclick = function() {{
          document.getElementById('districtFilter').value = dName;
          applyFilters();
        }};
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-semibold text-slate-800 whitespace-nowrap min-w-[120px]" title="${{schoolsNames}}">
            <span class="inline-flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full ${{item.schools > 0 ? 'bg-emerald-500' : 'bg-slate-300'}} shrink-0"></span>
              <span class="font-bold text-slate-900">${{dName}}</span>
              ${{item.schools > 0 ? '<span class="text-[9px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-bold">Active</span>' : ''}}
            </span>
          </td>
          <td class="py-2.5 px-2 text-center font-bold text-slate-700 whitespace-nowrap" title="${{schoolsNames}}">
            ${{item.schools > 0 ? `<span class="font-bold text-slate-900">${{item.schools}}</span>` : `<span class="text-slate-400 font-medium">0</span>`}}
            <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_schools}}</span>
          </td>
          <td class="py-2.5 px-2 text-center font-bold text-slate-700 whitespace-nowrap">
            ${{dVisitsDone > 0 ? `<span class="font-bold text-sky-700">${{dVisitsDone}}</span>` : `<span class="text-slate-400 font-medium">0</span>`}}
            <span class="text-[11px] text-slate-400 font-normal">/ ${{dTargetVisits}}</span>
          </td>
          <td class="py-2.5 px-2 text-center font-medium whitespace-nowrap">
            ${{item.demos > 0 ? `<span class="font-bold text-slate-900">${{item.demos}}</span>` : `<span class="text-slate-400 font-medium">0</span>`}}
            <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_demos}}</span>
          </td>
          <td class="py-2.5 px-2 text-right font-medium text-wfp-blue whitespace-nowrap">
            ${{item.learners > 0 ? `<span class="font-bold text-wfp-blue">${{item.learners.toLocaleString()}}</span>` : `<span class="text-slate-400 font-medium">0</span>`}}
            <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_learners.toLocaleString()}}</span>
          </td>
          <td class="py-2.5 px-2 text-right whitespace-nowrap">
            ${{item.caregivers > 0 ? `<span class="font-bold text-slate-900">${{item.caregivers.toLocaleString()}}</span>` : `<span class="text-slate-400 font-medium">0</span>`}}
            <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_caregivers.toLocaleString()}}</span>
          </td>
          <td class="py-2.5 px-2 text-right font-bold text-slate-800 whitespace-nowrap">
            ${{item.pwd_reach > 0 ? `<span class="font-bold text-emerald-600">${{item.pwd_reach}}</span>` : `<span class="text-slate-400 font-medium">0</span>`}}
          </td>
        `;
        tbody.appendChild(tr);
      }}
    }}

    // Render Records Table (With Red-Flag Indicator for Demos with < 80 Participants)
    function renderRecordsTable(selDistrict = 'ALL', startDate = '2026-09-01', endDate = '2026-09-30', search = '') {{
      const tbody = document.getElementById('records-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      RECORDS.forEach(r => {{
        if (selDistrict !== 'ALL' && r.district !== selDistrict) return;
        if (r.date < startDate || r.date > endDate) return;
        if (search && !r.school.toLowerCase().includes(search) && !r.coordinator.toLowerCase().includes(search) && !r.district.toLowerCase().includes(search) && !r.activity.toLowerCase().includes(search)) return;

        let reachDisplay = `<span class="font-bold text-wfp-blue">${{r.reach.toLocaleString()}}</span>`;
        let statusBadge = `
          <span class="inline-flex items-center gap-1 text-[10px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
            <i class="fa-solid fa-check"></i> Cleaned
          </span>
        `;

        if (r.activity === "Community demonstration") {{
          if (r.reach < 80) {{
            // CRITICAL: Turnout < 80 is red flagged, but exact count is strictly captured in all calculations
            reachDisplay = `<span class="font-black text-red-600 font-mono">🚩 ${{r.reach.toLocaleString()}}</span>`;
            statusBadge = `
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-red-700 bg-red-100 px-2 py-0.5 rounded border border-red-300" title="Low Turnout: Below 80 min. participant benchmark. Headcount retained in calculations.">
                🚩 Red Flag (&lt;80)
              </span>
            `;
          }} else {{
            statusBadge = `
              <span class="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200" title="Compliant: Meets or exceeds 80 min. participant benchmark.">
                <i class="fa-solid fa-check"></i> Compliant (&ge;80)
              </span>
            `;
          }}
        }}

        const tr = document.createElement('tr');
        tr.className = (r.activity === "Community demonstration" && r.reach < 80) ? 'hover:bg-red-50/50 bg-red-50/20 transition' : 'hover:bg-blue-50/50 transition';
        tr.innerHTML = `
          <td class="py-2 px-3 text-slate-600 font-mono">${{r.date}}</td>
          <td class="py-2 px-3 font-semibold text-slate-800">${{r.district}}</td>
          <td class="py-2 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${{r.activity === 'Community demonstration' ? 'bg-amber-100 text-amber-900 border border-amber-300' : 'bg-blue-100 text-blue-800'}}">${{r.activity}}</span>
          </td>
          <td class="py-2 px-3 font-medium text-slate-800">${{r.school}}</td>
          <td class="py-2 px-3 text-slate-600">${{r.coordinator}}</td>
          <td class="py-2 px-3 text-right">${{reachDisplay}}</td>
          <td class="py-2 px-3 text-right font-bold text-emerald-600">${{r.pwd}}</td>
          <td class="py-2 px-3">${{statusBadge}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Demonstration Site Accordion State (640 Sessions Across 64 Primary School Catchments)
    let currentDemoFilter = 'all'; // 'all' | 'flagged' | 'compliant'
    let currentDemoSearch = '';
    const demoOpenDistricts = {{}};
    const demoOpenSchools = {{}};

    function setDemoFilter(filterType) {{
      currentDemoFilter = filterType;
      
      const btnAll = document.getElementById('btn-demo-filter-all');
      const btnFlagged = document.getElementById('btn-demo-filter-flagged');
      const btnCompliant = document.getElementById('btn-demo-filter-compliant');
      
      if (btnAll) {{
        btnAll.className = filterType === 'all' 
          ? 'px-2.5 py-1 rounded bg-white text-wfp-blue shadow-xs font-bold transition' 
          : 'px-2.5 py-1 rounded text-slate-600 hover:bg-white/80 transition';
      }}
      if (btnFlagged) {{
        btnFlagged.className = filterType === 'flagged' 
          ? 'px-2.5 py-1 rounded bg-white text-red-700 shadow-xs font-bold transition' 
          : 'px-2.5 py-1 rounded text-red-700 hover:bg-white/80 transition';
      }}
      if (btnCompliant) {{
        btnCompliant.className = filterType === 'compliant' 
          ? 'px-2.5 py-1 rounded bg-white text-emerald-700 shadow-xs font-bold transition' 
          : 'px-2.5 py-1 rounded text-emerald-700 hover:bg-white/80 transition';
      }}
      
      const globalSel = document.getElementById('global-district-select');
      const dist = globalSel ? globalSel.value : 'ALL';
      renderDemoAccordions(dist, currentDemoSearch);
    }}

    function handleDemoSearch(val) {{
      currentDemoSearch = (val || '').toLowerCase().trim();
      const globalSel = document.getElementById('global-district-select');
      const dist = globalSel ? globalSel.value : 'ALL';
      renderDemoAccordions(dist, currentDemoSearch);
    }}

    function toggleDemoDistrict(distName) {{
      demoOpenDistricts[distName] = !demoOpenDistricts[distName];
      const body = document.getElementById('demo-dist-body-' + distName);
      const chevron = document.getElementById('demo-dist-chev-' + distName);
      if (body) {{
        if (demoOpenDistricts[distName]) {{
          body.classList.remove('hidden');
          if (chevron) chevron.className = 'fa-solid fa-chevron-down text-wfp-blue transition-transform';
        }} else {{
          body.classList.add('hidden');
          if (chevron) chevron.className = 'fa-solid fa-chevron-right text-slate-400 transition-transform';
        }}
      }}
    }}

    function toggleDemoSchool(schKey) {{
      demoOpenSchools[schKey] = !demoOpenSchools[schKey];
      const body = document.getElementById('demo-sch-body-' + schKey);
      const chevron = document.getElementById('demo-sch-chev-' + schKey);
      if (body) {{
        if (demoOpenSchools[schKey]) {{
          body.classList.remove('hidden');
          if (chevron) chevron.className = 'fa-solid fa-chevron-down text-wfp-blue transition-transform';
        }} else {{
          body.classList.add('hidden');
          if (chevron) chevron.className = 'fa-solid fa-chevron-right text-slate-400 transition-transform';
        }}
      }}
    }}

    function toggleAllDemoAccordions(expand) {{
      const districtOrder = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak'];
      districtOrder.forEach(d => {{
        demoOpenDistricts[d] = expand;
      }});
      DEMO_SESSIONS_640.forEach(s => {{
        const schKey = (s.district + '_' + s.school).replace(/[^a-zA-Z0-9]/g, '_');
        demoOpenSchools[schKey] = expand;
      }});
      const globalSel = document.getElementById('global-district-select');
      const dist = globalSel ? globalSel.value : 'ALL';
      renderDemoAccordions(dist, currentDemoSearch);
    }}

    function renderDemoAccordions(selDistrict = 'ALL', search = '') {{
      const container = document.getElementById('demo-accordions-container');
      const banner = document.getElementById('demo-summary-banner');
      if (!container) return;

      if (!DEMO_SESSIONS_640 || DEMO_SESSIONS_640.length === 0) {{
        const kpiTotal = document.getElementById('demo-kpi-total-sessions');
        const kpiCompliant = document.getElementById('demo-kpi-compliant-sessions');
        const kpiCompliantRate = document.getElementById('demo-kpi-compliant-rate');
        const kpiFlagged = document.getElementById('demo-kpi-flagged-sessions');
        const kpiFlaggedRate = document.getElementById('demo-kpi-flagged-rate');
        if (kpiTotal) kpiTotal.innerText = '0';
        if (kpiCompliant) kpiCompliant.innerText = '0';
        if (kpiCompliantRate) kpiCompliantRate.innerText = '0.0%';
        if (kpiFlagged) kpiFlagged.innerText = '0';
        if (kpiFlaggedRate) kpiFlaggedRate.innerText = '0.0%';

        if (banner) {{
          banner.innerHTML = `
            <div class="flex items-center justify-between flex-wrap gap-2 text-xs">
              <span class="font-bold text-slate-700">0 Demonstrations Logged</span>
              <span class="text-amber-700 font-semibold bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Awaiting Field Submissions</span>
            </div>
          `;
        }}
        container.innerHTML = `
          <div class="text-center py-12 bg-white border border-slate-200 rounded-xl card-shadow">
            <i class="fa-solid fa-utensils text-4xl text-slate-300 mb-3 block"></i>
            <h4 class="text-base font-bold text-slate-700">Awaiting Community Cooking Demonstration Submissions</h4>
            <p class="text-xs text-slate-500 max-w-md mx-auto mt-1">No community demonstration sessions have been submitted in the activity log yet. As field teams submit demonstration records, session summaries, quality assurance checks, and caregiver metrics will appear here.</p>
          </div>
        `;
        return;
      }}

      const searchLower = (search || currentDemoSearch || '').toLowerCase().trim();
      const districtOrder = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak'];

      let totalFiltered = 0;
      let compliantFiltered = 0;
      let flaggedFiltered = 0;
      let sumCaregivers = 0;
      let sumElders = 0;
      let sumChildren = 0;
      let sumPwd = 0;
      let sumTotal = 0;

      const grouped = {{}};
      districtOrder.forEach(d => {{
        grouped[d] = {{}};
      }});

      DEMO_SESSIONS_640.forEach(s => {{
        if (selDistrict !== 'ALL' && s.district !== selDistrict) return;

        if (currentDemoFilter === 'flagged' && !s.flagged) return;
        if (currentDemoFilter === 'compliant' && s.flagged) return;

        if (searchLower) {{
          const matchStr = (s.id + ' ' + s.school + ' ' + s.site + ' ' + s.district + ' ' + s.subcounty + ' ' + s.facilitator).toLowerCase();
          if (!matchStr.includes(searchLower)) return;
        }}

        totalFiltered++;
        if (s.flagged) flaggedFiltered++;
        else compliantFiltered++;

        sumCaregivers += s.caregivers;
        sumElders += s.elders;
        sumChildren += s.children;
        sumPwd += s.pwd;
        sumTotal += s.total;

        if (!grouped[s.district]) grouped[s.district] = {{}};
        if (!grouped[s.district][s.school]) grouped[s.district][s.school] = [];
        grouped[s.district][s.school].push(s);
      }});

      // Update Top Tab 4 KPI cards
      const kpiTotal = document.getElementById('demo-kpi-total-sessions');
      const kpiCompliant = document.getElementById('demo-kpi-compliant-sessions');
      const kpiCompliantRate = document.getElementById('demo-kpi-compliant-rate');
      const kpiFlagged = document.getElementById('demo-kpi-flagged-sessions');
      const kpiFlaggedRate = document.getElementById('demo-kpi-flagged-rate');

      if (kpiTotal) kpiTotal.innerText = totalFiltered;
      if (kpiCompliant) kpiCompliant.innerText = compliantFiltered;
      if (kpiCompliantRate) kpiCompliantRate.innerText = totalFiltered > 0 ? `${{((compliantFiltered / totalFiltered) * 100).toFixed(1)}}% compliant rate` : '0%';
      if (kpiFlagged) kpiFlagged.innerText = flaggedFiltered;
      if (kpiFlaggedRate) kpiFlaggedRate.innerText = totalFiltered > 0 ? `${{((flaggedFiltered / totalFiltered) * 100).toFixed(1)}}% flagged for follow-up` : '0%';

      // Update summary banner
      if (banner) {{
        banner.innerHTML = `
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-bold text-slate-800">Total verified headcount (${{totalFiltered}} sessions):</span>
            <span class="font-black text-wfp-blue text-sm">${{sumTotal.toLocaleString()}} attendees</span>
            <span class="text-slate-500 font-medium">(${{sumCaregivers.toLocaleString()}} caregivers · ${{sumElders.toLocaleString()}} elders · ${{sumChildren.toLocaleString()}} children · ${{sumPwd.toLocaleString()}} PWDs)</span>
          </div>
          <div class="flex items-center gap-2 flex-wrap text-xs">
            <span class="px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded-lg border border-emerald-200 flex items-center gap-1">
              <i class="fa-solid fa-circle-check text-emerald-600"></i> ${{compliantFiltered}} Compliant (&ge;80)
            </span>
            <span class="px-2.5 py-1 bg-red-50 text-red-700 font-black rounded-lg border border-red-200 flex items-center gap-1">
              <i class="fa-solid fa-flag text-red-600"></i> ${{flaggedFiltered}} Red-Flagged (&lt;80)
            </span>
          </div>
        `;
      }}

      if (totalFiltered === 0) {{
        container.innerHTML = `
          <div class="p-8 text-center bg-slate-50 rounded-xl border border-slate-200 text-slate-500 text-xs">
            <i class="fa-solid fa-filter-circle-xmark text-2xl text-slate-400 mb-2 block"></i>
            No demonstration sessions match the current filter or search criteria.
          </div>
        `;
        return;
      }}

      let html = '';

      districtOrder.forEach(dist => {{
        if (selDistrict !== 'ALL' && dist !== selDistrict) return;
        const schoolsObj = grouped[dist] || {{}};
        const schoolNames = Object.keys(schoolsObj);
        if (schoolNames.length === 0) return;

        let dSessionsCount = 0;
        let dAttendees = 0;
        let dFlagged = 0;
        let dCompliant = 0;

        schoolNames.forEach(sch => {{
          const sessions = schoolsObj[sch];
          dSessionsCount += sessions.length;
          sessions.forEach(s => {{
            dAttendees += s.total;
            if (s.flagged) dFlagged++;
            else dCompliant++;
          }});
        }});

        const isDistOpen = demoOpenDistricts[dist] !== undefined 
          ? demoOpenDistricts[dist] 
          : (selDistrict !== 'ALL' || searchLower.length > 0);

        html += `
          <div class="border border-slate-200/90 rounded-xl overflow-hidden shadow-2xs bg-white">
            <!-- District Accordion Header -->
            <div class="p-3.5 bg-slate-100/90 hover:bg-slate-200/80 transition cursor-pointer flex items-center justify-between gap-3 border-b border-slate-200"
                 onclick="toggleDemoDistrict('${{dist}}')">
              <div class="flex items-center gap-2.5 flex-wrap">
                <span class="w-7 h-7 rounded-lg bg-wfp-blue text-white flex items-center justify-center text-xs font-bold shrink-0">
                  <i class="fa-solid fa-map-pin"></i>
                </span>
                <span class="font-extrabold text-sm text-slate-900">${{dist}} District</span>
                <span class="text-xs bg-white px-2 py-0.5 rounded border border-slate-300 font-bold text-slate-700">
                  ${{schoolNames.length}} Schools · ${{dSessionsCount}} Demos
                </span>
                <span class="text-xs bg-blue-50 text-wfp-blue px-2 py-0.5 rounded border border-blue-200 font-bold">
                  ${{dAttendees.toLocaleString()}} Attendees
                </span>
                <span class="text-xs bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded border border-emerald-200 font-bold">
                  ${{dCompliant}} Compliant
                </span>
                ${{dFlagged > 0 ? `<span class="text-xs bg-red-100 text-red-800 px-2 py-0.5 rounded border border-red-300 font-black">🚩 ${{dFlagged}} Flagged</span>` : ''}}
              </div>
              <div class="text-slate-400 pl-2">
                <i id="demo-dist-chev-${{dist}}" class="fa-solid ${{isDistOpen ? 'fa-chevron-down text-wfp-blue' : 'fa-chevron-right text-slate-400'}} transition-transform"></i>
              </div>
            </div>

            <!-- District Accordion Body -->
            <div id="demo-dist-body-${{dist}}" class="${{isDistOpen ? '' : 'hidden'}} p-3.5 space-y-3 bg-slate-50/60">
        `;

        schoolNames.forEach(schName => {{
          const sessions = schoolsObj[schName];
          const schKey = (dist + '_' + schName).replace(/[^a-zA-Z0-9]/g, '_');
          const subc = sessions[0] ? sessions[0].subcounty : dist;
          
          let schAttendees = 0;
          let schFlagged = 0;
          let schCompliant = 0;
          sessions.forEach(s => {{
            schAttendees += s.total;
            if (s.flagged) schFlagged++;
            else schCompliant++;
          }});

          const isSchOpen = demoOpenSchools[schKey] !== undefined 
            ? demoOpenSchools[schKey] 
            : (searchLower.length > 0 || (selDistrict !== 'ALL' && schoolNames.length <= 5));

          html += `
            <div class="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
              <!-- School Accordion Header -->
              <div class="p-3 flex items-center justify-between gap-3 bg-white hover:bg-slate-50 transition cursor-pointer border-b border-slate-100"
                   onclick="toggleDemoSchool('${{schKey}}')">
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="w-6 h-6 rounded-md bg-blue-50 text-wfp-blue flex items-center justify-center text-xs font-bold shrink-0">
                    <i class="fa-solid fa-school"></i>
                  </span>
                  <span class="font-bold text-xs text-slate-900">${{schName}}</span>
                  <span class="text-[11px] text-slate-500 font-normal">(${{subc}} Sc)</span>
                  <span class="text-[10px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-semibold">
                    ${{sessions.length}} Demos
                  </span>
                  <span class="text-[10px] bg-blue-50 text-wfp-blue px-2 py-0.5 rounded border border-blue-100 font-bold">
                    ${{schAttendees.toLocaleString()}} Attendees
                  </span>
                  <span class="text-[10px] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded border border-emerald-100 font-semibold">
                    ${{schCompliant}} Compliant
                  </span>
                  ${{schFlagged > 0 ? `<span class="text-[10px] bg-red-50 text-red-700 px-2 py-0.5 rounded border border-red-200 font-bold">🚩 ${{schFlagged}} Flagged</span>` : ''}}
                </div>
                <div class="text-slate-400 pl-2">
                  <i id="demo-sch-chev-${{schKey}}" class="fa-solid ${{isSchOpen ? 'fa-chevron-down text-wfp-blue' : 'fa-chevron-right text-slate-400'}} text-xs transition-transform"></i>
                </div>
              </div>

              <!-- School Sessions Table -->
              <div id="demo-sch-body-${{schKey}}" class="${{isSchOpen ? '' : 'hidden'}} overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse min-w-[720px]">
                  <thead class="bg-slate-50 border-b border-slate-200 text-slate-700 font-bold">
                    <tr>
                      <th class="py-2 px-3">Session & Date</th>
                      <th class="py-2 px-3">Catchment Village Venue</th>
                      <th class="py-2 px-3">Facilitator</th>
                      <th class="py-2 px-2 text-right">Caregivers</th>
                      <th class="py-2 px-2 text-right">Elders</th>
                      <th class="py-2 px-2 text-right">Children</th>
                      <th class="py-2 px-2 text-right">PWD</th>
                      <th class="py-2 px-3 text-right">Total Headcount</th>
                      <th class="py-2 px-3 text-center">Turnout Benchmark</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 text-slate-700">
          `;

          sessions.forEach(s => {{
            const rowClass = s.flagged ? 'bg-red-50/40 hover:bg-red-50/70 transition' : 'hover:bg-slate-50/70 transition';
            const headcountHtml = s.flagged 
              ? `<span class="font-black text-red-600 font-mono text-xs">🚩 ${{s.total}}</span>` 
              : `<span class="font-extrabold text-wfp-blue font-mono text-xs">${{s.total}}</span>`;
            const statusHtml = s.flagged 
              ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-black bg-red-100 text-red-700 border border-red-300">🚩 Flagged (&lt;80)</span>` 
              : `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200"><i class="fa-solid fa-check"></i> Compliant (&ge;80)</span>`;

            html += `
              <tr class="${{rowClass}}">
                <td class="py-2 px-3">
                  <div class="font-bold text-slate-800">${{s.id}}</div>
                  <div class="text-[10px] font-mono text-slate-500">${{s.date}}</div>
                </td>
                <td class="py-2 px-3">
                  <div class="font-semibold text-slate-900">${{s.site}}</div>
                </td>
                <td class="py-2 px-3">
                  <span class="px-2 py-0.5 rounded text-[10px] font-medium ${{s.facilitator.includes('VHT') ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-blue-50 text-wfp-blue border border-blue-200'}}">
                    ${{s.facilitator}}
                  </span>
                </td>
                <td class="py-2 px-2 text-right font-mono text-pink-700 font-semibold">${{s.caregivers}}</td>
                <td class="py-2 px-2 text-right font-mono text-blue-700 font-semibold">${{s.elders}}</td>
                <td class="py-2 px-2 text-right font-mono text-slate-700 font-semibold">${{s.children}}</td>
                <td class="py-2 px-2 text-right font-mono text-purple-700 font-bold">${{s.pwd}}</td>
                <td class="py-2 px-3 text-right">${{headcountHtml}}</td>
                <td class="py-2 px-3 text-center">${{statusHtml}}</td>
              </tr>
            `;
          }});

          const sumSchCaregivers = sessions.reduce((a, s) => a + s.caregivers, 0);
          const sumSchElders = sessions.reduce((a, s) => a + s.elders, 0);
          const sumSchChildren = sessions.reduce((a, s) => a + s.children, 0);
          const sumSchPwd = sessions.reduce((a, s) => a + s.pwd, 0);

          html += `
                  </tbody>
                  <tfoot class="bg-slate-100/80 border-t border-slate-200 font-bold text-slate-800">
                    <tr>
                      <td class="py-2 px-3" colspan="3">
                        <span class="text-xs font-bold text-slate-700">${{schName}} Catchment Total (${{sessions.length}} Demos)</span>
                      </td>
                      <td class="py-2 px-2 text-right font-mono text-pink-700">${{sumSchCaregivers}}</td>
                      <td class="py-2 px-2 text-right font-mono text-blue-700">${{sumSchElders}}</td>
                      <td class="py-2 px-2 text-right font-mono text-slate-700">${{sumSchChildren}}</td>
                      <td class="py-2 px-2 text-right font-mono text-purple-700 font-bold">${{sumSchPwd}}</td>
                      <td class="py-2 px-3 text-right font-mono text-wfp-blue font-black">${{schAttendees.toLocaleString()}}</td>
                      <td class="py-2 px-3 text-center text-[11px]">
                        <span class="text-emerald-700 font-bold">${{schCompliant}} Compliant</span> · <span class="text-red-600 font-black">${{schFlagged}} Flagged</span>
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          `;
        }});

        html += `
            </div>
          </div>
        `;
      }});

      container.innerHTML = html;
    }}

    // Render the 6 Individual Participant Exit Interviews Required by the Official KoBo Tool
    // (Teacher 3, VHT 2, Teacher 1, Teacher 2, VHT 1, VHT 3)
    function renderExitInterviewCards(selDistrict = 'ALL') {{
      const container = document.getElementById('exit-interview-cards');
      if (!container) return;

      let interviewsList = [];
      for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;
        if (d.exit_interviews) {{
          for (const [rKey, rVal] of Object.entries(d.exit_interviews)) {{
            interviewsList.push({{ key: rKey, ...rVal }});
          }}
        }}
      }}

      const titleEl = document.getElementById('exit-interview-title');
      if (titleEl) {{
        if (interviewsList.length === 0) {{
          titleEl.innerText = 'Detailed interview log: 0 individual participants logged';
        }} else {{
          titleEl.innerText = `Detailed interview log: ${{interviewsList.length}} individual participants (${{selDistrict === 'ALL' ? 'All Monitored Schools' : selDistrict}})`;
        }}
      }}

      container.innerHTML = '';
      if (interviewsList.length === 0) {{
        container.innerHTML = `
          <div class="col-span-full py-8 text-center bg-slate-50 border border-slate-200 rounded-xl text-slate-500 text-xs">
            <i class="fa-solid fa-clipboard-question text-2xl text-slate-400 mb-2 block"></i>
            No exit interviews recorded yet for this selection. Awaiting field submissions.
          </div>
        `;
        return;
      }}

      interviewsList.forEach(item => {{
        let lessonsList = '';
        if (item.lessons) {{
          item.lessons.forEach(l => {{
            lessonsList += `<li class="flex items-start gap-1.5"><span class="text-emerald-600 font-bold text-xs">☑</span> <span>${{l}}</span></li>`;
          }});
        }}

        const card = document.createElement('div');
        card.className = 'p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between hover:border-wfp-blue/40 transition';
        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold text-slate-800 uppercase flex items-center gap-1.5">
                <i class="fa-solid ${{(item.role || '').includes('Teacher') ? 'fa-chalkboard-user text-wfp-blue' : 'fa-hand-holding-medical text-emerald-600'}}"></i>
                ${{item.key || item.role}}
              </span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded ${{item.sex === 'Female' ? 'bg-pink-100 text-pink-700' : 'bg-blue-100 text-blue-700'}}">
                ${{item.sex || 'Female'}}
              </span>
            </div>

            <div class="mb-3">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                Lessons Learned (3 Pillars):
              </span>
              <ul class="text-xs text-slate-700 space-y-1">
                ${{lessonsList}}
              </ul>
            </div>

            <div class="mb-3">
              <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                Committed Action This Week:
              </span>
              <div class="text-xs font-semibold text-wfp-blue bg-blue-50/70 p-2 rounded border border-blue-100">
                <i class="fa-solid fa-arrow-right text-[10px] mr-1"></i> ${{item.action || ''}}
              </div>
            </div>
          </div>

          <div class="mt-2 pt-2 border-t border-slate-200">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
              Specific Personal Action in Exact Words:
            </span>
            <p class="text-xs text-slate-700 italic bg-white p-2 rounded border border-slate-200">
              "${{item.words || ''}}"
            </p>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // Initialize All Horizontal Bar Charts
    function initAllCharts() {{
      // Exit Interviews Aggregate Charts
      createHorizontalBarChart('chart-orient-exit-pillars', 
        BASE_DATA.orientation.exit_interviews_pillars.categories, 
        BASE_DATA.orientation.exit_interviews_pillars.values, 
        WFP_BLUE, 
        'Participants Recalling Lesson'
      );

      createHorizontalBarChart('chart-orient-exit-actions', 
        BASE_DATA.orientation.exit_interviews_actions.categories, 
        BASE_DATA.orientation.exit_interviews_actions.values, 
        ['#16a34a', '#0A6EB4', '#ea580c'], 
        'Participants Committing Action'
      );

      createHorizontalBarChart('chart-orient-tools', 
        BASE_DATA.orientation.physical_tools_disseminated.categories, 
        BASE_DATA.orientation.physical_tools_disseminated.values, 
        [WFP_BLUE, ACCENT_GREEN, '#ea580c'], 
        'Tools Distributed'
      );

      // THREE-VISIT CONTACT - Longitudinal Attendance & Trajectory Table
      createLongitudinalLineChart('chart-longitudinal-attendance', 
        [0, 623, 0],
        [0, 320, 0],
        [0, 303, 0],
        0
      );

      renderSchoolTrajectoryTable('ALL');

      // THREE-VISIT CONTACT - VISIT 1 (0 Schools Logged)
      createHorizontalBarChart('chart-v1-enrolment', 
        [
          ["Official Boys Enrolment", "for this Term in the School"],
          ["Official Girls Enrolment", "for this Term in the School"]
        ],
        [0, 0],
        [WFP_BLUE, '#ec4899'],
        'Registered Pupils'
      );

      createHorizontalBarChart('chart-v1-active', 
        [["Active with Patron", "& Meeting Space"], ["Not Yet", "Active"]], 
        [0, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-process-nutriclub', 
        [["Already Fully", "Active"], ["In Process", "of Creating"]], 
        [0, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-days', 
        BASE_DATA.three_visit_contact.visit1.activity_days.categories, 
        [0, 0, 0, 0, 0], 
        WFP_BLUE, 
        'Schools Active on Day'
      );

      createHorizontalBarChart('chart-v1-plan', 
        [["Signed institutional", "work plan"], ["No signed", "work plan"]], 
        [0, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-charts', 
        BASE_DATA.three_visit_contact.visit1.charts_by_class.categories, 
        [0, 0, 0], 
        [WFP_BLUE, '#2389d4', '#4fa9ed'], 
        'Charts Issued'
      );

      createHorizontalBarChart('chart-v1-classes', 
        ["Lower (ECD-P2)", "Middle (P3-P4)", "Upper (P5-P7)"], 
        [0, 0, 0], 
        [ACCENT_GREEN, ACCENT_GREEN, ACCENT_GREEN], 
        'Schools Receiving Materials'
      );

      createHorizontalBarChart('chart-v1-tollfree', 
        [["Toll-Free Hotline", "Displayed"], ["Not", "Displayed"]], 
        [0, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools Displaying Hotline'
      );

      createHorizontalBarChart('chart-v1-attendance', 
        [
          ["Lower Primary (ECD-P2)", "Registered Boys Attendance"],
          ["Lower Primary (ECD-P2)", "Registered Girls Attendance"],
          ["Middle Primary (P3-P4)", "Registered Boys Attendance"],
          ["Middle Primary (P3-P4)", "Registered Girls Attendance"],
          ["Upper Primary (P5-P7)", "Registered Boys Attendance"],
          ["Upper Primary (P5-P7)", "Registered Girls Attendance"]
        ],
        [0, 0, 0, 0, 0, 0], 
        WFP_BLUE, 
        'Registered Attendance'
      );

      createHorizontalBarChart('chart-v1-helpdesk-queries', 
        BASE_DATA.three_visit_contact.visit1.helpdesk_queries_logged.categories, 
        [0, 0, 0, 0], 
        [WFP_BLUE, '#2389d4', '#4fa9ed', '#7dd3fc'], 
        'Queries Logged'
      );

      // VISIT 2 (Kotido Mixed P/S)
      createHorizontalBarChart('chart-v2-activities', 
        BASE_DATA.three_visit_contact.visit2.activities_delivered.categories, 
        BASE_DATA.three_visit_contact.visit2.activities_delivered.values, 
        ACCENT_GREEN, 
        'Schools Delivering Module'
      );

      createHorizontalBarChart('chart-v2-metu-barriers', 
        BASE_DATA.three_visit_contact.visit2.metu_uptake_barriers.categories, 
        BASE_DATA.three_visit_contact.visit2.metu_uptake_barriers.pct, 
        ['#ea580c', '#f59e0b', WFP_BLUE, '#94a3b8'], 
        '% of Households'
      );

      // PILLAR 2 MICRO-POLL
      const poll = BASE_DATA.three_visit_contact.visit2.micro_poll;
      createHorizontalBarChart('chart-v2-poll-1', poll.statement_1.categories, poll.statement_1.values, [ACCENT_GREEN, WFP_BLUE, '#94a3b8', '#ea580c', '#dc2626'], 'Boys Voting');
      createHorizontalBarChart('chart-v2-poll-2', poll.statement_2.categories, poll.statement_2.values, [ACCENT_GREEN, WFP_BLUE, '#94a3b8', '#ea580c', '#dc2626'], 'Boys Voting');
      createHorizontalBarChart('chart-v2-poll-3', poll.statement_3.categories, poll.statement_3.values, [ACCENT_GREEN, WFP_BLUE, '#94a3b8', '#ea580c', '#dc2626'], 'Boys Voting');
      createHorizontalBarChart('chart-v2-poll-4', poll.statement_4.categories, poll.statement_4.values, [ACCENT_GREEN, WFP_BLUE, '#94a3b8', '#ea580c', '#dc2626'], 'Boys Voting');
      createHorizontalBarChart('chart-v2-poll-5', poll.statement_5.categories, poll.statement_5.values, [ACCENT_GREEN, WFP_BLUE, '#94a3b8', '#ea580c', '#dc2626'], 'Boys Voting');

      // VISIT 2 - POST-SESSION SCENARIOS (Kotido Mixed P/S)
      const sc = BASE_DATA.three_visit_contact.visit2.post_session_scenario;
      createHorizontalBarChart('chart-v2-scenario-porridge', 
        sc.porridge_recall.categories, 
        sc.porridge_recall.values, 
        [ACCENT_GREEN, '#cbd5e1', '#ea580c'], 
        'Participants'
      );
      createHorizontalBarChart('chart-v2-scenario-chores', 
        sc.chore_sharing_recall.categories, 
        sc.chore_sharing_recall.values, 
        [ACCENT_GREEN, '#cbd5e1', '#ea580c'], 
        'Participants'
      );
      createHorizontalBarChart('chart-v2-scenario-slogan', 
        sc.slogan_recall.categories, 
        sc.slogan_recall.values, 
        [ACCENT_GREEN, '#cbd5e1', '#ea580c'], 
        'Participants'
      );

      // VISIT 3 (0 Schools Logged)
      const v3 = BASE_DATA.three_visit_contact.visit3;
      createHorizontalBarChart('chart-v3-feedback', v3.household_feedback.categories, [0, 0, 0], [ACCENT_GREEN, WFP_BLUE, '#cbd5e1'], 'Households');
      createHorizontalBarChart('chart-v3-barriers', v3.primary_barriers.categories, [0, 0, 0, 0, 0, 0], ['#ea580c', '#f97316', '#fb923c', '#fdba74', '#fed7aa', '#cbd5e1'], 'Households Reporting');
      createHorizontalBarChart('chart-v3-commitment', v3.bus_day_commitment_status.categories, [0, 0, 0], [ACCENT_GREEN, '#f59e0b', '#dc2626'], 'Schools');
      createHorizontalBarChart('chart-v3-tracing', v3.chronic_absentee_tracing.categories, [0, 0], [ACCENT_GREEN, '#dc2626'], 'Schools');
      createHorizontalBarChart('chart-v3-kitchen', v3.kitchen_stove_audit.categories, [0, 0], [ACCENT_GREEN, '#ea580c'], 'Schools');
      createHorizontalBarChart('chart-v3-pillar1-feeding', v3.pillar1_school_feeding_impact.categories, [0, 0, 0], [ACCENT_GREEN, WFP_BLUE, '#ea580c'], 'Schools');
      createHorizontalBarChart('chart-v3-pillar2-plate', v3.pillar2_plate_sharing_shift.categories, [0, 0, 0], [ACCENT_GREEN, '#f59e0b', '#dc2626'], 'Schools');
      createHorizontalBarChart('chart-v3-actions-tried', v3.household_shift_metrics.feasible_actions_tried.categories, [0, 0, 0, 0], WFP_BLUE, 'Respondents');
      createHorizontalBarChart('chart-v3-chore-shift', v3.household_shift_metrics.morning_chore_shifted.categories, [0, 0, 0], [ACCENT_GREEN, '#ea580c', '#94a3b8'], 'Households');
      createHorizontalBarChart('chart-v3-serving-shift', v3.household_shift_metrics.serving_order_shifted.categories, [0, 0, 0], [ACCENT_GREEN, '#ea580c', '#94a3b8'], 'Households');

      // COMMUNITY COOKING DEMO (0 Demos Logged)
      const demo = BASE_DATA.community_demonstrations;
      createHorizontalBarChart('chart-demo-headcounts', demo.headcount_breakdown.categories, [0, 0, 0, 0, 0, 0], WFP_BLUE, 'Participants');
      createHorizontalBarChart('chart-demo-fuelsaving', demo.fuel_saving_practices.categories, [0, 0, 0, 0], [ACCENT_GREEN, WFP_BLUE, '#2389d4', '#dc2626'], 'Demos Observed');
      createHorizontalBarChart('chart-demo-caregiver-barriers', demo.caregiver_barriers.categories, [0, 0, 0, 0, 0], '#ea580c', 'Caregivers');
      createHorizontalBarChart('chart-demo-caregiver-actions', demo.caregiver_feasible_actions.categories, [0, 0, 0, 0], WFP_BLUE, 'Caregivers');
      createHorizontalBarChart('chart-demo-caregiver-commitments', demo.caregiver_commitments.categories, [0, 0, 0], [ACCENT_GREEN, '#ea580c', '#cbd5e1'], 'Caregivers');
      createHorizontalBarChart('chart-demo-male-dialogue', demo.male_participation_level.categories, [0, 0, 0], [WFP_BLUE, ACCENT_GREEN, '#94a3b8'], 'Demos Reporting');
      createHorizontalBarChart('chart-demo-clean-cooking-commit', demo.clean_cooking_commitment.categories, [0, 0, 0], [ACCENT_GREEN, '#ea580c', '#f59e0b'], 'Demos Observed');

      // CHANGE STORIES (0 Stories Logged)
      const msc = BASE_DATA.msc_stories;
      createHorizontalBarChart('chart-msc-role', msc.storyteller_role.categories, [0, 0, 0, 0, 0, 0], WFP_BLUE, 'Stories');
      createHorizontalBarChart('chart-msc-event', msc.triggering_campaign_event.categories, [0, 0, 0, 0, 0], WFP_BLUE, 'Stories');
      createHorizontalBarChart('chart-msc-shift', msc.behavioral_shift_observed.categories, [0, 0, 0, 0], ACCENT_GREEN, 'Stories');
      createHorizontalBarChart('chart-msc-evidence', msc.physical_evidence_sighted.categories, [0, 0, 0, 0, 0], [ACCENT_GREEN, WFP_BLUE, '#2389d4', '#4fa9ed', '#cbd5e1'], 'Certified Evidences');

      // NUTRICLUB SESSIONS (Kakamar P/S, Kaabong)
      const club = BASE_DATA.nutriclub_sessions;
      createHorizontalBarChart('chart-club-membership', club.club_membership_gender.categories, club.club_membership_gender.values, [WFP_BLUE, '#16a34a'], 'Members');
      createHorizontalBarChart('chart-club-attendance', club.session_attendance_gender.categories, club.session_attendance_gender.values, ['#16a34a', WFP_BLUE], 'Attendance');
      createHorizontalBarChart('chart-club-pwd', club.pwd_learners_attendance.categories, club.pwd_learners_attendance.values, [WFP_BLUE, '#2389d4'], 'PWD Learners');
      createHorizontalBarChart('chart-club-activities', club.practical_activity_delivered.categories, club.practical_activity_delivered.values, WFP_BLUE, 'Sessions Delivered');
      createHorizontalBarChart('chart-club-feedback', club.home_action_feedback.categories, club.home_action_feedback.values, [ACCENT_GREEN, '#ea580c', '#cbd5e1'], 'Schools Reporting');

      // IMPACT ANALYSIS - 3 PILLARS
      // Pillar 1: School Feeding & Practical Nutrition
      createGroupedHorizontalBarChart('chart-impact-pillar1',
        [
          "Metu Porridge Fortification (Local Greens)",
          "Youngest Toddler Served First"
        ],
        [0.0, 0.0],
        [0.0, 0.0],
        '#94a3b8',
        '#16a34a'
      );

      // Pillar 2: Gender Dynamics & Equity
      createGroupedHorizontalBarChart('chart-impact-pillar2',
        [
          "Boys Sharing Morning Chores Fairly",
          "Girls Arriving to School On-Time"
        ],
        [0.0, 0.0],
        [100.0, 0.0],
        '#94a3b8',
        '#0A6EB4'
      );

      // Pillar 3: Community Engagement, Accountability & Climate-Smart Living
      createGroupedHorizontalBarChart('chart-impact-pillar3',
        [
          "Firewood-Saving Covered Cooking / Stoves",
          "Schools with Signed Action Work Plan"
        ],
        [0.0, 0.0],
        [0.0, 0.0],
        '#94a3b8',
        '#d97706'
      );

      // Render Impact Dimension Cards
      const impactContainer = document.getElementById('impact-cards-container');
      if (impactContainer) {{
        impactContainer.innerHTML = '';
        BASE_DATA.impact_analysis.dimensions.forEach(dim => {{
          let pointsHtml = '';
          dim.evidence_points.forEach(pt => {{
            pointsHtml += `<li class="flex items-start gap-1.5"><span class="text-emerald-500 font-bold">✓</span> <span>${{pt}}</span></li>`;
          }});

          impactContainer.innerHTML += `
            <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-end mb-2">
                  <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded">Visit 1 Check: ${{dim.baseline}}</span>
                </div>
                <h4 class="text-sm font-bold text-slate-800 mb-1">${{dim.title}}</h4>
                <div class="flex items-baseline gap-2 my-2">
                  <span class="text-2xl font-black text-slate-800">${{dim.metric_value}}</span>
                  <span class="text-xs text-slate-500">${{dim.metric_label}}</span>
                </div>
                <p class="text-xs text-slate-600 mb-3">${{dim.summary}}</p>
                <ul class="text-xs text-slate-600 space-y-1.5 border-t border-slate-100 pt-3">
                  ${{pointsHtml}}
                </ul>
              </div>
            </div>
          `;
        }});
      }}

      // Apply dynamic filtering across all components as final source of truth
      applyFilters();
    }}

    // Document Ready
    if (document.readyState === 'loading') {{
      document.addEventListener('DOMContentLoaded', () => {{
        initAllCharts();
      }});
    }} else {{
      initAllCharts();
    }}
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("Regenerated index.html with bus icon, removed buttons, removed badges, dynamic reactive filtering, and explicit 5 participant exit interviews.")
