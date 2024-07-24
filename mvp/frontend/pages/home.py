# import streamlit as st
# import requests

# # URLs for the APIs
# OCR_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ocr/"
# TRANSLATE_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/translate/"
# NER_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ner/"
# LOG_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/log_user_activity/"

# def main():
#     st.title("Home Page")

#     # Initialize session state variables
#     if 'recognized_text' not in st.session_state:
#         st.session_state.recognized_text = ""

#     # Start Over Button
#     if st.button("Start Over"):
#         st.session_state.recognized_text = ""
#         st.rerun()

#     st.subheader("Upload and Process File")
#     upload_option = st.radio("Choose an option", ("Upload Image for OCR", "Upload Text File", "Enter Text for Translation"))

#     if upload_option == "Upload Image for OCR":
#         uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
#         if uploaded_image is not None:
#             st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)

#             if st.button("Recognize Text"):
#                 files = {"file": uploaded_image.getvalue()}
#                 response = requests.post(OCR_API_URL, files=files)
#                 if response.status_code == 200:
#                     st.session_state.recognized_text = response.json().get("text", "No text found")
#                     st.write("Recognized Text:")
#                     st.write(st.session_state.recognized_text)
#                 else:
#                     st.write("Error occurred:", response.text)

#     elif upload_option == "Upload Text File":
#         uploaded_text_file = st.file_uploader("Choose a text file", type=["txt"])
#         if uploaded_text_file is not None:
#             if uploaded_text_file.name.endswith(".txt"):
#                 text_content = uploaded_text_file.read().decode("utf-8")
#                 st.session_state.recognized_text = text_content
#                 st.write("Uploaded Text File Content:")
#                 st.write(st.session_state.recognized_text)
#             else:
#                 st.error("Please upload a file in .txt format")

#     elif upload_option == "Enter Text for Translation":
#         st.subheader("Text Translation")
#         text_to_translate = st.text_area("Enter text to translate")
#         #target_language = st.text_input("Enter target language (e.g., 'es' for Spanish, 'fr' for French)")

#         # Dropdown for source language
#         source_language = st.selectbox("Select source language", ["en", "fr"])
#         # Determine target language based on source language
#         target_language = "fr" if source_language == "en" else "en"
#         st.write(f"Target language is set to: {target_language}")

#         if st.button("Translate"):
#             if text_to_translate:
#                 try:
#                     payload = {"text": text_to_translate, "source_language": source_language, "target_language": target_language}
#                     response = requests.post(TRANSLATE_API_URL, json=payload)
#                     if response.status_code == 200:
#                         st.session_state.recognized_text = response.json().get("translated_text", "Translation failed")
#                         st.write("Translated Text:")
#                         st.write(st.session_state.recognized_text)
#                     else:
#                         st.error(f"Failed to translate text. Status code: {response.status_code}")
#                 except Exception as e:
#                     st.error(f"An error occurred: {str(e)}")
#             else:
#                 st.error("Please enter text to translate")

#     # Run NER button, sending the recognized text to the model
#     if st.session_state.recognized_text:
#         if st.button("Run NER"):
#             try:
#                 response = requests.post(NER_API_URL, json={"text": st.session_state.recognized_text})
#                 if response.status_code == 200:
#                     ner_result = response.json()
#                     st.write("NER Result:")
#                     st.write(ner_result)
#                 else:
#                     st.error(f"Failed to run NER. Status code: {response.status_code}")
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import json
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import io
import time
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import numpy as np
import speech_recognition as sr
import threading
import asyncio
import websockets


# URLs for the APIs
OCR_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ocr/"
TRANSLATE_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/translate/"
NER_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/ner/"
LOG_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/log_user_activity/"  # New log endpoint
FEEDBACK_API_URL = "http://127.0.0.1:8000/api/v1/endpoints/feedback/"

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_data = np.array([], dtype=np.int16)
        self.result = ""
        self.lock = threading.Lock()

    def recv(self, frame: av.AudioFrame):
        audio = frame.to_ndarray()
        with self.lock:
            self.audio_data = np.concatenate((self.audio_data, audio))
            if len(self.audio_data) > frame.sample_rate * 10:  # keep only last 10 seconds
                self.audio_data = self.audio_data[-frame.sample_rate * 10:]
        return frame

    def recognize(self):
        with self.lock:
            if len(self.audio_data) == 0:
                return
            audio_data = sr.AudioData(self.audio_data.tobytes(), 16000, 1)
            try:
                self.result = self.recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                self.result = "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                self.result = f"Could not request results from Google Speech Recognition service; {e}"



# class AudioProcessor(AudioProcessorBase):
#     def __init__(self):
#         self.recognizer = sr.Recognizer()
#         self.result = ""

#     def recv(self, frame: av.AudioFrame):
#         audio_data = np.frombuffer(frame.to_ndarray(), np.int16)
#         audio_data = sr.AudioData(audio_data.tobytes(), frame.sample_rate, 2)  # Assuming 16-bit PCM
#         try:
#             self.result = self.recognizer.recognize_google(audio_data)
#         except sr.UnknownValueError:
#             self.result = "Google Speech Recognition could not understand audio"
#         except sr.RequestError as e:
#             self.result = f"Could not request results from Google Speech Recognition service; {e}"
#         return frame


