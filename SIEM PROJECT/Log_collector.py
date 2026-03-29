import os
import re
from database import init_db, insert_event

def read_log_file(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return

    print(f"[*] Reading: {filepath}\n")

    with open(filepath, "r") as f:
        for line in f:
            process_log(line.strip())


def process_log(line):
    pattern = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+):\s+(.*)'
    match = re.match(pattern, line)

    if match:
        timestamp = match.group(1)
        hostname = match.group(2)
        service = match.group(3)
        message = match.group(4)

        if "Failed password" in message:
            event_type = "FAILED_LOGIN"
        elif "Accepted password" in message:
            event_type = "SUCCESSFUL_LOGIN"
        else:
            event_type = "UNKNOWN"

        insert_event(timestamp, hostname, service, event_type, message)
        print(f"[{event_type}] {timestamp} | Host: {hostname} | Service: {service} | {message}")
    else:
        print(f"[UNMATCHED] {line}")

if __name__ == "__main__":
    init_db()
    log_file = "auth.log"  # Same project folder
    read_log_file(log_file)