import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha AI Skaner", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri va Sharhlovchi")

# 2. Xavfsiz API kalitni olish (Secrets orqali)
# Agar secrets'ga qo'shgan bo'lsangiz, u avtomatik ishlaydi
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi. Iltimos, Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash qismi
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI matnni o‘qimoqda...'):
            prompt = "Ushbu rasmdagi arabcha matnni aniq, harakatlari (i'rob) bilan tering. Faqat arabcha matnni qaytaring."
            response = model.generate_content([prompt, image])
            st.session_state['arab_text'] = response.text
            st.success("Matn aniqlandi!")
            st.text_area("Aniqlangan arabcha matn:", st.session_state['arab_text'], height=200)

    if 'arab_text' in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tarjima qilish"):
                with st.spinner('Tarjima...'):
                    res = model.generate_content(f"Ushbu matnni o‘zbekchaga tarjima qil: {st.session_state['arab_text']}")
                    st.info(res.text)
        with col2:
            if st.button("Sharhlash"):
                with st.spinner('Sharh...'):
                    res_sh = model.generate_content(f"Ushbu matnni grammatik tahlil va ma'noviy sharhla: {st.session_state['arab_text']}")
                    st.warning(res_sh.text)
