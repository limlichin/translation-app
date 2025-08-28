import streamlit as st
import easyocr
from deep_translator import GoogleTranslator
from PIL import Image
import io

st.title("🌍 Image Text Translator")

# Step 1: Language selection (before image upload)
st.subheader("Step 1: Select Target Language")

# 💡 Supported Languages
language_options = {
    "ID": "Bahasa Indonesia",
    "MS": "Bahasa Melayu",
    "TH": "Thai",
    "VI": "Vietnamese",
    "ZH": "Simplified Chinese",
    "JA": "Japanese",
    "KO": "Korean"
}
target_lang = st.selectbox(
    "Choose the target language:",
    options=list(language_options.keys()),
    format_func=lambda x: f"{x} - {language_options[x]}"
)

# Step 2: Upload image
st.subheader("Step 2: Upload Image")
uploaded_file = st.file_uploader("Upload an image containing text", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image properly with PIL
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Step 3: OCR
    st.subheader("Step 3: Extracted Text")
    reader = easyocr.Reader(['en'])  # we assume English text only
    results = reader.readtext(np.array(image))

    extracted_text = " ".join([res[1] for res in results])
    st.write("**Detected Text:**")
    st.write(extracted_text)

    # Step 4: Translation
    if extracted_text.strip():
        st.subheader("Step 4: Translated Text")
        try:
            translated = GoogleTranslator(source='en', target=target_lang.lower()).translate(extracted_text)
            st.success(f"**Translation ({language_options[target_lang]}):**")
            st.write(translated)
        except Exception as e:
            st.error(f"Translation failed: {str(e)}")
