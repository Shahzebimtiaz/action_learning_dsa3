from fastapi import FastAPI
from app.api.v1.endpoints import ocr, test, translate #, auth, ner, ocr

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#app.include_router(auth.router, prefix="/auth", tags=["auth"])
#app.include_router(ner.router, prefix="/ner", tags=["ner"])
#app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
#app.include_router(translate.router, prefix="/translate", tags=["translate"])

# app/main.py

app.include_router(ocr.router, prefix="/api/v1/endpoints", tags=["ocr"])
app.include_router(translate.router, prefix="/api/v1/endpoints", tags=["translate"])

app.include_router(test.router, prefix="/api/v1/endpoints", tags=["test"])