#!/bin/bash
set -e

echo "🚌 1/3 Ingesting latest field data from Nutribus_2.0_Activity.xlsx..."
python3 ingest_actual_data.py

echo "📊 2/3 Rebuilding HTML dashboard (index.html)..."
python3 build_full_dashboard.py

echo "📑 3/3 Updating Master Excel Extracts & Tracking Sheets..."
python3 update_master_extracts.py

echo "✅ Dashboard and all Master Extracts are up to date!"
