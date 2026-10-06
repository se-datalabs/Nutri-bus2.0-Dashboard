#!/usr/bin/env python3
"""
watch_and_update.py
Continuously monitors 'Nutribus_2.0_Activity.xlsx' for changes and automatically
re-runs './update_dashboard.sh' whenever the file is saved in Excel.
"""

import os
import sys
import time
import subprocess

WATCH_FILE = "Nutribus_2.0_Activity.xlsx"

def main():
    if not os.path.exists(WATCH_FILE):
        print(f"❌ Error: {WATCH_FILE} not found in current directory.")
        sys.exit(1)

    print("=" * 65)
    print("👀 NUTRIBUS 2.0 AUTO-SYNC WATCHER STARTED")
    print(f"📁 Watching: {WATCH_FILE}")
    print("⚡ Whenever you save changes in Excel (Cmd+S), the dashboard will update automatically!")
    print("Press Ctrl+C to stop.")
    print("=" * 65)

    last_mtime = os.path.getmtime(WATCH_FILE)

    while True:
        try:
            time.sleep(2)
            if not os.path.exists(WATCH_FILE):
                continue
            current_mtime = os.path.getmtime(WATCH_FILE)
            if current_mtime != last_mtime:
                # Give Excel a split second to finish writing the file
                time.sleep(0.5)
                last_mtime = os.path.getmtime(WATCH_FILE)
                print(f"\n🔄 Detected change in {WATCH_FILE} at {time.strftime('%H:%M:%S')}! Updating dashboard...")
                res = subprocess.run(["./update_dashboard.sh"], capture_output=True, text=True)
                print(res.stdout)
                if res.stderr:
                    print("Warnings/Errors:", res.stderr)
                print("✨ Finished auto-update! Now refresh your browser (Cmd + Shift + R).\n")
        except KeyboardInterrupt:
            print("\n🛑 Watcher stopped.")
            break
        except Exception as e:
            print(f"⚠️ Watcher error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
