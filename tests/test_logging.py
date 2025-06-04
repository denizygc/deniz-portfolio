import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch, MagicMock
from app.utils.logging import log_startup

@patch("app.utils.logging.db")  # Mock the db object in the logging module
def test_log_startup_success(mock_db):
    # Simulate environment variables
    os.environ["FLASK_ENV"] = "development"
    os.environ["WERKZEUG_RUN_MAIN"] = "true"  # simulate main process

    # Mock insert_one to avoid real DB call
    mock_insert_one = MagicMock()
    mock_db.logs.insert_one = mock_insert_one

    # Run the function
    log_startup()

    # Assert insert_one was called once
    assert mock_insert_one.called
    assert mock_insert_one.call_count == 1

    # Check call arguments (dict keys exist)
    call_args = mock_insert_one.call_args[0][0]
    assert "event" in call_args
    assert call_args["event"] == "app_started"
    assert "started_at_utc" in call_args
    assert "started_at_local" in call_args
    assert "environment" in call_args
    

@patch("app.utils.logging.db")  # Mock db again
def test_log_startup_db_failure(mock_db, capsys):
    # Simulate environment for main process
    os.environ["FLASK_ENV"] = "development"
    os.environ["WERKZEUG_RUN_MAIN"] = "true"

    # Make insert_one raise an exception
    mock_db.logs.insert_one.side_effect = Exception("Simulated DB failure")

    # Run the function (should hit except block)
    log_startup()

    # Capture printed output to verify exception handling
    captured = capsys.readouterr()
    assert "MongoDB startup logging failed: Simulated DB failure" in captured.out


@patch("app.utils.logging.db")  # Mock the db object
def test_log_startup_non_main_process(mock_db):
    # Simulate environment variables for non-main process in dev
    os.environ["FLASK_ENV"] = "development"
    os.environ["WERKZEUG_RUN_MAIN"] = "false"  # simulate reloader boot

    # Mock insert_one
    mock_insert_one = MagicMock()
    mock_db.logs.insert_one = mock_insert_one

    # Run the function
    log_startup()

    # Should NOT call insert_one
    mock_insert_one.assert_not_called()

@patch("app.utils.logging.db")  # Mock the db object
def test_log_startup_production(mock_db):
    # Simulate environment variables for production (no reloader check)
    os.environ["FLASK_ENV"] = "production"
    if "WERKZEUG_RUN_MAIN" in os.environ:
        del os.environ["WERKZEUG_RUN_MAIN"]

    # Mock insert_one
    mock_insert_one = MagicMock()
    mock_db.logs.insert_one = mock_insert_one

    # Run the function
    log_startup()

    # Should call insert_one even in prod
    mock_insert_one.assert_called_once()


    """
    | Test                                | What it does                                                                          |
    | ----------------------------------- | ------------------------------------------------------------------------------------- |
    | `test_log_startup_success`          | Ensures log\_startup() works in main process & calls insert\_one with correct fields. |
    | `test_log_startup_non_main_process` | Simulates reloader process → insert\_one should NOT be called.                        |
    | `test_log_startup_production`       | In production env, should log regardless of WERKZEUG\_RUN\_MAIN.                      |

    """
