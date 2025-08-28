import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from deep_translator import GoogleTranslator
import pandas as pd
import io

# 💡 Supported Languages
LANGUAGES = {
    "Bahasa Indonesia (ID)": "id",
    "Bahasa Melayu (MS)": "ms",
    "Thai (TH)": "th",
    "Vietnamese (VI)": "vi",
    "Simplified Chinese (ZH)": "zh-CN",
    "Japanese (JA)": "ja",
    "Korean (KO)": "ko"
}

st.set_page_config(page_title="🌏 Shared Translation Tool", layout="wide")
st.title("🌏 Shared Translation Tool (POC)")

# Step 1: Language selection first
selected_langs = st.multiselect(
    "Select languages to translate into:",
    options=list(LANGUAGES.keys())
)

# Step 2: Image uploader
uploaded_file = st.file_uploader(
    "Upload an image (JPG, PNG, JPEG, GIF)", type=["jpg", "png", "jpeg", "gif"]
)

def preprocess_image(img: Image.Image) -> Image.Image:
    # Convert to grayscale
    img = img.convert("L")
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    # Optional: apply sharpening filter
    img = img.filter(ImageFilter.SHARPEN)
    # Resize if very large
    max_size = (1200, 1200)
    img.thumbnail(max_size, Image.ANTIALIAS)
    return img

if uploaded_file and selected_langs:
    image = Image.open(uploaded_file)
    image = preprocess_image(image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # OCR text extraction
    extracted_text = pytesseract.image_to_string(image, lang="eng")
    lines = [line.strip() for line in extracted_text.split("\n") if line.strip()]

    if not lines:
        st.warning("⚠️ No text detected in the image.")
    else:
        st.subheader("📋 Translation Table")

        # Build header
        header_cols = ["EN"] + [lang for lang in selected_langs]
        table_rows = []

        for line in lines:
            row = [line]
            for lang in selected_langs:
                try:
                    translation = GoogleTranslator(source="en", target=LANGUAGES[lang]).translate(line)
                    row.append(translation)
                except Exception:
                    row.append("⚠️ Translation failed")
            table_rows.append(row)

        # Scrollable table using Pandas + Streamlit
        df = pd.DataFrame(table_rows, columns=header_cols)
        st.dataframe(df, height=400)  # scrollable

        # Bonus: Correction input
        st.subheader("✍️ Provide Corrected Translations")
        corrections = {}
        for idx, row in df.iterrows():
            st.markdown(f"**Original (EN):** {row['EN']}")
            for lang in selected_langs:
                corrected = st.text_input(
                    f"Corrected {lang}:", value=row[lang], key=f"{row['EN']}-{lang}"
                )
                if corrected != row[lang]:
                    corrections[(row['EN'], lang)] = corrected

        if corrections:
            st.write("✅ Stored corrections for future use:")
            st.json(corrections)
