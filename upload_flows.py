import os
import requests


KESTRA_URL = os.getenv("KESTRA_URL", "http://localhost:8080")
USERNAME = os.getenv("KESTRA_USERNAME", "admin@kestra.io")
PASSWORD = os.getenv("KESTRA_PASSWORD", "Admin1234!")
FLOW_DIR = os.getenv("FLOW_DIR", "./flows")



def upload_flow(path):
    with open(path, "r") as f:
        yaml_content = f.read()

    response = requests.post(
        f"{KESTRA_URL}/api/v1/main/flows",
        auth=(USERNAME, PASSWORD),
        headers={"Content-Type": "application/x-yaml"},
        data=yaml_content,
    )

    if response.status_code in [200, 201]:
        print(f"Uploaded: {os.path.basename(path)}")
    else:
        print(f"Failed: {path}")
        print(response.text)


for file in os.listdir(FLOW_DIR):
    if file.endswith(".yaml") or file.endswith(".yml"):
        upload_flow(os.path.join(FLOW_DIR, file))
