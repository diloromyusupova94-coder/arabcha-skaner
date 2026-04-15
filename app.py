import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

st.title("📝 Arabcha Matn Tahlilchisi")

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    # Google API'ni eng yangi standart bo'yicha sozlaymiz
    genai.configure(api_key=api_key)
    # Modelni versiyasiz, to'g'ridan-to'g'ri chaqiramiz
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi!")
    st.stop()

uploaded_file = st.file_uploader("Rasmni yuklang", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Tahlil qilish"):
        with st.spinner('AI ulanmoqda...'):
            try:
                # generate_content funksiyasini eng sodda ko'rinishda ishlatamiz
                response = model.generate_content(["Ushbu rasmdagi arabcha matnni o'qing va tahlil qiling", image])
                st.write(response.text)
            except Exception as e:
                # Agar yana 404 chiqsa, demak Google sizning kalitingizni hali aktivlashtirmagan
                st.error(f"Xatolik yuz berdi: {e}")
                st.info("Maslahat: Google AI Studio-da yangi 'Project' ochib, yangi kalit olib ko'ring.")
