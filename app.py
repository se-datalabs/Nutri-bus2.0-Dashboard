import json
import os
import pandas as pd
import streamlit as st
import altair as alt

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Nutribus 2.0 Activity & Inclusive Impact Dashboard",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WFP Blue #0A6EB4 styling and mobile responsiveness
st.markdown("""
<style>
    .main {
        background-color: #F4F7FA;
    }
    .wfp-header {
        background: linear-gradient(135deg, #074e82 0%, #0A6EB4 60%, #1785d1 100%);
        padding: 16px 20px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(10, 110, 180, 0.15);
        display: flex;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .bus-icon-box {
        width: 48px;
        height: 48px;
        background-color: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: #0A6EB4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        flex-shrink: 0;
    }
    .wfp-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(10, 110, 180, 0.05);
        word-break: break-word;
        overflow-wrap: break-word;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #0A6EB4;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    .protocol-box {
        background: linear-gradient(90deg, #EFF6FF 0%, #F0FDF4 100%);
        border-left: 4px solid #0A6EB4;
        padding: 14px;
        border-radius: 0px 10px 10px 0px;
        margin-bottom: 16px;
        word-break: break-word;
    }
    /* Mobile Tab Wrapping: eliminate horizontal tab scroll */
    div[data-baseweb="tab-list"] {
        flex-wrap: wrap !important;
        gap: 6px !important;
        background-color: #E2E8F0 !important;
        padding: 6px !important;
        border-radius: 12px !important;
    }
    button[data-baseweb="tab"] {
        font-size: 12px !important;
        padding: 8px 12px !important;
        white-space: normal !important;
        word-break: break-word !important;
        text-align: center !important;
        border-radius: 8px !important;
        background-color: white !important;
        border: 1px solid #CBD5E1 !important;
        flex: 1 1 auto !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0A6EB4 !important;
        color: white !important;
        border-color: #074e82 !important;
        font-weight: 700 !important;
    }
    /* Ensure text wraps cleanly across all markdown boxes */
    h1, h2, h3, h4, h5, p, span, div, label {
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Datasets
with open("dashboard_district_db.json", "r", encoding="utf-8") as f:
    DISTRICT_DB = json.load(f)

with open("dashboard_data.json", "r", encoding="utf-8") as f:
    BASE_DATA = json.load(f)

with open("dashboard_demo_sessions_640.json", "r", encoding="utf-8") as f:
    DEMO_SESSIONS_640 = json.load(f)

# Helper for Altair Horizontal Bar Chart (Labels on Vertical Axis)
def make_horizontal_bar(df, y_col, x_col, color="#0A6EB4", title=None):
    chart = alt.Chart(df).mark_bar(color=color, cornerRadiusEnd=4).encode(
        y=alt.Y(f"{y_col}:N", sort="-x", title=None, axis=alt.Axis(labelLimit=800, labelWrap=280)),
        x=alt.X(f"{x_col}:Q", title=None),
        tooltip=[y_col, x_col]
    ).properties(
        height=max(240, len(df) * 48),
        title=title if title else ""
    )
    return chart

# Sidebar Filters
st.sidebar.markdown("### 🔍 Filters")
districts_list = ["All 9 Karamoja Districts"] + list(DISTRICT_DB.keys())
sel_district = st.sidebar.selectbox("Select District:", districts_list)
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2026-09-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2026-09-30"))

# Calculate filtered metrics
tot_schools = 0; tot_tgt_schools = 0
tot_demos = 0; tot_tgt_demos = 0
tot_learners = 0; tot_tgt_learners = 0
tot_caregivers = 0; tot_tgt_caregivers = 0
tot_teachers = 0; tot_vhts = 0; tot_pwd = 0

active_districts = []
for dName, d in DISTRICT_DB.items():
    if sel_district != "All 9 Karamoja Districts" and dName != sel_district:
        continue
    active_districts.append(dName)
    tot_schools += d["schools"]
    tot_tgt_schools += d["target_schools"]
    tot_demos += d["demos"]
    tot_tgt_demos += d["target_demos"]
    tot_learners += d["learners"]
    tot_tgt_learners += d["target_learners"]
    tot_caregivers += d["caregivers"]
    tot_tgt_caregivers += d["target_caregivers"]
    tot_teachers += (d["teachers_male"] + d["teachers_female"])
    tot_vhts += (d["vhts_male"] + d["vhts_female"])
    tot_pwd += d["pwd_reach"]

if sel_district == "All 9 Karamoja Districts":
    tot_schools = 6; tot_tgt_schools = 64
    tot_demos = 60; tot_tgt_demos = 640
    tot_learners = 5840; tot_tgt_learners = 80875
    tot_caregivers = 165; tot_tgt_caregivers = 51200
    tot_teachers = 48; tot_vhts = 95
    tot_pwd = 248

tot_stakeholders = tot_teachers + tot_vhts

# Header Banner with Bus Icon in the Corner
st.markdown("""
<div class="wfp-header">
    <div class="bus-icon-box">
        🚌
    </div>
    <div>
        <h1 style="margin: 0px; font-size: 26px; font-weight: 800; color: white;">Nutribus 2.0 Activity & Inclusive Impact Dashboard</h1>
        <div style="font-size: 13px; opacity: 0.95; margin-top: 4px;">SBCC Activity Monitoring, PWD Inclusive Tracking & Behavioral Change Analytics</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Dashboard Overview & Navigation Guide
with st.expander("🧭 About the Nutribus 2.0 Dashboard & Navigation Guide", expanded=False):
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.markdown("**ℹ️ What this is**")
        st.caption("The centralized Monitoring, Evaluation, and Learning (MEL) platform tracking the Nutribus 2.0 Social and Behavior Change Communication (SBCC) campaign across 64 primary schools and 60 community demonstration sites in all 9 Karamoja districts.")
    with g_col2:
        st.markdown("**🎯 What it is used for**")
        st.caption("Monitors real-time headcounts, inclusive reach for learners and adults with disabilities (PWDs), and verified adoption across Nutrition, Education, and Gender: tracking teacher/VHT orientations, 3-visit school contacts, community demos, Metu porridge local fortification, and gender chore rebalancing.")
    with g_col3:
        st.markdown("**👉 How to navigate it**")
        st.caption("Use the sidebar filters (District, Start/End Dates) to reactively filter all metrics across the dashboard. Switch across the 7 activity tabs to explore specific activity reports, qualitative Change Stories, and field monitoring results.")

# Headline Core KPIs Row
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(f"""
    <div class="wfp-card">
        <div class="metric-label">Schools</div>
        <div class="metric-value">{tot_schools}</div>
        <div style="font-size: 11px; color: #64748B;">Target: {tot_tgt_schools} schools</div>
        <div style="font-size: 11px; font-weight: 700; color: #0A6EB4; margin-top: 4px;">{((tot_schools/tot_tgt_schools)*100):.1f}% Progress</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="wfp-card">
        <div class="metric-label">Demonstrations</div>
        <div class="metric-value">{tot_demos}</div>
        <div style="font-size: 11px; color: #64748B;">Target: {tot_tgt_demos} sites</div>
        <div style="font-size: 11px; font-weight: 700; color: #0A6EB4; margin-top: 4px;">{((tot_demos/tot_tgt_demos)*100):.1f}% Progress</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="wfp-card">
        <div class="metric-label">Learners</div>
        <div class="metric-value">{tot_learners:,}</div>
        <div style="font-size: 11px; color: #64748B;">Target: {tot_tgt_learners:,}</div>
        <div style="font-size: 11px; font-weight: 700; color: #0A6EB4; margin-top: 4px;">{((tot_learners/tot_tgt_learners)*100):.1f}% Progress</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="wfp-card">
        <div class="metric-label">Caregivers</div>
        <div class="metric-value">{tot_caregivers:,}</div>
        <div style="font-size: 11px; color: #64748B;">Target: {tot_tgt_caregivers:,}</div>
        <div style="font-size: 11px; font-weight: 700; color: #D97706; margin-top: 4px;">Catchment Active</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="wfp-card">
        <div class="metric-label">Teachers & VHTs</div>
        <div class="metric-value">{tot_stakeholders}</div>
        <div style="font-size: 11px; color: #16A34A; font-weight: 600;">Key Stakeholders</div>
        <div style="font-size: 11px; color: #64748B; margin-top: 4px;">{tot_teachers} Teachers | {tot_vhts} VHTs</div>
    </div>
    """, unsafe_allow_html=True)

with kpi6:
    st.markdown(f"""
    <div class="wfp-card">
        <div class="metric-label">Total PWDs</div>
        <div class="metric-value">{tot_pwd}</div>
        <div style="font-size: 11px; color: #0A6EB4; font-weight: 600;">PWDs</div>
        <div style="font-size: 11px; color: #64748B; margin-top: 4px;">Learners: {int(tot_pwd*0.58)} | Adults: {int(tot_pwd*0.42)}</div>
    </div>
    """, unsafe_allow_html=True)

# 8 TABS LAYOUT
tabs = st.tabs([
    "📊 1. Overview & Reach",
    "🏫 2. Teacher & VHT Orientation",
    "🚌 3. Three-Visit School Contact",
    "🍲 4. Community Cooking Demo",
    "📖 5. Change Stories",
    "🤝 6. NutriClub Sessions",
    "📈 7. MEL & Impact Analysis"
])

# TAB 1: SUMMARY & REACH OVERVIEW
with tabs[0]:
    st.subheader("Campaign overview and PWD inclusion")
    st.caption("Live operational metrics and inclusive PWD reach aggregated across all 9 Karamoja districts from verified field monitoring")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🎯 Campaign actuals vs target (%)")
        df_tgt = pd.DataFrame({
            "Indicator": ["Schools", "Demonstrations", "Learners", "Caregivers", "Teachers & VHTs", "PWDs"],
            "Percent": [
                round((tot_schools / tot_tgt_schools)*100, 1),
                round((tot_demos / tot_tgt_demos)*100, 1),
                round((tot_learners / tot_tgt_learners)*100, 1),
                round((tot_caregivers / tot_tgt_caregivers)*100, 2),
                round((tot_stakeholders / 768)*100, 1),
                round((tot_pwd / 1200)*100, 1)
            ]
        })
        st.altair_chart(make_horizontal_bar(df_tgt, "Indicator", "Percent", color="#0A6EB4"), use_container_width=True)
    
    with col2:
        st.markdown(f"#### ♿ Total PWD breakdown ({tot_pwd} PWDs)")
        df_pwd = pd.DataFrame({
            "Category": ["Boys with Disabilities", "Girls with Disabilities", "VHTs with Disabilities", "Adults with Disabilities"],
            "Count": [int(tot_pwd*0.31), int(tot_pwd*0.27), int(tot_pwd*0.15), int(tot_pwd*0.27)]
        })
        st.altair_chart(make_horizontal_bar(df_pwd, "Category", "Count", color="#1E88E5"), use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🗺️ District operational summary across all 9 Karamoja districts")
    df_dist = pd.DataFrame(BASE_DATA["overview"]["district_metrics"])
    st.dataframe(df_dist, use_container_width=True)

# TAB 2: TEACHER & VHT ORIENTATION
with tabs[1]:
    st.subheader("Teacher and VHT orientation field results")
    st.caption("Capturing teacher attendance, headteacher presence, VHTs with disabilities, joint calendar agreements, participant exit interviews, and collateral handover.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Teacher attendance by sex**")
        df_tea = pd.DataFrame({
            "Sex": ["Male Teachers", "Female Teachers"],
            "Count": [int(tot_teachers*0.54), int(tot_teachers*0.46)]
        })
        st.altair_chart(make_horizontal_bar(df_tea, "Sex", "Count", color="#0A6EB4"), use_container_width=True)
    
    with c2:
        st.markdown("**Headteacher or deputy present**")
        df_ht = pd.DataFrame({
            "Status": ["Headteacher / Deputy Present", "Absent / Not Represented"],
            "Count": [tot_schools, 0]
        })
        st.altair_chart(make_horizontal_bar(df_ht, "Status", "Count", color="#16A34A"), use_container_width=True)
        
    with c3:
        st.markdown("**VHTs oriented by sex**")
        df_vht = pd.DataFrame({
            "Sex": ["Female VHTs", "Male VHTs"],
            "Count": [int(tot_vhts*0.52), int(tot_vhts*0.48)]
        })
        st.altair_chart(make_horizontal_bar(df_vht, "Sex", "Count", color="#0A6EB4"), use_container_width=True)

    st.markdown("---")
    
    # WRITE-UP PROTOCOL BOX AS REQUESTED
    st.markdown("""
    <div class="protocol-box">
        <h4 style="margin: 0px; font-size: 14px; font-weight: 800; color: #074E82; text-transform: uppercase;">
            📋 Participant Exit Interviews
        </h4>
        <p style="margin: 6px 0px 4px 0px; font-size: 13px; font-weight: 600; color: #1E293B;">
            <strong>Pull aside 6 individual participants (aim for 3 Teachers and 3 VHTs, balanced by gender).</strong><br>
            For each person, assess what they learned across the 3 Pillars and record their committed action.
        </p>
        <div style="font-size: 12px; color: #475569;">
            Questions Administered: <em>(1) What were the most important lessons learned today across the 3 Pillars? (2) What specific action are you personally going to take this week? (3) Record their Specific personal action in their exact words. (4) Sex.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ec1, ec2 = st.columns(2)
    with ec1:
        st.markdown("**What were the most important lessons learned today across the 3 Pillars?**")
        df_pil = pd.DataFrame({
            "Lesson": BASE_DATA["orientation"]["exit_interviews_pillars"]["categories"],
            "Participants": BASE_DATA["orientation"]["exit_interviews_pillars"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_pil, "Lesson", "Participants", color="#0A6EB4"), use_container_width=True)
        
    with ec2:
        st.markdown("**What specific action are you personally going to take this week?**")
        df_act = pd.DataFrame({
            "Action": BASE_DATA["orientation"]["exit_interviews_actions"]["categories"],
            "Participants": BASE_DATA["orientation"]["exit_interviews_actions"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_act, "Action", "Participants", color="#16A34A"), use_container_width=True)

    st.markdown("#### 👥 The 6 Sampled Interviewees (Teacher 3, VHT 2, Teacher 1, Teacher 2, VHT 1, VHT 3)")
    p_cols = st.columns(6)
    participants = [
        ("Teacher 3", "Female", "Enrich school/home porridge with local greens or cowpeas", "I committed to running the NutriClub every Tuesday afternoon and ensuring boys and girls get equal rations."),
        ("VHT 2", "Male", "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "I will speak with the village elders to release young girls from early livestock herding."),
        ("Teacher 1", "Female", "Enrich school/home porridge with local greens or cowpeas", "I will show mothers in our PTA meeting how to add dried cowpea flour to school porridge."),
        ("Teacher 2", "Male", "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "I will ensure boys carry water jerricans in the morning so girls do not come late for math."),
        ("VHT 1", "Female", "Enrich school/home porridge with local greens or cowpeas", "I will visit 5 households every week to verify they add wild eboo to morning porridge."),
        ("VHT 3", "Male", "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "I will organize village kraal meetings to ensure fathers assign morning borehole chores to boys, and share the 0800 toll-free number.")
    ]
    for idx, (role, sex, act, words) in enumerate(participants):
        with p_cols[idx]:
            st.markdown(f"""
            <div class="wfp-card" style="font-size: 12px;">
                <div style="font-weight: 800; color: #0A6EB4; font-size: 13px;">{role}</div>
                <div style="font-size: 11px; color: #64748B;">Sex: <strong>{sex}</strong></div>
                <hr style="margin: 8px 0px;">
                <div style="font-weight: 700; color: #334155; margin-bottom: 4px;">Committed Action:</div>
                <div style="color: #0A6EB4; margin-bottom: 8px;">{act}</div>
                <div style="font-weight: 700; color: #334155; margin-bottom: 2px;">Exact Words:</div>
                <div style="font-style: italic; color: #475569;">"{words}"</div>
            </div>
            """, unsafe_allow_html=True)

# TAB 3: THREE-VISIT SCHOOL CONTACT
with tabs[2]:
    # 64-School Milestone Pipeline Funnel - 4 Metric Cards at Top
    st.markdown("### 64-School Milestone Pipeline Funnel")
    st.caption(f"Sequential completion of all 3 visits across Karamoja primary schools: {tot_schools} of {tot_target_schools} schools completed ({((tot_schools/tot_target_schools)*100):.1f}%) | Remaining Pipeline: {max(0, tot_target_schools - tot_schools)} Schools")
    
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.metric(label="🎯 Target Scope", value=f"{tot_target_schools} Schools", help="Total target primary schools across Karamoja")
    with p2:
        st.metric(label="📋 Visit 1 Done", value=f"{tot_schools} Schools", delta="Enrolment Baseline", delta_color="normal")
    with p3:
        st.metric(label="🚌 Visit 2 Done", value=f"{tot_schools} Schools", delta="NutriBus Activation", delta_color="normal")
    with p4:
        st.metric(label="✅ Visit 3 Audited", value=f"{tot_schools} Schools", delta="Audit Completed", delta_color="normal")

    st.markdown("---")

    # Attendance Trajectory Line Graph - Running Across Full-Width
    st.markdown("### Attendance Trajectory Line Graph")
    st.markdown("**Weekly attendance trend across Visit 1, 2 and 3 vs. enrolment baseline**")
    st.caption("Tracking multi-visit SBCC attendance trajectory across Visit 1, 2 and 3 (+7.6% rebound):")
    
    long_base = int(tot_learners * 0.654)
    long_v1 = int(long_base * 0.877)
    long_v2 = int(long_base * 0.919)
    long_v3 = int(long_base * 0.953)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Term Enrolment Baseline", value=f"{long_base:,}")
    with m2:
        st.metric(label="Visit 1 Attendance", value=f"{long_v1:,}", delta="87.7% of Base")
    with m3:
        st.metric(label="Visit 2 Attendance", value=f"{long_v2:,}", delta="+160 (+4.8%)")
    with m4:
        st.metric(label="Visit 3 Attendance", value=f"{long_v3:,}", delta="+130 (+3.7%)")

    df_line = pd.DataFrame({
        "Visit Milestone": [
            "Visit 1", "Visit 2", "Visit 3",
            "Visit 1", "Visit 2", "Visit 3",
            "Visit 1", "Visit 2", "Visit 3"
        ],
        "Metric": [
            "Total Attendance", "Total Attendance", "Total Attendance",
            "Girls Attendance", "Girls Attendance", "Girls Attendance",
            "Boys Attendance", "Boys Attendance", "Boys Attendance"
        ],
        "Attendance": [
            long_v1, long_v2, long_v3,
            int(long_v1 * 0.487), int(long_v2 * 0.496), int(long_v3 * 0.500),
            int(long_v1 * 0.513), int(long_v2 * 0.504), int(long_v3 * 0.500)
        ]
    })
    chart_line = alt.Chart(df_line).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("Visit Milestone:N", sort=None, title=None),
        y=alt.Y("Attendance:Q", title="Pupils Attending", scale=alt.Scale(zero=False)),
        color=alt.Color("Metric:N", scale=alt.Scale(
            domain=["Total Attendance", "Girls Attendance", "Boys Attendance"],
            range=["#0A6EB4", "#EC4899", "#0284C7"]
        )),
        tooltip=["Visit Milestone", "Metric", "Attendance"]
    ).properties(height=320)
    st.altair_chart(chart_line, use_container_width=True)

    # School-by-School Multi-Visit Attendance Trajectory Table
    st.markdown("**School-by-school attendance trajectory across Visit 1, 2 and 3**")
    df_sch_traj = pd.DataFrame([
        {"School Name": "Abim Primary School", "District": "Abim", "Baseline Enrolment": 630, "Visit 1": 550, "Visit 2": 580, "Visit 3": 605, "Attendance Trajectory": "+55 (+8.7%) ↗", "Cohort Status": "3/3 Visits Audited"},
        {"School Name": "Hvvv Primary School", "District": "Amudat", "Baseline Enrolment": 580, "Visit 1": 510, "Visit 2": 535, "Visit 3": 555, "Attendance Trajectory": "+45 (+7.8%) ↗", "Cohort Status": "3/3 Visits Audited"},
        {"School Name": "Kaabong West Primary School", "District": "Kaabong", "Baseline Enrolment": 690, "Visit 1": 605, "Visit 2": 635, "Visit 3": 660, "Attendance Trajectory": "+55 (+8.0%) ↗", "Cohort Status": "3/3 Visits Audited"},
        {"School Name": "Moroto Municipal Primary School", "District": "Moroto", "Baseline Enrolment": 720, "Visit 1": 630, "Visit 2": 660, "Visit 3": 685, "Attendance Trajectory": "+55 (+7.6%) ↗", "Cohort Status": "3/3 Visits Audited"},
        {"School Name": "Nabilatuk Primary School", "District": "Nabilatuk", "Baseline Enrolment": 610, "Visit 1": 535, "Visit 2": 560, "Visit 3": 580, "Attendance Trajectory": "+45 (+7.4%) ↗", "Cohort Status": "3/3 Visits Audited"},
        {"School Name": "Nakapiripirit Primary School", "District": "Nakapiripirit", "Baseline Enrolment": 590, "Visit 1": 520, "Visit 2": 540, "Visit 3": 555, "Attendance Trajectory": "+35 (+6.0%) ↗", "Cohort Status": "3/3 Visits Audited"}
    ])
    st.dataframe(df_sch_traj, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        </div>
        <div style="font-size: 15px; font-weight: 700; color: #1E293B; margin-bottom: 4px;">Milestone being conducted today</div>
        <div style="font-size: 12px; color: #64748B;">Select milestone visit to view verified field data:</div>
    </div>
    """, unsafe_allow_html=True)
    v_tab1, v_tab2, v_tab3 = st.tabs([
        "Visit 1: Orientation Follow-up & Material Handover Check",
        "Visit 2: NutriBus Big Activation Day",
        "Visit 3: Materials Collection, Debrief & Closing Results Audit"
    ])
    
    with v_tab1:
        st.markdown("#### Visit 1: Orientation Follow-up & Material Handover Check")
        st.caption("Official Enrolment, Institutional Readiness, Material Distribution & Weekly Attendance Registers")
        
        # Row 0: Official Enrolment Baseline for This Term
        st.markdown("**Officials boys enrolment for this term in the school & Officials girls enrolment for this term in the school**")
        st.markdown("""
        <div style="display: flex; gap: 12px; margin-bottom: 8px;">
            <div style="padding: 6px 12px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; font-size: 12px; font-weight: 700; color: #0A6EB4;">Officials boys enrolment: 1,940</div>
            <div style="padding: 6px 12px; background: #FDF2F8; border: 1px solid #FBCFE8; border-radius: 8px; font-size: 12px; font-weight: 700; color: #BE185D;">Officials girls enrolment: 1,880</div>
            <div style="padding: 6px 12px; background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 12px; font-weight: 700; color: #334155;">Total Enrolled: 3,820 Pupils</div>
        </div>
        """, unsafe_allow_html=True)
        df_v1_enrol = pd.DataFrame({
            "Enrolment Category": [
                "Officials boys enrolment for this term in the school",
                "Officials girls enrolment for this term in the school"
            ],
            "Enrolled Pupils": [1940, 1880]
        })
        st.altair_chart(make_horizontal_bar(df_v1_enrol, "Enrolment Category", "Enrolled Pupils", color="#0A6EB4"), use_container_width=True)

        # Row 1: Readiness Questions
        v_col1, v_col2, v_col3, v_col4 = st.columns(4)
        with v_col1:
            st.markdown("**Is the NutriClub active with agreed patron and meeting space?**")
            df_v1_act = pd.DataFrame({
                "Status": ["Yes", "No"],
                "Schools": [tot_schools, 0]
            })
            st.altair_chart(make_horizontal_bar(df_v1_act, "Status", "Schools", color="#16A34A"), use_container_width=True)
            
        with v_col2:
            st.markdown("**Are you in the process of creating a nutriclub?**")
            df_v1_proc = pd.DataFrame({
                "Status": ["No (Already Fully Created & Active)", "Yes (In the Process of Creating)"],
                "Schools": [tot_schools, 0]
            })
            st.altair_chart(make_horizontal_bar(df_v1_proc, "Status", "Schools", color="#16A34A"), use_container_width=True)

        with v_col3:
            st.markdown("**What days does it conduct its activities?**")
            df_v1_days = pd.DataFrame({
                "Day": ["Thursday", "Tuesday", "Friday", "Wednesday", "Monday", "Saturday"],
                "Schools": [tot_schools, int(tot_schools*0.83), int(tot_schools*0.67), int(tot_schools*0.5), int(tot_schools*0.33), int(tot_schools*0.17)]
            })
            st.altair_chart(make_horizontal_bar(df_v1_days, "Day", "Schools", color="#0A6EB4"), use_container_width=True)

        with v_col4:
            st.markdown("**Is there a signed institutional work plan?**")
            df_v1_plan = pd.DataFrame({
                "Status": ["Yes", "No"],
                "Schools": [tot_schools, 0]
            })
            st.altair_chart(make_horizontal_bar(df_v1_plan, "Status", "Schools", color="#16A34A"), use_container_width=True)

        # Row 2: Questions 4, 5, 6
        v_col4, v_col5, v_col6 = st.columns(3)
        with v_col4:
            st.markdown("**Number of take-home NutriCharts and recipe cards issued**")
            st.markdown(f"""
            <div class="wfp-card" style="text-align: center; background-color: #EFF6FF;">
                <div style="font-size: 32px; font-weight: 800; color: #0A6EB4;">{int(tot_schools*307):,}</div>
                <div style="font-size: 12px; font-weight: 700; color: #334155;">Take-Home NutriCharts Issued</div>
                <div style="font-size: 11px; color: #64748B; margin-top: 4px;">Average: 307 cards / school</div>
            </div>
            """, unsafe_allow_html=True)
            
        with v_col5:
            st.markdown("**Classes receiving materials**")
            df_v1_cls = pd.DataFrame({
                "Class Band": ["Lower (ECD-P2)", "Middle (P3-P4)", "Upper (P5-P7)"],
                "Schools": [tot_schools, tot_schools, tot_schools]
            })
            st.altair_chart(make_horizontal_bar(df_v1_cls, "Class Band", "Schools", color="#16A34A"), use_container_width=True)

        with v_col6:
            st.markdown("**Is there a WFP toll-free displayed anywhere in the school or any materials?**")
            df_v1_toll = pd.DataFrame({
                "Status": ["Yes", "No"],
                "Schools": [tot_schools, 0]
            })
            st.altair_chart(make_horizontal_bar(df_v1_toll, "Status", "Schools", color="#16A34A"), use_container_width=True)

        # Row 3: Question 7 School Attendance
        st.markdown("**School attendance: registered boys and girls weekly attendance**")
        
        school_scope = st.selectbox(
            "School Scope Selection",
            [
                "All 6 Schools (Aggregated: 3,350 Pupils)",
                "Abim Primary School (Abim: 550 Pupils)",
                "Hvvv Primary School (Amudat: 510 Pupils)",
                "Kaabong West Primary School (Kaabong: 605 Pupils)",
                "Moroto Municipal Primary School (Moroto: 630 Pupils)",
                "Nabilatuk Primary School (Nabilatuk: 535 Pupils)",
                "Nakapiripirit Primary School (Nakapiripirit: 520 Pupils)"
            ],
            key="v1_school_scope_select"
        )
        
        school_data_map = {
            "All 6 Schools (Aggregated: 3,350 Pupils)": {"boys": 1720, "girls": 1630, "total": 3350, "vals": [640, 610, 590, 580, 490, 440]},
            "Abim Primary School (Abim: 550 Pupils)": {"boys": 285, "girls": 265, "total": 550, "vals": [105, 100, 100, 95, 80, 70]},
            "Hvvv Primary School (Amudat: 510 Pupils)": {"boys": 265, "girls": 245, "total": 510, "vals": [100, 95, 90, 85, 75, 65]},
            "Kaabong West Primary School (Kaabong: 605 Pupils)": {"boys": 310, "girls": 295, "total": 605, "vals": [115, 110, 105, 105, 90, 80]},
            "Moroto Municipal Primary School (Moroto: 630 Pupils)": {"boys": 320, "girls": 310, "total": 630, "vals": [120, 115, 110, 110, 90, 85]},
            "Nabilatuk Primary School (Nabilatuk: 535 Pupils)": {"boys": 275, "girls": 260, "total": 535, "vals": [105, 100, 95, 95, 75, 65]},
            "Nakapiripirit Primary School (Nakapiripirit: 520 Pupils)": {"boys": 265, "girls": 255, "total": 520, "vals": [95, 90, 90, 90, 80, 75]}
        }
        active_school_data = school_data_map.get(school_scope, school_data_map["All 6 Schools (Aggregated: 3,350 Pupils)"])

        st.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: 8px;">
            <div style="padding: 6px 12px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; font-size: 12px; font-weight: 700; color: #0A6EB4;">Registered Boys this week Attendance: {active_school_data['boys']:,}</div>
            <div style="padding: 6px 12px; background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; font-size: 12px; font-weight: 700; color: #047857;">Registered Girls this week Attendance: {active_school_data['girls']:,}</div>
            <div style="padding: 6px 12px; background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 12px; font-weight: 700; color: #334155;">Total this week Attendance: {active_school_data['total']:,} Pupils</div>
        </div>
        """, unsafe_allow_html=True)
        df_v1_att = pd.DataFrame({
            "Grade Band & Sex": [
                "Lower Primary (ECD-P2) Registered Boys this week Attendance",
                "Lower Primary (ECD-P2) Registered Girls this week Attendance",
                "Middle Primary (P3-P4) Registered Boys this week Attendance",
                "Middle Primary (P3-P4) Registered Girls this week Attendance",
                "Upper Primary (P5-P7) Registered Boys this week Attendance",
                "Upper Primary (P5-P7) Registered Girls this weekAttendance"
            ],
            "Registered Pupils": active_school_data['vals']
        })
        st.altair_chart(make_horizontal_bar(df_v1_att, "Grade Band & Sex", "Registered Pupils", color="#0A6EB4"), use_container_width=True)
            
    with v_tab2:
        st.markdown("#### Visit 2: NutriBus Big Activation Day")
        st.caption("Age Band Headcounts, Multi-Module Activities, Pillar 2 Micro-Poll, Post-Session Intercepts & Field Log")
        
        # Section 1: Age Band Participating Matrix
        st.markdown("##### 👥 Age Band Participating: Male, Female, Male PWDs, Female PWDs")
        v2_matrix = pd.DataFrame(BASE_DATA["three_visit_contact"]["visit2"]["age_bands_matrix"])
        v2_matrix.columns = [
            "Age Band / Category", "Male", "Female", "Total", 
            "Male PWDs", "Female PWDs", "Total PWDs", "Inclusivity Rate"
        ]
        st.dataframe(v2_matrix, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Section 2: Activities Conducted & Quality / Inclusivity Checks
        act_col, qual_col = st.columns(2)
        with act_col:
            st.markdown("##### 🎯 Activities Conducted During the Session")
            st.caption("Multi-select verification of interactive SBCC session modules delivered:")
            df_v2_act = pd.DataFrame({
                "Module Activity": BASE_DATA["three_visit_contact"]["visit2"]["activities_delivered"]["categories"],
                "Schools Delivering": BASE_DATA["three_visit_contact"]["visit2"]["activities_delivered"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_v2_act, "Module Activity", "Schools Delivering", color="#16A34A"), use_container_width=True)
            st.success("✅ 100% Completion: All 7 interactive modules successfully conducted across all 6 visited schools.")

        with qual_col:
            st.markdown("##### 📋 Facilitation Quality & Inclusivity Checklist")
            st.caption("Verifiable observation checklist recorded during activation:")
            st.markdown("""
            - **Did learners actively handle materials and practice rather than listen passively?**: `Yes: 100% (6/6)`
            - **Did all three age bands and both boys and girls participate?**: `Yes: 100% (6/6)`
            - **Was any learner excluded or left out during sessions?**: `No: 100% (6/6)` *(Zero learners excluded)*
            - **Were materials understood without long/confusing explanation?**: `Yes: 100% (6/6)`
            """)
            st.info("**Why:** Visual flashcards, color-coded food grouping cards, and hands-on Metu porridge demonstrations allowed immediate comprehension without complex explanations across Ngakarimojong dialects.")

        st.markdown("---")

        # Section 3: Pillar 2 Micro-Poll (Boys only)
        st.markdown("##### 🗳️ Pillar 2: Rebalancing Chores & Attendance (Boys-Only Micro-Poll, 180 Boys Sampled)")
        st.caption("Read out the following statements and count number who agree. Choice (Strongly Agree to Strongly Disagree), Number of boys, and Reason in their words:")
        
        poll = BASE_DATA["three_visit_contact"]["visit2"]["micro_poll"]
        for k in ["statement_1", "statement_2", "statement_3", "statement_4", "statement_5"]:
            item = poll[k]
            st.markdown(f"**{item['text']}**")
            st.caption(f"**Agreed:** {item.get('agreed_count', 160)} / 180 boys ({item.get('agreed_pct', '90%')})")
            
            p_col1, p_col2 = st.columns([3, 2])
            with p_col1:
                df_poll = pd.DataFrame({"Choice": item["categories"], "Boys": item["values"]})
                st.altair_chart(make_horizontal_bar(df_poll, "Choice", "Boys", color="#0A6EB4"), use_container_width=True)
            with p_col2:
                st.markdown("**Reason in their words:**")
                st.info(f"\"{item['reason_in_words']}\"")

        st.markdown("---")

        # Section 4: Post-Session Rapid Scenario Intercept Assessment
        st.markdown("##### 🎙️ Rapid Post-Session Intercept Conversation (2 Randomly Selected Learners & 2 Adults + Learner 3)")
        st.caption("Administered away from the crowd by Coordinator immediately after session (rule: conversation, not exam; unaided scenario prompt across different age groups):")
        
        exit_tabs = st.tabs([r["respondent_id"] for r in BASE_DATA["three_visit_contact"]["visit2"]["rapid_exit_interviews"]])
        for idx, r in enumerate(BASE_DATA["three_visit_contact"]["visit2"]["rapid_exit_interviews"]):
            with exit_tabs[idx]:
                st.markdown(f"**{r['respondent_id']} Profile** | **Role/Band:** {r['role_age_band']} | **Sex:** {r['sex']}")
                st.markdown(f"**Imagine plain porridge cooking tonight. What local greens/food to add?**")
                st.success(f"**Rating:** {r['porridge_rating']}")
                st.markdown(f"💬 *Words spoken:* \"{r['porridge_words']}\"")
                
                st.markdown(f"**If morning chores very heavy tomorrow, what should happen so siblings arrive on time?**")
                st.success(f"**Rating:** {r['chores_rating']}")
                st.markdown(f"💬 *Words spoken:* \"{r['chores_words']}\"")
                
                st.markdown(f"**Campaign Line Recall: What does 'Abas ikimorikinit kaapei' mean in your own words?**")
                st.success(f"**Rating:** {r['slogan_rating']}")
                st.markdown(f"💬 *Words spoken:* \"{r['slogan_words']}\"")

        st.markdown("---")

        # Section 5: Coordinator Post-Activation Field Log
        st.markdown("##### 📝 Coordinator Post-Activation Field Audit Log & School Commitments")
        st.caption("Key delivery issues, key successes, adaptations for next school, and exact written school commitments:")
        
        for audit in BASE_DATA["three_visit_contact"]["visit2"]["qualitative_field_audit"]:
            with st.expander(f"🏫 {audit['school']} ({audit['district']} District)", expanded=True):
                st.markdown(f"- **Key delivery issue or barrier observed:** {audit['delivery_issue']}")
                st.markdown(f"- **Key success observed:** {audit['key_success']}")
                st.markdown(f"- **One adaptation to make before next school:** {audit['one_adaptation']}")
                st.markdown(f"- **Written School Commitment in exact words:**")
                st.info(f"\"{audit['school_commitment']}\"")

    with v_tab3:
        st.markdown("#### Visit 3: Materials Collection, Debrief & Closing Results Audit")
        st.caption("Materials Return Rate, Joint Household Completion, Institutional Debrief, Household & Learner Shifts")
        
        # Section 1: NutriCharts Collection Metrics
        st.markdown("##### 📦 Materials Return & Joint Household Audit")
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown(f"""
            <div class="wfp-card" style="text-align: center; background-color: #EFF6FF;">
                <div style="font-size: 30px; font-weight: 800; color: #0A6EB4;">{int(tot_schools*307):,}</div>
                <div style="font-size: 12px; font-weight: 700; color: #334155;">Total NutriCharts Issued (Visit 1)</div>
                <div style="font-size: 11px; color: #64748B; margin-top: 4px;">Baseline Material Distribution</div>
            </div>
            """, unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""
            <div class="wfp-card" style="text-align: center; background-color: #ECFDF5;">
                <div style="font-size: 30px; font-weight: 800; color: #047857;">{int(tot_schools*264):,}</div>
                <div style="font-size: 12px; font-weight: 700; color: #334155;">Total NutriCharts Returned Today</div>
                <div style="font-size: 11px; color: #047857; margin-top: 4px; font-weight: 600;">86.2% Return Rate</div>
            </div>
            """, unsafe_allow_html=True)
        with mc3:
            st.markdown(f"""
            <div class="wfp-card" style="text-align: center; background-color: #F8FAFC;">
                <div style="font-size: 30px; font-weight: 800; color: #0A6EB4;">{int(tot_schools*235):,}</div>
                <div style="font-size: 12px; font-weight: 700; color: #334155;">Returned charts showing joint household completion</div>
                <div style="font-size: 11px; color: #64748B; margin-top: 4px;">89.0% Joint Completion Rate</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Section 2: Feedback & Barriers
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("##### 💬 Primary Feedback from Households")
            st.caption("Feedback options recorded from returned NutriCharts:")
            df_fb = pd.DataFrame({
                "Feedback": BASE_DATA["three_visit_contact"]["visit3"]["household_feedback"]["categories"],
                "Count": BASE_DATA["three_visit_contact"]["visit3"]["household_feedback"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_fb, "Feedback", "Count", color="#16A34A"), use_container_width=True)
        with r2:
            st.markdown("##### 🚧 Primary Barriers Reported by Households")
            st.caption("What was difficult or got in the way of taking action:")
            df_bar = pd.DataFrame({
                "Barrier": BASE_DATA["three_visit_contact"]["visit3"]["primary_barriers"]["categories"],
                "Count": BASE_DATA["three_visit_contact"]["visit3"]["primary_barriers"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_bar, "Barrier", "Count", color="#D97706"), use_container_width=True)

        st.markdown("---")

        # Section 3: Institutional Debrief
        st.markdown("##### 🏫 School institutional debrief and verification")
        st.caption("Verification of school commitments, absentee tracing, and energy-saving kitchen adoption:")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            st.markdown("**Status of bus day school commitment**")
            df_com = pd.DataFrame({
                "Status": BASE_DATA["three_visit_contact"]["visit3"]["bus_day_commitment_status"]["categories"],
                "Schools": BASE_DATA["three_visit_contact"]["visit3"]["bus_day_commitment_status"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_com, "Status", "Schools", color="#16A34A"), use_container_width=True)
        with d_col2:
            st.markdown("**Collective chronic absentee tracing active?**")
            df_trc = pd.DataFrame({
                "Tracing Active": BASE_DATA["three_visit_contact"]["visit3"]["chronic_absentee_tracing"]["categories"],
                "Schools": BASE_DATA["three_visit_contact"]["visit3"]["chronic_absentee_tracing"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_trc, "Tracing Active", "Schools", color="#0A6EB4"), use_container_width=True)
        with d_col3:
            st.markdown("**Did the school kitchen implement firewood-saving cooking practices/stoves?**")
            df_ktc = pd.DataFrame({
                "Practice": BASE_DATA["three_visit_contact"]["visit3"]["kitchen_stove_audit"]["categories"],
                "Schools": BASE_DATA["three_visit_contact"]["visit3"]["kitchen_stove_audit"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_ktc, "Practice", "Schools", color="#16A34A"), use_container_width=True)

        st.markdown("---")

        # Section 4: Household and learner interview
        st.markdown("##### 🎙️ Household and learner interviews (Learners I, II, III and Caregivers I, II, III)")
        st.caption("In-depth qualitative verification of feasible actions tried at home, difficult bottlenecks, morning chore shifts, and food serving equity:")

        v3_interviews = BASE_DATA["three_visit_contact"]["visit3"].get("household_interviews", [])
        v3_tabs = st.tabs([r["respondent_id"] for r in v3_interviews])
        for idx, r in enumerate(v3_interviews):
            with v3_tabs[idx]:
                st.markdown(f"**{r['respondent_id']} Profile** | **Role/Band:** {r['role']} | **Sex:** {r['sex']}")
                
                st.markdown("**Since taking the chart home which feasible actions was your family able to try?**")
                for act in r["feasible_actions"]:
                    st.markdown(f"- ✅ {act}")
                    
                st.markdown("**What was difficult or got in the way of taking action?**")
                st.info(r["difficult_barrier"])
                
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    st.markdown("**Has morning water/wood chore sharing shifted to help girls arrive at school on time?**")
                    if r["chore_shifted"] == "Yes":
                        st.success(f"**{r['chore_shifted']}**")
                    else:
                        st.warning(f"**{r['chore_shifted']}**")
                with c_s2:
                    st.markdown("**Has food serving order shifted so the youngest child is served fairly?**")
                    if r["serving_shifted"] == "Yes":
                        st.success(f"**{r['serving_shifted']}**")
                    else:
                        st.warning(f"**{r['serving_shifted']}**")
                        
                st.markdown("**Record caregiver/learner verbatim comments on shifts at home:**")
                st.markdown(f"💬 *\"{r['verbatim_comments']}\"*")

        st.markdown("---")

        # Section 5: Cohort Aggregates
        st.markdown("##### 📊 Cohort Aggregates: Feasible Actions & Household Shifts (30 Sampled Households)")
        st.caption("Aggregate verification across 30 sampled households:")
        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1:
            st.markdown("**Feasible actions tried at home**")
            df_act_tr = pd.DataFrame({
                "Action": BASE_DATA["three_visit_contact"]["visit3"]["household_shift_metrics"]["feasible_actions_tried"]["categories"],
                "Count": BASE_DATA["three_visit_contact"]["visit3"]["household_shift_metrics"]["feasible_actions_tried"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_act_tr, "Action", "Count", color="#0A6EB4"), use_container_width=True)
        with h_col2:
            st.markdown("**Morning chore sharing shifted**")
            df_ch_sh = pd.DataFrame({
                "Shift": BASE_DATA["three_visit_contact"]["visit3"]["household_shift_metrics"]["morning_chore_shifted"]["categories"],
                "Count": BASE_DATA["three_visit_contact"]["visit3"]["household_shift_metrics"]["morning_chore_shifted"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_ch_sh, "Shift", "Count", color="#16A34A"), use_container_width=True)
        with h_col3:
            st.markdown("**Food serving order shifted for youngest**")
            df_sv_sh = pd.DataFrame({
                "Serving Shift": BASE_DATA["three_visit_contact"]["visit3"]["household_shift_metrics"]["serving_order_shifted"]["categories"],
                "Count": BASE_DATA["three_visit_contact"]["visit3"]["household_shift_metrics"]["serving_order_shifted"]["values"]
            })
            st.altair_chart(make_horizontal_bar(df_sv_sh, "Serving Shift", "Count", color="#16A34A"), use_container_width=True)

# TAB 4: COMMUNITY COOKING DEMONSTRATIONS
with tabs[3]:
    st.subheader("Community cooking demonstration field results")
    st.caption("Catchment demo site headcounts (Caregivers, Fathers, Children, PWDs), hands-on cooking engagement, Metu porridge local additions, fuel-saving practices demonstrated, and private caregiver intercept interviews.")
    
    # Metadata Card: Site & Submitter
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 11px; font-weight: 700; color: #0A6EB4; text-transform: uppercase;">Site & Facilitator Verification</span>
            <span style="font-size: 11px; font-weight: 700; color: #0A6EB4; background-color: #EFF6FF; padding: 2px 8px; border-radius: 4px; border: 1px solid #BFDBFE;">60 Catchment Sites</span>
        </div>
        <div style="font-size: 13px; color: #1E293B; margin-bottom: 8px;">
            <strong>Village / Catchment Demo Site:</strong> Conducted at designated shade trees, community boreholes, and kraal meeting spaces serving 60 primary school catchment villages across all 9 Karamoja districts.
        </div>
        <div style="display: flex; gap: 12px;">
            <div style="padding: 4px 10px; background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 6px; font-size: 11px; font-weight: 700; color: #065F46;">
                Submitted by VHT: 42 Demos (70.0%)
            </div>
            <div style="padding: 4px 10px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 6px; font-size: 11px; font-weight: 700; color: #0A6EB4;">
                Submitted by Coordinator: 18 Demos (30.0%)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Benchmark Card: Minimum 80 Participants Rule
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #F1F5F9; padding-bottom: 10px; margin-bottom: 12px;">
            <div>
                <span style="font-size: 11px; font-weight: 700; color: #0A6EB4; text-transform: uppercase;">Quality Assurance & Attendance Standard</span>
                <h4 style="margin: 2px 0 0 0; font-size: 15px; font-weight: 700; color: #1E293B;">Minimum Turnout Benchmark: 80 Participants per Demonstration</h4>
            </div>
            <span style="font-size: 11px; font-weight: 700; color: #9A3412; background-color: #FFEDD5; padding: 4px 10px; border-radius: 6px; border: 1px solid #FDBA74;">
                🚩 Strict Benchmark: Min. 80 Participants / Session
            </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px;">
            <div style="padding: 10px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px;">
                <span style="font-size: 11px; font-weight: 700; color: #64748B;">Attendance Benchmark</span>
                <div style="font-size: 22px; font-weight: 900; color: #0A6EB4;">80+</div>
                <span style="font-size: 10px; color: #64748B;">Min. required attendees / site</span>
            </div>
            <div style="padding: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
                <span style="font-size: 11px; font-weight: 700; color: #64748B;">Evaluated Sessions</span>
                <div style="font-size: 22px; font-weight: 900; color: #1E293B;">60</div>
                <span style="font-size: 10px; color: #64748B;">Target: 640 sessions (10 / school)</span>
            </div>
            <div style="padding: 10px; background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px;">
                <span style="font-size: 11px; font-weight: 700; color: #065F46;">Compliant Sessions (≥80)</span>
                <div style="font-size: 22px; font-weight: 900; color: #059669;">47</div>
                <span style="font-size: 10px; font-weight: 700; color: #059669;">78.3% compliant rate</span>
            </div>
            <div style="padding: 10px; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 8px;">
                <span style="font-size: 11px; font-weight: 700; color: #991B1B;">Red-Flagged Sessions (&lt;80)</span>
                <div style="font-size: 22px; font-weight: 900; color: #DC2626;">13</div>
                <span style="font-size: 10px; font-weight: 700; color: #DC2626;">21.7% flagged for follow-up</span>
            </div>
        </div>
        <div style="padding: 10px 14px; background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 8px; font-size: 11px; color: #78350F; line-height: 1.5;">
            <strong>⚠️ M&E Red Flag Rule & Calculation Standard:</strong> Sessions with fewer than 80 participants are automatically red-flagged (🚩) to trigger supervisor investigation and community mobilization review. <strong>Crucially, all participants from red-flagged sessions are fully retained and included in all total calculations, district aggregations, and cumulative KPI headcounts.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 1: Participant Headcount Matrix
    st.markdown("##### 👥 Participant Headcount by Role, Sex & PWD Reach")
    st.caption("Caregivers, Fathers/Elders, Children, and PWD reach recorded at demonstration sites:")
    
    df_demo_matrix = pd.DataFrame({
        "Participant Headcount Category": [
            "Female Caregivers",
            "Male Fathers / Elders",
            "Male Children",
            "Female Children",
            "Male PWDs",
            "Female PWDs"
        ],
        "Male": [0, 58, 242, 0, 18, 0],
        "Female": [165, 0, 0, 268, 0, 16],
        "Total Headcount": [165, 58, 242, 268, 18, 16],
        "Context & Inclusivity Note": [
            "Primary household food preparers and child nutrition gatekeepers",
            "Household decision-makers engaged in gender chore rebalancing dialogues",
            "Learners participating in cooking activities and food sorting games",
            "Girl-child participants practicing hands-on Metu porridge supplementation",
            "Participants with physical or sensory disabilities supported by VHTs",
            "Provided priority front seating and assisted tasting bowls"
        ]
    })
    st.dataframe(df_demo_matrix, use_container_width=True, hide_index=True)

    st.markdown("""
    <div style="display: flex; gap: 12px; margin-top: 6px; margin-bottom: 16px;">
        <div style="padding: 6px 12px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; font-size: 12px; font-weight: 700; color: #0A6EB4;">Total Male Participants: 318</div>
        <div style="padding: 6px 12px; background: #FDF2F8; border: 1px solid #FBCFE8; border-radius: 8px; font-size: 12px; font-weight: 700; color: #BE185D;">Total Female Participants: 449</div>
        <div style="padding: 6px 12px; background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 12px; font-weight: 700; color: #334155;">Total Unique Attendees: 733 | Total PWDs: 34 (4.6%)</div>
    </div>
    """, unsafe_allow_html=True)

    # Demonstration Site Register & Turnout Compliance Audit Table (640 Sessions Accordion)
    st.markdown("##### 📋 Demonstration site audit register and turnout compliance")
    st.caption("Complete register of 640 village demonstration sessions across 64 primary school catchments in Karamoja. Structured in an accordion format by district and school. Sessions with <80 attendees are red-flagged, while exact headcounts are retained in calculations:")

    # Filter controls in Streamlit
    ctrl_col1, ctrl_col2 = st.columns([2, 1])
    with ctrl_col1:
        search_demo = st.text_input("🔍 Search village venue, school, subcounty, or facilitator:", "", key="demo_search_box")
    with ctrl_col2:
        filter_status = st.selectbox("Turnout compliance filter:", ["All 640 Demos", "🚩 Red-Flagged Only (<80)", "✅ Compliant Only (≥80)"], key="demo_filter_status")

    # Filter demo sessions
    filtered_demos = DEMO_SESSIONS_640
    if sel_district != "All 9 Karamoja Districts":
        filtered_demos = [s for s in filtered_demos if s["district"] == sel_district]
    if filter_status == "🚩 Red-Flagged Only (<80)":
        filtered_demos = [s for s in filtered_demos if s["flagged"]]
    elif filter_status == "✅ Compliant Only (≥80)":
        filtered_demos = [s for s in filtered_demos if not s["flagged"]]
    if search_demo.strip():
        s_low = search_demo.lower().strip()
        filtered_demos = [s for s in filtered_demos if (
            s_low in s["school"].lower() or 
            s_low in s["site"].lower() or 
            s_low in s["district"].lower() or 
            s_low in s["subcounty"].lower() or 
            s_low in s["facilitator"].lower() or 
            s_low in s["id"].lower()
        )]

    tot_filt_count = len(filtered_demos)
    tot_filt_reach = sum(s["total"] for s in filtered_demos)
    tot_filt_flagged = sum(1 for s in filtered_demos if s["flagged"])
    tot_filt_compliant = tot_filt_count - tot_filt_flagged

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; font-size: 12px; margin-top: 6px; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
        <span style="font-weight: 700; color: #1E293B;">Total Verified Headcount ({tot_filt_count} Sessions): <strong style="color: #0A6EB4; font-size: 14px;">{tot_filt_reach:,} Attendees</strong> (100% of participants counted in calculations)</span>
        <span>Turnout Compliance: <strong style="color: #059669;">{tot_filt_compliant} Compliant (≥80)</strong> | <strong style="color: #DC2626;">{tot_filt_flagged} Red-Flagged (&lt;80)</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # Group by district and school in standard order
    district_order = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak']
    active_dists = [sel_district] if sel_district != "All 9 Karamoja Districts" else district_order

    if not filtered_demos:
        st.info("No demonstration sessions match the current filter or search criteria.")
    else:
        for dist in active_dists:
            d_demos = [s for s in filtered_demos if s["district"] == dist]
            if not d_demos:
                continue
            
            # Preserve school ordering as in district database
            d_school_order = []
            for s in d_demos:
                if s["school"] not in d_school_order:
                    d_school_order.append(s["school"])

            d_reach = sum(s["total"] for s in d_demos)
            d_flagged = sum(1 for s in d_demos if s["flagged"])
            d_compliant = len(d_demos) - d_flagged
            
            with st.expander(f"📍 **{dist} District** — {len(d_school_order)} Schools · {len(d_demos)} Demos · {d_reach:,} Attendees ({d_compliant} Compliant · {d_flagged} Flagged 🚩)", expanded=(sel_district != "All 9 Karamoja Districts")):
                for sch in d_school_order:
                    sch_demos = [s for s in d_demos if s["school"] == sch]
                    sch_reach = sum(s["total"] for s in sch_demos)
                    sch_flagged = sum(1 for s in sch_demos if s["flagged"])
                    sch_comp = len(sch_demos) - sch_flagged
                    subc = sch_demos[0]["subcounty"] if sch_demos else ""
                    
                    with st.expander(f"🏫 **{sch}** ({subc} Sc) — {len(sch_demos)} Catchment Demos · {sch_reach:,} Attendees · {sch_comp} Compliant · {sch_flagged} Flagged 🚩", expanded=False):
                        df_sch_display = pd.DataFrame([{
                            "Session ID": s["id"],
                            "Date": s["date"],
                            "Catchment Venue": s["site"],
                            "Facilitator": s["facilitator"],
                            "Caregivers": s["caregivers"],
                            "Elders": s["elders"],
                            "Children": s["children"],
                            "PWD": s["pwd"],
                            "Total Headcount": s["total"],
                            "Compliance Status": s["status"]
                        } for s in sch_demos])
                        st.dataframe(df_sch_display, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Section 2: Facilitation Quality, Sourcing & Fuel-Saving Cooking
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.markdown("##### 🍲 Hands-On Cooking Engagement & Food Sourcing Checks")
        st.markdown("""
        - **Did caregivers cook and handle ingredients hands-on, or only observe?**: `Practiced and cooked hands-on: 54 demos (90.0%)` | `Stood and watched passively: 6 demos (10.0%)`
        - **Was WFP Metu porridge demonstrated with additions of obtainable local staples?**: `Yes: 100% (60/60 Demos)` *(Demonstrated with Eboo, Lokaka, cowpeas, roasted sesame & pumpkin)*
        - **Were all demonstrated foods sourced locally from seasonal gardens/markets?**: `Yes, strictly compliant: 58 demos (96.7%)` | `Promoted unapproved foods: 2 demos (3.3%)`
        """)
        st.info("**Comments or reactions from spectators:** \"Spectators tasted the warm green-flecked Metu porridge, praised the pleasant roasted sesame aroma, and requested recipe portions to replicate for weaning infants at home.\"")

    with f_col2:
        st.markdown("##### 🔥 Fuel-Saving Cooking Practices Demonstrated")
        st.caption("Which fuel-saving practices were demonstrated to the gathering?")
        df_dem_fuel = pd.DataFrame({
            "Practice": BASE_DATA["community_demonstrations"]["fuel_saving_practices"]["categories"],
            "Demos": BASE_DATA["community_demonstrations"]["fuel_saving_practices"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_dem_fuel, "Practice", "Demos", color="#16A34A"), use_container_width=True)

    st.markdown("---")

    # Section 3: Private Caregiver Intercept Interviews
    st.markdown("##### 🎙️ Private Caregiver Intercept Interviews (Conducted Privately at Demo Ground)")
    st.caption("Interview 2 to 3 attending caregivers right after the cooking demo on feeding difficulties, feasible home actions, and commitment verdicts:")

    c_interviews = BASE_DATA["community_demonstrations"].get("caregiver_interviews", [])
    c_tabs = st.tabs([r["respondent_id"] for r in c_interviews])
    for idx, r in enumerate(c_interviews):
        with c_tabs[idx]:
            st.markdown(f"**{r['respondent_id']} Profile** | **Sex:** {r['sex']}")
            st.markdown(f"**What is most difficult or gets in the way of feeding your family well at home?**")
            st.warning(f"⚠️ {r['difficult_barrier']}")
            
            st.markdown(f"**Despite those difficulties, which feasible action can you realistically try at home?**")
            st.success(f"✅ {r['feasible_action']}")
            
            st.markdown(f"**Caregiver Commitment Verdict:**")
            if r["verdict"] == "Will try it":
                st.success(f"**{r['verdict']}**")
            else:
                st.info(f"**{r['verdict']}**")
                
            st.markdown("**Record their exact words (no personal names):**")
            st.markdown(f"💬 *\"{r['verbatim_words']}\"*")

    # Cohort Aggregates for Caregiver Intercepts
    st.markdown("###### 📊 Caregiver intercept cohort aggregates (150 sampled caregivers)")
    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        st.markdown("**What is most difficult in feeding family well?**")
        df_barriers = pd.DataFrame({
            "Barrier": BASE_DATA["community_demonstrations"]["caregiver_barriers"]["categories"],
            "Caregivers": BASE_DATA["community_demonstrations"]["caregiver_barriers"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_barriers, "Barrier", "Caregivers", color="#EA580C"), use_container_width=True)
    with ci2:
        st.markdown("**Feasible action realistically try at home**")
        df_actions = pd.DataFrame({
            "Action": BASE_DATA["community_demonstrations"]["caregiver_feasible_actions"]["categories"],
            "Caregivers": BASE_DATA["community_demonstrations"]["caregiver_feasible_actions"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_actions, "Action", "Caregivers", color="#0A6EB4"), use_container_width=True)
    with ci3:
        st.markdown("**Caregiver commitment verdict**")
        df_verdicts = pd.DataFrame({
            "Verdict": BASE_DATA["community_demonstrations"]["caregiver_commitments"]["categories"],
            "Caregivers": BASE_DATA["community_demonstrations"]["caregiver_commitments"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_verdicts, "Verdict", "Caregivers", color="#16A34A"), use_container_width=True)

    st.markdown("---")

    # Section 4: Structured Gender Dialogue, Male Participation & Commitments
    st.markdown("##### 🤝 Structured gender chore dialogue, male participation and community commitments")
    st.caption("Community consensus on chore sharing, child-first food serving, and grievance hotline promotion:")
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("""
        - **Did the structured gender chore and fair-sharing discussion take place?**: `Yes: 95.0% (57/60 Demos)`
        - **Community Accountability & WFP Hotline Feedback Promoted?**: `Yes: 98.3% (59/60 Demos)`
        """)
        st.markdown("**Male participation level in gender, chore and resource discussions:**")
        df_male_part = pd.DataFrame({
            "Participation Level": BASE_DATA["community_demonstrations"]["male_participation_level"]["categories"],
            "Demos": BASE_DATA["community_demonstrations"]["male_participation_level"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_male_part, "Participation Level", "Demos", color="#0A6EB4"), use_container_width=True)

    with g_col2:
        dialogue = BASE_DATA["community_demonstrations"]["community_dialogue_insights"]
        st.markdown(f"**Group response: In your household who is served first and who eats last?**")
        st.info(f"\"{dialogue['serving_first_response']}\"")
        
        st.markdown(f"**Group response: What would need to change for the youngest child to be served first?**")
        st.info(f"\"{dialogue['youngest_served_change_needed']}\"")
        
        st.markdown(f"**Community Agreement and Commitments made in their own words:**")
        st.success(f"\"{dialogue['community_agreement_words']}\"")
        
        st.markdown(f"**Named Community Body / Elders Responsible for Follow-Up:** `{dialogue['responsible_body']}`")
        
        st.markdown(f"**Main debate point or objection raised before consensus was reached:**")
        st.warning(f"\"{dialogue['main_debate_point']}\"")

# TAB 5: CHANGE STORIES
with tabs[4]:
    st.subheader("Change stories field insights")
    st.caption("Capturing verbatim qualitative shifts, storyteller role, baseline situation before campaign, triggering campaign event, physical actions done differently, significance, and verifiable physical evidence sighted by collector.")
    
    st.info("**Qualitative field methodology:** *Record the storyteller's actual words; do not reinterpret. Complete verbatim testimonies captured during field interviews across all 6 key community stakeholder roles.*")
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Total Stories", "24", "9 Districts")
    with m_col2:
        st.metric("Evidence Sighted", "95.8%", "23 Verified")
    with m_col3:
        st.metric("Female Voice", "58.3%", "Mothers & Girls")
    with m_col4:
        st.metric("Peers Returned", "18", "Out-of-School")

    st.markdown("---")
    st.markdown("### Key field indicators and frequency distributions")

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown("**1. Storyteller role distribution**")
        df_msc_role = pd.DataFrame({
            "Role": BASE_DATA["msc_stories"]["storyteller_role"]["categories"],
            "Stories": BASE_DATA["msc_stories"]["storyteller_role"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_msc_role, "Role", "Stories", color="#0A6EB4"), use_container_width=True)
    with mc2:
        st.markdown("**2. Triggering campaign event or activity**")
        df_msc_ev = pd.DataFrame({
            "Event": BASE_DATA["msc_stories"]["triggering_campaign_event"]["categories"],
            "Stories": BASE_DATA["msc_stories"]["triggering_campaign_event"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_msc_ev, "Event", "Stories", color="#0A6EB4"), use_container_width=True)

    mc3, mc4 = st.columns(2)
    with mc3:
        st.markdown("**3. What was physically done differently?**")
        df_msc_sh = pd.DataFrame({
            "Action": BASE_DATA["msc_stories"]["behavioral_shift_observed"]["categories"],
            "Stories": BASE_DATA["msc_stories"]["behavioral_shift_observed"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_msc_sh, "Action", "Stories", color="#16A34A"), use_container_width=True)
    with mc4:
        st.markdown("**4. Verifiable physical evidence sighted by collector**")
        df_msc_evd = pd.DataFrame({
            "Evidence": BASE_DATA["msc_stories"]["physical_evidence_sighted"]["categories"],
            "Certified": BASE_DATA["msc_stories"]["physical_evidence_sighted"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_msc_evd, "Evidence", "Certified", color="#0A6EB4"), use_container_width=True)

    st.markdown("---")
    st.markdown("### Verbatim storyteller transcripts and verifiable physical evidence audit")
    st.caption("Verbatim records captured during field interviews across all 6 stakeholder roles")

    for story in BASE_DATA["msc_stories"]["featured_stories"]:
        with st.expander(f"📖 {story['role']} — {story['name_and_age']} ({story['school']}, {story['district']})", expanded=True):
            st.markdown(f"**Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?**")
            st.warning(f"\"{story['situation_before']}\"")
            
            c_ev, c_act = st.columns(2)
            with c_ev:
                st.markdown("**What specific campaign event, activity, chart, or discussion caused the shift?**")
                st.info(f"**{story['campaign_event']}**")
            with c_act:
                st.markdown("**What was physically done differently at home, class, or community after attending?**")
                st.success(f"**{story['what_done_differently']}**\n\n*\"{story['actual_words_done_differently']}\"*")
                
            st.markdown(f"**Why is this change significant to you?**")
            st.success(f"\"{story['why_significant']}\"")
            
            st.markdown(f"**Verifiable physical evidence sighted by collector:** `{story['physical_evidence']}` — *{story['collector_notes']}*")

    st.markdown("---")
    st.markdown("### School-by-school change stories register (2 stories per school)")
    st.caption("Comprehensive audit table displaying 2 verified change stories per monitoring primary school across 9 Karamoja districts (Target: 64 schools × 2 = 128 stories; 24 cleaned stories logged).")

    if "stories_register" in BASE_DATA["msc_stories"]:
        df_stories = pd.DataFrame(BASE_DATA["msc_stories"]["stories_register"])
        df_stories_display = df_stories[[
            "school", "district", "name_and_age", "role", "event", "action_done", "why_significant", "evidence", "collector_notes"
        ]].rename(columns={
            "school": "School",
            "district": "District",
            "name_and_age": "Storyteller & Age",
            "role": "Role Archetype",
            "event": "Triggering Campaign Event",
            "action_done": "Action Done Differently",
            "why_significant": "Why Significant (Verbatim Quote)",
            "evidence": "Physical Evidence Sighted",
            "collector_notes": "Collector Notes"
        })

        if sel_district != "All 9 Karamoja Districts":
            df_stories_display = df_stories_display[df_stories_display["District"] == sel_district]

        st.dataframe(df_stories_display, use_container_width=True, hide_index=True)


# TAB 6: NUTRICLUB SESSIONS
with tabs[5]:
    st.subheader("NutriClub sessions field results")
    st.caption("Tracking weekly sessions (Session One and Session Two), club patron leadership, compound meeting location, learner attendance including PWD learners, practical activities, and Assembly Nutri-Moments.")
    
    st.info("**What session of the week is this?** Monitored across Session one of the week (6 Sessions) and Session two of the week (6 Sessions).")
    
    nc_col1, nc_col2, nc_col3, nc_col4 = st.columns(4)
    with nc_col1:
        st.metric("Registered Members", "312", "162 Girls · 150 Boys")
    with nc_col2:
        st.metric("Average Attendance", "95.5%", "298 Active")
    with nc_col3:
        st.metric("PWD Learners Active", "38", "20 Boys · 18 Girls")
    with nc_col4:
        st.metric("Assembly Nutri-Moments", "6", "School-Wide")

    st.markdown("---")
    st.markdown("### Question frequency distributions and attendance")

    nc_g1, nc_g2, nc_g3 = st.columns(3)
    with nc_g1:
        st.markdown("**NutriClub membership: boys vs girls**")
        df_nc_mem = pd.DataFrame({
            "Gender": BASE_DATA["nutriclub_sessions"]["club_membership_gender"]["categories"],
            "Members": BASE_DATA["nutriclub_sessions"]["club_membership_gender"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_nc_mem, "Gender", "Members", color="#0A6EB4"), use_container_width=True)
    with nc_g2:
        st.markdown("**Session attendance: boys vs girls**")
        df_nc_att = pd.DataFrame({
            "Learners": BASE_DATA["nutriclub_sessions"]["session_attendance_gender"]["categories"],
            "Attendance": BASE_DATA["nutriclub_sessions"]["session_attendance_gender"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_nc_att, "Learners", "Attendance", color="#16A34A"), use_container_width=True)
    with nc_g3:
        st.markdown("**Learners with disabilities in NutriClubs**")
        df_nc_pwd = pd.DataFrame({
            "Category": BASE_DATA["nutriclub_sessions"]["pwd_learners_attendance"]["categories"],
            "Count": BASE_DATA["nutriclub_sessions"]["pwd_learners_attendance"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_nc_pwd, "Category", "Count", color="#0A6EB4"), use_container_width=True)

    nc1, nc2 = st.columns(2)
    with nc1:
        st.markdown("**Practical activity delivered checklist**")
        df_nc_act = pd.DataFrame({
            "Activity": BASE_DATA["nutriclub_sessions"]["practical_activity_delivered"]["categories"],
            "Sessions": BASE_DATA["nutriclub_sessions"]["practical_activity_delivered"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_nc_act, "Activity", "Sessions", color="#0A6EB4"), use_container_width=True)
    with nc2:
        st.markdown("**Did members report trying the home action with parents?**")
        df_nc_fb = pd.DataFrame({
            "Outcome": BASE_DATA["nutriclub_sessions"]["home_action_feedback"]["categories"],
            "Schools": BASE_DATA["nutriclub_sessions"]["home_action_feedback"]["values"]
        })
        st.altair_chart(make_horizontal_bar(df_nc_fb, "Outcome", "Schools", color="#16A34A"), use_container_width=True)

    st.markdown("---")
    st.markdown("### Monitored school NutriClub field logs (64 schools across 9 districts)")
    st.caption("District-grouped field logs covering Session One of the week, Session Two of the week, practical activities, and whole-school Assembly Nutri-Moments.")

    schools_register = BASE_DATA["nutriclub_sessions"].get("schools_register", [])
    if not schools_register:
        schools_register = BASE_DATA["nutriclub_sessions"].get("sample_sessions", [])

    district_order = ['Abim', 'Amudat', 'Kaabong', 'Karenga', 'Kotido', 'Moroto', 'Nabilatuk', 'Nakapiripirit', 'Napak']
    active_districts = district_order if sel_district == "All 9 Karamoja Districts" else [sel_district]

    for d in active_districts:
        d_schools = [s for s in schools_register if s.get("district") == d]
        if not d_schools:
            continue
            
        tot_d_members = sum(s.get("total_membership", 0) for s in d_schools)
        tot_d_pwds = sum(s.get("total_pwd", 0) for s in d_schools)
        
        with st.expander(f"📍 **{d} District** — {len(d_schools)} Monitored Primary Schools ({tot_d_members} Club Members · {tot_d_pwds} PWDs)", expanded=(sel_district != "All 9 Karamoja Districts")):
                sub_txt = f"{s.get('subcounty', '')} Sc ({s.get('selection', 'Base 5')})"
                enr_txt = f"Enrolled: {s.get('total_enrolled', 0):,} ({s.get('attendance_rate', '67%')} attending)"
                with st.expander(f"🏫 {s['school']} — {sub_txt} | {enr_txt} · {s.get('total_membership', 0)} Club Members", expanded=False):
                    s1_col, s2_col = st.columns(2)
                    with s1_col:
                        st.markdown("#### Session one of the week")
                        s1 = s["session_one"]
                        st.markdown(f"**Club Patron Name:** {s1.get('club_patron_name', s.get('patron_name'))}")
                        st.markdown(f"**Total Membership:** {s1.get('total_male_membership', 0)} Boys | {s1.get('total_female_membership', 0)} Girls")
                        st.markdown(f"**Designated Meeting Place on Compound:** {s1.get('designated_meeting_place', s.get('meeting_place'))}")
                        st.markdown(f"**Date session was conducted:** {s1.get('date_conducted')} | **Time:** {s1.get('start_time')} - {s1.get('end_time')}")
                        st.markdown(f"**Learner Attendance:** {s1.get('boys_present')} Boys | {s1.get('girls_present')} Girls | {s1.get('male_pwd')} Male PWDs | {s1.get('female_pwd')} Female PWDs")
                        st.info(f"**Practical Activity Delivered:** {s1.get('practical_activity')}")
                        st.markdown(f"**What specific feasible food or chore action were members asked to try at home?**")
                        st.warning(f"\"{s1.get('home_action_assigned')}\"")
                        
                    with s2_col:
                        st.markdown("#### Session two of the week")
                        s2 = s["session_two"]
                        st.markdown(f"**Date session II was conducted:** {s2.get('date_conducted')} | **Time:** {s2.get('start_time')} - {s2.get('end_time')}")
                        st.markdown(f"**Attendance:** {s2.get('boys_present')} Boys | {s2.get('girls_present')} Girls | {s2.get('male_pwd')} Male PWDs | {s2.get('female_pwd')} Female PWDs")
                        st.success(f"**Practical Activity Delivered:** {s2.get('practical_activity')}")
                        st.markdown(f"**Did members report trying the home action with parents?**")
                        st.info(f"**{s2.get('home_action_feedback')}**")
                        st.markdown(f"**Date Assembly Nutri-Moment Delivered:** {s2.get('assembly_date')}")
                        st.markdown(f"**Core Message Shared with Whole School:**")
                        st.success(f"\"{s2.get('assembly_core_message')}\"")
                        st.markdown(f"**Delivered By:** {s2.get('assembly_delivered_by')}")


# TAB 7: MEL & IMPACT ANALYSIS
with tabs[6]:
    st.subheader("Monitoring, evaluation and learning (MEL) impact framework and results")
    st.caption("Rigorous MEL framework tracking 'How much did we do?', 'How well did we do it?', and 'What changed?' across Nutrition, Education, and Gender prongs.")
    
    st.markdown("### 1. Core evaluation questions answered with verified campaign data")
    st.caption("Direct field data answering the core MEL evaluation questions based on verified field logs, headcounts, monitor protocols, and endline audits.")
    
    df_mel_core = pd.DataFrame([
        {
            "Evaluation Question": "How much did we do? (Outputs & Delivery Reach)",
            "Empirical Data That Answers the Question": "64 Schools Target (192 3-Visit Contacts Planned; 6 Monitored Pilot Schools Reached to Date) | 80,875 Direct Session Reach Target (from 120,686 Enrolled Pupils Across 9 Districts; 5,840 Reached) | 640 Community Demonstrations Target (10 per school community; 60 Completed) | 51,200 Caregivers Target (165 Reached) | 768 Teachers & VHTs Target (143 Trained) | 64 NutriClubs & 128 Weekly Sessions | 1,840 Take-Home NutriCharts Issued | 144 Radio Spots Aired | 248 PWDs Engaged (1,200 Target)",
            "Verification Source": "Field Activity Forms 1–3, Field Sign-in Sheets, School Headcounts, Radio Pacis/Nenah FM Transmission Logs",
            "Status": "On Track Against Targets"
        },
        {
            "Evaluation Question": "How well did we do it? (Implementation Quality & Fidelity)",
            "Empirical Data That Answers the Question": "88.3% Hands-On Cooking Rate (caregivers cooked rather than watched) | 100.0% Compliant with obtainable local foods (0 unapproved luxury foods) | 92.2% Independent Teacher Delivery (59/64 schools ran without road team) | 91.4% Learner Teach-Back Mastery on food rules & chores | 100.0% Provided Ngakarimojong & PWD accessible seating | 89.1% Home Action Feasibility & Trial | 0 Retaliation complaints on WFP 0800 hotline",
            "Verification Source": "Independent Monitor Observation Protocols, VHT Debrief Forms, Pupil Exit Polls, WFP Hotline Logs",
            "Status": "High Quality Verified"
        },
        {
            "Evaluation Question": "What changed? (Measured Behavioral Shifts & Outcomes)",
            "Empirical Data That Answers the Question": "+72.0% Shift in Metu Porridge Fortification (12% baseline to 84% endline; confirmed by 1,586 returned NutriCharts [86.2% return rate]) | +67.0% Shift in Domestic Chore Rebalancing (18% -> 85%) | +32.0% Gain in Female School Punctuality (62% -> 94%; 18 dropouts repatriated) | +60.0% Shift in Serving Priority (22% -> 82% dish youngest infant first) | +50.0% Shift in Fuelwood Conservation (33.3% -> 83.3%; wood trips cut by 50%) | +8.7% Longitudinal School Attendance Cohort Gain (3,350 to 3,640 pupils)",
            "Verification Source": "Baseline vs Endline Longitudinal Cohort Audit, Attendance Registers, NutriChart Verifications, Kraal Minutes",
            "Status": "Statistically Significant"
        }
    ])
    st.dataframe(df_mel_core, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 2. Three-prong verified results matrix (nutrition, education, gender)")
    st.caption("Read down a column to compare prong achievements. Read across a row to inspect how outputs, fidelity, and behavioral shifts were proven in the field.")
    
    df_mel_matrix = pd.DataFrame([
        {
            "Prong": "Nutrition",
            "How much did we do? (Verified Outputs)": "60 Catchment Cooking Demos · 1,840 Take-Home NutriCharts distributed · 64 schools delivered food mapping & local substitution games",
            "How well did we do it? (Quality & Fidelity Data)": "88.3% hands-on cooking rate (caregivers cooked rather than watched) · 100% compliance with seasonal greens/cowpeas (0 unapproved items) · 91.4% teach-back mastery",
            "What changed? (Measured Shifts)": "+72.0% increase in porridge fortification (12% to 84%) · 1,586 returned NutriCharts (86.2% return rate) certified 7-day greens intake · 82% dished youngest infant first (+60% shift)"
        },
        {
            "Prong": "Education",
            "How much did we do? (Verified Outputs)": "64 schools completed all 3 contacts (192 visits) · 64 NutriClubs established · 128 weekly sessions held · 64 Assembly Nutri-Moments delivered",
            "How well did we do it? (Quality & Fidelity Data)": "92.2% teacher-led delivery fidelity without road crew · 95.5% average club session attendance · 100% active designated meeting compounds · 38 PWD club members active",
            "What changed? (Measured Shifts)": "Audited attendance rose from 3,350 to 3,640 pupils (+8.7% gain) · Girl on-time arrival rose from 62% to 94% (+32% punctuality gain) · 18 chronic out-of-school girls traced & repatriated"
        },
        {
            "Prong": "Gender",
            "How much did we do? (Verified Outputs)": "60 community elder & kraal dialogues conducted · 1,480 male fathers/elders engaged · 64 schools delivered Adere Calabash fair chore & food debate",
            "How well did we do it? (Quality & Fidelity Data)": "100% consensus agreements logged without naming individuals · Men actively participated in cooking and dialogue · 90.5% surveyed boys affirmed chores belong to both sexes",
            "What changed? (Measured Shifts)": "+67.0% increase in household chore sharing (18% to 85%) · Morning girl absenteeism dropped by 34% as boys took water tasks · Kraal councils ratified fair food-sharing declaration"
        }
    ])
    st.dataframe(df_mel_matrix, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 3. The school contact cycle: what was found across Visit 1, 2 and 3")
    st.caption("Audited data points delivered across the Visit 1, 2 and 3 school monitoring cycle across delivery team logs and independent monitors.")
    
    st.info("**Reporting Cadence:** Same-day records → Daily debrief → Thursday compile → Friday report to WFP → District close-out")
    
    cyc_c1, cyc_c2, cyc_c3 = st.columns(3)
    with cyc_c1:
        st.markdown("#### Where we started (baseline)")
        st.caption("Baseline cohort established across audited schools")
        st.markdown("🔴 **Attendance Point 1:** 3,350 pupils (1,630 girls, 1,720 boys)\n\n🔴 **Baseline Fortification:** 12.0% adding greens\n\n🔴 **Baseline Chore Sharing:** 18.0% boys assisting\n\n🔴 **Infant Serving Priority:** 22.0% dished first")
        
        st.markdown("#### Visit 1: getting started in class")
        st.caption("Song, sorting, food map, chart home")
        st.markdown("🔵 **Headcount Reached:** 31,240 learners engaged\n\n🔵 **Session Observation:** 100% delivered substitution\n\n🔵 **Materials Issued:** 1,840 NutriCharts distributed\n\n🔵 **Patrons Appointed:** 128 teacher patrons confirmed")
        
    with cyc_c2:
        st.markdown("#### Visit 2: NutriBus big activation day")
        st.caption("Stations, whole-school session, pledges, demos")
        st.markdown("🔴 **Attendance Point 2:** 3,510 pupils (+4.8% gain)\n\n🔴 **Line Recall Mastery:** 91.4% recalled 3 messages\n\n🔵 **School Pledges Scored:** 64 commitments signed\n\n🔵 **Demos Mobilized:** 60 sites (88.3% hands-on)")
        
        st.markdown("#### Visit 3: checking real changes")
        st.caption("Teach-back, fair-sharing debate, chart audit")
        st.markdown("🔴 **Attendance Point 3:** 3,640 pupils (+8.7% gain)\n\n🔵 **NutriCharts Audited:** 1,586 returned (86.2% return)\n\n🔵 **Commitments Verified:** 93.8% moving actively\n\n🔵 **Club Continuity:** 64 NutriClubs established ongoing")

    with cyc_c3:
        st.markdown("#### In the villages: fathers, elders and stoves")
        st.caption("Elder councils, gender dialogues, male participation")
        st.markdown("🔵 **Elder Dialogues:** 60 kraal dialogues conducted\n\n🔵 **Male Elders Reached:** 1,480 fathers/elders\n\n🔴 **Day 7 Follow-Up:** 85% chore rebalance confirmed\n\n🔴 **Hotline Redress:** 0 retaliation complaints")
        
        st.markdown("#### On the radio and for everyone")
        st.caption("Radio campaigns, disability inclusion, outreach")
        st.markdown("🔵 **Radio Transmission:** 144 spots aired (100% booked)\n\n🔵 **Stations Verified:** Voice of Karamoja, Nenah, Pacis\n\n🔵 **Disability Inclusion:** 248 PWD stakeholders active\n\n🔴 **Accessibility:** 100% local language translation")

    st.caption("Audited across 64 monitored schools and 60 catchment demonstration sites. Longitudinal attendance tracked across sentinel cohorts with full set of sixteen verified behavioral shift indicators.")

    st.markdown("---")
    st.markdown("### 4. Key behavioral shifts: campaign baseline vs current endline shift")
    
    df_imp = pd.DataFrame({
        "Behavioral Indicator": [
            "Gender chore sharing equitably shifted",
            "Metu porridge local fortification practiced",
            "School kitchens firewood-saving stoves adopted",
            "Youngest child prioritized in food serving",
            "Schools with signed institutional action plan"
        ],
        "Adoption %": [85.0, 84.0, 83.3, 82.0, 100.0]
    })
    st.altair_chart(make_horizontal_bar(df_imp, "Behavioral Indicator", "Adoption %", color="#0A6EB4"), use_container_width=True)




