import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time

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

# Model — mavjud modellardan birinchisini ishlatadi
@st.cache_resource
def load_model():
    # Qaysi model mavjud bo'lsa, o'shani ishlatadi
    model_names = [
        "gemini-1.5-flash",
        "gemini-1.0-pro-vision",
        "gemini-pro-vision",
    ]
    try:
        available = [m.name for m in genai.list_models()
                     if 'generateContent' in m.supported_generation_methods]
    except Exception:
        available = []

    for name in model_names:
        full_name = f"models/{name}"
        if not available or full_name in available or name in available:
            try:
                return genai.GenerativeModel(name), name
            except Exception:
                continue

    # Oxirgi fallback
    return genai.GenerativeModel("gemini-1.5-flash"), "gemini-1.5-flash"

model, model_name = load_model()

# Session state
if "result" not in st.session_state:
    st.session_state.result = None

# Retry funksiyasi
def generate_with_retry(prompt, image, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                [prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=4096,
                )
            )
            return response.text, None

        except Exception as e:
            error_str = str(e)

            if "429" in error_str or "ResourceExhausted" in error_str or "Quota" in error_str:
                wait_time = 30 * (attempt + 1)
                if attempt < max_retries - 1:
                    st.warning(f"⏳ API limiti to'ldi. {wait_time} soniya kutilmoqda... ({attempt+1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    return None, "quota"

            return None, error_str

    return None, "Maksimal urinishlar soni tugadi."

# Fayl yuklash
uploaded_file = st.file_uploader(
    "📷 Arabcha matnli rasm yuklang",
    type=['jpg', 'jpeg', 'png', 'webp'],
    help="Kitob, hujjat, yozuv rasmlari qo'llaniladi"
)

if uploaded_file is not None:
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()

    image = Image.open(io.BytesIO(file_bytes))
    if image.mode != 'RGB':
        image = image.convert('RGB')

    st.image(image, caption="Yuklangan rasm", use_container_width=True)
    st.success(f"✅ Rasm yuklandi: {uploaded_file.name}")

    target_lang = st.selectbox(
        "🌐 Tarjima tili:",
        ["O'zbek tili", "Rus tili", "Ingliz tili"]
    )

    do_analysis = st.checkbox("🔍 Grammatika tahlili", value=True)

    if st.button("🚀 Skanerlash va Tahlil", type="primary", use_container_width=True):
        st.session_state.result = None

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

        with st.spinner(f"⏳ {model_name} tahlil qilmoqda..."):
            result, error = generate_with_retry(prompt, image)

        if result:
            st.session_state.result = result
        elif error == "quota":
            st.error("❌ API limiti to'ldi. Bir oz kuting va qayta urining.")
            st.markdown("💡 Yangi API kalit: [Google AI Studio](https://aistudio.google.com/apikey)")
        else:
            st.error(f"❌ Xato: {error}")

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
