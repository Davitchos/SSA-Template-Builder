import random
import re

def slugify(text):
    text = str(text).lower()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"^[^a-z_]+", "_", text)
    return text.strip("_") + str(random.randint(1000, 9999))