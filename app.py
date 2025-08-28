import streamlit as st
import easyocr
from deep_translator import GoogleTranslator
from PIL import Image

# 💡 Supported Languages
LANGUAGES = {
    "Bahasa Indonesia 🇮🇩": "id",
    "Bahasa Melayu 🇲🇾": "ms",
    "Thai 🇹🇭": "th",
    "Vietnamese 🇻🇳": "vi",
    "Simplified Chinese 🇨🇳": "zh-CN",
    "Japanese 🇯🇵": "ja",
    "Korean 🇰🇷": "ko"
}

st.title("🌏 Shared Translation Tool (POC)")

# Step 1: Language selection (multi-select)
selected_langs = st.multiselect(
    "Select target languages:",
    options=list(LANGUAGES.keys())
)

# Step 2: File uploader
uploaded_file = st.file_uploader("Upload an image (JPG, PNG, JPEG, GIF)", type=["jpg", "jpeg", "png", "gif"])

if uploaded_file and selected_langs:
    # Convert to PIL image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # OCR with EasyOCR (English only)
    reader = easyocr.Reader(['en'])
    ocr_results = reader.readtext(image)
    lines = [text for _, text, _ in ocr_results]

    if not lines:
        st.warning("⚠️ No text detected in the image.")
    else:
        st.subheader("📋 Translation Table")
        header_cols = ["EN"] + [lang.split()[0] for lang in selected_langs]
        table = []

        for line in lines:
            row = [line]
            for lang in selected_langs:
                try:
                    translation = GoogleTranslator(source='en', target=LANGUAGES[lang]).translate(line)
                    row.append(translation)
                except Exception:
                    row.append("⚠️ Translation failed")
            table.append(row)

        st.table([header_cols] + table)

        # Bonus: correction input
        st.subheader("✍️ Provide Corrected Translations")
        corrections = {}
        for row in table:
            st.markdown(f"**Original (EN):** {row[0]}")
            for i, lang in enumerate(selected_langs, start=1):
                corrected = st.text_input(f"Corrected {lang}:", value=row[i], key=f"{row[0]}-{lang}")
                if corrected != row[i]:
                    corrections[(row[0], lang)] = corrected

        if corrections:
            st.write("✅ Stored corrections for future use:")
            st.json(corrections)
