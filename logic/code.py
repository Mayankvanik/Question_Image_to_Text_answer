import pytesseract
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
import os
os.environ["GROQ_API_KEY"] = "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"


GROQ_LLM = ChatGroq(
            model="llama3-70b-8192"
        )

os.environ['TESSDATA_PREFIX'] = r'C:/Users/mayank.vanik/AppData/Local/Programs/Tesseract-OCR/tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/mayank.vanik/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

prompt = PromptTemplate( template="""Choose the correct option for the question. If the question is code-related,
                         ensure correct code indentation and select the right option from the given choices and Explain in short why is option correct.
Question: \n\n {initial_Question} \n\n """, input_variables=["initial_Question"], )

mail_category_generator = prompt | GROQ_LLM | StrOutputParser()

def llm(msg):
    result = mail_category_generator.invoke({"initial_Question": msg})
    return result




