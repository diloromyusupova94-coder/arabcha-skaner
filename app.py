import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Arabcha AI Skaner", page_icon="🌙")
st.title("🌙 Arabcha Matn Skaneri va Sharhlovchi")
st.write("Rasm yuklang, matnni aniqlaymiz va sharhlaymiz.")

# 2. Xavfsiz API kalitni Secrets'dan olish
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    try:
        genai.configure(api_key=api_key)
        # Model nomini to'liq yo'l bilan ko'rsatamiz (xatolikni oldini olish uchun)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except Exception as e:
        st.error(f"API konfiguratsiyada xato: {e}")
        st.stop()
else:
    st.error("API kalit topilmadi. Iltimos, Streamlit Settings -> Secrets bo'limiga kalitni qo'shing.")
    st.stop()

# 3. Fayl yuklash qismi
uploaded_file = st.file_uploader("Arabcha matnli rasm yuklang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Skanerlash"):
        with st.spinner('AI matnni o‘qimoqda...'):
            try:
                # AI uchun aniq vazifa (prompt)
                prompt = "Ushbu rasmdagi arabcha matnni aniq, harakatlari (i'rob) bilan tering. Faqat arabcha matnni o'zini qaytaring."
                response = model.generate_content([prompt, image])
                
                # Natijani saqlash
                st.session_state['arab_text'] = response.text
                st.success("Matn muvaffaqiyatli aniqlandi!")
                st.text_area("Aniqlangan arabcha matn:", st.session_state['arab_text'], height=200)
            except Exception as e:
                st.error(f"Skanerlashda xatolik yuz berdi: {e}")

    # 4. Tarjima va Sharh bo'limi
    if 'arab_text' in st.session_state:
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("O‘zbekchaga tarjima qilish"):
                with st.spinner('Tarjima qilinmoqda...'):
                    res = model.generate_content(f"Ushbu arabcha matnni o'zbek tiliga tarjima qil: {st.session_state['arab_text']}")
                    st.info(f"**Tarjima:**\n\n{res.text}")
        
        with col2:
            if st.button("Grammatik sharhlash"):
                with st.spinner('Tahlil qilinmoqda...'):
                    res_sh = model.generate_content(f"Ushbu arabcha matnni nahv va sarf qoidalari bo'yicha grammatik tahlil qiling va ma'nosini sharhlang: {st.session_state['arab_text']}")
                    st.warning(f"**Sharh:**\n\n{res_sh.text}")
