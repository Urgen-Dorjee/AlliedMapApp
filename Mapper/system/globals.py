import streamlit as st
import pandas as pd
import logging
import io
import zipfile

# --- CONFIGURATION & GLOBALS ---

# Allied does NOT use complex license/state/compact sets

# Fallback values for required columns in case they're empty
REQUIRED_DEFAULTS = {
    "Region": "Unknown Region",
    "Fname": "Not Provided",
    "Lname": "Not Provided",
    "Category": "Not Provided",
    "Status": "Active"
}

# Fallback mapping from BlueSky columns to KEAP columns (edit as needed)
FALLBACK_MAP = {
    "Person_key": "Id",
    "Fname": "First Name",
    "Lname": "Last Name",
    "ZIPCode": "Postal Code",
    "Phone1": "Phone ",
    "cellPhone1": "Phone ",
    "BirthDate": "Birthday",
    "MName": "Middle Name",
    "EMail": "Email"
}

# If you want to define all possible specialties for validation/reporting, do it here:
ALLIED_SPECIALTIES = [
    # e.g. 'Physical Therapy', 'Respiratory Therapy', 'Radiology', ...
]

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
