import streamlit as st
import pandas as pd

from helpers import ensure_str_columns

def display_data_with_controls(df, name, key_prefix):
    """
    Show a preview of generated records in a paged table, with filter/search UI in Streamlit.
    """
    df = ensure_str_columns(df)
    total_rows = len(df)
    st.write(f"**{total_rows} {name} records generated**")
    if total_rows == 0:
        st.info(f"No {name} records found to display.")
        return
    col1, col2, col3 = st.columns([1, 1, 1])
    max_rows = max(5, min(500, total_rows))
    default_rows = min(20, max_rows)
    with col1:
        show_rows = st.number_input(
            "Rows to display:",
            min_value=5,
            max_value=max_rows,
            value=default_rows,
            step=5,
            key=f"{key_prefix}_rows"
        )
    with col2:
        max_start = max(0, total_rows - 1)
        start_row = st.number_input(
            "Start from row:",
            min_value=0,
            max_value=max_start,
            value=0,
            key=f"{key_prefix}_start"
        )
    with col3:
        if st.button(f"Show all records", key=f"{key_prefix}_all"):
            show_rows = total_rows
            start_row = 0
    end_row = min(start_row + show_rows, total_rows)
    if start_row > 0 or end_row < total_rows:
        st.write(f"Showing rows {start_row} to {end_row - 1} of {total_rows}")
    st.dataframe(df.iloc[start_row:end_row], use_container_width=True)

    if not df.empty and len(df.columns) > 0:
        search_col = st.selectbox(
            "Search/Filter by column:",
            ["None"] + list(df.columns),
            key=f"{key_prefix}_search_col"
        )
        if search_col != "None":
            search_term = st.text_input(
                f"Enter search term for {search_col}:",
                key=f"{key_prefix}_search_term"
            )
            if search_term:
                try:
                    filtered_df = df[df[search_col].astype(str).str.contains(search_term, case=False, na=False)]
                    filtered_df = ensure_str_columns(filtered_df)
                    st.write(f"Found {len(filtered_df)} matching records")
                    if not filtered_df.empty:
                        st.dataframe(filtered_df, use_container_width=True)
                    else:
                        st.info(f"No matches found for '{search_term}' in column '{search_col}'")
                except Exception as e:
                    st.error(f"Error during search: {str(e)}")

def preview_keap_data(df, max_preview=50):
    """
    Show a quick preview of the first few rows of uploaded KEAP data in Streamlit.
    """
    df = ensure_str_columns(df)
    if df is None or df.empty:
        st.info("No data available to preview.")
        return
    display_rows = st.slider(
        "Preview rows:",
        min_value=5,
        max_value=min(max_preview, len(df)),
        value=min(10, len(df))
    )
    st.dataframe(df.head(display_rows), use_container_width=True)
