import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha AI Skaner", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri va Sharhlovchi")
st.write("Rasm yuklang, matnni aniqlaymiz va sharhlaymiz.")

# 2. API va Modelni sozlash
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Modelni faqat SHU YERDA, bir marta aniqlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash qismi
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI matnni o‘qimoqda...'):
            try:
                # Rasmdan matnni ajratib olish vazifasi
                prompt = "Rasmdagi arabcha matnni i'rob (harakatlari) bilan birma-bir ko'chirib yozing."
                response = model.generate_content([prompt, image])
                
                if response.text:
                    st.session_state['arab_text'] = response.text
                    st.success("Matn aniqlandi!")
                else:
                    st.error("AI matnni aniqlay olmadi.")
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")

    # 4. Natijani ko'rsatish va Tahlil
    if 'arab_text' in st.session_state:
        st.text_area("Aniqlangan arabcha matn:", st.session_state['arab_text'], height=200)
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("O‘zbekchaga tarjima qilish"):
                with st.spinner('Tarjima qilinmoqda...'):
                    t_res = model.generate_content(f"Ushbu matnni o'zbek tiliga tarjima qiling: {st.session_state['arab_text']}")
                    st.info(f"**Tarjima:**\n\n{t_res.text}")
        
        with col2:
            if st.button("Grammatik sharhlash"):
                with st.spinner('Tahlil qilinmoqda...'):
                    s_res = model.generate_content(f"Ushbu matnni nahv va sarf bo'yicha tahlil qiling: {st.session_state['arab_text']}")
                    st.warning(f"**Sharh:**\n\n{s_res.text}")
