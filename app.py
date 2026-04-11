import streamlit as st
import requests
import json
import os
from PIL import Image
import io
import base64

st.set_page_config(page_title="Arabcha Skaner Pro", page_icon="📖")
st.title("📖 Arabcha Matn Tahlilchisi")

# API Kalitni olish
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API kalit topilmadi. Railway Variables bo'limini tekshiring!")
    st.stop()

uploaded_file = st.file_uploader("Rasmni yuklang", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Skanerlashni boshlash"):
        with st.spinner('AI to'g'ridan-to'g'ri ulanmoqda...'):
            try:
                # Rasmni kodga aylantirish
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # Google API'ga to'g'ridan-to'g'ri so'rov (v1 barqaror versiya)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Ushbu rasmdagi arabcha matnni o'qing va o'zbekchaga tarjima qiling."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_str}}
                        ]
                    }]
                }
                
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                result = response.json()

                if response.status_code == 200:
                    text_output = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("Tahlil yakunlandi!")
                    st.write(text_output)
                else:
                    st.error(f"Xato kodi: {response.status_code}")
                    st.json(result) # Xatoni aniq ko'rish uchun
            except Exception as e:
                st.error(f"Kutilmagan xato: {e}")
