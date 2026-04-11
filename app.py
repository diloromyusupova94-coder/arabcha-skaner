import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Ilova ko'rinishi
st.set_page_config(page_title="Arabcha Skaner AI", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")
st.write("Istalgan arabcha matnli rasm yuklang.")

# 2. API Kalitni ulash
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # DIQQAT: 404 xatosini yopish uchun model nomini o'zgartirdik
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Rasmni yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Matnni aniqlash"):
        with st.spinner('AI ishlamoqda...'):
            try:
                # Vazifani inglizcha beramiz (AI inglizchada yaxshiroq tushunadi)
                prompt = "Please read the Arabic text in this image, provide it with vowels (tashkeel), translate it into Uzbek, and explain the grammar briefly."
                response = model.generate_content([prompt, image])
                
                st.success("Bajarildi!")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                # Agar yana 404 bersa, eng oxirgi chora: model nomini o'zgartirish
                st.error("Ulanishda xatolik. API kalitingiz Google AI Studio'da 'Pay-as-you-go' emas, 'Free' ekanini tekshiring.")
                st.info(f"Tizim xabari: {e}")

st.divider()
st.caption("Ilova barcha turdagi arabcha matnlarni (gazeta, kitob, qo'lyozma) tahlil qila oladi.")
