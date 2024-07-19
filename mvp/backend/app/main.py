from fastapi import FastAPI
from app.api.v1.endpoints import ocr #, auth, ner, ocr, translate

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#app.include_router(auth.router, prefix="/auth", tags=["auth"])
#app.include_router(ner.router, prefix="/ner", tags=["ner"])
#app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
#app.include_router(translate.router, prefix="/translate", tags=["translate"])

# app/main.py

app.include_router(ocr.router, prefix="/api/v1", tags=["ocr"])

