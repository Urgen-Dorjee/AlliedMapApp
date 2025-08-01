# setup.py
import pandas as pd

VALID_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "GU", "PR", "VI", "MP", "AS"
}
COMPACT_STATES = [
    # ...your compact states...
    "AL", "AR", "AZ", "CO", "DE", "FL", "GA", "ID", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MS", "MO", "MT", "NE", "NH", "NJ", "NM",
    "NC", "ND", "OH", "OK", "PA", "SC", "SD", "TN", "TX", "UT", "VA",
    "VT", "WV", "WI", "WY"
]
REQUIRED_DEFAULTS = {
    "Region": "Unknown Region",
    "Fname": "Not Provided",
    "Lname": "Not Provided",
    "Category": "Not Provided",
    "Status": "Active"
}
FALLBACK_MAP = {
    # ...your fallback mappings...
    "Person_key": "Id",
    "Fname": "First Name",
    "Lname": "Last Name",
    "ZIPCode": "Postal Code",
    "Phone1": "Phone1.1",
    "cellPhone1": "Phone1.1",
    "BirthDate": "BirthDate",
    "MName": "Middle Name",
    "EMail": "Email"
}
