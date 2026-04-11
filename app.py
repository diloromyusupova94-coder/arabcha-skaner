import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

st.set_page_config(page_title="Arabcha Skaner", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")

# Railway'da Environment Variables qismiga GEMINI_API_KEY deb qo'shasiz
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi. Railway sozlamalarini tekshiring.")
    st.stop()

uploaded_file = st.file_uploader("Rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI ishlamoqda...'):
            try:
                prompt = "Ushbu rasmdagi arabcha matnni o'qing, o'zbekchaga tarjima qiling va grammatik tahlil qiling."
                response = model.generate_content([prompt, image])
                st.success("Tayyor!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Xatolik: {e}")
