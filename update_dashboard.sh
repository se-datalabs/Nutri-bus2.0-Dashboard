#!/bin/bash
set -e

echo "🚌 1/2 Ingesting latest field data from Nutribus_2.0_Activity.xlsx..."
python3 ingest_actual_data.py

echo "📊 2/2 Rebuilding HTML dashboard (index.html)..."
python3 build_full_dashboard.py

echo "✅ Dashboard update complete! index.html and database JSONs are up to date."
