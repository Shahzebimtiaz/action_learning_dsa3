# import streamlit as st
# import requests

# def main():
#     st.title("Clinical NER Web App")
    
#     st.subheader("Text Input")
#     text_input = st.text_area("Enter clinical text here")
    
#     st.subheader("Image Input")
#     image_file = st.file_uploader("Upload an image containing clinical text", type=["jpg", "png", "jpeg"])
    
#     if image_file is not None:
#         # Process the image for OCR
#         files = {"file": image_file.getvalue()}
#         response = requests.post("https://api-ninjas.com/api/imagetotext", files=files)
#         if response.status_code == 200:
#             st.write("OCR Result:", response.json()["text"])
    
#     if st.button("Run NER Model"):
#         ner_response = requests.post("http://backend:8000/api/v1/ner", json={"text": text_input})
#         st.write("Identified Entities:", ner_response.json())


import streamlit as st
import requests

# URL for the OCR API
  # Update this URL if needed
OCR_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ocr/"
TRANSLATE_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/translate/"
test_api_url = "http://127.0.0.1:8000/api/v1/endpoints/test"

def main():
    st.title("Home Page")

    # Upload Image
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

        # Send the image to OCR API
        if st.button("Recognize Text"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(OCR_API_URL, files=files)
            
            if response.status_code == 200:
                result = response.json().get("text", "No text found")
                st.write("Recognized Text:")
                st.write(result)
            else:
                st.write("Error occurred:", response.text)


    # Translation Feature
    st.subheader("Text Translation")
    text_to_translate = st.text_area("Enter text to translate")
    target_language = st.text_input("Enter target language (e.g., 'es' for Spanish, 'fr' for French)")

    if st.button("Translate"):
        if text_to_translate and target_language:
            try:
                payload = {"text": text_to_translate, "target_language": target_language}
                response = requests.post(TRANSLATE_API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json().get("translated_text", "Translation failed")
                    st.write("Translated Text:")
                    st.write(result)
                else:
                    st.error(f"Failed to translate text. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please enter text and target language")
    
