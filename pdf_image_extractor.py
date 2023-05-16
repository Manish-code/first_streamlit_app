import streamlit as st
import sqlite3
from PyPDF4 import PdfFileReader
from PIL import Image
import tempfile
import shutil
import os

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
    try:
        pdf = PdfFileReader(input_pdf_path)
        images = []

        for page_num in range(pdf.getNumPages()):
            try:
                page = pdf.getPage(page_num)
                if '/XObject' in page['/Resources']:
                    x_objects = page['/Resources']['/XObject'].getObject()
                    for obj in x_objects:
                        if x_objects[obj]['/Subtype'] == '/Image':
                            img = x_objects[obj]
                            if '/Filter' in img:
                                if img['/Filter'] == '/FlateDecode':
                                    img_data = img._data
                                    img = Image.frombytes(
                                        img['/ColorSpace'] if '/ColorSpace' in img else '/DeviceRGB',
                                        (img['/Width'], img['/Height']),
                                        img_data,
                                        'raw',
                                        (img['/ColorSpace'] if '/ColorSpace' in img else '/DeviceRGB'),
                                        0,
                                        1
                                    )
                                elif img['/Filter'] == '/DCTDecode':
                                    img_data = img._data
                                    img = Image.open(img_data)

                            images.append(img)

            except Exception as e:
                st.warning(f"Failed to extract images from page {page_num+1}: {str(e)}")

        if images:
            with open(output_pdf_path, 'wb') as output_file:
                images[0].save(output_file, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
        else:
            st.warning("No images found in the PDF.")

    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")

def save_to_database(pdf_path, image_pdf_path):
    c.execute("INSERT INTO pdfs (pdf_path, image_pdf_path) VALUES (?, ?)", (pdf_path, image_pdf_path))
    conn.commit()

# Streamlit app
st.title("PDF Image Extractor and Creator")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Save the uploaded file to the temporary directory
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, 'wb') as temp_file:
        shutil.copyfileobj(uploaded_file, temp_file)

    # Extract and create PDF
    st.write("Extracting images and creating PDF...")
    output_pdf_path = os.path.join(temp_dir, "output_images.pdf")
    extract_images_from_pdf(temp_file_path, output_pdf_path)
    st.success("Extraction complete!")

    # Save to database
    save_to_database(uploaded_file.name, output_pdf_path)

    # Provide a download link to the output PDF
    st.download_button(
        label="Download Output PDF",
        data=open(output_pdf_path, 'rb').read(),
        file_name="output_images.pdf",
        mime="application/pdf"
    )


    # Display the output PDF
    st.image(output_pdf_path, caption="Output PDF")

    # Fetch the copied PDF file for further processing
    st.write("Copied PDF file for further processing:")
    st.markdown(f"[{uploaded_file.name}]({output_pdf_path})")

    # Cleanup: Remove the temporary directory
    shutil.rmtree(temp_dir)


# Close database connection
conn.close()