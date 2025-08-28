import streamlit as st
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator

# 💡 Supported Languages
LANGUAGES = {
    "ID (Bahasa Indonesia)": "id",
    "MS (Bahasa Melayu)": "ms",
    "TH (Thai)": "th",
    "VI (Vietnamese)": "vi",
    "ZH (Simplified Chinese)": "zh-CN",
    "JA (Japanese)": "ja",
    "KO (Korean)": "ko"
}

st.title("🌏 Shared Translation Tool (POC)")

# Step 1: Language selection
selected_langs = st.multiselect(
    "Select languages to translate into:",
    options=list(LANGUAGES.keys())
)

# Step 2: File uploader
uploaded_file = st.file_uploader(
    "Upload an image (JPG, PNG, JPEG, GIF)", type=["jpg", "png", "jpeg", "gif"]
)

if uploaded_file and selected_langs:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # OCR text extraction (English only)
    extracted_text = pytesseract.image_to_string(image, lang="eng")
    lines = [line.strip() for line in extracted_text.split("\n") if line.strip()]

    if not lines:
        st.warning("⚠️ No text detected in the image.")
    else:
        st.subheader("📋 Translation Table")
        header_cols = ["EN"] + [lang for lang in selected_langs]

        table = []
        for line in lines:
            row = [line]
            for lang in selected_langs:
                try:
                    translation = GoogleTranslator(source="en", target=LANGUAGES[lang]).translate(line)
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
                corrected = st.text_input(
                    f"Corrected {lang}:", value=row[i], key=f"{row[0]}-{lang}"
                )
                if corrected != row[i]:
                    corrections[(row[0], lang)] = corrected

        if corrections:
            st.write("✅ Stored corrections for future use:")
            st.json(corrections)
