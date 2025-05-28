import re
from googletrans import Translator
from utils import get_openai_summary

def extract_patient_info(text):
    info = {}

    name_match = re.search(r'(?:Name|नाम)\s*[:\-]?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
    age_match = re.search(r'(?:Age|उम्र)\s*[:\-]?\s*(\d{1,3})', text)
    phone_match = re.search(r'(\+91[\-\s]?)?\d{10}', text)

    if name_match:
        info['name'] = name_match.group(1).strip()
    if age_match:
        info['age'] = age_match.group(1).strip()
    if phone_match:
        info['phone'] = phone_match.group(0).strip()

    return info

def generate_summary(text):
    eng_summary = get_openai_summary(text)
    translator = Translator()
    translated = translator.translate(eng_summary, dest='hi')
    return translated.text
