import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Arabcha Skaner AI", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Eng barqaror modelni tanlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Secrets-da API kalit topilmadi!")
    st.stop()

uploaded_file = st.file_uploader("Rasmni yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Skanerlash"):
        # Yuklanish jarayoni boshlanganini aniq ko'rsatamiz
        placeholder = st.empty()
        placeholder.info("AI matnni tahlil qilyapti, iltimos kuting (30 soniyagacha vaqt olishi mumkin)...")
        
        try:
            # So'rov yuborish
            prompt = "Rasmdagi arabcha matnni aniq ko'chirib yozing va o'zbekchaga tarjima qiling."
            response = model.generate_content([prompt, image])
            
            # Agar javob kelsa, spinerni o'chirib natijani chiqaramiz
            placeholder.empty()
            st.success("Tahlil yakunlandi!")
            st.write(response.text)
            
        except Exception as e:
            placeholder.empty()
            st.error(f"Kutilmagan xatolik: {e}")
            st.info("Agar bu holat uzoq davom etsa, Google AI Studio-dan yangi kalit olib ko'ring.")
