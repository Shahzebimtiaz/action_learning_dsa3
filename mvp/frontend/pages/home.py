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
test_api_url = "http://127.0.0.1:8000/api/v1/endpoints/test"

def main():
    st.title("Home Pagee")
    # if st.button("Test Endpoint"):
    #     try:
    #         # Make a GET request to the /test/ endpoint
    #         response = requests.get(f"{test_api_url}")
            
    #         # Check if the request was successful
    #         if response.status_code == 200:
    #             result = response.json()
    #             st.success(f"Success: {result}")
    #         else:
    #             st.error(f"Failed to fetch data. Status code: {response.status_code}")
    #     except Exception as e:
    #         st.error(f"An error occurred: {str(e)}")


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
