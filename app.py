import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha AI Skaner", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri va Sharhlovchi")
st.write("Rasm yuklang, matnni aniqlaymiz va sharhlaymiz.")

# 2. API Kalitni kiritish (Xavfsizlik uchun yon paneldan kiritiladi)
with st.sidebar:
    st.header("Sozlamalar")
    api_key = st.text_input("Gemini API Keyni kiriting:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Fayl yuklash qismi
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI matnni o‘qimoqda...'):
            prompt = "Ushbu rasmdagi arabcha matnni aniq, harakatlari (i'rob) bilan tering. Faqat arabcha matnni qaytaring."
            response = model.generate_content([prompt, image])
            st.session_state['arab_text'] = response.text
            st.success("Matn aniqlandi!")
            st.text_area("Aniqlangan arabcha matn:", st.session_state['arab_text'], height=200)

    # 4. Tarjima va Sharh
    if 'arab_text' in st.session_state:
        if st.button("O‘zbekchaga tarjima qilaymi?"):
            with st.spinner('Tarjima qilinmoqda...'):
                res = model.generate_content(f"Ushbu matnni o‘zbekchaga tarjima qil: {st.session_state['arab_text']}")
                st.info(f"Tarjima: \n\n {res.text}")
                
                if st.button("Sharhlab beraymi?"):
                    with st.spinner('Sharhlanmoqda...'):
                        res_sh = model.generate_content(f"Ushbu matnni grammatik va ma'noviy sharhla: {st.session_state['arab_text']}")
                        st.warning(f"Sharh: \n\n {res_sh.text}")

elif not api_key and uploaded_file:
    st.warning("Iltimos, avval chap tarafdagi menyuga API kalitingizni kiriting.")
