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
    st.error("❌ API kalit topilmadi! Streamlit Secrets'ga GEMINI_API_KEY qo'shing.")
    st.code('[secrets]\nGEMINI_API_KEY = "AIza..."', language="toml")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Model — gemini-2.0-flash yangi va tezroq
@st.cache_resource
def load_model():
    return genai.GenerativeModel('gemini-2.0-flash')

model = load_model()

# Fayl yuklash
uploaded_file = st.file_uploader(
    "📷 Arabcha matnli rasm yuklang",
    type=['jpg', 'jpeg', 'png', 'webp'],
    help="Kitob, hujjat, yozuv rasmlari qo'llaniladi"
)

if uploaded_file:
    image = Image.open(uploaded_file)

    # RGB ga o'tkazish (RGBA/palette muammolarini oldini olish)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    st.image(image, caption="Yuklangan rasm", use_container_width=True)

    # Til tanlash
    target_lang = st.selectbox(
        "Tarjima tili:",
        ["O'zbek tili", "Rus tili", "Ingliz tili"]
    )

    col1, col2 = st.columns(2)

    with col1:
        do_ocr = st.checkbox("📝 Matnni ajratib olish", value=True)
    with col2:
        do_analysis = st.checkbox("🔍 Grammatika tahlili", value=True)

    if st.button("🚀 Skanerlash va Tahlil qilish", type="primary"):

        # Rasmni bytes ga o'tkazish
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG', quality=95)
        img_bytes = img_bytes.getvalue()

        # Gemini uchun image part
        image_part = {
            "mime_type": "image/jpeg",
            "data": img_bytes
        }

        # Prompt
        prompt = f"""Siz arabcha matn mutaxassisiysiz. Quyidagi vazifalarni bajaring:

1. **ARABCHA MATN (OCR)**: Rasmdagi BARCHA arabcha matnni aynan ko'chirib yozing. Agar matn yo'q bo'lsa, "Rasm matn topilmadi" deb yozing.

2. **{target_lang.upper()}GA TARJIMA**: Yuqoridagi matnni to'liq {target_lang}ga tarjima qiling. Mazmunini aniq va tushunarli yetkazing.

{"3. **GRAMMATIKA TAHLILI**: Asosiy grammatik tuzilmalar, fe'l zamonlari va qiziqarli iboralar haqida qisqacha izohlang." if do_analysis else ""}

Javobni quyidagi formatda bering:
---
📜 ARABCHA MATN:
[arabcha matn bu yerda]

🌐 TARJIMA:
[tarjima bu yerda]

{"📚 TAHLIL:" + chr(10) + "[tahlil bu yerda]" if do_analysis else ""}
"""

        with st.spinner("⏳ Gemini tahlil qilmoqda..."):
            try:
                response = model.generate_content(
                    [prompt, image_part],
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.1,  # Aniqlik uchun past temperature
                        max_output_tokens=4096,
                    )
                )

                st.success("✅ Muvaffaqiyatli!")
                st.markdown("---")
                st.markdown(response.text)

                # Natijani yuklab olish
                st.download_button(
                    label="💾 Natijani saqlash (.txt)",
                    data=response.text,
                    file_name="arabcha_tarjima.txt",
                    mime="text/plain"
                )

            except genai.types.BlockedPromptException:
                st.error("⚠️ Rasm bloklandi. Boshqa rasm sinab ko'ring.")
            except Exception as e:
                st.error(f"❌ Xato: {type(e).__name__}")
                st.code(str(e))
                st.info("💡 Yechim: Google AI Studio'da API kalitingiz faol ekanligini tekshiring: https://aistudio.google.com")
