import streamlit as st
import sqlite3
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
from PIL import Image

# Create SQLite database connection
conn = sqlite3.connect('pdf_image.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS pdfs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pdf_path TEXT,
        image_pdf_path TEXT
    )
''')

def extract_images_from_pdf(input_pdf_path, output_pdf_path):
    pdf = PdfFileReader(input_pdf_path)
    images = []

    for page_num in range(pdf.getNumPages()):
        images += convert_from_path(input_pdf_path, dpi=200, first_page=page_num+1, last_page=page_num+1)

    with open(output_pdf_path, 'wb') as output_file:
        output_images = [Image.open(img) for img in images]
        output_images[0].save(output_file, "PDF", resolution=100.0, save_all=True, append_images=output_images[1:])

def save_to_database(pdf_path, image_pdf_path):
    c.execute("INSERT INTO pdfs (pdf_path, image_pdf_path) VALUES (?, ?)", (pdf_path, image_pdf_path))
    conn.commit()

# Streamlit app
st.title("PDF Image Extractor and Creator")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract and create PDF
    st.write("Extracting images and creating PDF...")
    output_pdf_path = f"output_images.pdf"
    extract_images_from_pdf(uploaded_file.name, output_pdf_path)
    st.success("Extraction complete!")

    # Save to database
    save_to_database(uploaded_file.name, output_pdf_path)

    # Download the created PDF
    st.download_button(
        label="Download Output PDF",
        data=open(output_pdf_path, 'rb').read(),
        file_name="output_images.pdf",
        mime="application/pdf"
    )

# Close database connection
conn.close()
