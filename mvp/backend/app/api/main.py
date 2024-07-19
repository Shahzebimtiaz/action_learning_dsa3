from fastapi import FastAPI
from .api.v1.endpoints import auth, ner, ocr, translate

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(ner.router, prefix="/api/v1/ner", tags=["ner"])
app.include_router(ocr.router, prefix="/api/v1/ocr", tags=["ocr"])
app.include_router(translate.router, prefix="/api/v1/translate", tags=["translate"])
