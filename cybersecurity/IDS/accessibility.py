import sqlite3
import os

tcc_path = os.path.expanduser("~/Library/Application Support/com.apple.TCC/TCC.db")
conn = sqlite3.connect(tcc_path)
cursor = conn.cursor()

services_to_watch = [
    'kTCCServiceCamera',
    'kTCCServiceMicrophone',
    'kTCCServiceScreenCapture'
]

def get_current_permissions():
    conn = sqlite3.connect(tcc_path)
    cursor = conn.cursor()
    found = []

    for service in services_to_watch:
        cursor.execute("SELECT client, auth_value FROM access WHERE service=?", (service,))
        rows = cursor.fetchall()
        for client, auth in rows:
            found.append((service, client, auth))

    conn.close()
    return found

def log_permissions(entries):
    print("=== Current App Permissions ===")
    for service, client, auth in entries:
        status = "Allowed" if auth == 1 else "Denied"
        print(f"{service} → {client}: {status}")
    print("===============================")

# Initial snapshot
current = get_current_permissions()
log_permissions(current)

# Optional: Monitor for changes every N seconds
WATCH = False
if WATCH:
    print("Watching for new permission grants...")
    while True:
        time.sleep(10)
        updated = get_current_permissions()
        new_entries = [entry for entry in updated if entry not in current]

        if new_entries:
            print("[!] New permissions detected:")
            log_permissions(new_entries)
            current = updated  # Update snapshot
