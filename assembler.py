from mappings import CUSTOM_PROPERTIES_MAPPING, STANDARD_PROPERTIES_MAPPING
import pandas as pd
import utils

def assemble_full_template(records_message, records_standard_properties, records_costom_properties):
    template = {
        "name": "Imported Template",
        "category": "SSA",
        "metadataLayout": [],
        "layout": {
            "pages": [{
                "name": {"de": "Fragen", "en": "Questions"},
                "sections": []
            }]
        }
    }

    ## MESSAGE RECORD PROCESSING
    template = add_message_to_template(template, records_message)

    ## STD RECORD PROCESSING
    template = add_standard_properties_to_template(template, records_standard_properties)

    ## CUSTOM RECORD PROCESSING
    properties = []
    used_slugs = set()
    sections = []
    section_questions = []
    current_section = None
    order_counter = 0

    for record in records_costom_properties:
        section = record["section"]
        title_de = record["title_de"]
        title_en = record["title_en"]
        question_de = record["question_de"]
        question_en = record["question_en"]
        field_type = record["field_type"]
        raw_options = record["raw_options"]
        raw_options_en = record.get("raw_options_en")
        mandatory = record["mandatory"]

        if pd.notna(section):
            if current_section and section_questions:
                sections.append({
                    "name": {"de": current_section, "en": current_section},
                    "questions": section_questions,
                    "type": "QUESTIONS"
                })
            current_section = section.strip()
            section_questions = []
            order_counter = 0

        if pd.isna(title_de):
            continue

        slug_base = utils.slugify(title_de)
        slug = slug_base
        suffix = 1
        while slug in used_slugs:
            slug = f"{slug_base}_{suffix}"
            suffix += 1
        used_slugs.add(slug)

        widget, ptype = CUSTOM_PROPERTIES_MAPPING.get(field_type.strip(), ("SINGLE_LINE", "TEXT"))

        prop = {
            "widget": widget,
            "text": {"de": question_de, "en": question_en},
            "shortText": {"de": title_de, "en": title_en},
            "slug": slug,
            "type": ptype,
            "isFilterable": False,
            "scope": "SUPPLIER"
        }

        # Handle dropdown/multi options
        if (
            ptype == "MULTI" and 
            raw_options and pd.notna(raw_options) and 
            raw_options_en and pd.notna(raw_options_en)
        ):
            options = []
            for line_de, line_en in zip(str(raw_options).splitlines(), str(raw_options_en).splitlines()):
                label_de = line_de.strip("•- \t\n\r")
                label_en = line_en.strip("•- \t\n\r")
                
                if label_de and label_en:
                    options.append({
                        "label": {"de": label_de, "en": label_en},
                        "slug": utils.slugify(label_de)
                    })
            if options:
                prop["options"] = options

        """if (
            ptype == "MULTI" and 
            raw_options and pd.notna(raw_options) and 
            raw_options_en and pd.notna(raw_options_en)
        ):
            options = []
            
            for line in str(raw_options).splitlines():
                label = line.strip("•- \t\n\r")
                if label:
                    options.append({
                        "label": {"de": label, "en": ""},
                        "slug": utils.slugify(label)
                    })
            if options:
                prop["options"] = options"""


        properties.append(prop)
        section_questions.append({
            "slug": slug,
            "required": mandatory,
            "order": order_counter
        })
        order_counter += 1

    if current_section and section_questions:
        sections.append({
            "name": {"de": current_section, "en": current_section},
            "questions": section_questions,
            "type": "QUESTIONS"
        })

    template["layout"]["pages"][0]["sections"].extend(sections) 

    return {"template": template, "properties": properties}

def add_message_to_template(template, message_record):
    section = {
        "name": {
            "de": "Nachricht vom Einkäufer",
            "en": "Message from buyer"
        },
        "richTextMessage": {
            "de": message_record, 
            "en": {}
        },
        "type": "MESSAGE",
        "version": "1"
    }

    # Insert as the first section on the first page
    template["layout"]["pages"][0]["sections"].insert(0, section)

    return template

def add_standard_properties_to_template(template, records):
    # Access the first page sections
    sections = template["layout"]["pages"][0]["sections"]

    # Add only the ones marked True in records
    for entry in STANDARD_PROPERTIES_MAPPING:
        key = entry["key"]
        if records.get(key):
            sections.append(entry["section"])

    return template