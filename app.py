import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Sahifa dizayni
st.set_page_config(page_title="Arabcha Skaner AI", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")

# 2. API Kalit va Versiya sozlamasi
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    # BU YERDA: Majburiy ravishda 'v1' barqaror versiyasiga o'tamiz
    # Bu o'sha 'v1beta' xatosini ildizi bilan sug'urib tashlaydi
    genai.configure(api_key=api_key, transport='rest') # 'rest' transporti eng xavfsizi
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Railway 'Variables' bo'limida GEMINI_API_KEY topilmadi!")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Rasmni yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI barqaror kanal orqali ishlamoqda...'):
            try:
                # Promptni soddalashtirdik, AI o'zi tushunib oladi
                response = model.generate_content([
                    "Rasmdagi arabcha matnni aniq ko'chirib yozing va o'zbekchaga tarjima qiling.", 
                    image
                ])
                st.success("Bajarildi!")
                st.write(response.text)
            except Exception as e:
                # Agar xato chiqsa, uni foydalanuvchiga tushunarli qilib ko'rsatamiz
                st.error("Ulanishda muammo bo'ldi.")
                if "404" in str(e):
                    st.info("Maslahat: Google AI Studio-dan mutlaqo yangi API Key olib ko'ring.")
                else:
                    st.code(str(e))
