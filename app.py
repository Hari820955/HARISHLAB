import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
from report_analyzer import extract_patient_info, generate_summary

st.set_page_config(page_title="Reportslelo", layout="centered")

st.title("🧾 Reportslelo – रिपोर्ट को समझो आसान हिंदी में")
uploaded_file = st.file_uploader("🖼 रिपोर्ट की फोटो अपलोड करो", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="अपलोड की गई रिपोर्ट", use_column_width=True)

    with st.spinner("🔍 रिपोर्ट पढ़ी जा रही है..."):
        ocr_text = pytesseract.image_to_string(image, lang='eng')
        patient_info = extract_patient_info(ocr_text)
        summary = generate_summary(ocr_text)

        st.subheader("👤 पेशेंट की जानकारी:")
        st.write(f"**नाम:** {patient_info.get('name', 'पता नहीं चला')}")
        st.write(f"**उम्र:** {patient_info.get('age', 'पता नहीं चला')}")
        st.write(f"**मोबाइल:** {patient_info.get('phone', 'पता नहीं चला')}")

        st.subheader("📝 रिपोर्ट सारांश (हिंदी):")
        st.success(summary)
