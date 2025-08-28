import streamlit as st
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator

# Initialize OCR reader
reader = easyocr.Reader(['en'])

st.title("Image to Translated Text App")

uploaded_file = st.file_uploader("Upload an image with text", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # OCR extraction
    with st.spinner("Extracting text..."):
        results = reader.readtext(uploaded_file, detail=0)
        extracted_text = " ".join(results)

    if extracted_text.strip():
        st.subheader("Extracted Text:")
        st.write(extracted_text)

        # Translation
        target_lang = st.selectbox(
            "Translate to:",
            ["zh-CN", "ms", "fr", "de", "ja", "ko", "es"],
            index=0
        )

        translated_text = GoogleTranslator(source="en", target=target_lang).translate(extracted_text)

        st.subheader("Translated Text:")
        st.write(translated_text)
    else:
        st.error("❌ No text could be extracted from the image.")
