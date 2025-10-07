import json

def safe_template(template, dir, name):
    with open(f"{dir}/{name}.json", "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=4)
    print(f"Template saved to {name}.json")