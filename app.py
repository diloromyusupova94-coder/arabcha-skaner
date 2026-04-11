import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Sahifa sozlamalari
st.set_page_config(page_title="Arabcha Matn Skaneri", page_icon="📖")
st.title("📖 Arabcha Matn Skaneri va Tarjimon")
st.caption("Rasm yuklang → Matnni skanerlaydi → O'zbekchaga tarjima qiladi")

# API sozlash
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ API kalit topilmadi! Streamlit Secrets ga GEMINI_API_KEY qo'shing.")
    st.code('[secrets]\nGEMINI_API_KEY = "AIza..."', language="toml")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def load_model():
    return genai.GenerativeModel('gemini-2.0-flash')

model = load_model()

# Session state boshlash
if "result" not in st.session_state:
    st.session_state.result = None

# Fayl yuklash
uploaded_file = st.file_uploader(
    "📷 Arabcha matnli rasm yuklang",
    type=['jpg', 'jpeg', 'png', 'webp'],
    help="Kitob, hujjat, yozuv rasmlari qo'llaniladi"
)

if uploaded_file is not None:
    # Faylni o'qib olish
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()

    # Rasmni ochish
    image = Image.open(io.BytesIO(file_bytes))

    # RGB ga o'tkazish
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Rasmni ko'rsatish
    st.image(image, caption="Yuklangan rasm", use_container_width=True)
    st.success(f"✅ Rasm yuklandi: {uploaded_file.name}")

    # Sozlamalar
    target_lang = st.selectbox(
        "🌐 Tarjima tili:",
        ["O'zbek tili", "Rus tili", "Ingliz tili"]
    )

    do_analysis = st.checkbox("🔍 Grammatika tahlili", value=True)

    # Tugma
    if st.button("🚀 Skanerlash va Tahlil", type="primary", use_container_width=True):
        st.session_state.result = None

        # Rasmni JPEG bytes ga o'tkazish
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=95)
        img_bytes = img_buffer.getvalue()

        # To'g'ri image format — PIL Image to'g'ridan uzatish
        prompt = f"""Siz arabcha matn mutaxassisiysiz. Quyidagi vazifalarni bajaring:

1. **ARABCHA MATN (OCR)**: Rasmdagi BARCHA arabcha matnni aynan ko'chirib yozing. Agar arabcha matn yo'q bo'lsa, shuni ayting.

2. **{target_lang.upper()}GA TARJIMA**: Matnni to'liq {target_lang}ga tarjima qiling.

{"3. **GRAMMATIKA TAHLILI**: Asosiy grammatik tuzilmalar va qiziqarli iboralar haqida qisqacha izohlang." if do_analysis else ""}

Javob formati:
---
📜 ARABCHA MATN:
[matn]

🌐 TARJIMA ({target_lang}):
[tarjima]

{"📚 GRAMMATIKA TAHLILI:" + chr(10) + "[tahlil]" if do_analysis else ""}
"""

        with st.spinner("⏳ Gemini tahlil qilmoqda..."):
            try:
                # PIL Image ni to'g'ridan Gemini ga uzatish (eng ishonchli usul)
                response = model.generate_content(
                    [prompt, image],
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.1,
                        max_output_tokens=4096,
                    )
                )
                st.session_state.result = response.text

            except Exception as e:
                st.error(f"❌ Xato turi: {type(e).__name__}")
                st.code(str(e), language="text")
                st.info("💡 API kalitingiz faolligini tekshiring: https://aistudio.google.com")

    # Natijani ko'rsatish
    if st.session_state.result:
        st.markdown("---")
        st.markdown("### 📋 Natija:")
        st.markdown(st.session_state.result)

        st.download_button(
            label="💾 Natijani saqlash (.txt)",
            data=st.session_state.result,
            file_name="arabcha_tarjima.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.info("👆 Yuqoridagi tugmani bosib arabcha matnli rasm yuklang")
    st.session_state.result = None
