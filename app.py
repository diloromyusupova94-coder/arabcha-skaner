import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

st.set_page_config(page_title="Arabcha Skaner")
st.title("📝 Arabcha Matn Tahlilchisi")

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    # Bu safar faqat v1 barqaror versiyani sinaymiz
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi!")
    st.stop()

uploaded_file = st.file_uploader("Rasmni yuklang", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('Tahlil qilinmoqda...'):
            try:
                # Rasmni yuborishning eng sodda usuli
                response = model.generate_content(["Ushbu arabcha matnni o'qing va tahlil qiling", image])
                st.success("Bajarildi!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Google xatosi: {e}")
