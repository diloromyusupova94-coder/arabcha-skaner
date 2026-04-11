import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa dizayni
st.set_page_config(page_title="Arabcha Skaner AI", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")
st.write("Har qanday arabcha rasm yuklang, AI uni tahlil qiladi.")

# 2. API Kalitni tekshirish va sozlash
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("API kalit topilmadi! Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Rasmni yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Matnni aniqlash"):
        with st.spinner('AI ulanmoqda...'):
            # BARCHA MUMKIN BO'LGAN MODEL NOMLARINI KETMA-KET SINAYMIZ
            possible_models = [
                'gemini-1.5-flash', 
                'models/gemini-1.5-flash', 
                'gemini-pro-vision', 
                'models/gemini-pro-vision'
            ]
            
            response = None
            error_message = ""
            
            for m_name in possible_models:
                try:
                    model = genai.GenerativeModel(m_name)
                    prompt = "Ushbu rasmdagi arabcha matnni o'qing, o'zbekchaga tarjima qiling va grammatik tahlil qiling."
                    response = model.generate_content([prompt, image])
                    if response:
                        break # Agar ishlasa, to'xtaydi
                except Exception as e:
                    error_message = str(e)
                    continue # Ishlamasa, keyingisiga o'tadi
            
            if response:
                st.success("Muvaffaqiyatli aniqlandi!")
                st.markdown("---")
                st.write(response.text)
            else:
                st.error("Xatolik yuz berdi. API kalitingiz ushbu modellarni qo'llab-quvvatlamayapti.")
                st.info(f"Tizim xabari: {error_message}")

st.divider()
st.caption("Ilova filologik tahlillar uchun mo'ljallangan.")
