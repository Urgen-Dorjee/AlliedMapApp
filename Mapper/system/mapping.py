import streamlit as st
import pandas as pd

def normalize_colname(col):
    """
    Lowercase and clean a column name for comparison and matching.
    Strips asterisks and non-breaking spaces.
    """
    if not isinstance(col, str):
        return ""
    col = col.strip().lower().replace('*', '')
    col = col.replace('\xa0', ' ')
    col = ' '.join(col.split())
    return col

def get_mapping(template_df, source_df, label):
    """
    Streamlit widget for mapping BlueSky template fields to Allied dataset columns.
    Supports auto-mapping and manual mapping via select boxes.
    Returns: Dictionary {template_col: source_col}.
    """
    st.markdown(f"#### {label} Field Mapping")
    mapping_key = f"{label}_mapping"
    source_col_lookup = {normalize_colname(col): col for col in source_df.columns}
    if mapping_key not in st.session_state or st.session_state[mapping_key] is None:
        st.session_state[mapping_key] = {}
    if st.button(f"Auto-map exact matches for {label}", key=f"automap_{label}"):
        for t_col in template_df.columns:
            norm_t_col = normalize_colname(t_col)
            if norm_t_col in source_col_lookup:
                st.session_state[mapping_key][t_col] = source_col_lookup[norm_t_col]
    with st.expander(f"Manually map fields for {label}", expanded=True):
        for target_field in template_df.columns:
            current_value = st.session_state[mapping_key].get(target_field, "")
            source_cols = [''] + list(source_df.columns)
            index_value = source_cols.index(current_value) if current_value in source_cols else 0
            selected = st.selectbox(
                f"Map BlueSky '{target_field}' to Allied field:",
                source_cols,
                index=index_value,
                key=f"{label}_{target_field}"
            )
            st.session_state[mapping_key][target_field] = selected
    return st.session_state[mapping_key]

def apply_mapping(template, mapping, source_df):
    """
    Apply user-defined field mapping to generate an output DataFrame with BlueSky template columns.
    If a field is not mapped, outputs an empty string.
    """
    output_df = pd.DataFrame(columns=template.columns)
    for template_col in template.columns:
        source_col = mapping.get(template_col)
        if source_col and source_col in source_df.columns:
            output_df[template_col] = source_df[source_col]
        else:
            output_df[template_col] = ""
    from helpers import ensure_str_columns
    return ensure_str_columns(output_df)
