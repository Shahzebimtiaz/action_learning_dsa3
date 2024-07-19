import streamlit as st
import requests

def main():
    st.title("Clinical NER Web App")
    
    st.subheader("Text Input")
    text_input = st.text_area("Enter clinical text here")
    
    st.subheader("Image Input")
    image_file = st.file_uploader("Upload an image containing clinical text", type=["jpg", "png", "jpeg"])
    
    if image_file is not None:
        # Process the image for OCR
        files = {"file": image_file.getvalue()}
        response = requests.post("https://api-ninjas.com/api/imagetotext", files=files)
        if response.status_code == 200:
            st.write("OCR Result:", response.json()["text"])
    
    if st.button("Run NER Model"):
        ner_response = requests.post("http://backend:8000/api/v1/ner", json={"text": text_input})
        st.write("Identified Entities:", ner_response.json())

