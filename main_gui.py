import streamlit as st
import pandas as pd
import json
import io
import extractor
import assembler
import saver
import os
from tempfile import TemporaryDirectory

st.set_page_config(page_title="SSA Template Builder", page_icon="📄", layout="centered")

st.title("📄 SSA Template Builder")
st.markdown("Upload an Excel file and generate your JSON template automatically.")

# --- Inputs ---
uploaded_file = st.file_uploader("Upload Excel File (.xlsm, .xlsx, .xls)", type=["xls", "xlsx", "xlsm"])
dest_name = st.text_input("Output File Name (without .json)", "final_template")

if st.button("Generate Template"):
    if not uploaded_file:
        st.error("Please upload an Excel file first.")
    else:
        try:
            # Temporary folder for processing
            with TemporaryDirectory() as tmp_dir:
                src_path = os.path.join(tmp_dir, uploaded_file.name)
                with open(src_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Extract and assemble template
                message_records, standard_records, custom_records = extractor.extract_all(src_path)
                template = assembler.assemble_full_template(message_records, standard_records, custom_records)

                # Convert to JSON bytes
                json_bytes = json.dumps(template, ensure_ascii=False, indent=4).encode("utf-8")

                st.success("✅ Template successfully generated!")

                # Download button
                st.download_button(
                    label="⬇️ Download Template JSON",
                    data=json_bytes,
                    file_name=f"{dest_name}.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")