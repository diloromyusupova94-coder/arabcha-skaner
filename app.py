import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha Matn Skaneri", page_icon="📝")
st.title("📝 Universal Arabcha Matn Skaneri")

# 2. API Kalitni sozlash (v1beta xatosini yopish uchun)
if "GEMINI_API_KEY" in st.secrets:
    # Google API'ni majburiy ravishda barqaror v1 versiyasiga o'tkazamiz
    os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Modelni chaqirishda 'models/' qo'shimchasini olib tashlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi! Iltimos, Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Tanlangan rasm', use_container_width=True)
    
    if st.button("Skanerlash va Tahlil"):
        with st.spinner('AI barqaror kanal orqali ulanmoqda...'):
            try:
                # Universal vazifa
                prompt = "Ushbu rasmdagi arabcha matnni o'qing, o'zbekchaga tarjima qiling va grammatikasini tahlil qiling."
                response = model.generate_content([prompt, image])
                
                st.success("Muvaffaqiyatli yakunlandi!")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                # Agar yana o'sha xato chiqsa, demak kutubxona versiyasini yangilash kerak
                st.error("Ulanishda texnik muammo.")
                st.info(f"Tizim xabari: {e}")
