from app import create_app
from app.extensions import db
from datetime import datetime
import os
import logging
from dotenv import load_dotenv
import pytz
from pre_run import run as run_pre_start
from app.utils.logging import log_startup 

# Load environment variables
load_dotenv()

# run pre-start logic
run_pre_start()

# Create Flask app
app = create_app()

if __name__ == "__main__":
    with app.app_context(): # Initialize app context
        log_startup()

    app.run() # Start the Flask app




