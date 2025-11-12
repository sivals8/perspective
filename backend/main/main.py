from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2, numpy as np
from io import BytesIO
from sqlalchemy import create_engine, text

app = FastAPI()

# allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect to PostgreSQL
engine = create_engine("postgresql://username:password@localhost/atmolens")

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), theme: str = "fall", context: str = "outdoor"):
    img_bytes = await file.read()
    npimg = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # --- Simple placeholder filter logic ---
    if theme == "fall":
        if context == "outdoor":
            img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
        else:
            img = cv2.applyColorMap(img, cv2.COLORMAP_PINK)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, buffer = cv2.imencode(".jpg", img)
    return {"image": buffer.tobytes().hex()}  # return as hex string
