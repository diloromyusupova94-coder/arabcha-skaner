import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha AI Skaner", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri va Sharhlovchi")
st.write("Rasm yuklang, matnni aniqlaymiz va sharhlaymiz.")

# 2. API konfiguratsiyasi
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Eng sodda va universal model nomi
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI matnni o‘qimoqda...'):
            try:
                # Promptni soddalashtirdik
                prompt = "Read the Arabic text in this image and provide it with tashkeel."
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.session_state['arab_text'] = response.text
                    st.success("Matn aniqlandi!")
                else:
                    st.error("AI matnni aniqlay olmadi.")
            except Exception as e:
                # Agar yana 404 bersa, muqobil modelni sinab ko'radi
                try:
                    alt_model = genai.GenerativeModel('gemini-pro-vision')
                    response = alt_model.generate_content([prompt, image])
                    st.session_state['arab_text'] = response.text
                    st.success("Matn muqobil model orqali aniqlandi!")
                except Exception as e2:
                    st.error(f"Xatolik: {e2}")

    # Natijalarni ko'rsatish
    if 'arab_text' in st.session_state:
        st.text_area("Aniqlangan arabcha matn:", st.session_state['arab_text'], height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("O‘zbekchaga tarjima"):
                res = model.generate_content(f"Tarjima qil: {st.session_state['arab_text']}")
                st.info(res.text)
        with col2:
            if st.button("Grammatik sharh"):
                res_sh = model.generate_content(f"Ushbu matnni nahviy tahlil qil: {st.session_state['arab_text']}")
                st.warning(res_sh.text)
