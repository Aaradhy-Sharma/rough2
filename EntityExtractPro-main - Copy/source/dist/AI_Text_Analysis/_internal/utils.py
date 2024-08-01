import fitz  # PyMuPDF
import docx
from tkinter import filedialog
from PIL import Image
import pytesseract
from pathlib import Path

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("All supported files", "*.pdf;*.docx;*.txt;*.png;*.jpg;*.jpeg"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx"),
            ("Text files", "*.txt"),
            ("Image files", "*.png;*.jpg;*.jpeg")
        ]
    )
    return file_path

def ensure_directories():
    for directory in ['logs', 'results', 'highlighted']:
        Path(directory).mkdir(exist_ok=True)