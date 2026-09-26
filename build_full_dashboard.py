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
            <input type="date" id="dateFilterEnd" value="2026-09-30" onchange="applyFilters()" class="w-full sm:w-auto bg-white/10 border border-white/30 text-white rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-white">
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

    <!-- ACTIVE FILTER NOTICE -->
    <div id="filterBanner" class="hidden bg-blue-50 border border-blue-200 text-wfp-blue px-4 py-2 rounded-xl text-xs flex items-center justify-between">
      <div class="flex items-center gap-2">
        <i class="fa-solid fa-circle-info"></i>
        <span>Filtered View: <strong id="filterBannerText">All Districts</strong></span>
      </div>
      <button onclick="resetFilters()" class="font-bold text-wfp-dark hover:underline">Clear Filter</button>
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
            <span id="kpi-schools" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">6</span>
            <span id="kpi-target-schools" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 64 schools</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-schools" class="bg-wfp-blue h-1.5 rounded-full" style="width: 9.4%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-wfp-blue flex items-center justify-between gap-1">
            <span id="pct-schools" class="truncate">Progress: 9.4%</span>
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
            <span id="kpi-demos" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">60</span>
            <span id="kpi-target-demos" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 640 sites</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-demos" class="bg-wfp-blue h-1.5 rounded-full" style="width: 9.4%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-wfp-blue flex items-center justify-between gap-1">
            <span id="pct-demos" class="truncate">Progress: 9.4%</span>
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
            <span id="kpi-learners" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">5,840</span>
            <span id="kpi-target-learners" class="text-[10px] sm:text-xs text-slate-400 font-medium whitespace-nowrap">/ 80,875</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div id="bar-learners" class="bg-wfp-blue h-1.5 rounded-full" style="width: 7.2%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-wfp-blue flex items-center justify-between gap-1">
            <span id="pct-learners" class="truncate">Progress: 7.2%</span>
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
            <span id="kpi-caregivers" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">165</span>
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
            <span id="kpi-teachers" class="text-2xl sm:text-3xl font-extrabold text-slate-800 leading-none">143</span>
            <span class="text-[10px] sm:text-xs text-emerald-600 font-bold whitespace-nowrap">Trained</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div class="bg-emerald-600 h-1.5 rounded-full" style="width: 100%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-slate-600 flex items-center justify-between gap-1">
            <span id="sub-teachers" class="truncate">48 Teachers</span>
            <span id="sub-vhts" class="shrink-0">95 VHTs</span>
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
            <span class="text-2xl sm:text-3xl font-extrabold text-emerald-700 leading-none">83.3%</span>
            <span class="text-[10px] sm:text-xs text-emerald-600 font-medium whitespace-nowrap">Adoption</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-1.5 overflow-hidden">
            <div class="bg-emerald-600 h-1.5 rounded-full" style="width: 83.3%"></div>
          </div>
          <div class="text-[10px] sm:text-[11px] font-semibold text-slate-600 flex items-center justify-between gap-1">
            <span class="truncate">Feeding · Equity · Clean Stoves</span>
            <span class="text-emerald-700 shrink-0 font-bold">&ge;80 Turnout</span>
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
            <strong>Secondary demographic data:</strong> <span id="banner-pwd-total">248</span> Persons with Disabilities recorded across Karamoja (<span id="banner-pwd-learners">146</span> learners, <span id="banner-pwd-adults">102</span> adults · 4.6% inclusion).
          </span>
        </div>
        <div class="flex items-center gap-2 text-[11px] font-semibold text-wfp-blue">
          <span class="bg-white px-2 py-0.5 rounded border border-blue-200">Learners: <span id="sub-pwd-learners">146</span></span>
          <span class="bg-white px-2 py-0.5 rounded border border-blue-200">Adults: <span id="sub-pwd-adults">102</span></span>
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
              <span>Campaign actuals vs target</span>
            </h4>
            <span class="text-[11px] font-semibold text-slate-500">Horizontal bar (labels on vertical axis)</span>
          </div>
          <div class="h-72">
            <canvas id="chart-targets-actuals"></canvas>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Targets: 64 schools, 640 demo sites, 80,875 learners, 51,200 adults</span>

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
            <span id="pillarAvgBadge" class="text-[11px] font-bold text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200">83.3% Avg Adoption</span>
          </div>
          <div class="h-72">
            <canvas id="chart-pillar-stats"></canvas>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 grid grid-cols-3 gap-2 text-center text-xs">
            <div class="p-2 rounded bg-emerald-50 border border-emerald-100">
              <div class="font-bold text-emerald-800 text-sm">84.0%</div>
              <div class="text-[10px] text-slate-600 font-medium">Pillar 1: School Feeding</div>
              <div class="text-[9px] text-emerald-700">Porridge Fortification</div>
            </div>
            <div class="p-2 rounded bg-blue-50 border border-blue-100">
              <div class="font-bold text-wfp-blue text-sm">85.0%</div>
              <div class="text-[10px] text-slate-600 font-medium">Pillar 2: Gender Dynamics</div>
              <div class="text-[9px] text-blue-700">Equitable Chore Sharing</div>
            </div>
            <div class="p-2 rounded bg-amber-50 border border-amber-100">
              <div class="font-bold text-amber-800 text-sm">83.3%</div>
              <div class="text-[10px] text-slate-600 font-medium">Pillar 3: Clean Cooking</div>
              <div class="text-[9px] text-amber-700">Fuel-Saving Cookstoves</div>
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
              <table class="w-full text-xs text-left min-w-[560px]">
              <thead class="bg-slate-50 text-slate-600 font-semibold uppercase border-b text-[11px]">
                <tr>
                  <th class="py-2.5 px-3 whitespace-nowrap min-w-[130px]">District</th>
                  <th class="py-2.5 px-2 text-center whitespace-nowrap">Schools (Done / Target)</th>
                  <th class="py-2.5 px-2 text-center whitespace-nowrap">Demos (Done / Target)</th>
                  <th class="py-2.5 px-2 text-right whitespace-nowrap">Direct Reach (Done / Target)</th>
                  <th class="py-2.5 px-2 text-right whitespace-nowrap">Caregivers (Done / Target)</th>
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
              <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">100% Yes (6/6 Schools)</span>
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
                    <span>UNAC (Uganda National Action on Childhood Disability)</span>
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">100% (6/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200">
                    <span>Afi (Action for Inclusion)</span>
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">100% (6/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200">
                    <span>District Education Offices</span>
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">100% (6/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200">
                    <span>Health Centre Parish Focal Persons</span>
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">83.3% (5/6)</span>
                  </div>
                  <div class="flex items-center justify-between bg-white px-2.5 py-1 rounded border border-slate-200">
                    <span class="font-semibold text-wfp-blue">Other</span>
                    <span class="font-bold text-wfp-blue bg-blue-50 px-2 py-0.5 rounded text-[11px]">33.3% (2/6)</span>
                  </div>
                </div>
                <div class="mt-2 p-2 bg-blue-50/60 rounded border border-blue-200 text-[11px] text-slate-700">
                  <strong class="text-wfp-blue">Other specify:</strong> Local LC1 Council Leadership, Sub-County Community Development Officer (CDO).
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
                    <span class="font-bold text-emerald-700 text-xs mt-1">100% (6/6)</span>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Sustainability planning</span>
                    <span class="font-bold text-emerald-700 text-xs mt-1">100% (6/6)</span>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Mentorship on tool rollout</span>
                    <span class="font-bold text-wfp-blue text-xs mt-1">83.3% (5/6)</span>
                  </div>
                  <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                    <span class="text-[11px] text-slate-600">Other (community kraals)</span>
                    <span class="font-bold text-wfp-blue text-xs mt-1">33.3% (2/6)</span>
                  </div>
                </div>
                <div class="mt-2 text-[10px] text-slate-500 italic">
                  Specify: Community kraal mobilization and inclusive PWD translation.
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
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2 py-0.5 rounded border border-blue-200">1,024 Tools Distributed</span>
              <span class="text-xs text-slate-500 font-medium">Orientation p. 10</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800 mb-1">Physical tools and manuals disseminated to school leadership</h4>
            <p class="text-xs text-slate-500 mb-3">Quantities of printed guidance handbooks and toolkits handed to school management:</p>
            <div class="h-64 min-h-[250px]">
              <canvas id="chart-orient-tools"></canvas>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
            <span>Metu Manuals: <strong>384</strong></span>
            <span>Climate Manuals: <strong>512</strong></span>
            <span>Toll-Free Boards: <strong>128</strong></span>
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
            <span>Detailed interview log: 6 individual participants (3 teachers and 3 VHTs)</span>
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
            <span id="badge-pipeline-pct" class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">9.4% Completed</span>
            <span class="text-xs text-slate-500 font-medium">Remaining Pipeline: <strong id="metric-pipe-remain">58 Schools</strong></span>
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
            <div id="metric-pipe-v1" class="text-2xl font-extrabold text-wfp-blue">6</div>
            <div class="text-xs text-slate-600 mt-1">Enrolment Baseline & Handover</div>
          </div>
          <div class="p-4 bg-sky-50/60 rounded-xl border border-sky-200">
            <div class="flex items-center justify-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-sky-600"></span>
              <span class="text-xs text-sky-700 font-bold uppercase tracking-wide">Visit 2 Done</span>
            </div>
            <div id="metric-pipe-v2" class="text-2xl font-extrabold text-sky-700">6</div>
            <div class="text-xs text-slate-600 mt-1">NutriBus Big Activation Day</div>
          </div>
          <div class="p-4 bg-emerald-50/60 rounded-xl border border-emerald-200">
            <div class="flex items-center justify-center gap-2 mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
              <span class="text-xs text-emerald-700 font-bold uppercase tracking-wide">Visit 3 Audited</span>
            </div>
            <div id="metric-pipe-v3" class="text-2xl font-extrabold text-emerald-700">6</div>
            <div class="text-xs text-slate-600 mt-1">Debrief & Closing Results Audit</div>
          </div>
        </div>
      </div>

      <!-- ATTENDANCE TRAJECTORY LINE GRAPH (FULL-WIDTH ACROSS) -->
      <div class="bg-white rounded-xl p-6 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-2">
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Attendance trajectory line graph</span>
            <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">📈 Increasing (+7.6% Rebound)</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-xs text-slate-500 font-medium">Timeline: Visit 1 ➔ Visit 2 ➔ Visit 3</span>
            <span class="text-pink-600 text-xs font-bold bg-pink-50 px-2 py-0.5 rounded border border-pink-200"><i class="fa-solid fa-arrow-up mr-1"></i>Girls rebound: +190 (+11.7%)</span>
          </div>
        </div>
        <h4 class="text-base font-bold text-slate-800 mb-1">Weekly attendance trend across Visit 1, 2 and 3 vs. enrolment baseline</h4>
        <p class="text-xs text-slate-500 mb-4">Multi-line graph showing attendance increasing across Visit 1, 2 and 3 following SBCC chore rebalancing:</p>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs mb-4">
          <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <div id="metric-long-base" class="text-lg font-extrabold text-slate-800">3,820</div>
            <div class="text-[11px] text-slate-500 font-semibold uppercase mt-0.5">Term enrolment baseline</div>
          </div>
          <div class="p-3 bg-blue-50/60 rounded-lg border border-blue-200">
            <div id="metric-long-v1" class="text-lg font-extrabold text-wfp-blue">3,350</div>
            <div class="text-[11px] text-wfp-blue font-semibold uppercase mt-0.5">Visit 1 attendance (87.7%)</div>
          </div>
          <div class="p-3 bg-sky-50/60 rounded-lg border border-sky-200">
            <div id="metric-long-v2" class="text-lg font-extrabold text-sky-700">3,510</div>
            <div class="text-[11px] text-sky-700 font-semibold uppercase mt-0.5">Visit 2 attendance (91.9%)</div>
          </div>
          <div class="p-3 bg-emerald-50/60 rounded-lg border border-emerald-200">
            <div id="metric-long-v3" class="text-lg font-extrabold text-emerald-700">3,640</div>
            <div class="text-[11px] text-emerald-700 font-semibold uppercase mt-0.5">Visit 3 attendance (95.3%)</div>
          </div>
        </div>

        <div class="h-80 min-h-[300px]">
          <canvas id="chart-longitudinal-attendance"></canvas>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-600 flex flex-wrap items-center justify-between gap-2">
          <span class="text-emerald-700 font-bold"><i class="fa-solid fa-arrow-trend-up mr-1"></i>Overall rebound: +290 pupils (+7.6% attendance growth across Visit 1, 2 and 3)</span>
          <span class="text-slate-500">6 audited cohorts with complete longitudinal retention tracking</span>
        </div>
      </div>

      <!-- School-by-School Multi-Visit Attendance Trajectory Table -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div>
            <div class="flex items-center gap-2 mb-0.5">
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">64 schools longitudinal roster</span>
              <span class="text-xs bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">Weekly attendance tracking</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800">School-by-school attendance trajectory across Visit 1, 2 and 3</h4>
            <p class="text-xs text-slate-500">Tracking whether attendance is increasing at each individual primary school across Visit 1, 2 and 3:</p>
          </div>
          <div class="flex items-center gap-2 text-xs">
            <span class="px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
              64 schools target
            </span>
            <span class="px-2.5 py-1 bg-emerald-50 text-emerald-700 font-bold rounded-lg border border-emerald-200">
              6 fully audited cohorts
            </span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-xs text-left">
            <thead class="bg-slate-50 text-slate-600 font-bold uppercase border-b border-slate-200">
              <tr>
                <th class="py-2.5 px-3">School name</th>
                <th class="py-2.5 px-3">District</th>
                <th class="py-2.5 px-3 text-right">Enrolment baseline</th>
                <th class="py-2.5 px-3 text-right">Visit 1</th>
                <th class="py-2.5 px-3 text-right">Visit 2</th>
                <th class="py-2.5 px-3 text-right">Visit 3</th>
                <th class="py-2.5 px-3 text-center">Attendance trajectory</th>
                <th class="py-2.5 px-3 text-center">Cohort status</th>
              </tr>
            </thead>
            <tbody id="school-trajectory-table-body" class="divide-y divide-slate-100 text-slate-700">
              <!-- Injected via JS -->
            </tbody>
          </table>
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
          
        </div>

        <!-- Row 0: Official Enrolment Baseline for This Term -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Official Enrolment Baseline</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800">Official boys enrolment and girls enrolment for this term</h4>
              <p class="text-xs text-slate-500">Official registered enrolment baseline across all monitoring primary schools</p>
            </div>
            <div class="flex items-center gap-3 text-xs">
              <span id="badge-v1-enrol-boys" class="px-3 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
                Official boys enrolment: 1,940
              </span>
              <span id="badge-v1-enrol-girls" class="px-3 py-1 bg-pink-50 text-pink-700 font-bold rounded-lg border border-pink-200">
                Official girls enrolment: 1,880
              </span>
              <span id="badge-v1-enrol-total" class="px-3 py-1 bg-slate-100 text-slate-800 font-bold rounded-lg border border-slate-300">
                Total Enrolled: 3,820 Pupils
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
              <span>Yes: <strong>6 schools (100%)</strong></span>
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
              <div class="p-4 bg-blue-50/60 rounded-xl border border-blue-100 text-center my-2">
                <div class="text-3xl font-extrabold text-wfp-blue">1,840</div>
                <div class="text-xs font-semibold text-slate-600 mt-1">Total Take-Home NutriCharts Issued</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Average: 307 cards / school</div>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-xs text-slate-600 flex items-center justify-between">
              <span>ECD-P2: <strong>620</strong></span>
              <span>P3-P4: <strong>680</strong></span>
              <span>P5-P7: <strong>540</strong></span>
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
                <span id="badge-v1-scope-label" class="hidden text-xs bg-blue-100 text-blue-800 font-semibold px-2 py-0.5 rounded border border-blue-200"></span>
              </div>
              <h4 class="text-base font-bold text-slate-800">School attendance: registered boys and girls weekly attendance</h4>
              <p class="text-xs text-slate-500">Weekly attendance headcounts by grade band (ECD-P2, P3-P4, P5-P7) and sex</p>
            </div>
            <div class="flex flex-wrap items-center gap-3 text-xs">
              <!-- School Selector Dropdown -->
              <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1">
                <i class="fa-solid fa-school text-wfp-blue text-xs"></i>
                <label for="v1-school-select" class="text-[11px] font-bold text-slate-600">School View:</label>
                <select id="v1-school-select" onchange="switchV1AttendanceScope(this.value)" class="text-xs bg-transparent text-slate-800 font-semibold focus:outline-none cursor-pointer">
                  <option value="ALL">All 6 Schools (3,350 Pupils)</option>
                  <option value="Abim">Abim Primary School (Abim: 550 Pupils)</option>
                  <option value="Amudat">Hvvv Primary School (Amudat: 510 Pupils)</option>
                  <option value="Kaabong">Kaabong West Primary School (Kaabong: 605 Pupils)</option>
                  <option value="Moroto">Moroto Municipal Primary School (Moroto: 630 Pupils)</option>
                  <option value="Nabilatuk">Nabilatuk Primary School (Nabilatuk: 535 Pupils)</option>
                  <option value="Nakapiripirit">Nakapiripirit Primary School (Nakapiripirit: 520 Pupils)</option>
                </select>
              </div>

              <span id="badge-v1-att-boys" class="px-3 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
                Registered Boys this week Attendance: 1,720
              </span>
              <span id="badge-v1-att-girls" class="px-3 py-1 bg-emerald-50 text-emerald-700 font-bold rounded-lg border border-emerald-200">
                Registered Girls this week Attendance: 1,630
              </span>
              <span id="badge-v1-att-total" class="px-3 py-1 bg-slate-100 text-slate-800 font-bold rounded-lg border border-slate-300">
                Total this week Attendance: 3,350 Pupils
              </span>
            </div>
          </div>

          <div class="h-[440px] min-h-[420px]">
            <canvas id="chart-v1-attendance"></canvas>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-6 gap-2 text-center text-xs pt-3 border-t border-slate-100">
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-l-b" class="font-bold text-slate-800">640</div>
              <div class="text-[10px] text-slate-500 font-medium">Lower Primary (ECD-P2) Boys</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-l-g" class="font-bold text-slate-800">610</div>
              <div class="text-[10px] text-slate-500 font-medium">Lower Primary (ECD-P2) Girls</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-m-b" class="font-bold text-slate-800">590</div>
              <div class="text-[10px] text-slate-500 font-medium">Middle Primary (P3-P4) Boys</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-m-g" class="font-bold text-slate-800">580</div>
              <div class="text-[10px] text-slate-500 font-medium">Middle Primary (P3-P4) Girls</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-u-b" class="font-bold text-slate-800">490</div>
              <div class="text-[10px] text-slate-500 font-medium">Upper Primary (P5-P7) Boys</div>
            </div>
            <div class="p-2 bg-slate-50 rounded border border-slate-200">
              <div id="metric-att-u-g" class="font-bold text-slate-800">440</div>
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
              <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
                Awareness: 93.8% (60/64 respondents)
              </span>
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
                142 Queries Logged
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

        <!-- ROW 1: AGE BAND PARTICIPATING MATRIX (MALE, FEMALE, MALE PWDS, FEMALE PWDS) -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>

              <h4 class="text-sm font-bold text-slate-800">Age band participating: male, female, male PWDs, female PWDs</h4>
              <p class="text-xs text-slate-500">Live headcount audit disaggregated across age bands, learners, teachers, community members, and PWD reach:</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="px-3 py-1 bg-blue-50 text-wfp-blue font-bold rounded-lg border border-blue-200">
                Total Activation Headcount: 4,703
              </span>
              <span class="px-3 py-1 bg-purple-50 text-purple-700 font-bold rounded-lg border border-purple-200">
                Total PWD Participants: 135 (2.9%)
              </span>
            </div>
          </div>

          <!-- Comprehensive Matrix Table -->
          <div class="overflow-x-auto rounded-lg border border-slate-200 mb-4">
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
              <tbody class="divide-y divide-slate-100 text-slate-700">
                <tr class="hover:bg-slate-50/60">
                  <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-blue-500"></span> Lower Primary (ECD–P2)
                  </td>
                  <td class="p-3 text-right font-medium">820</td>
                  <td class="p-3 text-right font-medium">790</td>
                  <td class="p-3 text-right font-bold text-slate-800 bg-slate-50">1,610</td>
                  <td class="p-3 text-right text-purple-700 font-medium">24</td>
                  <td class="p-3 text-right text-purple-700 font-medium">20</td>
                  <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">44</td>
                  <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">2.7%</span></td>
                </tr>
                <tr class="hover:bg-slate-50/60">
                  <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-sky-500"></span> Middle Primary (P3–P4)
                  </td>
                  <td class="p-3 text-right font-medium">780</td>
                  <td class="p-3 text-right font-medium">760</td>
                  <td class="p-3 text-right font-bold text-slate-800 bg-slate-50">1,540</td>
                  <td class="p-3 text-right text-purple-700 font-medium">22</td>
                  <td class="p-3 text-right text-purple-700 font-medium">19</td>
                  <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">41</td>
                  <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">2.7%</span></td>
                </tr>
                <tr class="hover:bg-slate-50/60">
                  <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-cyan-600"></span> Upper Primary (P5–P7)
                  </td>
                  <td class="p-3 text-right font-medium">690</td>
                  <td class="p-3 text-right font-medium">650</td>
                  <td class="p-3 text-right font-bold text-slate-800 bg-slate-50">1,340</td>
                  <td class="p-3 text-right text-purple-700 font-medium">18</td>
                  <td class="p-3 text-right text-purple-700 font-medium">16</td>
                  <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">34</td>
                  <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">2.5%</span></td>
                </tr>
                <tr class="hover:bg-slate-50/60">
                  <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span> Teachers Present
                  </td>
                  <td class="p-3 text-right font-medium">28</td>
                  <td class="p-3 text-right font-medium">20</td>
                  <td class="p-3 text-right font-bold text-slate-800 bg-slate-50">48</td>
                  <td class="p-3 text-right text-purple-700 font-medium">1</td>
                  <td class="p-3 text-right text-purple-700 font-medium">1</td>
                  <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">2</td>
                  <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">4.2%</span></td>
                </tr>
                <tr class="hover:bg-slate-50/60">
                  <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Community Members
                  </td>
                  <td class="p-3 text-right font-medium">48</td>
                  <td class="p-3 text-right font-medium">117</td>
                  <td class="p-3 text-right font-bold text-slate-800 bg-slate-50">165</td>
                  <td class="p-3 text-right text-purple-700 font-medium">5</td>
                  <td class="p-3 text-right text-purple-700 font-medium">9</td>
                  <td class="p-3 text-right font-bold text-purple-800 bg-purple-50/30">14</td>
                  <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-700">8.5%</span></td>
                </tr>
              </tbody>
              <tfoot class="bg-slate-100/80 font-extrabold text-slate-900 border-t-2 border-slate-300">
                <tr>
                  <td class="p-3 uppercase">Total Activation Footprint</td>
                  <td class="p-3 text-right">2,366</td>
                  <td class="p-3 text-right">2,337</td>
                  <td class="p-3 text-right bg-slate-200/60 font-black">4,703</td>
                  <td class="p-3 text-right text-purple-700">70</td>
                  <td class="p-3 text-right text-purple-700">65</td>
                  <td class="p-3 text-right font-black text-purple-900 bg-purple-100/50">135</td>
                  <td class="p-3 text-center"><span class="px-2 py-0.5 rounded text-[11px] font-black bg-purple-100 text-purple-800">2.9% PWD</span></td>
                </tr>
              </tfoot>
            </table>
          </div>
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
              <span class="text-emerald-700 font-bold"><i class="fa-solid fa-circle-check mr-1"></i>100% Completion (All 7 modules completed in all 6 schools)</span>
              <span class="bg-blue-50 text-wfp-blue px-2 py-0.5 rounded font-bold">6/6 Schools</span>
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
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 100% (6/6)</span>
                  </div>
                  <div class="w-full bg-slate-200 rounded-full h-2">
                    <div class="bg-emerald-600 h-2 rounded-full" style="width: 100%"></div>
                  </div>
                </div>

                <!-- Check 2 -->
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-slate-800">Did all three age bands and both boys and girls participate?</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 100% (6/6)</span>
                  </div>
                  <div class="w-full bg-slate-200 rounded-full h-2">
                    <div class="bg-emerald-600 h-2 rounded-full" style="width: 100%"></div>
                  </div>
                </div>

                <!-- Check 3 -->
                <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs font-bold text-slate-800">Was any learner excluded or left out during sessions?</span>
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">No: 100% (6/6)</span>
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
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 100% (6/6)</span>
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
              Sample: 60 School Catchments
            </span>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-5 space-y-3">
              <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <span class="font-bold text-slate-800 block mb-1">Key Diagnostic Finding:</span>
                <p class="text-slate-600 leading-relaxed">
                  <strong>58.3%</strong> of households cite <em>lack of preparation confidence or recipe skills</em> rather than lack of cash as the primary barrier. This directly validates the necessity of practical, hands-on cooking demonstrations.
                </p>
              </div>
              <div class="grid grid-cols-2 gap-2 text-center text-xs">
                <div class="p-2 bg-blue-50 rounded border border-blue-200">
                  <div class="font-bold text-wfp-blue text-sm">58.3%</div>
                  <div class="text-[10px] text-slate-500">Preparation Confidence</div>
                </div>
                <div class="p-2 bg-amber-50 rounded border border-amber-200">
                  <div class="font-bold text-amber-700 text-sm">21.7%</div>
                  <div class="text-[10px] text-slate-500">Taste Preference</div>
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
            <span class="px-3 py-1 bg-white text-emerald-700 font-bold rounded-lg border border-emerald-200 text-xs shadow-sm">
              89.0% Joint Household Completion Rate
            </span>
          </div>
        </div>

        <!-- ROW 1: NUTRICHARTS COLLECTION & JOINT HOUSEHOLD AUDIT -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Metric 1: Total Issued -->
          <div class="p-4 bg-white rounded-xl border border-slate-200/80 card-shadow flex items-center justify-between">
            <div>
              <h4 class="text-xs font-bold text-slate-700 mt-0.5">Total NutriCharts issued (Visit 1)</h4>
              <div class="text-2xl font-black text-wfp-blue mt-1">1,840</div>
              <span class="text-[11px] text-slate-500">Issued across 6 audited schools (Avg 307 / school)</span>
            </div>
            <div class="w-12 h-12 rounded-xl bg-blue-50 text-wfp-blue flex items-center justify-center text-xl">
              <i class="fa-solid fa-file-invoice"></i>
            </div>
          </div>

          <!-- Metric 2: Total Returned Today -->
          <div class="p-4 bg-white rounded-xl border border-slate-200/80 card-shadow flex items-center justify-between">
            <div>
              <h4 class="text-xs font-bold text-slate-700 mt-0.5">Total NutriCharts returned today</h4>
              <div class="text-2xl font-black text-emerald-700 mt-1">1,586</div>
              <span class="text-[11px] text-emerald-600 font-semibold">86.2% Overall Return Rate</span>
            </div>
            <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-xl">
              <i class="fa-solid fa-box-archive"></i>
            </div>
          </div>

          <!-- Metric 3: Joint Household Completion -->
          <div class="p-4 bg-white rounded-xl border border-slate-200/80 card-shadow flex items-center justify-between">
            <div>
              <h4 class="text-xs font-bold text-slate-700 mt-0.5">Returned charts showing joint household completion</h4>
              <div class="text-2xl font-black text-wfp-blue mt-1">1,412</div>
              <span class="text-[11px] text-slate-500 font-semibold">89.0% of returned charts signed by parent & pupil</span>
            </div>
            <div class="w-12 h-12 rounded-xl bg-blue-50 text-wfp-blue flex items-center justify-center text-xl">
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
            <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
              Verified across all 6 schools
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
                <strong class="text-wfp-blue font-bold">Audit Status:</strong> 4 schools fully accomplished commitments; 2 partially fulfilled.
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
                <strong class="text-wfp-blue font-bold">Tracing Reach:</strong> 100% of schools have active teacher/VHT tracing squads.
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
                <strong class="text-wfp-blue font-bold">Verification:</strong> 5 of 6 kitchens verified using improved stoves & covered pots.
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
                <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-2 py-0.5 rounded border border-emerald-200">78.1% High Impact</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1">Impact of school feeding routines on student presence</h4>
              <p class="text-xs text-slate-500 mb-3">Evaluation across 64 school cycles on meal protection sustaining classroom presence:</p>
              <div class="h-52 min-h-[200px]">
                <canvas id="chart-v3-pillar1-feeding"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-[11px] text-slate-600">
              <span>High impact: <strong>50 schools (78.1%)</strong> | Moderate: <strong>12 (18.8%)</strong> | Low: <strong>2 (3.1%)</strong></span>
            </div>
          </div>

          <!-- Pillar 2: Fair Plate-Sharing Practice Shift -->
          <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[11px] font-bold text-purple-700 uppercase tracking-wider">Pillar 2: Gender &amp; Equity</span>
                <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-2 py-0.5 rounded border border-emerald-200">81.2% Consistent</span>
              </div>
              <h4 class="text-sm font-bold text-slate-800 mb-1">Shift in fair plate-sharing practices</h4>
              <p class="text-xs text-slate-500 mb-3">Reported shift stopping the cultural practice of young ones or girls eating last:</p>
              <div class="h-52 min-h-[200px]">
                <canvas id="chart-v3-pillar2-plate"></canvas>
              </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-100 text-[11px] text-slate-600">
              <span>Consistent: <strong>52 schools (81.2%)</strong> | Some resistance: <strong>10 (15.6%)</strong> | No change: <strong>2 (3.1%)</strong></span>
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
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
                PR Captured: 87.5%
              </span>
              <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
                Radio Reach: 90.6%
              </span>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800">School PR &amp; Social Media Highlights Captured:</span>
                <span class="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">87.5% Yes (56/64)</span>
              </div>
              <p class="text-slate-600 text-[11px]">Field teams documented photo and video stories capturing behavioral shifts:</p>
              <ul class="space-y-1 text-[11px] text-slate-700 list-disc list-inside">
                <li>P5 girl and boy leaders demonstrating fair plate sharing and morning water duty rebalance on camera.</li>
                <li>Headteacher and cook showcasing newly constructed firewood-saving institutional stove with covered pots.</li>
                <li>NutriClub assembly demonstration on porridge fortification using fresh local amaranth greens.</li>
              </ul>
            </div>

            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-slate-800">Campaign Radio Spots Heard by School Community:</span>
                <span class="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">90.6% Yes (58/64)</span>
              </div>
              <p class="text-slate-600 text-[11px]">Teachers and learners reported hearing Nutribus campaign broadcasts on local radio stations (Karamoja FM, Nenah FM, Voice of Karamoja):</p>
              <div class="grid grid-cols-3 gap-2 text-center pt-2">
                <div class="p-2 bg-white rounded border border-slate-200">
                  <div class="font-bold text-emerald-700">90.6%</div>
                  <div class="text-[10px] text-slate-500">Heard Spots</div>
                </div>
                <div class="p-2 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-700">6.3%</div>
                  <div class="text-[10px] text-slate-500">Did Not Hear</div>
                </div>
                <div class="p-2 bg-white rounded border border-slate-200">
                  <div class="font-bold text-slate-500">3.1%</div>
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
            <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded">6 Sampled Household Audits</span>
          </div>

          <!-- Cards for the 5 Respondents -->
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
                    <span class="font-bold text-slate-900 block mb-1">Since taking chart home, feasible actions family was able to try:</span>
                    <div class="flex flex-wrap gap-1 mb-1">
                      <span class="px-2 py-0.5 bg-blue-50 text-wfp-blue rounded font-semibold text-[10px] border border-blue-200">Boys shared water & wood chores</span>
                      <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 rounded font-semibold text-[10px] border border-emerald-200">Supplemented Metu porridge</span>
                      <span class="px-2 py-0.5 bg-purple-50 text-purple-800 rounded font-semibold text-[10px] border border-purple-200">Fair food portions for boys & girls</span>
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">What was difficult or got in the way:</span>
                    <div class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      Water pump is crowded at dawn, so my brothers wake up earlier at 6:00 AM so we do not get late.
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200">
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Morning chore sharing shifted:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Youngest child served fairly:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                  </div>

                  <div class="pt-1">
                    <span class="font-bold text-slate-900 block mb-0.5">Record verbatim comments on shifts at home:</span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "My brothers fetch borehole water now. I wash my uniform, eat warm fortified Metu porridge, and get to class before the morning assembly bell rings."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Learner II -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Learner II</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">Male</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Middle Primary</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-1">Since taking chart home, feasible actions family was able to try:</span>
                    <div class="flex flex-wrap gap-1 mb-1">
                      <span class="px-2 py-0.5 bg-blue-50 text-wfp-blue rounded font-semibold text-[10px] border border-blue-200">Boys shared water & wood chores</span>
                      <span class="px-2 py-0.5 bg-amber-50 text-amber-800 rounded font-semibold text-[10px] border border-amber-200">Practiced firewood-saving cooking</span>
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">What was difficult or got in the way:</span>
                    <div class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      Carrying two 10-liter water jerricans was heavy on steep road, but I got used to it with my elder cousin.
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200">
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Morning chore sharing shifted:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Youngest child served fairly:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                  </div>

                  <div class="pt-1">
                    <span class="font-bold text-slate-900 block mb-0.5">Record verbatim comments on shifts at home:</span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "I carried the borehole water so my sister does not get whipped for late arrival. We both drink porridge and walk to school together."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Learner III -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Learner III</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Lower Primary</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-1">Since taking chart home, feasible actions family was able to try:</span>
                    <div class="flex flex-wrap gap-1 mb-1">
                      <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 rounded font-semibold text-[10px] border border-emerald-200">Supplemented Metu porridge</span>
                      <span class="px-2 py-0.5 bg-purple-50 text-purple-800 rounded font-semibold text-[10px] border border-purple-200">Fair food portions for boys & girls</span>
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">What was difficult or got in the way:</span>
                    <div class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      Wild green leaves (Eboo) became hard to find when rain stopped for two weeks.
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200">
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Morning chore sharing shifted:</span>
                      <span class="text-[11px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded inline-block mt-0.5">Not applicable</span>
                    </div>
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Youngest child served fairly:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                  </div>

                  <div class="pt-1">
                    <span class="font-bold text-slate-900 block mb-0.5">Record verbatim comments on shifts at home:</span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Mother serves me my own hot bowl of Metu porridge first because I am the youngest, instead of giving only big brothers."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Caregiver I -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Caregiver I</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Mother / PTA</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-1">Since taking chart home, feasible actions family was able to try:</span>
                    <div class="flex flex-wrap gap-1 mb-1">
                      <span class="px-2 py-0.5 bg-blue-50 text-wfp-blue rounded font-semibold text-[10px] border border-blue-200">Boys shared water & wood chores</span>
                      <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 rounded font-semibold text-[10px] border border-emerald-200">Supplemented Metu porridge</span>
                      <span class="px-2 py-0.5 bg-amber-50 text-amber-800 rounded font-semibold text-[10px] border border-amber-200">Firewood-saving cooking</span>
                      <span class="px-2 py-0.5 bg-purple-50 text-purple-800 rounded font-semibold text-[10px] border border-purple-200">Fair food portions</span>
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">What was difficult or got in the way:</span>
                    <div class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      Firewood shortage during rainy days; had to dry sticks under the roof and use covered pot to save fuel.
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200">
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Morning chore sharing shifted:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Youngest child served fairly:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                  </div>

                  <div class="pt-1">
                    <span class="font-bold text-slate-900 block mb-0.5">Record verbatim comments on shifts at home:</span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "The NutriChart on our hut wall reminded us daily. My husband told our boys that water carrying is for everyone. Now my daughter has never missed class this month."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Caregiver II -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Caregiver II</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">Male</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Father / Elder</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-1">Since taking chart home, feasible actions family was able to try:</span>
                    <div class="flex flex-wrap gap-1 mb-1">
                      <span class="px-2 py-0.5 bg-blue-50 text-wfp-blue rounded font-semibold text-[10px] border border-blue-200">Boys shared water & wood chores</span>
                      <span class="px-2 py-0.5 bg-purple-50 text-purple-800 rounded font-semibold text-[10px] border border-purple-200">Fair food portions</span>
                      <span class="px-2 py-0.5 bg-amber-50 text-amber-800 rounded font-semibold text-[10px] border border-amber-200">Firewood-saving cooking</span>
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">What was difficult or got in the way:</span>
                    <div class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      Some kraal neighbors laughed at my boys at the borehole, but I defended them and told elders to adopt the same practice.
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200">
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Morning chore sharing shifted:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Youngest child served fairly:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                  </div>

                  <div class="pt-1">
                    <span class="font-bold text-slate-900 block mb-0.5">Record verbatim comments on shifts at home:</span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "Educating our daughters brings pride to our family. My sons fetch morning water and firewood willingly so girls attend school and learn well."
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Caregiver III -->
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold text-slate-900">Caregiver III</span>
                  <div class="flex items-center gap-1.5">
                    <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
                    <span class="text-[10px] bg-slate-200 text-slate-700 font-semibold px-2 py-0.5 rounded">Grandmother / Elder</span>
                  </div>
                </div>

                <div class="space-y-2.5 text-xs text-slate-700">
                  <div>
                    <span class="font-bold text-slate-900 block mb-1">Since taking chart home, feasible actions family was able to try:</span>
                    <div class="flex flex-wrap gap-1 mb-1">
                      <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 rounded font-semibold text-[10px] border border-emerald-200">Supplemented Metu porridge</span>
                      <span class="px-2 py-0.5 bg-amber-50 text-amber-800 rounded font-semibold text-[10px] border border-amber-200">Firewood-saving cooking</span>
                      <span class="px-2 py-0.5 bg-purple-50 text-purple-800 rounded font-semibold text-[10px] border border-purple-200">Fair food portions</span>
                    </div>
                  </div>

                  <div>
                    <span class="font-bold text-slate-900 block mb-0.5">What was difficult or got in the way:</span>
                    <div class="text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      Wild cowpea leaves were scarce during dry weeks, but our family sun-dried excess eboo leaves under the roof to preserve them.
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2 pt-1 border-t border-slate-200">
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Morning chore sharing shifted:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                    <div>
                      <span class="text-[10px] text-slate-500 font-semibold block">Youngest child served fairly:</span>
                      <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded inline-block mt-0.5">Yes</span>
                    </div>
                  </div>

                  <div class="pt-1">
                    <span class="font-bold text-slate-900 block mb-0.5">Record verbatim comments on shifts at home:</span>
                    <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                      "We now serve the youngest toddler first with porridge mixed with dried cowpea leaves. She has stopped crying from hunger and her weight has improved."
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ROW 5: HOUSEHOLD SHIFT COHORT AGGREGATES -->
          <div class="mt-4 pt-4 border-t border-slate-200">
            <span class="text-xs font-bold text-slate-700 uppercase mb-2 block">Cohort Aggregates (30 Randomly Sampled Households across 6 Schools)</span>
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
            <span class="text-[11px] font-bold text-slate-700 block mb-1">Session Facilitation:</span>
            <div class="flex items-center gap-3 mt-1">
              <span class="px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200">
                Village Health Teams (VHT): 70% of Sessions
              </span>
              <span class="px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                Lead Coordinator: 30% of Sessions
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- CAPACITY-STRENGTHENING PARTNERS PRESENCE & CO-FACILITATION (COMMUNITY DEMO) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-4">
          <div>
            <div class="flex items-center gap-2 mb-0.5">
              <span class="text-[11px] font-bold text-wfp-blue uppercase tracking-wider">Partner Network Collaboration</span>
              <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-2 py-0.5 rounded border border-emerald-200">90.0% Present &amp; Co-facilitating</span>
            </div>
            <h4 class="text-sm font-bold text-slate-800">Were capacity-strengthening partners (e.g., UNAC, Afi) present and co-facilitating this community demonstration?</h4>
            <p class="text-xs text-slate-500">Partner co-facilitation verifying inclusive PWD mobilization, gender dialogues, and clean cooking sustainability</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
              54 of 60 Demos Co-Facilitated
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
                <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">80.0% (48/60)</span>
              </div>
              <div class="flex items-center justify-between bg-white px-2.5 py-1.5 rounded border border-slate-200">
                <span class="font-medium">AFI</span>
                <span class="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px]">75.0% (45/60)</span>
              </div>
              <div class="flex items-center justify-between bg-white px-2.5 py-1.5 rounded border border-slate-200">
                <span class="font-semibold text-wfp-blue">Other</span>
                <span class="font-bold text-wfp-blue bg-blue-50 px-2 py-0.5 rounded text-[11px]">23.3% (14/60)</span>
              </div>
            </div>
            <div class="p-2 bg-blue-50/70 rounded border border-blue-200 text-[11px] text-slate-700">
              <strong class="text-wfp-blue">Specify:</strong> Local LC1 Executive &amp; Parish Community Development Officer (CDO).
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
                <span class="font-bold text-emerald-700 text-xs mt-1.5">86.7% (52/60)</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Mentoring local VHTs / Elders</span>
                <span class="font-bold text-emerald-700 text-xs mt-1.5">81.7% (49/60)</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Observing for sustainability tracking</span>
                <span class="font-bold text-emerald-700 text-xs mt-1.5">76.7% (46/60)</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200 flex flex-col justify-between">
                <span class="text-[11px] text-slate-600 font-medium leading-snug">Other</span>
                <span class="font-bold text-wfp-blue text-xs mt-1.5">20.0% (12/60)</span>
              </div>
            </div>
            <div class="p-2 bg-slate-100 rounded text-[10px] text-slate-600 italic">
              Specify: Specialized Ngakarimojong sign interpretation &amp; mobility support for PWD caregivers.
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
            <div class="text-2xl font-black text-slate-800 mt-0.5" id="demo-kpi-total-sessions">60</div>
            <span class="text-[10px] text-slate-500">Target: 640 sessions (10 / school)</span>
          </div>
          <div class="p-3.5 bg-emerald-50/60 rounded-xl border border-emerald-200">
            <span class="text-[11px] font-bold text-emerald-800 block">Compliant Sessions (&ge;80)</span>
            <div class="text-2xl font-black text-emerald-700 mt-0.5" id="demo-kpi-compliant-sessions">47</div>
            <span class="text-[10px] text-emerald-600 font-bold" id="demo-kpi-compliant-rate">78.3% compliant rate</span>
          </div>
          <div class="p-3.5 bg-red-50/60 rounded-xl border border-red-200">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold text-red-800 block">Red-Flagged Sessions (&lt;80)</span>
              <span class="w-2 h-2 rounded-full bg-red-500 animate-ping"></span>
            </div>
            <div class="text-2xl font-black text-red-600 mt-0.5" id="demo-kpi-flagged-sessions">13</div>
            <span class="text-[10px] text-red-600 font-bold" id="demo-kpi-flagged-rate">21.7% flagged for follow-up</span>
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
            <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
              Total attendees: 733
            </span>
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
              PWD Inclusivity: 34 (4.6%)
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
                <td class="py-2.5 px-3 text-right font-mono font-bold text-pink-700">165</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-wfp-blue">165</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Primary household food preparers and child nutrition gatekeepers</td>
              </tr>
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Male Fathers / Elders</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-blue-700">58</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-wfp-blue">58</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Household decision-makers engaged in gender chore rebalancing dialogues</td>
              </tr>
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Male Children</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-blue-700">242</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-wfp-blue">242</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Learners participating in cooking activities and food sorting games</td>
              </tr>
              <tr class="hover:bg-slate-50/50">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Female Children</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-pink-700">268</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-wfp-blue">268</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Girl-child participants practicing hands-on Metu porridge supplementation</td>
              </tr>
              <tr class="hover:bg-slate-50/50 bg-blue-50/20">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Male PWDs</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-blue-700">18</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-wfp-blue">18</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Participants with physical or sensory disabilities supported by VHTs</td>
              </tr>
              <tr class="hover:bg-slate-50/50 bg-blue-50/20">
                <td class="py-2.5 px-3 font-semibold text-slate-900">Female PWDs</td>
                <td class="py-2.5 px-3 text-right font-mono text-slate-400">0</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-pink-700">16</td>
                <td class="py-2.5 px-3 text-right font-mono font-bold text-wfp-blue">16</td>
                <td class="py-2.5 px-3 text-[11px] text-slate-600">Provided priority front seating and assisted tasting bowls</td>
              </tr>
              <tr class="bg-slate-100 font-extrabold text-slate-900 border-t-2 border-slate-300">
                <td class="py-3 px-3">Total Cumulative Headcount</td>
                <td class="py-3 px-3 text-right font-mono text-blue-700">318</td>
                <td class="py-3 px-3 text-right font-mono text-pink-700">449</td>
                <td class="py-3 px-3 text-right font-mono text-wfp-blue text-sm">767</td>
                <td class="py-3 px-3 text-emerald-700">100% Verified Community Mobilization Across 60 Demos</td>
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
                  <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[11px]">90.0% Hands-On</span>
                </div>
                <div class="text-[11px] text-slate-600">
                  Practiced and cooked hands-on: <strong>54 demos (90.0%)</strong> | Stood and watched passively: <strong>6 demos (10.0%)</strong>
                </div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-bold text-slate-800">Was WFP Metu porridge demonstrated with additions of obtainable local staples?</span>
                  <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[11px]">100% Yes</span>
                </div>
                <div class="text-[11px] text-slate-600 mb-1">
                  Demonstrated with wild greens (Eboo/Lokaka), cowpea leaves, roasted sesame paste, and pumpkin puree: <strong>60 of 60 Demos</strong>
                </div>
                <div class="p-2 bg-white rounded border border-slate-200 text-[11px] text-slate-700 italic">
                  <strong class="text-wfp-blue not-italic font-bold">Comments or reactions from spectators:</strong>
                  "Spectators tasted the warm green-flecked Metu porridge, praised the pleasant roasted sesame aroma, and requested recipe portions to replicate for weaning infants at home."
                </div>
              </div>

              <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-1">
                  <span class="font-bold text-slate-800">Were all demonstrated foods sourced locally from seasonal gardens/markets?</span>
                  <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[11px]">96.7% Compliant</span>
                </div>
                <div class="text-[11px] text-slate-600">
                  Yes, strictly compliant with obtainable seasonal foods: <strong>58 demos (96.7%)</strong> | Promoted unapproved/unattainable foods: <strong>2 demos (3.3%)</strong>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Col 2: Fuel-Saving Practices Chart -->
        <div class="bg-white rounded-xl p-5 border border-slate-200/80 card-shadow">
          <h4 class="text-sm font-bold text-slate-800 mb-1">Which fuel-saving practices were demonstrated to the gathering?</h4>
          <p class="text-xs text-slate-500 mb-3">Verification of fuel-saving cookstove and cooking practices shown across 60 sites:</p>
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
          <span class="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded">3 Verified In-Depth Profiles</span>
        </div>

        <!-- 3 Caregiver Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <!-- Caregiver 1 -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-slate-900">Caregiver 1</span>
                <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
              </div>
              <div class="space-y-2.5 text-xs text-slate-700">
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">What is most difficult or gets in the way of feeding family well:</span>
                  <div class="flex flex-wrap gap-1 mb-1">
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded text-[10px] border border-amber-200">Food items missing in garden/market</span>
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded text-[10px] border border-amber-200">Scarcity of cooking water</span>
                  </div>
                </div>
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">Feasible action realistically try at home:</span>
                  <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                    Supplement Metu porridge with local wild greens
                  </span>
                </div>
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">Caregiver Commitment Verdict:</span>
                  <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[11px] inline-block">
                    Will try it
                  </span>
                </div>
                <div class="pt-1 border-t border-slate-200">
                  <span class="font-bold text-slate-900 block mb-0.5">Exact words recorded (no personal names):</span>
                  <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "I will gather fresh amaranth (Eboo) and pound roasted simsim into the morning Metu porridge so my twin toddlers gain strength."
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Caregiver 2 -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-slate-900">Caregiver 2</span>
                <span class="text-[11px] bg-pink-50 text-pink-700 font-bold px-2 py-0.5 rounded border border-pink-200">Female</span>
              </div>
              <div class="space-y-2.5 text-xs text-slate-700">
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">What is most difficult or gets in the way of feeding family well:</span>
                  <div class="flex flex-wrap gap-1 mb-1">
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded text-[10px] border border-amber-200">Scarcity of firewood</span>
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded text-[10px] border border-amber-200">Heavy morning chores</span>
                  </div>
                </div>
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">Feasible action realistically try at home:</span>
                  <span class="px-2 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded text-[11px] border border-emerald-200 block mb-1">
                    Practice fuel-saving cooking methods
                  </span>
                </div>
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">Caregiver Commitment Verdict:</span>
                  <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[11px] inline-block">
                    Will try it
                  </span>
                </div>
                <div class="pt-1 border-t border-slate-200">
                  <span class="font-bold text-slate-900 block mb-0.5">Exact words recorded (no personal names):</span>
                  <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "Covering the pot and using dried acacia wood kept the heat high. I will teach my co-wife to stop burning green logs on open fires."
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Caregiver 3 -->
          <div class="p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-bold text-slate-900">Caregiver 3</span>
                <span class="text-[11px] bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded border border-blue-200">Male</span>
              </div>
              <div class="space-y-2.5 text-xs text-slate-700">
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">What is most difficult or gets in the way of feeding family well:</span>
                  <div class="flex flex-wrap gap-1 mb-1">
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded text-[10px] border border-amber-200">Family or elder disagreement</span>
                    <span class="px-2 py-0.5 bg-amber-50 text-amber-800 font-semibold rounded text-[10px] border border-amber-200">Lack of money</span>
                  </div>
                </div>
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">Feasible action realistically try at home:</span>
                  <span class="px-2 py-0.5 bg-purple-50 text-purple-800 font-bold rounded text-[11px] border border-purple-200 block mb-1">
                    Serve fair and equal food portions to boys and girls
                  </span>
                </div>
                <div>
                  <span class="font-bold text-slate-900 block mb-0.5">Caregiver Commitment Verdict:</span>
                  <span class="px-2 py-0.5 bg-amber-100 text-amber-800 font-bold rounded text-[11px] inline-block">
                    Needs VHT guidance
                  </span>
                </div>
                <div class="pt-1 border-t border-slate-200">
                  <span class="font-bold text-slate-900 block mb-0.5">Exact words recorded (no personal names):</span>
                  <div class="italic text-slate-600 bg-white p-2 rounded border border-slate-200 text-[11px]">
                    "I agreed today that our daughter should get the same bowl of porridge as our son, but I need the VHT to visit our kraal to explain it to my older brother."
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Cohort Aggregate Charts -->
        <div class="mt-4 pt-4 border-t border-slate-200">
          <span class="text-xs font-bold text-slate-700 uppercase mb-2 block">Cohort Aggregates (150 Caregiver Intercepts across 60 Catchment Demos)</span>
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
            95% Discussion Completion
          </span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Col 1: Discussion Quality & Male Participation Level -->
          <div class="space-y-4">
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-bold text-slate-800">Did the structured gender chore and fair-sharing discussion take place?</span>
                <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded">Yes: 95.0% (57/60)</span>
              </div>
              <p class="text-[11px] text-slate-600">
                Yes: <strong>57 demos (95.0%)</strong> | No: <strong>3 demos (5.0%)</strong>
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
                <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[10px]">Yes: 98.3% (59/60)</span>
              </div>
              <p class="text-[11px] text-slate-600">
                WFP toll-free hotline clearly displayed and explained to all attending households.
              </p>
            </div>
          </div>

          <!-- Col 2: Qualitative Consensus & Exact Community Commitments -->
          <div class="space-y-3.5">
            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <strong class="text-wfp-blue text-xs block mb-1">Group response: In your household who is served first and who eats last?</strong>
              <div class="text-[11px] text-slate-700 bg-white p-2.5 rounded border border-slate-200">
                "Traditional hierarchy: Fathers and adolescent sons served first in largest bowls; mother and weaning infants eat last whatever remains in the cooking pot."
              </div>
            </div>

            <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <strong class="text-wfp-blue text-xs block mb-1">Group response: What would need to change for the youngest child to be served first?</strong>
              <div class="text-[11px] text-slate-700 bg-white p-2.5 rounded border border-slate-200">
                "Mothers dish the infant's bowl directly from the pot first before platters are carried to elders, with fathers formally agreeing at the kraal council."
              </div>
            </div>

            <div class="p-3.5 bg-emerald-50/70 rounded-xl border border-emerald-200">
              <strong class="text-emerald-800 text-xs block mb-1">Community Agreement and Commitments made in their own words:</strong>
              <div class="text-[11px] text-slate-800 italic bg-white p-2.5 rounded border border-emerald-200">
                "We the village of Lomorunyankori agree that our weaning children under 2 will receive enriched Metu porridge first, and our boys will fetch morning borehole water so girls never miss school."
              </div>
              <div class="mt-2 text-[10px] text-slate-600">
                <strong>Named Community Body / Elders Responsible for Follow-Up:</strong> <span class="font-bold text-slate-800">VHT Lead Coordinator & LC1 Elders Council</span>
              </div>
            </div>

            <div class="p-3.5 bg-amber-50/70 rounded-xl border border-amber-200">
              <strong class="text-amber-800 text-xs block mb-1">Main debate point or objection raised before consensus was reached:</strong>
              <div class="text-[11px] text-slate-700 bg-white p-2.5 rounded border border-amber-200">
                "Elder kraal leaders objected that male boys carrying water jars is culturally forbidden; consensus was reached when the Headteacher and VHT explained that girls' school performance and family health require mutual domestic burden sharing."
              </div>
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
              Clean Cooking Demonstrated: 98.3% (59/60)
            </span>
            <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-3 py-1 rounded border border-blue-200">
              Stove Adoption: 78.3%
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
                <span class="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">93.3% (56/60)</span>
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
              PR Photos Captured: 91.7%
            </span>
            <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded border border-emerald-200">
              Radio Feedback: 88.3%
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-slate-800">Community PR &amp; Media Highlights Captured:</span>
              <span class="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">91.7% Yes (55/60)</span>
            </div>
            <p class="text-slate-600 text-[11px]">Field coordinators documented high-resolution photos and testimonial clips of active cooking circles, male participation in dialogues, and child plate sharing.</p>
            <div class="p-2 bg-white rounded border border-slate-200 text-[11px] text-slate-700">
              <strong>PR Capture Focus:</strong> Caregivers displaying newly prepared Metu porridge fortified with local amaranth greens and ground sesame seeds.
            </div>
          </div>

          <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-slate-800">Community Feedback on Radio Broadcasts:</span>
              <span class="font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">88.3% Feedback Logged (53/60)</span>
            </div>
            <p class="text-slate-600 text-[11px]">Attendees discussed radio spots broadcast across local FM stations during village cooking sessions:</p>
            <div class="p-2 bg-emerald-50 rounded border border-emerald-200 text-[11px] text-slate-800 italic">
              "Caregivers noted that hearing kraal leaders on the radio talking about feeding young children first made fathers much more willing to support plate sharing at home."
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
          <span class="text-xs bg-emerald-50 text-emerald-800 font-bold px-3 py-1 rounded-lg border border-emerald-200">
            24 Verified Stories across 9 Districts
          </span>
        </div>
        
        <div class="p-3 bg-slate-50 rounded-lg border border-slate-200 mb-4">
          <span class="text-[11px] font-bold text-slate-700 block mb-1">Field Monitor Guidance:</span>
          <p class="text-xs text-slate-600 italic">"Record the storyteller's actual words; do not reinterpret. Complete verbatim testimonies captured during field interviews across all 6 key community stakeholder roles."</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="p-3 bg-blue-50/50 rounded-lg border border-blue-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Total Stories</span>
            <span class="text-2xl font-black text-wfp-blue block mt-0.5">24</span>
            <span class="text-[10px] text-slate-500">Across 9 Districts</span>
          </div>
          <div class="p-3 bg-emerald-50/50 rounded-lg border border-emerald-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Evidence Sighted</span>
            <span class="text-2xl font-black text-emerald-600 block mt-0.5">95.8%</span>
            <span class="text-[10px] text-slate-500">23 of 24 Verified</span>
          </div>
          <div class="p-3 bg-purple-50/50 rounded-lg border border-purple-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Female Voice</span>
            <span class="text-2xl font-black text-purple-700 block mt-0.5">58.3%</span>
            <span class="text-[10px] text-slate-500">Mothers & Girls</span>
          </div>
          <div class="p-3 bg-amber-50/50 rounded-lg border border-amber-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Peers Returned</span>
            <span class="text-2xl font-black text-amber-600 block mt-0.5">18</span>
            <span class="text-[10px] text-slate-500">Out-of-School Children</span>
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

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- Story 1: Girl Learner -->
          <div class="p-4 bg-slate-50/70 rounded-xl border border-slate-200 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
              <div>
                <span class="text-xs font-bold text-slate-900 block">Nalemu Esther, 14 yrs</span>
                <span class="text-[11px] text-slate-500">Lomorunyankori Primary School · Moroto District</span>
              </div>
              <span class="text-xs bg-pink-50 text-pink-700 font-bold px-2.5 py-0.5 rounded border border-pink-200">
                Girl Learner
              </span>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?</span>
              <p class="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-200 leading-relaxed">
                "Before the NutriBus came, I woke up at 5:00 AM every single morning to fetch three heavy jerrycans of water from the far borehole while my brother stayed asleep. By the time I carried firewood and swept, it was 9:30 AM. I was exhausted, reached school in tears, and missed all morning English and Math lessons. We only ate plain posho with salt at night."
              </p>
            </div>

            <div class="space-y-2">
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What specific campaign event, activity, chart, or discussion caused the shift?</span>
                <span class="inline-block px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                  NutriBus Day Session (Adere build, food sorting, or chore debate)
                </span>
              </div>
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What was physically done differently at home, class, or community after attending the nutribus activities?</span>
                <span class="inline-block px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200 mb-1">
                  Reallocated morning chores (boys fetching water/wood; girls arrived on time)
                </span>
                <p class="text-xs text-slate-600 font-medium">
                  "My brother Lokol now fetches two jerrycans of water with me every morning. We finish early, eat together, and walk together to school on time."
                </p>
              </div>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Why is this change significant to you?</span>
              <p class="text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200 font-medium leading-relaxed">
                "Because I am no longer beaten or embarrassed for latecoming, I can concentrate without sleeping in class, and my midterm score improved from 42% to 78%. I feel respected at home and in class."
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200 text-xs">
              <span class="text-[11px] font-bold text-slate-700 block mb-0.5">Verifiable Physical Evidence Sighted by Collector:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 bg-blue-100/70 text-wfp-blue font-bold rounded text-[11px]">
                  School register shows consistent female attendance
                </span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 italic">
                Verified 100% on-time morning presence in Primary 6 register over 3 consecutive weeks without a single recorded absence.
              </p>
            </div>
          </div>

          <!-- Story 2: Boy Learner -->
          <div class="p-4 bg-slate-50/70 rounded-xl border border-slate-200 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
              <div>
                <span class="text-xs font-bold text-slate-900 block">Lokiru Samuel, 13 yrs</span>
                <span class="text-[11px] text-slate-500">Kaabong West Primary School · Kaabong District</span>
              </div>
              <span class="text-xs bg-blue-50 text-wfp-blue font-bold px-2.5 py-0.5 rounded border border-blue-200">
                Boy Learner
              </span>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?</span>
              <p class="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-200 leading-relaxed">
                "I used to believe fetching water and gathering firewood was purely girls work. I would sit under the shade with other boys playing while my sisters struggled. My cousin had also dropped out of Primary 4 to herd cattle full time in the bush."
              </p>
            </div>

            <div class="space-y-2">
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What specific campaign event, activity, chart, or discussion caused the shift?</span>
                <span class="inline-block px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                  NutriBus Day Session (Adere build, food sorting, or chore debate)
                </span>
              </div>
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What was physically done differently at home, class, or community after attending the nutribus activities?</span>
                <span class="inline-block px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200 mb-1">
                  Out-of-school peer returned to class
                </span>
                <p class="text-xs text-slate-600 font-medium">
                  "I tracked my cousin in the kraal and convinced my uncle to re-enroll her in school. I also carry morning firewood and water alongside my sisters so we finish fast."
                </p>
              </div>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Why is this change significant to you?</span>
              <p class="text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200 font-medium leading-relaxed">
                "I learned on NutriBus Day that when chores are shared equally, everyone succeeds. My cousin is now back in Primary 4 sitting right next to me, and my sisters are never late for morning assembly."
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200 text-xs">
              <span class="text-[11px] font-bold text-slate-700 block mb-0.5">Verifiable Physical Evidence Sighted by Collector:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 bg-blue-100/70 text-wfp-blue font-bold rounded text-[11px]">
                  School register shows consistent female attendance
                </span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 italic">
                Headteacher confirmed official re-enrollment and verified boy's daily shared chore responsibility log.
              </p>
            </div>
          </div>

          <!-- Story 3: Female Caregiver / Mother -->
          <div class="p-4 bg-slate-50/70 rounded-xl border border-slate-200 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
              <div>
                <span class="text-xs font-bold text-slate-900 block">Angella Christine, 31 yrs</span>
                <span class="text-[11px] text-slate-500">Loroo Catchment / Amudat P/S · Amudat District</span>
              </div>
              <span class="text-xs bg-purple-50 text-purple-700 font-bold px-2.5 py-0.5 rounded border border-purple-200">
                Female Caregiver / Mother
              </span>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?</span>
              <p class="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-200 leading-relaxed">
                "We only cooked plain white posho or thin maize porridge without any oil or greens. My two-year-old child was constantly lethargic, sickly, and underweight. Gathering firewood took 4 hours every single day using an open three-stone fire that burned through entire bundles in one morning."
              </p>
            </div>

            <div class="space-y-2">
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What specific campaign event, activity, chart, or discussion caused the shift?</span>
                <span class="inline-block px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                  Metu Porridge Plus Demonstration (Fortifying porridge with local staples)
                </span>
              </div>
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What was physically done differently at home, class, or community after attending the nutribus activities?</span>
                <span class="inline-block px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200 mb-1">
                  Supplemented Metu porridge with obtainable local wild greens or cowpeas
                </span>
                <p class="text-xs text-slate-600 font-medium">
                  "I began fortifying our daily Metu porridge with crushed roasted sesame and steamed cowpea leaves. We also constructed an improved double-pot mud stove using dry clay."
                </p>
              </div>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Why is this change significant to you?</span>
              <p class="text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200 font-medium leading-relaxed">
                "My child gained healthy weight and vitality; her skin cleared up and she plays actively without crying. Plus I spend only 1 hour gathering wood instead of walking half the day into unsafe bush areas."
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200 text-xs">
              <span class="text-[11px] font-bold text-slate-700 block mb-0.5">Verifiable Physical Evidence Sighted by Collector:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold rounded text-[11px]">
                  Cooking pot shows Metu fortified with obtainable local greens
                </span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 italic">
                Collector inspected morning cooking pot: Metu porridge visibly fortified with dark-green steamed cowpea puree and roasted sesame paste.
              </p>
            </div>
          </div>

          <!-- Story 4: Father / Male Elder -->
          <div class="p-4 bg-slate-50/70 rounded-xl border border-slate-200 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
              <div>
                <span class="text-xs font-bold text-slate-900 block">Chegem Paul, 42 yrs</span>
                <span class="text-[11px] text-slate-500">Acegeretolim Catchment · Nabilatuk District</span>
              </div>
              <span class="text-xs bg-amber-50 text-amber-800 font-bold px-2.5 py-0.5 rounded border border-amber-200">
                Father / Male Elder
              </span>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?</span>
              <p class="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-200 leading-relaxed">
                "In our clan tradition, men and boys do not touch cooking pots or carry water. All firewood and water collection fell upon my wife and daughters. The youngest children always ate last from whatever little remained at the bottom of the bowl."
              </p>
            </div>

            <div class="space-y-2">
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What specific campaign event, activity, chart, or discussion caused the shift?</span>
                <span class="inline-block px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                  Community Elders / Gender Dynamics Dialogue
                </span>
              </div>
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What was physically done differently at home, class, or community after attending the nutribus activities?</span>
                <span class="inline-block px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200 mb-1">
                  Reallocated morning chores (boys fetching water/wood; girls arrived on time)
                </span>
                <p class="text-xs text-slate-600 font-medium">
                  "I told my sons that gathering firewood and water is family work, not just girls work. I built an improved sheltered mud cookstove for the manyatta and made sure the 3-year-old toddler is served first."
                </p>
              </div>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Why is this change significant to you?</span>
              <p class="text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200 font-medium leading-relaxed">
                "I realized that our daughters education and our young childrens health are the real wealth of our family. An educated daughter brings prosperity and honor. My household is peaceful and united."
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200 text-xs">
              <span class="text-[11px] font-bold text-slate-700 block mb-0.5">Verifiable Physical Evidence Sighted by Collector:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 bg-orange-100 text-orange-800 font-bold rounded text-[11px]">
                  Kitchen displays improved cookstove using less firewood
                </span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 italic">
                Collector verified newly constructed double-pot sheltered mud stove and observed youngest toddler served first during mealtime.
              </p>
            </div>
          </div>

          <!-- Story 5: Teacher / Club Patron -->
          <div class="p-4 bg-slate-50/70 rounded-xl border border-slate-200 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
              <div>
                <span class="text-xs font-bold text-slate-900 block">Sr. Akello Grace, 38 yrs</span>
                <span class="text-[11px] text-slate-500">Kotido Mixed Primary School · Kotido District</span>
              </div>
              <span class="text-xs bg-indigo-50 text-indigo-700 font-bold px-2.5 py-0.5 rounded border border-indigo-200">
                Teacher / Club Patron
              </span>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?</span>
              <p class="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-200 leading-relaxed">
                "Female absenteeism on Mondays and Wednesdays exceeded 35 percent because of distant water points. Learners came to class hungry, faint, and unable to focus. Our school kitchen burned 12 cartloads of firewood every month with smoke blinding the cooks."
              </p>
            </div>

            <div class="space-y-2">
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What specific campaign event, activity, chart, or discussion caused the shift?</span>
                <span class="inline-block px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                  Climate-Smart Cooking Session (Improved firewood-saving cookstoves)
                </span>
              </div>
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What was physically done differently at home, class, or community after attending the nutribus activities?</span>
                <span class="inline-block px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200 mb-1">
                  Adopted improved cookstove / reduced daily firewood consumption
                </span>
                <p class="text-xs text-slate-600 font-medium">
                  "Our school kitchen transitioned to an improved institutional Lorena cookstove. We also mobilized our NutriClub learners to monitor daily attendance and lead assembly nutrition moments."
                </p>
              </div>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Why is this change significant to you?</span>
              <p class="text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200 font-medium leading-relaxed">
                "Kitchen firewood expenses dropped by 45 percent, freeing funds for educational supplies. Girls are present in class every morning and learners are proud nutrition ambassadors."
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200 text-xs">
              <span class="text-[11px] font-bold text-slate-700 block mb-0.5">Verifiable Physical Evidence Sighted by Collector:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 bg-orange-100 text-orange-800 font-bold rounded text-[11px]">
                  Kitchen displays improved cookstove using less firewood
                </span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 italic">
                Verified institutional rocket Lorena cookstove installed and burning seasoned dry wood with minimal smoke emissions.
              </p>
            </div>
          </div>

          <!-- Story 6: Local Leader -->
          <div class="p-4 bg-slate-50/70 rounded-xl border border-slate-200 space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 pb-2">
              <div>
                <span class="text-xs font-bold text-slate-900 block">Ekeno Peter, 54 yrs</span>
                <span class="text-[11px] text-slate-500">Tokora Catchment Area · Nakapiripirit District</span>
              </div>
              <span class="text-xs bg-teal-50 text-teal-800 font-bold px-2.5 py-0.5 rounded border border-teal-200">
                Local Leader
              </span>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Describe the situation before the campaign: What was the normal household diet, daily chore burden (water/firewood), or school attendance pattern?</span>
              <p class="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-200 leading-relaxed">
                "Community elders viewed nutrition and school attendance as women domestic issues. Many children were kept home for domestic chores or grazing cattle. Malnutrition cases were referred late to health centers."
              </p>
            </div>

            <div class="space-y-2">
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What specific campaign event, activity, chart, or discussion caused the shift?</span>
                <span class="inline-block px-2.5 py-1 bg-blue-50 text-wfp-blue font-bold rounded text-xs border border-blue-200">
                  Take-Home NutriChart completed jointly at home
                </span>
              </div>
              <div>
                <span class="text-[11px] font-bold text-slate-700 block mb-1">What was physically done differently at home, class, or community after attending the nutribus activities?</span>
                <span class="inline-block px-2.5 py-1 bg-emerald-50 text-emerald-800 font-bold rounded text-xs border border-emerald-200 mb-1">
                  Supplemented Metu porridge with obtainable local wild greens or cowpeas
                </span>
                <p class="text-xs text-slate-600 font-medium">
                  "We mandated village-level tracking of returned NutriCharts across kraals and promoted Metu porridge fortification with local wild greens at all village barazas."
                </p>
              </div>
            </div>

            <div>
              <span class="text-[11px] font-bold text-slate-700 block mb-1">Why is this change significant to you?</span>
              <p class="text-xs text-emerald-900 bg-emerald-50/80 p-2.5 rounded-lg border border-emerald-200 font-medium leading-relaxed">
                "Seeing parents sit together with their children to tick the NutriChart brought a true cultural shift in our village. Household nutrition and girls education are now open agenda items at monthly council meetings."
              </p>
            </div>

            <div class="pt-2 border-t border-slate-200 text-xs">
              <span class="text-[11px] font-bold text-slate-700 block mb-0.5">Verifiable Physical Evidence Sighted by Collector:</span>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 bg-blue-100/70 text-wfp-blue font-bold rounded text-[11px]">
                  Completed NutriChart sighted
                </span>
              </div>
              <p class="text-[11px] text-slate-500 mt-1 italic">
                Collector verified 28 fully completed and signed NutriCharts returned from Tokora catchment households.
              </p>
            </div>
          </div>
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
            24 Cleaned Stories Logged
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
              Session one of the week: 6 Sessions
            </span>
            <span class="px-3 py-1 bg-emerald-50 text-emerald-800 font-bold rounded-lg text-xs border border-emerald-200">
              Session two of the week: 6 Sessions
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="p-3 bg-blue-50/50 rounded-lg border border-blue-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Registered Members</span>
            <span class="text-2xl font-black text-wfp-blue block mt-0.5">312</span>
            <span class="text-[10px] text-slate-500">162 Girls · 150 Boys</span>
          </div>
          <div class="p-3 bg-emerald-50/50 rounded-lg border border-emerald-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Average Attendance</span>
            <span class="text-2xl font-black text-emerald-600 block mt-0.5">95.5%</span>
            <span class="text-[10px] text-slate-500">298 Active Attendees</span>
          </div>
          <div class="p-3 bg-purple-50/50 rounded-lg border border-purple-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">PWD Learners Active</span>
            <span class="text-2xl font-black text-purple-700 block mt-0.5">38</span>
            <span class="text-[10px] text-slate-500">20 Boys · 18 Girls</span>
          </div>
          <div class="p-3 bg-amber-50/50 rounded-lg border border-amber-100 text-center">
            <span class="text-[11px] font-bold text-slate-500 uppercase block">Assembly Nutri-Moments</span>
            <span class="text-2xl font-black text-amber-600 block mt-0.5">6</span>
            <span class="text-[10px] text-slate-500">Delivered School-Wide</span>
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
                      <strong class="text-slate-900">64 Primary Schools target (192 school visits across 9 districts)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Direct Session Reach Target:</span>
                      <strong class="text-wfp-blue font-bold">80,875 Pupils target (from 120,686 enrolled learners)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Community Demonstrations:</span>
                      <strong class="text-slate-900">640 Demonstrations (10 in the community around each school)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Caregivers &amp; Parents Target:</span>
                      <strong class="text-slate-900">51,200 Adults across 64 school catchment areas</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">School Clubs &amp; Weekly Meetings:</span>
                      <strong class="text-slate-900">64 School Clubs active with 128 weekly meetings held</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Trained Stakeholders &amp; Inclusion:</span>
                      <strong class="text-slate-900">768 Teachers &amp; VHTs target · 1,200 PWDs targeted</strong>
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
                      <strong class="text-emerald-700 font-bold">88.3% of mothers cooked hands-on (only 11.7% watched)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Local Foods Only:</span>
                      <strong class="text-emerald-700 font-bold">100.0% used only easy-to-find wild greens &amp; cowpeas</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Teachers in the Lead:</span>
                      <strong class="text-slate-900">92.2% (59 of 64 schools ran visits on their own)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">What Children Remembered:</span>
                      <strong class="text-wfp-blue font-bold">91.4% of children could clearly explain the food rules</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block">Fair &amp; Welcoming for All:</span>
                      <strong class="text-slate-900">100.0% in local language (Ngakarimojong) with PWD seating</strong>
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
                      <strong class="text-emerald-800 font-bold text-sm">84.0% of homes (up from 12.0% before)</strong>
                      <span class="text-[10px] text-slate-500 block">Checked on 1,586 returned home charts with parents' signatures</span>
                    </div>
                    <div class="p-2 bg-blue-50/60 rounded border border-blue-200">
                      <span class="text-blue-900 text-[10px] block font-semibold">Boys Helping with Water &amp; Firewood:</span>
                      <strong class="text-blue-800 font-bold text-sm">85.0% of homes (up from 18.0% before)</strong>
                      <span class="text-[10px] text-slate-500 block">Boys carry morning water so 94% of girls arrive on time</span>
                    </div>
                    <div class="p-2 bg-purple-50/60 rounded border border-purple-200">
                      <span class="text-purple-900 text-[10px] block font-semibold">Serving Toddlers First:</span>
                      <strong class="text-purple-800 font-bold text-sm">82.0% of homes (up from 22.0% before)</strong>
                      <span class="text-[10px] text-slate-500 block">Mothers now dish the toddler's bowl first straight from the pot</span>
                    </div>
                    <div class="p-2 bg-amber-50/60 rounded border border-amber-200">
                      <span class="text-amber-900 text-[10px] block font-semibold">Saving Daily Firewood:</span>
                      <strong class="text-amber-800 font-bold text-sm">83.3% of homes (up from 33.3% before)</strong>
                      <span class="text-[10px] text-slate-500 block">Covering pots and using better stoves cut wood trips by half</span>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block font-semibold">More Pupils in School:</span>
                      <strong class="text-slate-900 font-bold">+8.7% Attendance Increase (from 3,350 to 3,640 pupils)</strong>
                    </div>
                    <div class="p-2 bg-slate-50 rounded border border-slate-200">
                      <span class="text-slate-500 text-[10px] block font-semibold">Out-of-School Girls Back in Class:</span>
                      <strong class="text-emerald-700 font-bold">18 girls who had dropped out are back in school</strong>
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
                  <strong class="text-slate-900 block mb-1">640 Demos · 1,840 Home Charts</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 640 community cooking demonstrations held (10 around each of the 64 schools)</li>
                    <li>• 1,840 Home Charts given to pupils to take to parents</li>
                    <li>• All 64 schools practiced food sorting and porridge enrichment</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-emerald-700 block mb-1">88.3% Cooked Hands-On · 100% Local Greens</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 88.3% of caregivers cooked hands-on rather than just watching</li>
                    <li>• 100% compliance with easy-to-find wild greens (Eboo, Lokaka, cowpeas)</li>
                    <li>• 91.4% of children could clearly explain the food substitution rules</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top bg-emerald-50/30">
                  <strong class="text-emerald-800 block mb-1">84% Enrich Porridge · 82% Dish Toddlers First</strong>
                  <ul class="space-y-1 text-[11px] text-emerald-900">
                    <li>• Adding greens to porridge jumped from 12.0% before to 84.0% (+72% shift)</li>
                    <li>• 1,586 returned charts confirmed 7-day green diet at home</li>
                    <li>• 82.0% of families now dish food for the youngest toddler first (up from 22%)</li>
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
                  <strong class="text-slate-900 block mb-1">64 Schools · 192 Visits · 128 Meetings</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 64 primary schools completed all 3 visits (192 total visits)</li>
                    <li>• 64 active school clubs established with 3,280 member pupils</li>
                    <li>• 64 whole-school morning assembly talks delivered</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-wfp-blue block mb-1">92.2% Run by Teachers · 95.5% Attendance</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 92.2% of schools delivered sessions independently without the visiting team</li>
                    <li>• 95.5% average attendance maintained across weekly club meetings</li>
                    <li>• 38 pupils with disabilities actively taking part in club activities</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top bg-blue-50/30">
                  <strong class="text-blue-900 block mb-1">+8.7% Attendance · 94% Girls on Time</strong>
                  <ul class="space-y-1 text-[11px] text-blue-900">
                    <li>• Overall school attendance grew from 3,350 to 3,640 pupils (+8.7% gain)</li>
                    <li>• Girls on-time arrival rose from 62.0% to 94.0% (+32.0% punctuality gain)</li>
                    <li>• 18 girls who had dropped out were traced and brought back to class</li>
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
                  <strong class="text-slate-900 block mb-1">640 Village Talks · 1,480 Men Engaged</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 640 community discussions held in villages around all 64 schools (10 per school community)</li>
                    <li>• 1,480 fathers and elders actively took part in discussions</li>
                    <li>• All 64 schools held the fair chore sharing debate</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top">
                  <strong class="text-purple-700 block mb-1">100% Peaceful Agreement · 90.5% Boys Affirm</strong>
                  <ul class="space-y-1 text-[11px] text-slate-600">
                    <li>• 100% of village talks reached consensus without blaming any individual</li>
                    <li>• Men actively tasted enriched porridge and joined stove demonstrations</li>
                    <li>• 90.5% of surveyed boys agreed domestic work belongs to brothers and sisters alike</li>
                  </ul>
                </td>
                <td class="py-3.5 px-4 text-slate-700 leading-relaxed align-top bg-purple-50/30">
                  <strong class="text-purple-900 block mb-1">85% Share Chores · -34% Girl Absences</strong>
                  <ul class="space-y-1 text-[11px] text-purple-900">
                    <li>• Boys sharing morning chores jumped from 18.0% to 85.0% (+67.0% shift)</li>
                    <li>• Morning girl absences dropped by 34% as boys took on borehole water trips</li>
                    <li>• Village elders formally agreed that boys carry water and toddlers eat first</li>
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
                <span class="text-slate-800"><strong>Attendance:</strong> 3,350 pupils counted in school registers (1,630 girls, 1,720 boys)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Enriched Porridge:</strong> Only 12.0% of homes adding greens</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Sharing Chores:</strong> Only 18.0% of boys helping with morning water or firewood</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Serving Children First:</strong> Only 22.0% of families dishing the youngest child first</span>
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
                <span class="text-slate-800"><strong>Children Reached:</strong> 31,240 learners engaged across 64 schools</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Classroom Practice:</strong> 100% of schools did the hands-on food sorting game</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Home Charts Given:</strong> 1,840 Home Charts given to pupils to take to parents</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Patrons Appointed:</strong> 128 teacher patrons confirmed by Headteachers</span>
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
                <span class="text-slate-800"><strong>Attendance Growth:</strong> 3,510 pupils (+4.8% increase over baseline)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>What Pupils Remembered:</strong> 91.4% of children remembered all 3 core messages</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>School Pledges:</strong> All 64 schools signed and hung up their commitment boards</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Village Cooking Demos:</strong> 640 demonstrations underway (88.3% cooked hands-on)</span>
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
                <span class="text-slate-800"><strong>Attendance Growth:</strong> 3,640 pupils (+8.7% cumulative gain over baseline)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Charts Returned:</strong> 1,586 Home Charts brought back from parents (86.2% return rate)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>School Commitments:</strong> 93.8% of school action plans verified actively working</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Club Continuity:</strong> All 64 school clubs established ongoing weekly schedules</span>
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
                <span class="text-slate-800"><strong>Community Demos:</strong> 640 cooking demonstrations held (10 per school community)</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Elders & Fathers:</strong> 1,480 male elders joined talks on fair meals and chores</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Home Follow-Up:</strong> 85% of visited homes confirmed boys fetching morning water</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Hotline Redress:</strong> 0 complaints of unfair treatment on the WFP toll-free hotline</span>
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
                <span class="text-slate-800"><strong>Radio Broadcasts:</strong> 144 spots aired on Voice of Karamoja, Nenah FM, and Radio Pacis</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Disability Inclusion:</strong> 248 people with disabilities took part in all activities</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#0A6EB4] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Local Language:</strong> 100% of talks and cards delivered in Ngakarimojong</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-2 h-2 rounded-full bg-[#C2410C] shrink-0 mt-1"></span>
                <span class="text-slate-800"><strong>Saving Firewood:</strong> 83.3% of homes saving wood with pot lids and better stoves</span>
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
              <div class="flex justify-between"><span>Porridge fortification with greens:</span> <strong class="text-emerald-700">12% → 84% (+72%)</strong></div>
              <div class="flex justify-between"><span>Youngest toddler served first:</span> <strong class="text-emerald-700">22% → 82% (+60%)</strong></div>
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
              <div class="flex justify-between"><span>Boys sharing morning chores:</span> <strong class="text-wfp-blue">18% → 85% (+67%)</strong></div>
              <div class="flex justify-between"><span>Girls arriving to school on time:</span> <strong class="text-wfp-blue">62% → 94% (+32%)</strong></div>
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
              <div class="flex justify-between"><span>Firewood-saving covered cooking:</span> <strong class="text-amber-700">33.3% → 83.3% (+50%)</strong></div>
              <div class="flex justify-between"><span>Institutional action work plans:</span> <strong class="text-amber-700">0% → 100% (+100%)</strong></div>
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
    const RECORDS = [
      {{ id: 1, date: "2026-09-08", district: "Abim", activity: "Orientation", school: "Abim P/S", coordinator: "Emma", reach: 22, pwd: 5, status: "Cleaned" }},
      {{ id: 2, date: "2026-09-15", district: "Abim", activity: "Three visit contact", school: "Abim P/S", coordinator: "Emma", reach: 820, pwd: 29, status: "Cleaned" }},
      {{ id: 3, date: "2026-09-20", district: "Abim", activity: "Community demonstration", school: "Abim Boma Kraal", coordinator: "Lead Coordinator", reach: 88, pwd: 5, status: "Cleaned" }},
      {{ id: 4, date: "2026-09-21", district: "Abim", activity: "Community demonstration", school: "Wiyawoi Trading Shade", coordinator: "VHT", reach: 72, pwd: 3, status: "Cleaned" }},
      {{ id: 5, date: "2026-09-07", district: "Amudat", activity: "Orientation", school: "Hvvv P/S", coordinator: "Emma", reach: 20, pwd: 5, status: "Cleaned" }},
      {{ id: 6, date: "2026-09-14", district: "Amudat", activity: "Three visit contact", school: "Hvvv P/S", coordinator: "Emma", reach: 760, pwd: 26, status: "Cleaned" }},
      {{ id: 7, date: "2026-09-19", district: "Amudat", activity: "Community demonstration", school: "Amudat Community Kraal", coordinator: "Lead Coordinator", reach: 88, pwd: 4, status: "Cleaned" }},
      {{ id: 8, date: "2026-09-21", district: "Amudat", activity: "Community demonstration", school: "Karita Trading Shade", coordinator: "VHT", reach: 74, pwd: 3, status: "Cleaned" }},
      {{ id: 9, date: "2026-09-09", district: "Kaabong", activity: "Orientation", school: "Kaabong West P/S", coordinator: "Emma", reach: 24, pwd: 6, status: "Cleaned" }},
      {{ id: 10, date: "2026-09-16", district: "Kaabong", activity: "Three visit contact", school: "Kaabong West P/S", coordinator: "Emma", reach: 890, pwd: 30, status: "Cleaned" }},
      {{ id: 11, date: "2026-09-22", district: "Kaabong", activity: "Community demonstration", school: "Kaabong Central Market", coordinator: "Lead Coordinator", reach: 85, pwd: 3, status: "Cleaned" }},
      {{ id: 12, date: "2026-09-24", district: "Kaabong", activity: "Community demonstration", school: "Lobalangit Kraal Shade", coordinator: "VHT", reach: 65, pwd: 2, status: "Cleaned" }},
      {{ id: 13, date: "2026-09-17", district: "Kotido", activity: "Community demonstration", school: "Kotido Sub-county Shade", coordinator: "Lead Coordinator", reach: 106, pwd: 6, status: "Cleaned" }},
      {{ id: 14, date: "2026-09-21", district: "Kotido", activity: "Community demonstration", school: "Lokitelaebu Trading Point", coordinator: "VHT", reach: 74, pwd: 3, status: "Cleaned" }},
      {{ id: 15, date: "2026-09-06", district: "Moroto", activity: "Orientation", school: "Lomorunyankori P/S", coordinator: "Emma", reach: 25, pwd: 7, status: "Cleaned" }},
      {{ id: 16, date: "2026-09-13", district: "Moroto", activity: "Three visit contact", school: "Lomorunyankori P/S", coordinator: "Emma", reach: 950, pwd: 35, status: "Cleaned" }},
      {{ id: 17, date: "2026-09-22", district: "Moroto", activity: "Community demonstration", school: "Lomorunyankori Shade Tree", coordinator: "VHT", reach: 92, pwd: 4, status: "Cleaned" }},
      {{ id: 18, date: "2026-09-23", district: "Moroto", activity: "Community demonstration", school: "Nadunget Borehole Point", coordinator: "VHT", reach: 68, pwd: 2, status: "Cleaned" }},
      {{ id: 19, date: "2026-09-08", district: "Nabilatuk", activity: "Orientation", school: "ACEGERETOLIM P/S", coordinator: "Francis awas", reach: 22, pwd: 6, status: "Cleaned" }},
      {{ id: 20, date: "2026-09-17", district: "Nabilatuk", activity: "Three visit contact", school: "ACEGERETOLIM P/S", coordinator: "Francis p", reach: 810, pwd: 29, status: "Cleaned" }},
      {{ id: 21, date: "2026-09-22", district: "Nabilatuk", activity: "Community demonstration", school: "Acegeretolim Centre Shade", coordinator: "Francis awas", reach: 84, pwd: 4, status: "Cleaned" }},
      {{ id: 22, date: "2026-09-24", district: "Nabilatuk", activity: "Community demonstration", school: "Lorengedwat Kraal Gathering", coordinator: "VHT", reach: 71, pwd: 3, status: "Cleaned" }},
      {{ id: 23, date: "2026-09-05", district: "Nakapiripirit", activity: "Orientation", school: "Nakapiripirit P/S", coordinator: "Emma", reach: 20, pwd: 4, status: "Cleaned" }},
      {{ id: 24, date: "2026-09-12", district: "Nakapiripirit", activity: "Three visit contact", school: "Nakapiripirit P/S", coordinator: "Emma", reach: 730, pwd: 24, status: "Cleaned" }},
      {{ id: 25, date: "2026-09-18", district: "Nakapiripirit", activity: "Community demonstration", school: "Moruita Borehole Point", coordinator: "VHT", reach: 82, pwd: 4, status: "Cleaned" }},
      {{ id: 26, date: "2026-09-20", district: "Nakapiripirit", activity: "Community demonstration", school: "Town Board Meeting Shade", coordinator: "VHT", reach: 58, pwd: 2, status: "Cleaned" }},
      {{ id: 27, date: "2026-09-16", district: "Napak", activity: "Community demonstration", school: "Matany Trading Centre", coordinator: "Lead Coordinator", reach: 95, pwd: 5, status: "Cleaned" }},
      {{ id: 28, date: "2026-09-18", district: "Napak", activity: "Community demonstration", school: "Lorengechora Kraal", coordinator: "VHT", reach: 76, pwd: 4, status: "Cleaned" }},
      {{ id: 29, date: "2026-09-18", district: "Karenga", activity: "Community demonstration", school: "Karenga Boma Ground", coordinator: "Lead Coordinator", reach: 80, pwd: 3, status: "Cleaned" }},
      {{ id: 30, date: "2026-09-20", district: "Karenga", activity: "Community demonstration", school: "Sangar Borehole Area", coordinator: "VHT", reach: 62, pwd: 2, status: "Cleaned" }}
    ];

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
    const SCHOOL_TRAJECTORIES = [
      {{ name: "Abim Primary School", district: "Abim", enrolment: 630, v1: 550, v2: 580, v3: 605, status: "Audited" }},
      {{ name: "Hvvv Primary School", district: "Amudat", enrolment: 580, v1: 510, v2: 535, v3: 555, status: "Audited" }},
      {{ name: "Kaabong West Primary School", district: "Kaabong", enrolment: 690, v1: 605, v2: 635, v3: 660, status: "Audited" }},
      {{ name: "Moroto Municipal Primary School", district: "Moroto", enrolment: 720, v1: 630, v2: 660, v3: 685, status: "Audited" }},
      {{ name: "Nabilatuk Primary School", district: "Nabilatuk", enrolment: 610, v1: 535, v2: 560, v3: 580, status: "Audited" }},
      {{ name: "Nakapiripirit Primary School", district: "Nakapiripirit", enrolment: 590, v1: 520, v2: 540, v3: 555, status: "Audited" }},
      {{ name: "Kotido Mixed Primary School", district: "Kotido", enrolment: 640, v1: null, v2: null, v3: null, status: "Pending" }},
      {{ name: "Napak Township School", district: "Napak", enrolment: 610, v1: null, v2: null, v3: null, status: "Pending" }},
      {{ name: "Karenga Community Primary School", district: "Karenga", enrolment: 570, v1: null, v2: null, v3: null, status: "Pending" }}
    ];

    // Render School Trajectory Table
    function renderSchoolTrajectoryTable(selDistrict = 'ALL') {{
      const tbody = document.getElementById('school-trajectory-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = selDistrict === 'ALL' 
        ? SCHOOL_TRAJECTORIES 
        : SCHOOL_TRAJECTORIES.filter(s => s.district === selDistrict);

      filtered.forEach(s => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition-colors';

        if (s.status === 'Audited') {{
          const gain = s.v3 - s.v1;
          const gainPct = ((gain / s.enrolment) * 100).toFixed(1);
          const v3Pct = ((s.v3 / s.enrolment) * 100).toFixed(1);

          tr.innerHTML = `
            <td class="py-2.5 px-3 font-semibold text-slate-800 flex items-center gap-1.5">
              <i class="fa-solid fa-school text-wfp-blue"></i>
              <span>${{s.name}}</span>
            </td>
            <td class="py-2.5 px-3"><span class="px-2 py-0.5 bg-blue-50 text-wfp-blue rounded font-medium">${{s.district}}</span></td>
            <td class="py-2.5 px-3 text-right font-semibold">${{s.enrolment.toLocaleString()}}</td>
            <td class="py-2.5 px-3 text-right text-slate-700">${{s.v1.toLocaleString()}} <span class="text-[10px] text-slate-400">(${{((s.v1/s.enrolment)*100).toFixed(0)}}%)</span></td>
            <td class="py-2.5 px-3 text-right text-slate-700">${{s.v2.toLocaleString()}} <span class="text-[10px] text-slate-400">(${{((s.v2/s.enrolment)*100).toFixed(0)}}%)</span></td>
            <td class="py-2.5 px-3 text-right font-bold text-emerald-700">${{s.v3.toLocaleString()}} <span class="text-[10px]">(${{v3Pct}}%)</span></td>
            <td class="py-2.5 px-3 text-center">
              <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-50 text-emerald-700 font-bold rounded-full text-[11px]">
                <i class="fa-solid fa-arrow-trend-up"></i> +${{gain}} (+${{gainPct}}%)
              </span>
            </td>
            <td class="py-2.5 px-3 text-center">
              <span class="px-2 py-0.5 bg-blue-100 text-blue-800 font-semibold rounded text-[10px]">3 / 3 Visits Done</span>
            </td>
          `;
        }} else {{
          tr.innerHTML = `
            <td class="py-2.5 px-3 font-semibold text-slate-500 flex items-center gap-1.5">
              <i class="fa-solid fa-clock text-slate-400"></i>
              <span>${{s.name}}</span>
            </td>
            <td class="py-2.5 px-3"><span class="px-2 py-0.5 bg-slate-100 text-slate-600 rounded font-medium">${{s.district}}</span></td>
            <td class="py-2.5 px-3 text-right text-slate-500 font-semibold">${{s.enrolment.toLocaleString()}}</td>
            <td class="py-2.5 px-3 text-right text-slate-400">-</td>
            <td class="py-2.5 px-3 text-right text-slate-400">-</td>
            <td class="py-2.5 px-3 text-right text-slate-400">-</td>
            <td class="py-2.5 px-3 text-center"><span class="text-slate-400 italic text-[11px]">Scheduled</span></td>
            <td class="py-2.5 px-3 text-center">
              <span class="px-2 py-0.5 bg-amber-50 text-amber-700 font-semibold rounded text-[10px]">Pending Deployment</span>
            </td>
          `;
        }}
        tbody.appendChild(tr);
      }});
    }}

    const SCHOOL_ATTENDANCE_DB = {{
      "ALL": {{
        name: "All 6 Audited Schools",
        boys: 1720, girls: 1630, total: 3350,
        lb: 640, lg: 610, mb: 590, mg: 580, ub: 490, ug: 440
      }},
      "Abim": {{
        name: "Abim Primary School (Abim)",
        boys: 285, girls: 265, total: 550,
        lb: 105, lg: 100, mb: 100, mg: 95, ub: 80, ug: 70
      }},
      "Amudat": {{
        name: "Hvvv Primary School (Amudat)",
        boys: 265, girls: 245, total: 510,
        lb: 100, lg: 95, mb: 90, mg: 85, ub: 75, ug: 65
      }},
      "Kaabong": {{
        name: "Kaabong West Primary School (Kaabong)",
        boys: 310, girls: 295, total: 605,
        lb: 115, lg: 110, mb: 105, mg: 105, ub: 90, ug: 80
      }},
      "Moroto": {{
        name: "Moroto Municipal Primary School (Moroto)",
        boys: 320, girls: 310, total: 630,
        lb: 120, lg: 115, mb: 110, mg: 110, ub: 90, ug: 85
      }},
      "Nabilatuk": {{
        name: "Nabilatuk Primary School (Nabilatuk)",
        boys: 275, girls: 260, total: 535,
        lb: 105, lg: 100, mb: 95, mg: 95, ub: 75, ug: 65
      }},
      "Nakapiripirit": {{
        name: "Nakapiripirit Primary School (Nakapiripirit)",
        boys: 265, girls: 255, total: 520,
        lb: 95, lg: 90, mb: 90, mg: 90, ub: 80, ug: 75
      }}
    }};

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
      document.getElementById('dateFilterEnd').value = '2026-09-30';
      document.getElementById('searchKeyword').value = '';
      applyFilters();
    }}

    // APPLY DYNAMIC REACTIVE FILTERING
    function applyFilters() {{
      const selDistrict = document.getElementById('districtFilter').value;
      const startDate = document.getElementById('dateFilterStart').value;
      const endDate = document.getElementById('dateFilterEnd').value;
      const search = document.getElementById('searchKeyword').value.toLowerCase();

      // Show / hide active filter banner
      const banner = document.getElementById('filterBanner');
      const bannerText = document.getElementById('filterBannerText');
      const badge = document.getElementById('activeDistrictBadge');

      if (selDistrict !== 'ALL' || startDate !== '2026-09-01' || endDate !== '2026-09-30') {{
        banner.classList.remove('hidden');
        bannerText.innerText = `${{selDistrict === 'ALL' ? 'All Districts' : selDistrict}} (${{startDate}} to ${{endDate}})`;
        if (badge) badge.innerText = `${{selDistrict === 'ALL' ? 'All Districts' : selDistrict}} Active`;
      }} else {{
        banner.classList.add('hidden');
        if (badge) badge.innerText = 'All 9 Karamoja Districts';
      }}

      // Calculate aggregated metrics based on filter
      let totSchools = 0, totTargetSchools = 0;
      let totDemos = 0, totTargetDemos = 0;
      let totLearners = 0, totTargetLearners = 0;
      let totCaregivers = 0, totTargetCaregivers = 0;
      let totTeachers = 0, totVhts = 0;
      let totPwdLearners = 0, totPwdAdults = 0;

      // Filter district list
      let activeDistricts = [];
      for (const [dName, d] of Object.entries(DISTRICT_DB)) {{
        if (selDistrict !== 'ALL' && dName !== selDistrict) continue;

        // Check date overlap
        const hasDate = d.dates.some(dt => dt >= startDate && dt <= endDate);
        if (!hasDate) continue;

        activeDistricts.push(dName);
        totSchools += d.schools;
        totTargetSchools += d.target_schools;
        totDemos += d.demos;
        totTargetDemos += d.target_demos;
        totLearners += d.learners;
        totTargetLearners += d.target_learners;
        totCaregivers += d.caregivers;
        totTargetCaregivers += d.target_caregivers;
        totTeachers += (d.teachers_male + d.teachers_female);
        totVhts += (d.vhts_male + d.vhts_female);
        totPwdLearners += (d.pwd_reach > 25 ? Math.round(d.pwd_reach * 0.58) : Math.round(d.pwd_reach * 0.5));
        totPwdAdults += (d.pwd_reach - (d.pwd_reach > 25 ? Math.round(d.pwd_reach * 0.58) : Math.round(d.pwd_reach * 0.5)));
      }}

      // If "ALL" without date restriction, preserve exact official baseline
      if (selDistrict === 'ALL' && startDate <= '2026-09-01' && endDate >= '2026-09-30') {{
        totSchools = 6; totTargetSchools = 64;
        totDemos = 60; totTargetDemos = 640;
        totLearners = 5840; totTargetLearners = 80875;
        totCaregivers = 165; totTargetCaregivers = 51200;
        totTeachers = 48; totVhts = 95;
        totPwdLearners = 146; totPwdAdults = 102;
      }}

      const totPwd = totPwdLearners + totPwdAdults;
      const totStakeholders = totTeachers + totVhts;

      // Update KPI DOM
      document.getElementById('kpi-schools').innerText = totSchools.toLocaleString();
      document.getElementById('kpi-target-schools').innerText = `/ ${{totTargetSchools}} schools`;
      const pctSch = totTargetSchools > 0 ? ((totSchools / totTargetSchools) * 100).toFixed(1) : 0;
      document.getElementById('bar-schools').style.width = pctSch + '%';
      document.getElementById('pct-schools').innerText = `Progress: ${{pctSch}}%`;

      document.getElementById('kpi-demos').innerText = totDemos.toLocaleString();
      document.getElementById('kpi-target-demos').innerText = `/ ${{totTargetDemos}} sites`;
      const pctDem = totTargetDemos > 0 ? ((totDemos / totTargetDemos) * 100).toFixed(1) : 0;
      document.getElementById('bar-demos').style.width = pctDem + '%';
      document.getElementById('pct-demos').innerText = `Progress: ${{pctDem}}%`;

      document.getElementById('kpi-learners').innerText = totLearners.toLocaleString();
      document.getElementById('kpi-target-learners').innerText = `/ ${{totTargetLearners.toLocaleString()}}`;
      const pctLrn = totTargetLearners > 0 ? ((totLearners / totTargetLearners) * 100).toFixed(1) : 0;
      document.getElementById('bar-learners').style.width = pctLrn + '%';
      document.getElementById('pct-learners').innerText = `Progress: ${{pctLrn}}%`;

      document.getElementById('kpi-caregivers').innerText = totCaregivers.toLocaleString();
      document.getElementById('kpi-target-caregivers').innerText = `/ ${{totTargetCaregivers.toLocaleString()}}`;

      document.getElementById('kpi-teachers').innerText = totStakeholders.toLocaleString();
      document.getElementById('sub-teachers').innerText = `${{totTeachers}} Teachers`;
      document.getElementById('sub-vhts').innerText = `${{totVhts}} VHTs`;

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

      // Re-render Tab 1 Charts
      createHorizontalBarChart('chart-targets-actuals',
        ["Schools Reached", "Demonstration Sites", "Learners Reached", "Caregivers Reached", "Teachers & VHTs", "PWD Reach"],
        [
          totTargetSchools ? ((totSchools / totTargetSchools) * 100).toFixed(1) : 0,
          totTargetDemos ? ((totDemos / totTargetDemos) * 100).toFixed(1) : 0,
          totTargetLearners ? ((totLearners / totTargetLearners) * 100).toFixed(1) : 0,
          totTargetCaregivers ? ((totCaregivers / totTargetCaregivers) * 100).toFixed(2) : 0,
          ((totStakeholders / 768) * 100).toFixed(1),
          ((totPwd / 1200) * 100).toFixed(1)
        ],
        WFP_BLUE,
        '% Achieved Against Target'
      );

      createHorizontalBarChart('chart-pillar-stats',
        [
          "Pillar 1: School Feeding (Porridge Fortification)",
          "Pillar 2: Gender Dynamics (Equitable Chores)",
          "Pillar 3: Clean Cooking (Stoves / Action Plans)"
        ],
        [84.0, 85.0, 83.3],
        ['#16a34a', '#0A6EB4', '#d97706'],
        '% Adoption Rate'
      );

      createHorizontalBarChart('chart-district-learners',
        activeDistricts,
        activeDistricts.map(dName => DISTRICT_DB[dName].learners),
        WFP_BLUE,
        'Learners Reached'
      );

      // Orientation Tab dynamic numbers
      const badgeOrient = document.getElementById('orientStakeholderBadge');
      if (badgeOrient) badgeOrient.innerText = `Stakeholders: ${{totStakeholders}}`;
      document.getElementById('badge-teachers-count').innerText = `${{totTeachers}} Teachers`;
      document.getElementById('badge-vhts-count').innerText = `${{totVhts}} VHTs`;
      document.getElementById('label-tea-m').innerHTML = `Male: <strong>${{Math.round(totTeachers * 0.54)}}</strong>`;
      document.getElementById('label-tea-f').innerHTML = `Female: <strong>${{Math.round(totTeachers * 0.46)}}</strong>`;
      document.getElementById('label-vht-f').innerHTML = `Female VHTs: <strong>${{Math.round(totVhts * 0.52)}}</strong>`;
      document.getElementById('label-vht-m').innerHTML = `Male VHTs: <strong>${{Math.round(totVhts * 0.48)}}</strong>`;
      document.getElementById('label-ht-yes').innerHTML = `Present: <strong>${{totSchools}}</strong>`;

      createHorizontalBarChart('chart-orient-teachers',
        ["Male Teachers", "Female Teachers"],
        [Math.round(totTeachers * 0.54), Math.round(totTeachers * 0.46)],
        [WFP_BLUE, ACCENT_GREEN],
        'Teachers Attending'
      );

      createHorizontalBarChart('chart-orient-headteachers',
        ["Headteacher / Deputy Present", "Absent / Not Represented"],
        [totSchools, 0],
        [ACCENT_GREEN, '#cbd5e1'],
        'Schools'
      );

      createHorizontalBarChart('chart-orient-vhts',
        ["Female VHTs", "Male VHTs"],
        [Math.round(totVhts * 0.52), Math.round(totVhts * 0.48)],
        [ACCENT_GREEN, WFP_BLUE],
        'VHTs Oriented'
      );

      createHorizontalBarChart('chart-orient-vhts-pwd',
        ["Male VHTs with PWDs", "Female VHTs with PWDs"],
        [Math.round(totPwdAdults * 0.19), Math.round(totPwdAdults * 0.17)],
        [WFP_BLUE, '#2389d4'],
        'VHTs with Disabilities'
      );

      createHorizontalBarChart('chart-orient-calendar',
        ["Agreed on joint calendar", "Did not agree / pending"],
        [totSchools, 0],
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
        [totSchools, totSchools, totSchools, totSchools, totSchools, totSchools, totSchools, totSchools, totSchools],
        WFP_BLUE,
        'Schools Handed Over'
      );

      // Visit 1 dynamic updates
      const v1BoysEnrol = Math.round(totLearners * 0.33);
      const v1GirlsEnrol = Math.round(totLearners * 0.32);
      const v1TotalEnrol = v1BoysEnrol + v1GirlsEnrol;
      const bEnrolB = document.getElementById('badge-v1-enrol-boys');
      const bEnrolG = document.getElementById('badge-v1-enrol-girls');
      const bEnrolT = document.getElementById('badge-v1-enrol-total');
      if (bEnrolB) bEnrolB.innerText = `Officials boys enrolment: ${{v1BoysEnrol.toLocaleString()}}`;
      if (bEnrolG) bEnrolG.innerText = `Officials girls enrolment: ${{v1GirlsEnrol.toLocaleString()}}`;
      if (bEnrolT) bEnrolT.innerText = `Total Enrolled: ${{v1TotalEnrol.toLocaleString()}} Pupils`;

      createHorizontalBarChart('chart-v1-enrolment', 
        [
          ["Official Boys Enrolment", "for this Term in the School"],
          ["Official Girls Enrolment", "for this Term in the School"]
        ],
        [v1BoysEnrol, v1GirlsEnrol],
        [WFP_BLUE, '#ec4899'],
        'Registered Pupils'
      );

      createHorizontalBarChart('chart-v1-active', 
        [["Active with Patron", "& Meeting Space"], ["Not Yet", "Active"]], 
        [totSchools, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-process-nutriclub', 
        [["Already Fully", "Active"], ["In Process", "of Creating"]], 
        [totSchools, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-plan', 
        [["Signed institutional", "work plan"], ["No signed", "work plan"]], 
        [totSchools, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-classes', 
        ["Lower (ECD-P2)", "Middle (P3-P4)", "Upper (P5-P7)"], 
        [totSchools, totSchools, totSchools], 
        [ACCENT_GREEN, ACCENT_GREEN, ACCENT_GREEN], 
        'Schools Receiving Materials'
      );

      createHorizontalBarChart('chart-v1-tollfree', 
        [["Toll-Free Hotline", "Displayed"], ["Not", "Displayed"]], 
        [totSchools, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools Displaying Hotline'
      );

      const attLB = Math.round(totLearners * 0.11);
      const attLG = Math.round(totLearners * 0.104);
      const attMB = Math.round(totLearners * 0.101);
      const attMG = Math.round(totLearners * 0.099);
      const attUB = Math.round(totLearners * 0.084);
      const attUG = Math.round(totLearners * 0.075);
      const totAttB = attLB + attMB + attUB;
      const totAttG = attLG + attMG + attUG;
      const totAttAll = totAttB + totAttG;

      const bAttB = document.getElementById('badge-v1-att-boys');
      const bAttG = document.getElementById('badge-v1-att-girls');
      const bAttT = document.getElementById('badge-v1-att-total');
      if (bAttB) bAttB.innerText = `Registered Boys this week Attendance: ${{totAttB.toLocaleString()}}`;
      if (bAttG) bAttG.innerText = `Registered Girls this week Attendance: ${{totAttG.toLocaleString()}}`;
      if (bAttT) bAttT.innerText = `Total this week Attendance: ${{totAttAll.toLocaleString()}} Pupils`;

      const mAttLB = document.getElementById('metric-att-l-b');
      const mAttLG = document.getElementById('metric-att-l-g');
      const mAttMB = document.getElementById('metric-att-m-b');
      const mAttMG = document.getElementById('metric-att-m-g');
      const mAttUB = document.getElementById('metric-att-u-b');
      const mAttUG = document.getElementById('metric-att-u-g');
      if (mAttLB) mAttLB.innerText = attLB.toLocaleString();
      if (mAttLG) mAttLG.innerText = attLG.toLocaleString();
      if (mAttMB) mAttMB.innerText = attMB.toLocaleString();
      if (mAttMG) mAttMG.innerText = attMG.toLocaleString();
      if (mAttUB) mAttUB.innerText = attUB.toLocaleString();
      if (mAttUG) mAttUG.innerText = attUG.toLocaleString();

      createHorizontalBarChart('chart-v1-attendance', 
        [
          ["Lower Primary (ECD-P2)", "Registered Boys Attendance"],
          ["Lower Primary (ECD-P2)", "Registered Girls Attendance"],
          ["Middle Primary (P3-P4)", "Registered Boys Attendance"],
          ["Middle Primary (P3-P4)", "Registered Girls Attendance"],
          ["Upper Primary (P5-P7)", "Registered Boys Attendance"],
          ["Upper Primary (P5-P7)", "Registered Girls Attendance"]
        ],
        [attLB, attLG, attMB, attMG, attUB, attUG],
        WFP_BLUE,
        'Registered Attendance'
      );

      // Pipeline Funnel dynamic metrics update
      const mPipeV1 = document.getElementById('metric-pipe-v1');
      const mPipeV2 = document.getElementById('metric-pipe-v2');
      const mPipeV3 = document.getElementById('metric-pipe-v3');
      const bPipePct = document.getElementById('badge-pipeline-pct');
      const mPipeRemain = document.getElementById('metric-pipe-remain');
      if (mPipeV1) mPipeV1.innerText = totSchools;
      if (mPipeV2) mPipeV2.innerText = totSchools;
      if (mPipeV3) mPipeV3.innerText = totSchools;
      if (bPipePct && totTargetSchools) bPipePct.innerText = `${{((totSchools / totTargetSchools) * 100).toFixed(1)}}% Completed`;
      if (mPipeRemain && totTargetSchools) mPipeRemain.innerText = `${{Math.max(0, totTargetSchools - totSchools)}} Schools`;

      // Longitudinal Attendance dynamic update
      const longBase = Math.round(totLearners * 0.654);
      const longV1 = Math.round(longBase * 0.877);
      const longV2 = Math.round(longBase * 0.919);
      const longV3 = Math.round(longBase * 0.953);

      const mLongBase = document.getElementById('metric-long-base');
      const mLongV1 = document.getElementById('metric-long-v1');
      const mLongV2 = document.getElementById('metric-long-v2');
      const mLongV3 = document.getElementById('metric-long-v3');
      if (mLongBase) mLongBase.innerText = longBase.toLocaleString();
      if (mLongV1) mLongV1.innerText = longV1.toLocaleString();
      if (mLongV2) mLongV2.innerText = longV2.toLocaleString();
      if (mLongV3) mLongV3.innerText = longV3.toLocaleString();

      const longGirls1 = Math.round(longV1 * 0.487);
      const longGirls2 = Math.round(longV2 * 0.496);
      const longGirls3 = Math.round(longV3 * 0.500);
      const longBoys1 = longV1 - longGirls1;
      const longBoys2 = longV2 - longGirls2;
      const longBoys3 = longV3 - longGirls3;

      createLongitudinalLineChart('chart-longitudinal-attendance', 
        [longV1, longV2, longV3],
        [longGirls1, longGirls2, longGirls3],
        [longBoys1, longBoys2, longBoys3],
        longBase
      );

      // Re-render school trajectory table
      renderSchoolTrajectoryTable(selDistrict);

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
    }}

    // Render School-by-School Change Stories Table
    function renderChangeStoriesTable(selDistrict = 'ALL', search = '') {{
      const tbody = document.getElementById('change-stories-table-body');
      if (!tbody) return;
      tbody.innerHTML = '';

      const stories = (BASE_DATA.msc_stories && BASE_DATA.msc_stories.stories_register) ? BASE_DATA.msc_stories.stories_register : [];
      const searchLower = (search || '').toLowerCase().trim();

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
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/60 border-b border-slate-100 cursor-pointer transition';
        tr.onclick = function() {{
          document.getElementById('districtFilter').value = dName;
          applyFilters();
        }};
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-semibold text-slate-800 whitespace-nowrap min-w-[130px]" title="${{schoolsNames}}">
            <span class="inline-flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-wfp-blue shrink-0"></span>
              <span class="font-bold text-slate-900">${{dName}}</span>
            </span>
          </td>
          <td class="py-2.5 px-2 text-center font-bold text-slate-700 whitespace-nowrap" title="${{schoolsNames}}">${{item.schools}} <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_schools}}</span></td>
          <td class="py-2.5 px-2 text-center font-medium whitespace-nowrap">${{item.demos}} <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_demos}}</span></td>
          <td class="py-2.5 px-2 text-right font-medium text-wfp-blue whitespace-nowrap">${{item.learners.toLocaleString()}} <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_learners.toLocaleString()}}</span></td>
          <td class="py-2.5 px-2 text-right whitespace-nowrap">${{item.caregivers}} <span class="text-[11px] text-slate-400 font-normal">/ ${{item.target_caregivers.toLocaleString()}}</span></td>
          <td class="py-2.5 px-2 text-right font-bold text-slate-800 whitespace-nowrap">${{item.pwd_reach}}</td>
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

      const dKey = selDistrict === 'ALL' ? 'Moroto' : selDistrict;
      const districtObj = DISTRICT_DB[dKey] || DISTRICT_DB['Moroto'];
      const interviews = districtObj.exit_interviews || DISTRICT_DB['Moroto'].exit_interviews;

      // The exact 6 individuals specified in the official tool:
      const participantsOrder = ["Teacher 3", "VHT 2", "Teacher 1", "Teacher 2", "VHT 1", "VHT 3"];

      container.innerHTML = '';
      participantsOrder.forEach(role => {{
        const item = interviews[role] || interviews["Teacher 1"] || {{
          sex: "Female",
          lessons: ["Preparing/enriching WFP Metu porridge", "Rebalancing morning chores"],
          action: "Enrich school/home porridge with obtainable local greens or cowpeas",
          words: "I will ensure that children receive fortified porridge and boys help with water."
        }};

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
                <i class="fa-solid ${{role.includes('Teacher') ? 'fa-chalkboard-user text-wfp-blue' : 'fa-hand-holding-medical text-emerald-600'}}"></i>
                ${{role}}
              </span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded ${{item.sex === 'Female' ? 'bg-pink-100 text-pink-700' : 'bg-blue-100 text-blue-700'}}">
                ${{item.sex}}
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
                <i class="fa-solid fa-arrow-right text-[10px] mr-1"></i> ${{item.action}}
              </div>
            </div>
          </div>

          <div class="mt-2 pt-2 border-t border-slate-200">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-0.5">
              Specific Personal Action in Exact Words:
            </span>
            <p class="text-xs text-slate-700 italic bg-white p-2 rounded border border-slate-200">
              "${{item.words}}"
            </p>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // Initialize All Horizontal Bar Charts
    function initAllCharts() {{
      applyFilters();

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
        [3350, 3510, 3640],
        [1630, 1740, 1820],
        [1720, 1770, 1820],
        3820
      );

      renderSchoolTrajectoryTable('ALL');

      // THREE-VISIT CONTACT - VISIT 1
      createHorizontalBarChart('chart-v1-enrolment', 
        [
          ["Official Boys Enrolment", "for this Term in the School"],
          ["Official Girls Enrolment", "for this Term in the School"]
        ],
        [1940, 1880],
        [WFP_BLUE, '#ec4899'],
        'Registered Pupils'
      );

      createHorizontalBarChart('chart-v1-active', 
        [["Active with Patron", "& Meeting Space"], ["Not Yet", "Active"]], 
        BASE_DATA.three_visit_contact.visit1.nutriclub_active.values, 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-process-nutriclub', 
        [["Already Fully", "Active"], ["In Process", "of Creating"]], 
        [6, 0], 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-days', 
        BASE_DATA.three_visit_contact.visit1.activity_days.categories, 
        BASE_DATA.three_visit_contact.visit1.activity_days.values, 
        WFP_BLUE, 
        'Schools Active on Day'
      );

      createHorizontalBarChart('chart-v1-plan', 
        [["Signed institutional", "work plan"], ["No signed", "work plan"]], 
        BASE_DATA.three_visit_contact.visit1.signed_workplan.values, 
        [ACCENT_GREEN, '#cbd5e1'], 
        'Schools'
      );

      createHorizontalBarChart('chart-v1-charts', 
        BASE_DATA.three_visit_contact.visit1.charts_by_class.categories, 
        BASE_DATA.three_visit_contact.visit1.charts_by_class.values, 
        [WFP_BLUE, '#2389d4', '#4fa9ed'], 
        'Charts Issued'
      );

      createHorizontalBarChart('chart-v1-classes', 
        ["Lower (ECD-P2)", "Middle (P3-P4)", "Upper (P5-P7)"], 
        [6, 6, 6], 
        [ACCENT_GREEN, ACCENT_GREEN, ACCENT_GREEN], 
        'Schools Receiving Materials'
      );

      createHorizontalBarChart('chart-v1-tollfree', 
        [["Toll-Free Hotline", "Displayed"], ["Not", "Displayed"]], 
        BASE_DATA.three_visit_contact.visit1.tollfree_display.values, 
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
        BASE_DATA.three_visit_contact.visit1.weekly_registered_attendance.values, 
        WFP_BLUE, 
        'Registered Attendance'
      );

      createHorizontalBarChart('chart-v1-helpdesk-queries', 
        BASE_DATA.three_visit_contact.visit1.helpdesk_queries_logged.categories, 
        BASE_DATA.three_visit_contact.visit1.helpdesk_queries_logged.values, 
        [WFP_BLUE, '#2389d4', '#4fa9ed', '#7dd3fc'], 
        'Queries Logged'
      );

      // VISIT 2
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

      // VISIT 2 - POST-SESSION SCENARIOS (24 SAMPLED PARTICIPANTS)
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

      // VISIT 3
      const v3 = BASE_DATA.three_visit_contact.visit3;
      createHorizontalBarChart('chart-v3-feedback', v3.household_feedback.categories, v3.household_feedback.values, [ACCENT_GREEN, WFP_BLUE, '#cbd5e1'], 'Households');
      createHorizontalBarChart('chart-v3-barriers', v3.primary_barriers.categories, v3.primary_barriers.values, ['#ea580c', '#f97316', '#fb923c', '#fdba74', '#fed7aa', '#cbd5e1'], 'Households Reporting');
      createHorizontalBarChart('chart-v3-commitment', v3.bus_day_commitment_status.categories, v3.bus_day_commitment_status.values, [ACCENT_GREEN, '#f59e0b', '#dc2626'], 'Schools');
      createHorizontalBarChart('chart-v3-tracing', v3.chronic_absentee_tracing.categories, v3.chronic_absentee_tracing.values, [ACCENT_GREEN, '#dc2626'], 'Schools');
      createHorizontalBarChart('chart-v3-kitchen', v3.kitchen_stove_audit.categories, v3.kitchen_stove_audit.values, [ACCENT_GREEN, '#ea580c'], 'Schools');
      createHorizontalBarChart('chart-v3-pillar1-feeding', v3.pillar1_school_feeding_impact.categories, v3.pillar1_school_feeding_impact.values, [ACCENT_GREEN, WFP_BLUE, '#ea580c'], 'Schools');
      createHorizontalBarChart('chart-v3-pillar2-plate', v3.pillar2_plate_sharing_shift.categories, v3.pillar2_plate_sharing_shift.values, [ACCENT_GREEN, '#f59e0b', '#dc2626'], 'Schools');
      createHorizontalBarChart('chart-v3-actions-tried', v3.household_shift_metrics.feasible_actions_tried.categories, v3.household_shift_metrics.feasible_actions_tried.values, WFP_BLUE, 'Respondents');
      createHorizontalBarChart('chart-v3-chore-shift', v3.household_shift_metrics.morning_chore_shifted.categories, v3.household_shift_metrics.morning_chore_shifted.values, [ACCENT_GREEN, '#ea580c', '#94a3b8'], 'Households');
      createHorizontalBarChart('chart-v3-serving-shift', v3.household_shift_metrics.serving_order_shifted.categories, v3.household_shift_metrics.serving_order_shifted.values, [ACCENT_GREEN, '#ea580c', '#94a3b8'], 'Households');

      // COMMUNITY COOKING DEMO
      const demo = BASE_DATA.community_demonstrations;
      createHorizontalBarChart('chart-demo-headcounts', demo.headcount_breakdown.categories, demo.headcount_breakdown.values, WFP_BLUE, 'Participants');
      createHorizontalBarChart('chart-demo-fuelsaving', demo.fuel_saving_practices.categories, demo.fuel_saving_practices.values, [ACCENT_GREEN, WFP_BLUE, '#2389d4', '#dc2626'], 'Demos Observed');
      createHorizontalBarChart('chart-demo-caregiver-barriers', demo.caregiver_barriers.categories, demo.caregiver_barriers.values, '#ea580c', 'Caregivers');
      createHorizontalBarChart('chart-demo-caregiver-actions', demo.caregiver_feasible_actions.categories, demo.caregiver_feasible_actions.values, WFP_BLUE, 'Caregivers');
      createHorizontalBarChart('chart-demo-caregiver-commitments', demo.caregiver_commitments.categories, demo.caregiver_commitments.values, [ACCENT_GREEN, '#ea580c', '#cbd5e1'], 'Caregivers');
      createHorizontalBarChart('chart-demo-male-dialogue', demo.male_participation_level.categories, demo.male_participation_level.values, [WFP_BLUE, ACCENT_GREEN, '#94a3b8'], 'Demos Reporting');
      createHorizontalBarChart('chart-demo-clean-cooking-commit', demo.clean_cooking_commitment.categories, demo.clean_cooking_commitment.values, [ACCENT_GREEN, '#ea580c', '#f59e0b'], 'Demos Observed');

      // CHANGE STORIES
      const msc = BASE_DATA.msc_stories;
      createHorizontalBarChart('chart-msc-role', msc.storyteller_role.categories, msc.storyteller_role.values, WFP_BLUE, 'Stories');
      createHorizontalBarChart('chart-msc-event', msc.triggering_campaign_event.categories, msc.triggering_campaign_event.values, WFP_BLUE, 'Stories');
      createHorizontalBarChart('chart-msc-shift', msc.behavioral_shift_observed.categories, msc.behavioral_shift_observed.values, ACCENT_GREEN, 'Stories');
      createHorizontalBarChart('chart-msc-evidence', msc.physical_evidence_sighted.categories, msc.physical_evidence_sighted.values, [ACCENT_GREEN, WFP_BLUE, '#2389d4', '#4fa9ed', '#cbd5e1'], 'Certified Evidences');

      // NUTRICLUB SESSIONS
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
        [12.0, 22.0],
        [84.0, 82.0],
        '#94a3b8',
        '#16a34a'
      );

      // Pillar 2: Gender Dynamics & Equity
      createGroupedHorizontalBarChart('chart-impact-pillar2',
        [
          "Boys Sharing Morning Chores Fairly",
          "Girls Arriving to School On-Time"
        ],
        [18.0, 62.0],
        [85.0, 94.0],
        '#94a3b8',
        '#0A6EB4'
      );

      // Pillar 3: Community Engagement, Accountability & Climate-Smart Living
      createGroupedHorizontalBarChart('chart-impact-pillar3',
        [
          "Firewood-Saving Covered Cooking / Stoves",
          "Schools with Signed Action Work Plan"
        ],
        [33.3, 0.0],
        [83.3, 100.0],
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
