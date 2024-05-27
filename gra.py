import gradio as gr
import pytesseract
from PIL import Image
from io import BytesIO
from logic.code import llm

def perform_ocr(img):
    # img is a PIL Image object when using the "image" input type in Gradio
    text = pytesseract.image_to_string(img, config='--psm 6')
    ans = llm(text)
    return ans

interface = gr.Interface(
    fn=perform_ocr,
    inputs=gr.Image(type="pil"),  # Use Gradio's Image input, specifying PIL Image type
    outputs="text",
    title="Answer From Image_Text Question",
    description="Upload or paste an image to extract text and generate a response with LLM"
)
interface.launch()

