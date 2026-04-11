import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa dizayni
st.set_page_config(page_title="Arabcha Skaner AI", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")
st.write("Har qanday rasm yuklang, AI uning ustida tahlil o'tkazadi.")

# 2. API Kalitni sozlash
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
            try:
                # ISHLAYDIGAN MODELNI AVTOMATIK ANIQLASH (404 xatosiga barham beradi)
                # Tizimda mavjud bo'lgan birinchi ishlaydigan modelni oladi
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not model_list:
                    st.error("Sizning kalitingiz uchun birorta ham model topilmadi.")
                else:
                    # Ro'yxatdagi eng yaxshisini tanlash
                    chosen_model_name = model_list[0] 
                    model = genai.GenerativeModel(chosen_model_name)
                    
                    prompt = "Ushbu rasmdagi arabcha matnni o'qing, i'robini ko'rsating, o'zbekchaga tarjima qiling va grammatik tahlil qiling."
                    response = model.generate_content([prompt, image])
                    
                    st.success(f"Aniqlangan model: {chosen_model_name}")
                    st.markdown("---")
                    st.write(response.text)
                    
            except Exception as e:
                st.error("Ulanishda xatolik yuz berdi.")
                st.info(f"Tafsilot: {e}")

st.divider()
st.caption("Ilova filologik va matniy tadqiqotlar uchun mo'ljallangan.")
