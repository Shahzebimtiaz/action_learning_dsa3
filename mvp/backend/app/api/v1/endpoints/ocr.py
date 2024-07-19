# app/api/v1/endpoints/ocr.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
import requests
from . import API_KEY_OCR
router = APIRouter()

@router.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...)) -> Dict[str, str]:
    print('hiiiiii')
    try:
        print('hereeeee')
        ocr_api_url = "https://api.api-ninjas.com/v1/imagetotext"
        headers = {"X-Api-Key": '6dJHuaNVoS94Kg1Zkkcg9Q==bnNzWycWizh12TXR'}  # Replace with your actual API key

        # Read the file content
        image_data = await file.read()

        # Log file content type
        print(f"File content type: {file.content_type}")
        print(f"File size: {len(image_data)} bytes")

        mime_type = file.content_type

        # Send the file to the OCR API
        response = requests.post(
            ocr_api_url,
            headers=headers,
            files={"file": (file.filename, image_data, mime_type)}
        )

        print(f"Request sent to {ocr_api_url} with headers {headers}")


        # Check if the request was successful
        if response.status_code != 200:
            print(f"OCR API response status code: {response.status_code}")
            print(f"OCR API response text: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"OCR API request failed with status code {response.status_code}")

        # Log the response text for debugging
        print("!!!!!!!!!!!!! ", response.text)

        # Return the text extracted by OCR
        result = response.json()
        print(f"OCR API response JSON: {result}")
        return {"text": result.get("text", "No text found")}
    
        
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
