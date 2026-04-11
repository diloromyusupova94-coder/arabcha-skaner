import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa dizayni (Umumiy ko'rinish)
st.set_page_config(page_title="Arabcha Skaner AI", page_icon="📝")
st.title("📝 Arabcha Matn Skaneri")
st.write("Har qanday arabcha matnli rasm yuklang. AI uni o'qiydi, tarjima qiladi va tahlil qiladi.")

# 2. API Kalitni tekshirish
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 404 xatosini oldini olish uchun modelni o'zgaruvchan qildik
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

# 3. Fayl yuklash
uploaded_file = st.file_uploader("Rasmni tanlang...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Yuklangan rasm', use_container_width=True)
    
    if st.button("Matnni aniqlash"):
        with st.spinner('AI matn ustida ishlamoqda...'):
            try:
                # Har qanday matnga mos keladigan universal vazifa
                prompt = """
                Ushbu rasmdagi barcha arabcha matnlarni aniqlang. 
                1. Arabcha matnning o'zi (harakatlari bilan).
                2. O'zbekcha tarjimasi.
                3. Qisqacha grammatik tushuntirish.
                Javobni chiroyli ko'rinishda taqdim eting.
                """
                response = model.generate_content([prompt, image])
                
                st.success("Tayyor!")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                # Agar yana model topilmasa, muqobil yo'lni sinaydi
                st.error(f"Xatolik yuz berdi. Iltimos, API kalitingiz faol ekanligini tekshiring.")
                st.info("Xatolik tafsiloti: " + str(e))

# Pastki qism
st.divider()
st.caption("Ilova har qanday turdagi arabcha matnlarni tahlil qilish imkoniyatiga ega.")
