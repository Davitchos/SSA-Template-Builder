import extractor
import assembler
import saver

src_path = "/Users/davitaghajanyan/Downloads/Abfrage Vorlage (2).xlsm"
dest_dir = "/Users/davitaghajanyan/Desktop/SSA Automation/Outputs"
dest_name = "final_template"

message_records, standard_records, custom_records = extractor.extract_all(src_path)

template = assembler.assemble_full_template(message_records, standard_records, custom_records)

saver.safe_template(template, dest_dir, dest_name)