from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from utils.pdf_analysis import extract_text_from_pdf, extract_images_from_pdf, extract_tables_from_pdf
import shutil
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode
from pathlib import Path

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

UPLOAD_DIRECTORY = "./uploads"
OUTPUT_DIRECTORY = './utils/extracted_content'


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        if Path(OUTPUT_DIRECTORY).is_dir():
            shutil.rmtree(OUTPUT_DIRECTORY)
        if Path(UPLOAD_DIRECTORY).is_dir():
            shutil.rmtree(UPLOAD_DIRECTORY)

        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        extracted_text = extract_text_from_pdf(file_path)
        extract_images_from_pdf(file_path)
        extract_tables_from_pdf(file_path)
        
        response_data = {"extracted_text": extracted_text}
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/images/")
async def get_images():
    encoded_images = []

    for image_file in Path(OUTPUT_DIRECTORY).glob("*.jpg"):
        print(f"Found JPEG files: {image_file}")
        with open(image_file, "rb") as file:
            encoded_images.append(b64encode(file.read()).decode("utf-8"))

    return {"images": encoded_images}

@app.get("/tables/")
async def get_images():
    encoded_tables = []

    for table_file in Path(OUTPUT_DIRECTORY).glob("*.xlsx"):
        print(f"Found JPEG files: {table_file}")
        with open(table_file, "rb") as file:
            encoded_tables.append({
                "filename": table_file.name,
                "content": b64encode(file.read()).decode("utf-8")
            })

    return {"tables": encoded_tables}

       


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)