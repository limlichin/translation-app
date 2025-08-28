import streamlit as st
import easyocr
from deep_translator import GoogleTranslator
from PIL import Image
import numpy as np

# Title
st.title("Image Text Translator")

# Step 1: Language selection first
st.subheader("Step 1: Choose Translation Language")
target_lang = st.selectbox(
    "Select the language you want to translate to:",
    ["en", "zh-CN", "fr", "de", "es", "ja", "ko", "id", "ms", "th", "vi"],
    index=1  # default to Chinese (zh-CN)
)

# Step 2: Upload image
st.subheader("Step 2: Upload Image")
uploaded_file = st.file_uploader("Upload an image with text", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Step 3: Extract text with EasyOCR
    st.subheader("Step 3: Extract Text from Image")
    reader = easyocr.Reader(["en"], gpu=False)  # English only
    results = reader.readtext(np.array(image))

    extracted_text = "\n".join([res[1] for res in results])
    st.text_area("Extracted Text (English)", extracted_text, height=150)

    # Step 4: Translate
    if extracted_text.strip():
        st.subheader("Step 4: Translated Text")
        try:
            translated_text = GoogleTranslator(source="auto", target=target_lang).translate(extracted_text)
            st.text_area("Translated Text", translated_text, height=150)

            # Optional: download translated text
            st.download_button(
                label="Download Translation",
                data=translated_text,
                file_name="translation.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Translation failed: {e}")
