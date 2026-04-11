import streamlit as st
from PIL import Image
import io
import base64
import requests
import os
import time

st.set_page_config(page_title="Arabcha Matn Skaneri", page_icon="📖")
st.title("📖 Arabcha Matn Skaneri va Tarjimon")
st.caption("Rasm yuklang → Matnni skanerlaydi → O'zbekchaga tarjima qiladi")

api_key = None
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API kalit topilmadi!")
    st.stop()

def call_gemini(prompt, image_base64, max_retries=3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 4096
        }
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"], None
            
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    wait = 30 * (attempt + 1)
                    st.warning(f"⏳ Limit to'ldi, {wait}s kutilmoqda...")
                    time.sleep(wait)
                    continue
                return None, "quota"
            
            else:
                return None, f"HTTP {response.status_code}: {response.text}"
                
        except Exception as e:
            return None, str(e)
    
    return None, "Xato"

if "result" not in st.session_state:
    st.session_state.result = None

uploaded_file = st.file_uploader(
    "📷 Arabcha matnli rasm yuklang",
    type=['jpg', 'jpeg', 'png', 'webp'],
)

if uploaded_file is not None:
    uploaded_file.seek(0)
    image = Image.open(io.BytesIO(uploaded_file.read()))
    if image.mode != 'RGB':
        image = image.convert('RGB')

    st.image(image, caption="Yuklangan rasm", use_container_width=True)
    st.success(f"✅ {uploaded_file.name}")

    # Rasmni base64 ga o'tkazish
    buf = io.BytesIO()
    image.save(buf, format='JPEG', quality=90)
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    target_lang = st.selectbox("🌐 Tarjima tili:", ["O'zbek tili", "Rus tili", "Ingliz tili"])
    do_analysis = st.checkbox("🔍 Grammatika tahlili", value=True)

    if st.button("🚀 Skanerlash va Tahlil", type="primary", use_container_width=True):
        st.session_state.result = None

        prompt = f"""Siz arabcha matn mutaxassisiysiz. Quyidagi vazifalarni bajaring:

1. **ARABCHA MATN (OCR)**: Rasmdagi BARCHA arabcha matnni aynan ko'chirib yozing.
2. **{target_lang.upper()}GA TARJIMA**: Matnni to'liq {target_lang}ga tarjima qiling.
{"3. **GRAMMATIKA TAHLILI**: Asosiy grammatik tuzilmalar haqida qisqacha izohlang." if do_analysis else ""}

Javob formati:
---
📜 ARABCHA MATN:
[matn]

🌐 TARJIMA ({target_lang}):
[tarjima]

{"📚 GRAMMATIKA TAHLILI:" + chr(10) + "[tahlil]" if do_analysis else ""}
"""
        with st.spinner("⏳ Tahlil qilmoqda..."):
            result, error = call_gemini(prompt, img_b64)

        if result:
            st.session_state.result = result
        elif error == "quota":
            st.error("❌ API limiti to'ldi. Biroz kuting.")
        else:
            st.error(f"❌ Xato: {error}")

    if st.session_state.result:
        st.markdown("---")
        st.markdown("### 📋 Natija:")
        st.markdown(st.session_state.result)
        st.download_button("💾 Saqlash (.txt)", st.session_state.result,
                           "natija.txt", "text/plain", use_container_width=True)
else:
    st.info("👆 Rasm yuklang")
    st.session_state.result = None