def log_activity(user_id, activity_type, detail, source_language=None):
    payload = {
        "user_id": user_id,
        "activity_type": activity_type,
        "detail": detail,
        "source_language": source_language
    }
    requests.post(LOG_API_URL, json=payload)

    # def submit_feedback(original_text, feedback):
    #     payload = {
    #         "original_text": original_text,
    #         "feedback": feedback
    #     }
    #     response = requests.post(FEEDBACK_API_URL, json=payload)
    #     if response.status_code == 200:
    #         st.success("Feedback submitted successfully!")
    #     else:
    #         st.error(f"Failed to submit feedback. Status code: {response.status_code}")


def main():
    st.title("Home Page")
    
    # Simulate a user_id for demonstration purposes
    user_id = 1


    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

    if 'feedback_text' not in st.session_state:
        st.session_state.feedback_text = ""

    if 'recording' not in st.session_state:
        st.session_state.recording = False

    if 'start_time' not in st.session_state:
        st.session_state.start_time = None


    st.subheader("Upload and Process File")
    upload_option = st.radio("Choose an option", 
                             ("Upload Image for OCR", 
                              "Direct Text Input",
                              "Upload Text File", 
                              "Enter Text for Translation"))

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
                    log_activity(user_id, 
                                 "Recognize Text", 
                                 f"Image: {uploaded_image.name}",
                                 '')
                else:
                    st.write("Error occurred:", response.text)

    elif upload_option == "Direct Text Input":
        st.subheader("Direct Text Input")
        direct_text = st.text_area("Enter your text here")

        if st.button("Submit Text"):
            if direct_text:
                st.session_state.recognized_text = direct_text
                st.write("Entered Text:")
                st.write(st.session_state.recognized_text)
                log_activity(user_id, 
                             "Direct Text Input", 
                             f"Text: {direct_text}")
            else:
                st.error("Please enter some text")

    elif upload_option == "Upload Text File":
        uploaded_text_file = st.file_uploader("Choose a text file", type=["txt"])
        if uploaded_text_file is not None:
            if uploaded_text_file.name.endswith(".txt"):
                text_content = uploaded_text_file.read().decode("utf-8")
                st.session_state.recognized_text = text_content
                st.write("Uploaded Text File Content:")
                st.write(st.session_state.recognized_text)
                log_activity(user_id, 
                             "Upload Text File", 
                             f"File: {uploaded_text_file.name}")
            else:
                st.error("Please upload a file in .txt format")

    elif upload_option == "Enter Text for Translation":
        st.subheader("Text Translation")
        text_to_translate = st.text_area("Enter text to translate")

        source_language = st.selectbox("Select source language", ["fr", "es"])
        target_language = "en"
        #target_language = "fr" if source_language == "en" else "en"
        st.write(f"Target language is: {target_language}")

        if st.button("Translate"):
            if text_to_translate:
                try:
                    payload = {"text": text_to_translate, "source_language": source_language, "target_language": target_language}
                    response = requests.post(TRANSLATE_API_URL, json=payload)
                    if response.status_code == 200:
                        st.session_state.recognized_text = response.json().get("translated_text", "Translation failed")
                        st.write("Translated Text:")
                        st.write(st.session_state.recognized_text)
                        log_activity(user_id, 
                                     "Translate Text", 
                                     f"Text: {text_to_translate}", 
                                     source_language)
                    else:
                        st.error(f"Failed to translate text. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.error("Please enter text to translate")

    if st.session_state.recognized_text:
        if st.button("Run NER"):
            try:
                response = requests.post(NER_API_URL, json={"text": st.session_state.recognized_text})
                if response.status_code == 200:
                    ner_result = response.json()
                    st.write("NER Result:")
                    st.write(ner_result)
                    log_activity(user_id, 
                                 "Run NER", 
                                 f"Text: {st.session_state.recognized_text}, NER Result: {ner_result}",
                                 '')
                else:
                    st.error(f"Failed to run NER. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = ""

    if 'feedback_text' not in st.session_state:
        st.session_state.feedback_text = ""

    if st.button("Start Over", key="start_over"):
        st.session_state.recognized_text = ""
        st.session_state.feedback_text = ""
        st.experimental_rerun()

    st.subheader("Submit Feedback")
    feedback_text = st.text_area("Enter your feedback here", value=st.session_state.feedback_text, key="feedback_area")

    audio_processor = AudioProcessor()
    webrtc_ctx = webrtc_streamer(key="speech-to-text", mode=WebRtcMode.SENDRECV,
                                 audio_processor_factory=lambda: audio_processor,
                                 media_stream_constraints={"video": False, "audio": True},
                                 async_processing=True)

    def update_feedback():
        while True:
            if webrtc_ctx.state.playing:
                audio_processor.recognize()
                if audio_processor.result:
                    st.session_state.feedback_text = audio_processor.result
                    st.experimental_rerun()
            else:
                break

    threading.Thread(target=update_feedback, daemon=True).start()

    if st.button("Submit Feedback", key="submit_feedback"):
        if feedback_text:
            st.session_state.feedback_text = feedback_text
            payload = {"original_text": st.session_state.recognized_text, "feedback": [{"comment": feedback_text}]}
            response = requests.post(FEEDBACK_API_URL, json=payload)
            if response.status_code == 200:
                st.success("Feedback submitted successfully!")
            else:
                st.error(f"Failed to submit feedback. Status code: {response.status_code}")
        else:
            st.error("Please enter your feedback")
                
if __name__ == "__main__":
    main()
