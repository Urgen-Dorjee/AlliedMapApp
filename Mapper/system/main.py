import streamlit as st
import pandas as pd
import traceback
import io, zipfile
from setup import REQUIRED_DEFAULTS
from helpers import reset_processing, ensure_str_columns
from mapping import get_mapping, apply_mapping
from processing import process_general_info, process_required_docs, process_specialties
from ui_helpers import display_data_with_controls, preview_keap_data

st.set_page_config(
    page_title="Allied Data Mapper",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
if "processed" not in st.session_state:
    st.session_state.processed = False
if "general_df" not in st.session_state:
    st.session_state.general_df = None
if "reqdoc_df" not in st.session_state:
    st.session_state.reqdoc_df = None
if "specialty_df" not in st.session_state:
    st.session_state.specialty_df = None
if "keap_df" not in st.session_state:  # You can call this "allied_df" if you like
    st.session_state.keap_df = None

st.title("💺 Allied Data Mapper App")
st.markdown("Upload your excel export, templates to map, and map fields before generating CSVs.")

# --- FILE UPLOADS ---
col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="upload-text">📅 Upload Allied Excel file</p>', unsafe_allow_html=True)
    allied_file = st.file_uploader("Allied Excel file", type="xlsx", key="allied_file", label_visibility="collapsed")
with col2:
    st.markdown('<p class="upload-text">📄 BlueSky <span class="special-text">Caregiver General Info</span> Template</p>', unsafe_allow_html=True)
    bs_general = st.file_uploader("General Info Template", type="csv", key="bs_general", label_visibility="collapsed")
    st.markdown('<p class="upload-text">📄 BlueSky <span class="special-text">Caregiver Required Docs</span> Template</p>', unsafe_allow_html=True)
    bs_reqdoc = st.file_uploader("Required Docs Template", type="csv", key="bs_reqdoc", label_visibility="collapsed")
    st.markdown('<p class="upload-text">📄 BlueSky <span class="special-text">Caregiver Specialty</span> Template</p>', unsafe_allow_html=True)
    bs_specialty = st.file_uploader("Specialty Template", type="csv", key="bs_specialty", label_visibility="collapsed")

def clean_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.replace("*", "").strip() for c in df.columns]
    return df

if all([allied_file, bs_general, bs_reqdoc, bs_specialty]):
    if st.session_state.processed:
        if st.button("Reset & Start New Mapping", type="secondary"):
            reset_processing()
            st.rerun()
    if not st.session_state.processed:
        try:
            allied = pd.read_excel(allied_file)
            general_template = clean_cols(pd.read_csv(bs_general))
            reqdoc_template = clean_cols(pd.read_csv(bs_reqdoc))
            specialty_template = clean_cols(pd.read_csv(bs_specialty))
            st.session_state.keap_df = allied
            st.success(f"✅ Loaded Allied data with {len(allied)} records and {len(allied.columns)} columns")
            with st.expander("Preview Allied Data", expanded=False):
                preview_keap_data(allied)
            st.subheader("🤩 Data Mapping")
            tab1, tab2, tab3 = st.tabs(["General Info", "Required Docs", "Specialty"])
            with tab1:
                general_mapping = get_mapping(general_template, allied, "General Info")
            with tab2:
                reqdoc_mapping = get_mapping(reqdoc_template, allied, "Required Docs")
            with tab3:
                specialty_mapping = get_mapping(specialty_template, allied, "Specialty")
            st.subheader("🔄 Process Data")
            if st.button("Process and Generate CSVs", type="primary"):
                with st.spinner("Processing data..."):
                    general = apply_mapping(general_template, general_mapping, allied)
                    for field, default in REQUIRED_DEFAULTS.items():
                        if field in general.columns:
                            general[field] = general[field].fillna(default).replace("", default)
                    reqdoc_df = process_required_docs(allied, reqdoc_template)
                    specialty_df = process_specialties(allied, specialty_template)
                    st.session_state.general_df = ensure_str_columns(general)
                    st.session_state.reqdoc_df = ensure_str_columns(reqdoc_df)
                    st.session_state.specialty_df = ensure_str_columns(specialty_df)
                    st.session_state.processed = True
                    st.rerun()
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.info("See the server/terminal log for the full error details.")
            traceback.print_exc()
    else:
        if (st.session_state.general_df is not None and 
            st.session_state.reqdoc_df is not None and
            st.session_state.specialty_df is not None):
            st.subheader("🔍 Data Preview")
            preview_tabs = st.tabs(["General Info", "Required Docs", "Specialty Info"])
            with preview_tabs[0]:
                display_data_with_controls(st.session_state.general_df, "general", "general")
            with preview_tabs[1]:
                display_data_with_controls(st.session_state.reqdoc_df, "certification", "reqdoc")
            with preview_tabs[2]:
                display_data_with_controls(st.session_state.specialty_df, "specialty", "specialty")
            st.subheader("📄 Download Transformed Files")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "Download Caregiver General Info", 
                    st.session_state.general_df.to_csv(index=False).encode(), 
                    "BlueSky_Caregiver_General_Info.csv", 
                    "text/csv"
                )
                st.download_button(
                    "Download Caregiver Required Docs", 
                    st.session_state.reqdoc_df.to_csv(index=False).encode(), 
                    "BlueSky_Caregiver_RequiredDocs_Info.csv", 
                    "text/csv"
                )
                st.download_button(
                    "Download Caregiver Specialty Info", 
                    st.session_state.specialty_df.to_csv(index=False).encode(), 
                    "BlueSky_Caregiver_Specialty_Info.csv", 
                    "text/csv"
                )
            with col2:
                def create_zip_with_csvs():
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
                        zip_file.writestr("BlueSky_Caregiver_General_Info.csv", 
                                          st.session_state.general_df.to_csv(index=False))
                        zip_file.writestr("BlueSky_Caregiver_RequiredDocs_Info.csv", 
                                          st.session_state.reqdoc_df.to_csv(index=False))
                        zip_file.writestr("BlueSky_Caregiver_Specialty_Info.csv", 
                                          st.session_state.specialty_df.to_csv(index=False))
                    return zip_buffer.getvalue()
                st.download_button(
                    "💾 Download All Files (ZIP)",
                    create_zip_with_csvs(),
                    "BlueSky_All_Files.zip",
                    "application/zip"
                )
        else:
            st.error("Processed data is missing. Please try processing again.")
            reset_processing()
else:
    st.info("📋 Instructions: Upload all required files above to begin the mapping process")
    with st.expander("ℹ️ About this app"):
        st.markdown("""
        This application helps you convert Allied data to BlueSky format by:

        1. Loading your Allied export (Excel) and BlueSky templates (CSV)
        2. Guiding you through mapping fields between the systems
        3. Automatically extracting certifications and specialties
        4. Generating properly formatted CSV files for BlueSky import

        **Tips:**
        - The app will try to auto-map fields when possible
        - Multi-value fields are split into separate rows as required
        """)
