import streamlit as st
import pandas as pd
import numpy as np
import re

def reset_processing():
    """
    Reset all Streamlit session state variables to allow a new mapping and processing run.
    """
    st.session_state.processed = False
    st.session_state.general_df = None
    st.session_state.reqdoc_df = None
    st.session_state.specialty_df = None
    # No license_df needed for Allied

def clean_text(text: str) -> str:
    """
    Clean up text by removing carriage returns, special codes, and collapsing whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.replace("_x000D_", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def ensure_str_columns(df):
    """Convert all columns in DataFrame to strings, blanking out missing values and weird types."""
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].replace(['nan', 'NaT', '<NA>', 'None', 'none', 'NULL', 'null'], '', regex=False)
        df[col] = df[col].replace({np.nan: '', None: ''})
    return df
