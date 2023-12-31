import os
import PyPDF2
import pytesseract
from PIL import Image
import decode

def pdf_to_text(pdf_file):
    pdf_text = ""
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()
    return pdf_text

def djvu_to_text(djvu_file):
    djvu_text = ""
    with open(djvu_file, 'rb') as file:
        djvu_document = decode(file)
        for page_num in range(len(djvu_document)):
            djvu_page = djvu_document[page_num]
            djvu_text += djvu_page.get_text()
    return djvu_text

def image_to_text(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

def convert_to_text(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_file = os.path.join(input_folder, filename)
            text = pdf_to_text(pdf_file)
        elif filename.lower().endswith('.djvu'):
            djvu_file = os.path.join(input_folder, filename)
            text = djvu_to_text(djvu_file)
        else:
            image_file = os.path.join(input_folder, filename)
            text = image_to_text(image_file)

        txt_file = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(output_folder, txt_file)
        with open(output_path, 'w', encoding='utf-8') as txt_output:
            txt_output.write(text)

if __name__ == "__main__":
    input_folder = "input"
    output_folder = "output"
    convert_to_text(input_folder, output_folder)
