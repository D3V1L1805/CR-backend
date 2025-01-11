import os
from tabula import read_pdf
import pandas as pd
from PIL import Image
from io import BytesIO
import fitz  # PyMuPDF

OUTPUT_DIR = "utils/extracted_content"

def extract_text_from_pdf(pdf_path):

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    text_content = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text_content += page.get_text()
    pdf_document.close()

    print(f"Text content extracted")
    return text_content


def extract_images_from_pdf(pdf_path):

    pdf_document = fitz.open(pdf_path)
    image_count = 0
    result = []

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(BytesIO(image_bytes))
            if image.mode == "RGBA":
                image = image.convert("RGB")
            image_path = os.path.join(OUTPUT_DIR, f"image_{page_num + 1}_{img_index + 1}.jpg")
            image.save(image_path, format="JPEG")
            image_count += 1
            result.append(image_path)

    pdf_document.close()
    print(f"{image_count} images extracted and saved as JPG to {OUTPUT_DIR}")
    return result


def extract_tables_from_pdf(pdf_path):

    result = []
    tables = read_pdf(pdf_path, pages='all', multiple_tables=True, pandas_options={'header': None})
    for i, table in enumerate(tables):
        print(f"Table {i + 1}")

        print(table)
        df = pd.DataFrame(table)

        j = 1
        while j < len(df):

            
            if pd.isna(df.iloc[j]).any(): 
                for col in range(df.shape[1]):
                    if not pd.isna(df.iloc[j, col]):
                        df.iloc[j-1, col] = str(df.iloc[j-1, col]) + " " + str(df.iloc[j, col])
                df = df.drop(index=j)
                df = df.reset_index(drop=True)
                j -= 1
            j += 1

        df = df.dropna(how='all')

        print(df)
        df.to_excel(f'{OUTPUT_DIR}/excel_{i+1}.xlsx',index = False)
        result.append(f'{OUTPUT_DIR}/excel_{i+1}.xlsx')
        
    return result

# def process_pdf(pdf_path):
#     """Process a PDF file to extract text, images, and tables."""
#     if not os.path.isfile(pdf_path):
#         print("Invalid file path.")
#         return

#     print(f"Processing PDF: {pdf_path}")

#     extract_text_from_pdf(pdf_path)

#     extract_images_from_pdf(pdf_path)

#     extract_tables_from_pdf(pdf_path)

