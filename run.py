from app import create_app
from app.extensions import db
from datetime import datetime
import os
import logging
from dotenv import load_dotenv
import pytz

load_dotenv()
app = create_app()

try:
    if not db.logs.find_one({"event": "app_started"}):
        istanbul_time = datetime.now(pytz.timezone("Europe/Istanbul"))
        db.logs.insert_one({
            "event": "app_started",
            "started_at": istanbul_time,
            "environment": os.environ.get("FLASK_ENV", "development")
        })
        print("✅ Logged app startup to MongoDB")
except Exception as e:
    logging.error(f"MongoDB startup logging failed: {e}")
