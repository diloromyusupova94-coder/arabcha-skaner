import streamlit as st
import google.generativeai as genai
from PIL import Image

# Sahifa sozlamalari
st.set_page_config(page_title="Arabcha Skaner AI", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri")
st.info("Al-Xorazmiy asarlari va arabcha matnlarni tahlil qilish tizimi.")

# API sozlash
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Eng barqaror model nomini tanlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

# Fayl yuklash
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash va Tahlil qilish"):
        with st.spinner('AI matnni o‘qimoqda va tahlil qilmoqda...'):
            try:
                # Promptni o'zbek va ingliz tillarida beramiz (aniqlik uchun)
                prompt = """
                1. Extract the Arabic text from this image with full diacritics (tashkeel).
                2. Provide an Uzbek translation.
                3. Briefly explain the grammatical structure (Nahv).
                Please format the response clearly in Uzbek.
                """
                response = model.generate_content([prompt, image])
                
                st.success("Tahlil yakunlandi!")
                st.markdown("### 📝 Natija:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")
                st.info("Maslahat: API kalitni Google AI Studio'dan yangilab ko'ring.")
