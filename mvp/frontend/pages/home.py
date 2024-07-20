import streamlit as st
import requests

# URLs for the APIs
OCR_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ocr/"
TRANSLATE_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/translate/"
NER_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ner/"

def main():
    st.title("Home Page")

    # Initialize session state variables
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

    # Start Over Button
    if st.button("Start Over"):
        st.session_state.recognized_text = ""
        st.rerun()

    st.subheader("Upload and Process File")
    upload_option = st.radio("Choose an option", ("Upload Image for OCR", "Upload Text File", "Enter Text for Translation"))

    if upload_option == "Upload Image for OCR":
        uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)

            if st.button("Recognize Text"):
                files = {"file": uploaded_image.getvalue()}
                response = requests.post(OCR_API_URL, files=files)
                if response.status_code == 200:
                    st.session_state.recognized_text = response.json().get("text", "No text found")
                    st.write("Recognized Text:")
                    st.write(st.session_state.recognized_text)
                else:
                    st.write("Error occurred:", response.text)

    elif upload_option == "Upload Text File":
        uploaded_text_file = st.file_uploader("Choose a text file", type=["txt"])
        if uploaded_text_file is not None:
            if uploaded_text_file.name.endswith(".txt"):
                text_content = uploaded_text_file.read().decode("utf-8")
                st.session_state.recognized_text = text_content
                st.write("Uploaded Text File Content:")
                st.write(st.session_state.recognized_text)
            else:
                st.error("Please upload a file in .txt format")

    elif upload_option == "Enter Text for Translation":
        st.subheader("Text Translation")
        text_to_translate = st.text_area("Enter text to translate")
        #target_language = st.text_input("Enter target language (e.g., 'es' for Spanish, 'fr' for French)")

        # Dropdown for source language
        source_language = st.selectbox("Select source language", ["en", "fr"])
        # Determine target language based on source language
        target_language = "fr" if source_language == "en" else "en"
        st.write(f"Target language is set to: {target_language}")

        if st.button("Translate"):
            if text_to_translate:
                try:
                    payload = {"text": text_to_translate, "source_language": source_language, "target_language": target_language}
                    response = requests.post(TRANSLATE_API_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.recognized_text = response.json().get("translated_text", "Translation failed")
                        st.write("Translated Text:")
                        st.write(st.session_state.recognized_text)
                    else:
                        st.error(f"Failed to translate text. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.error("Please enter text to translate")

    # Run NER button, sending the recognized text to the model
    if st.session_state.recognized_text:
        if st.button("Run NER"):
            try:
                response = requests.post(NER_API_URL, json={"text": st.session_state.recognized_text})
                if response.status_code == 200:
                    ner_result = response.json()
                    st.write("NER Result:")
                    st.write(ner_result)
                else:
                    st.error(f"Failed to run NER. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
