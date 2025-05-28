import re
import openai

def extract_patient_info(text):
    """
    OCR से निकले text में से नाम, उम्र, फोन नंबर निकालने की कोशिश।
    (यहाँ simple regex use किया है, जरूरत अनुसार सुधार सकते हो)
    """
    info = {}

    # नाम खोजने की कोशिश - "Name:" या "Patient Name:" के बाद का टेक्स्ट
    name_match = re.search(r"(Name|Patient Name|नाम)[:\s]*([A-Za-z\s]+)", text, re.IGNORECASE)
    if name_match:
        info["name"] = name_match.group(2).strip()
    else:
        info["name"] = None

    # उम्र खोजने की कोशिश - "Age:" या "उम्र:" के बाद नंबर
    age_match = re.search(r"(Age|उम्र)[:\s]*(\d{1,3})", text, re.IGNORECASE)
    if age_match:
        info["age"] = age_match.group(2).strip()
    else:
        info["age"] = None

    # मोबाइल नंबर खोजने की कोशिश - 10 डिजिट का नंबर
    phone_match = re.search(r"(\+91[-\s]?|0)?\d{10}", text)
    if phone_match:
        info["phone"] = phone_match.group(0).strip()
    else:
        info["phone"] = None

    return info


def generate_summary(ocr_text, openai_api_key):
    """
    OpenAI API से हिंदी में 5 लाइन का सारांश बनाओ
    """
    openai.api_key = openai_api_key

    prompt = f"नीचे दी गई मेडिकल रिपोर्ट का हिंदी में सरल और 5 लाइन में सारांश दो:\n\n{ocr_text}\n\nसारांश:"

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary = response.choices[0].text.strip()
    except Exception as e:
        summary = "क्षमा करें, सारांश बनाने में समस्या आ गई। कृपया पुनः प्रयास करें।"

    return summary

