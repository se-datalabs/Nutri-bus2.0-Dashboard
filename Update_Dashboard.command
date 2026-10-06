#!/bin/bash
# Move to the script's directory automatically regardless of where it is run
cd "$(dirname "$0")"

echo "========================================================"
echo "🚌 NUTRIBUS 2.0 DASHBOARD AUTO-UPDATER"
echo "========================================================"
echo ""
echo "Running ingestion pipeline..."
./update_dashboard.sh
echo ""
echo "========================================================"
echo "✨ DONE! The dashboard has been updated successfully."
echo "👉 Now switch to your browser and press Cmd + Shift + R."
echo "========================================================"
echo ""
read -p "Press [Enter] to close this window..."
