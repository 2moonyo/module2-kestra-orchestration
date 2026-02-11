import time
import requests
import subprocess

# Wait up to 3 minutes for Kestra management endpoint
for _ in range(90):
    try:
        r = requests.get("http://kestra:8081/health", timeout=2)
        if r.status_code == 200:
            print("Kestra is ready")
            break
    except Exception as e:
        print("Waiting for Kestra...", e)

    time.sleep(2)
else:
    raise SystemExit("Kestra did not become ready in time")

print("Starting upload...")
subprocess.check_call(["python", "upload_flows.py"])
