import streamlit as st
import requests
import json
import os
from PIL import Image
import io
import base64

st.set_page_config(page_title="Arabcha Skaner Pro", page_icon="📖")
st.title("📖 Arabcha Matn Tahlilchisi")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API kalit topilmadi. Railway Variables bo'limini tekshiring!")
    st.stop()

uploaded_file = st.file_uploader("Rasmni yuklang", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Skanerlashni boshlash"):
        with st.spinner("AI ulanmoqda..."):
            # Modellarni navbat bilan sinash ro'yxati
            models_to_try = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro-vision"]
            success = False

            for model_name in models_to_try:
                try:
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()

                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                    
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": "Ushbu rasmdagi arabcha matnni o'qing va o'zbekchaga tarjima qiling."},
                                {"inline_data": {"mime_type": "image/jpeg", "data": img_str}}
                            ]
                        }]
                    }
                    
                    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
                    
                    if response.status_code == 200:
                        result = response.json()
                        text_output = result['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"Tahlil yakunlandi! (Model: {model_name})")
                        st.write(text_output)
                        success = True
                        break # Agar ishlasa, keyingi modellarni sinab o'tirmaymiz
                except:
                    continue
            
            if not success:
                st.error("Hozircha Google modellari sizning kalitingizga ruxsat bermayapti. Iltimos, 10 daqiqa kutib qayta urining.")
