"""
Configuration for the qualtrix microservice settings.
Context is switched based on if the app is in debug mode.
"""
import json
import logging
import os

log = logging.getLogger(__name__)


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG set is set to True if env var is "True"
DEBUG = os.getenv("DEBUG", "False") == "True"

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.getLevelName(logging.INFO))

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = os.getenv("BASE_URL")
SURVEY_ID = os.getenv("SURVEY_ID")
DIRECTORY_ID = os.getenv("DIRECTORY_ID")
