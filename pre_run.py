import requests
import json
from app.config import Config

def run():
    PUBLIC_KEY = Config.PUBLIC_KEY
    PRIVATE_KEY = Config.PRIVATE_KEY
    PROJECT_ID = Config.PROJECT_ID

    if not all([PUBLIC_KEY, PRIVATE_KEY, PROJECT_ID]):
        print("Missing MongoDB Atlas credentials.")
        return

    BASE_URL = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{PROJECT_ID}/accessList"
    
    try:
        ip = requests.get("https://api.ipify.org").text
        print("Current IP:", ip)

        headers = {"Content-Type": "application/json"}

        from requests.auth import HTTPDigestAuth
        auth = HTTPDigestAuth(PUBLIC_KEY, PRIVATE_KEY)

        payload = json.dumps([{
            "ipAddress": ip,
            "comment": "Auto-added by setup script"
        }])

        response = requests.post(BASE_URL, auth=auth, headers=headers, data=payload)

        if response.status_code == 201:
            print(f"IP {ip} successfully added to MongoDB Atlas.")
        elif response.status_code == 409:
            print(f"IP {ip} already exists in access list.")
        else:
            print(f"Failed to update access list: {response.text}")
    except Exception as e:
        print(f"Exception in pre_run: {e}")

# standalone run
if __name__ == "__main__":
    run()
