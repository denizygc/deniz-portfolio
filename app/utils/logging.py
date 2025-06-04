from datetime import datetime
import pytz
import os
from app.extensions import db
import tzlocal

def log_startup():
    # Only log for main process  
    if os.environ.get("FLASK_ENV") == "development":
        if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            return 

    try:
        timezone = tzlocal.get_localzone()
        print(f"Detected local timezone: {timezone}")
        now = datetime.now(timezone)

        db.logs.insert_one({
            "event": "app_started",  # Event type
            "started_at_utc": now.astimezone(pytz.utc),  # UTC time
            "started_at_local": now.strftime("%Y-%m-%d %H:%M:%S %Z%z"),  # Local time
            "environment": os.environ.get("FLASK_ENV", "development")  # Environment
        })
        print(f"Logged app startup at {now.isoformat()}")

    except Exception as e:
        print(f"MongoDB startup logging failed: {e}")
