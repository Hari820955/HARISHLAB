import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
from report_analyzer import extract_patient_info, generate_summary

import openai

st.set_page_config(page_title="Reportslelo", layout="centered")

# OpenAI API key को secret से load करो
openai.api_key = st.secrets["openai"]["api_key"]

st.title("🧾 Reportslelo – रिपोर्ट को समझो आसान हिंदी में")
uploaded_file = st.file_uploader("🖼 रिपोर्ट की फोटो अपलोड करो", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="अपलोड की गई रिपोर्ट", use_column_width=True)

    with st.spinner("🔍 रिपोर्ट पढ़ी जा रही है..."):
        # OCR से टेक्स्ट निकालो
        ocr_text = pytesseract.image_to_string(image, lang='eng')
        
        # Patient info निकालो (तेरे report_analyzer से)
        patient_info = extract_patient_info(ocr_text)

        # AI से summary generate करने के लिए फंक्शन में API key भेजो (नीचे बता रहा हूँ)
        summary = generate_summary(ocr_text, openai_api_key=openai.api_key)

        st.subheader("👤 पेशेंट की जानकारी:")
        st.write(f"**नाम:** {patient_info.get('name', 'पता नहीं चला')}")
        st.write(f"**उम्र:** {patient_info.get('age', 'पता नहीं चला')}")
        st.write(f"**मोबाइल:** {patient_info.get('phone', 'पता नहीं चला')}")

        st.subheader("📝 रिपोर्ट सारांश (हिंदी):")
        st.success(summary)
