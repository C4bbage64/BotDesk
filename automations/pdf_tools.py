from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(file_list, output_file):
    pdf_writer = PdfWriter()
    for file in file_list:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return f"Merged PDFs into: {output_file}"

def split_pdfs(input_file):
    pdf_reader = PdfReader(input_file)
    split_files = []
    for i, page in enumerate(pdf_reader.pages):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)
        output_file = f"page_{i + 1}.pdf"
        with open(output_file, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        split_files.append(output_file)
    return f"Split PDF into: {split_files}"

def extract_text_from_pdf(input_file):
    pdf_reader = PdfReader(input_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
