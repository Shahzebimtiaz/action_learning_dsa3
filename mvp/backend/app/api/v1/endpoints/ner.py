from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class NERRequest(BaseModel):
    text: str

@router.post("/ner/")
async def run_ner(request: NERRequest) -> Dict[str, str]:
    # For now, just return a simple response confirming the received text
    received_text = request.text
    return {"message": "Text received for NER", "received_text": received_text}
