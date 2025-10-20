import pandas as pd

def extract_all(file_path):
    message_records = extract_supplier_message(file_path)
    standard_records = extract_standard_properties(file_path)
    custom_records = extract_custom_properties(file_path)

    return message_records, standard_records, custom_records

# Extract message
def extract_supplier_message(file_path):
    # Read Excel with pandas — no openpyxl workbook object
    df = pd.read_excel(file_path, header=None)

    # Read the value of cell B1 (row index 0, column index 1)
    text = str(df.iat[0, 1]).strip() if not pd.isna(df.iat[0, 1]) else ""

    records = {"type": "doc", "content": []}

    if not text:
        return None

    lines = [l.strip() for l in text.split("\n")]
    bullet_buffer = []
    paragraph_buffer = []

    def flush_bullets():
        if bullet_buffer:
            records["content"].append({
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {"type": "paragraph", "content": [{"text": t, "type": "text"}]}
                        ]
                    } for t in bullet_buffer
                ]
            })
            bullet_buffer.clear()

    def flush_paragraph():
        if paragraph_buffer:
            joined = " ".join(paragraph_buffer).strip()
            if joined:
                records["content"].append({
                    "type": "paragraph",
                    "content": [{"text": joined, "type": "text"}]
                })
            paragraph_buffer.clear()

    for line in lines:
        if not line:
            flush_bullets()
            flush_paragraph()
            continue

        if line.startswith(("•", "-")):
            flush_paragraph()
            bullet_buffer.append(line.lstrip("•- ").strip())
            continue

        flush_bullets()
        paragraph_buffer.append(line)

    flush_bullets()
    flush_paragraph()

    return records

# Extract pre-defined properties
def extract_standard_properties(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name="Vorlagen",header=0)

    records = {}

    for _, row in df.iterrows():
        header = row[0]
        implement = row[2] if len(row) > 2 else None

        # Only process if header is not empty
        if pd.notna(header) and str(header).strip():
            records[str(header).strip()] = str(implement).strip().lower() == "ja"

    return records

# Extract custom properties
def extract_custom_properties(file_path):
    df = pd.read_excel(file_path, sheet_name="Custom", header=0)
    records = []

    for _, row in df.iterrows():
        record = {
            "section": row.iloc[0],
            "title_de": row.iloc[1],
            "title_en": row.iloc[7],
            "question_de": row.iloc[2],
            "question_en": row.iloc[8],
            "field_type": row.iloc[3],
            "raw_options": row.iloc[10] if len(row) > 10 else None,
            "raw_options_en": row.iloc[11] if len(row) > 11 else None,
            "mandatory": str(row.iloc[4]).strip().lower() in ["yes", "ja", "true", "1"]
            if len(row) > 5 else False
        }
        records.append(record)
    return records