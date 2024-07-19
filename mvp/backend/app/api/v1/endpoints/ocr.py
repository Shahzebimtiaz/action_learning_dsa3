# app/api/v1/endpoints/ocr.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
import requests
from . import API_KEY_OCR
router = APIRouter()

@router.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...)) -> Dict[str, str]:
    try:
        # Replace this URL with the actual OCR API URL
        ocr_api_url = "https://api-ninjas.com/api/imagetotext"
        headers = {"X-Api-Key": "your_api_key_here"}  # Replace with your API key if needed

        # Read the file content
        image_data = await file.read()

        # Send the file to the OCR API
        response = requests.post(
            ocr_api_url,
            headers=headers,
            files={"file": ("image.png", image_data, "image/png")}
        )

        # Check if the request was successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="OCR API request failed")

        # Return the text extracted by OCR
        result = response.json()
        return {"text": result.get("text", "No text found")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
