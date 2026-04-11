import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Sahifa dizayni
st.set_page_config(page_title="Arabcha Skaner", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")

# 2. API Kalitni Railway'dan olish
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    # v1beta xatosini yo'qotish uchun majburiy sozlama
    genai.configure(api_key=api_key)
    # Eng barqaror modelni tanlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Railway Variables bo'limida API kalit topilmadi!")
    st.info("Railway panelida 'Variables' bo'limiga kiring va GEMINI_API_KEY qo'shing.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Rasmni yuklang (JPG, PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlashni boshlash"):
        with st.spinner('AI ulanmoqda va tahlil qilyapti...'):
            try:
                # Rasmni AIga tushunarli formatga o'tkazamiz
                prompt = "Ushbu rasmdagi arabcha matnni aniqlang, o'zbekchaga tarjima qiling va qisqacha grammatik tahlil bering."
                response = model.generate_content([prompt, image])
                
                st.success("Tahlil tayyor!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error("Xatolik yuz berdi.")
                st.info(f"Tizim xabari: {e}")
