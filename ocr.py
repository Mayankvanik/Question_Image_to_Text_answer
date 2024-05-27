from fastapi import FastAPI, File, UploadFile , Request
from fastapi.templating import Jinja2Templates
import pytesseract
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
from logic.code import llm
import os

app = FastAPI()

class OCRResponse(BaseModel):
    text: str

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def name(request:Request):
    return templates.TemplateResponse("home.html",{"request":request,"name":"Coding with Mack"})


@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    img = Image.open(BytesIO(await file.read()))
    text = pytesseract.image_to_string(img, config='--psm 6')
    print(text)
    ans = llm(text)
    # return templates.TemplateResponse("01.html", {"text": ans})
    return {"text": ans}
