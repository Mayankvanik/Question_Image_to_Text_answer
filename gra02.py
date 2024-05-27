import gradio as gr
import pytesseract
from PIL import Image
from fpdf import FPDF
from logic.code import llm
from pathlib import Path
import os

# Initialize PDF object
pdf = FPDF()

# Global list to keep track of Q/A for the PDF
qa_list = []
image_folder = "Image_folder"

# Ensure the image folder exists
os.makedirs(image_folder, exist_ok=True)

def perform_ocr(img):
    text = pytesseract.image_to_string(img, config='--psm 6')
    ans = llm(text)
    # Append the image and answer to the global list
    qa_list.append((img, ans))
    return ans

def save_pdf():
    global qa_list
    pdf.add_page()
    
    # Save each image with an incremental name
    for index, (img, ans) in enumerate(qa_list):
        img_path = os.path.join(image_folder, f"image_{index+1}.png")
        img.save(img_path)
        pdf.image(img_path, x=5, y=None, w=100)  # Adjust positioning and size as needed
        pdf.ln(10)  # Move to next line, adjust as needed
        # Add the answer text
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(0, 4, f"Answer: {ans}")#, align='L'
        pdf.ln(3)
        
    pdf_file_path = "output01.pdf"
    pdf.output(pdf_file_path)
    print('aaaaaaaa',pdf_file_path)
    return pdf_file_path

# Create a Gradio interface
ocr_interface = gr.Interface(
    fn=perform_ocr,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Answer From Image_Text Question",
    description="Upload or paste an image to extract text and generate a response with LLM"
)

# Create a Gradio button to save the PDF and define its output
pdf_button = gr.DownloadButton("Create PDF",visible=True)

def download_pdf():
    pdf_file_path = save_pdf()
    return pdf_file_path #'E:/practice/Image_mcq/output01.pdf'

# pdf_interface = gr.Interface(
#     fn=download_pdf,
#     inputs=None,
#     outputs=gr.File(label="Download your PDF"),
# )

app = gr.Blocks()

with app:
    gr.Markdown("# OCR and PDF Generation")
    with gr.Column():
        ocr_interface.render()
    pdf_button.render()
    #pdf_button.click(fn=download_pdf,None, pdf_button)
    pdf_button.click(fn=download_pdf, inputs=None, outputs=gr.File(label="Download PDF"))  #pdf_interface)
    #pdf_button.click( None, gr.DownloadButton("Download PDF",value='E:/practice/Image_mcq/output01.pdf',visible=True))

app.launch()


