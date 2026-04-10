import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha AI Skaner", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri")

# 2. API va Modelni sozlash
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Arabcha rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI matnni o‘qimoqda...'):
            # MODEL NOMLARINI SHU YERDA KETMA-KET SINAB KO'RAMIZ
            model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash']
            
            success = False
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(m_name)
                    prompt = "Extract the Arabic text from this image with all diacritics (tashkeel)."
                    response = model.generate_content([prompt, image])
                    
                    if response.text:
                        st.session_state['arab_text'] = response.text
                        st.success(f"Matn aniqlandi!")
                        success = True
                        break # Agar ishlasa, tsikldan chiqadi
                except Exception:
                    continue # Agar bu nom ishlamasa, keyingisiga o'tadi
            
            if not success:
                st.error("Hech qaysi model ishlamadi. API kalitingizni tekshiring.")

    # 4. Natijalar
    if 'arab_text' in st.session_state:
        st.text_area("Aniqlangan arabcha matn:", st.session_state['arab_text'], height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tarjima qilish"):
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(f"Tarjima qil: {st.session_state['arab_text']}")
                st.info(res.text)
        with col2:
            if st.button("Grammatik tahlil"):
                model = genai.GenerativeModel('gemini-1.5-flash')
                res_sh = model.generate_content(f"Ushbu matnni nahviy tahlil qil: {st.session_state['arab_text']}")
                st.warning(res_sh.text)
