
import streamlit as st
import pandas as pd
import os

from utils.file_validation import FilenameValidator
from utils.excel_validator import validate_excel_sheets
from databricks.sdk import WorkspaceClient

st.set_page_config(page_title="LinkedIn Analytics Ingestion", layout="centered")

st.title("LinkedIn Analytics Ingestion App")
st.write("Upload your LinkedIn Analytics Excel export files here.")

uploaded_files = st.file_uploader("Choose Excel file(s)", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    st.divider()
    

    # Validate all files first
    valid_files = []
    for uploaded_file in uploaded_files:
        with st.expander(f"📄 {uploaded_file.name}", expanded=True):
            # 1. Validate Filename
            validator = FilenameValidator(uploaded_file.name)
            if not validator.is_valid_format():
                st.error(f"❌ Invalid filename format. Expected: Content_YYYY-MM-DD_YYYY-MM-DD_ProfileName.xlsx")
                continue

            # 2. Validate Content (Sheets)
            required_sheets = ["DISCOVERY", "ENGAGEMENT", "FOLLOWERS", "TOP POSTS"]
            is_valid, error_msg = validate_excel_sheets(uploaded_file, required_sheets)
            if not is_valid:
                st.error(f"❌ {error_msg}")
                continue
            
            st.success(f"✅ Valid — all required sheets present.")
            valid_files.append(uploaded_file)

    # Ingest button — only shown if at least one valid file
    if valid_files:
        st.divider()
        st.info(f"{len(valid_files)} of {len(uploaded_files)} file(s) ready to ingest.")
        if st.button(f"Ingest {len(valid_files)} File(s)"):
            w = WorkspaceClient()
            landing_catalog = os.getenv("LANDING_CATALOG", "landing")
            landing_schema = os.getenv("LANDING_SCHEMA", "linkedin")
            landing_volume = os.getenv("LANDING_VOLUME", "content_daily")
            ingestion_folder = os.getenv("INGESTION_FOLDER", "pending")

            progress = st.progress(0, text="Starting upload...")
            for i, uploaded_file in enumerate(valid_files):
                volume_path = f"/Volumes/{landing_catalog}/{landing_schema}/{landing_volume}/{ingestion_folder}/{uploaded_file.name}"
                try:
                    progress.progress((i) / len(valid_files), text=f"Uploading {uploaded_file.name}...")
                    w.files.upload(volume_path, uploaded_file.getvalue(), overwrite=True)
                    st.success(f"✅ Uploaded: `{uploaded_file.name}`")
                except Exception as e:
                    st.error(f"❌ Failed to upload `{uploaded_file.name}`: {e}")
            progress.progress(1.0, text="Done!")
