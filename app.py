import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. Sahifa sozlamalari (Dizayn uchun)
st.set_page_config(page_title="Arabcha Skaner Pro", page_icon="📝")
st.title("📝 Arabcha Matn Tahlilchisi")
st.markdown("---")

# 2. API Kalitni Railway'dan olish
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    # Google AI sozlamasi
    genai.configure(api_key=api_key)
    # Eng barqaror model
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Diqqat! API kalit topilmadi. Railway Variables bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash qismi
uploaded_file = st.file_uploader("Arabcha matnli rasmni yuklang", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    # Rasmni ochish va ko'rsatish
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    # Tugma bosilganda AI ishga tushadi
    if st.button("Skanerlash va Tahlil qilish"):
        with st.spinner('AI matnni o‘qimoqda, kuting...'):
            try:
                # AIga yuboriladigan buyruq (Prompt)
                vazifa = "Rasmdagi arabcha matnni aniq ko'chirib yozing, o'zbek tiliga tarjima qiling va qisqacha grammatik tahlil bering."
                
                # Natijani olish
                response = model.generate_content([vazifa, image])
                
                # Natijani ekranga chiqarish
                st.success("Tahlil yakunlandi!")
                st.markdown("### Natija:")
                st.write(response.text)
                
            except Exception as e:
                st.error("Kutilmagan xatolik yuz berdi.")
                st.info(f"Xato xabari: {e}")
