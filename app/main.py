from fastapi import FastAPI, UploadFile, File, HTTPException
from pdf2image import convert_from_bytes
from PIL import Image
import io
import base64
from app.baml_client import b
from baml_py import Image as BamlImage
from typing import List
import logging

app = FastAPI()


def convert_pdf_to_images(pdf_bytes: bytes) -> List[Image.Image]:
    try:
        return convert_from_bytes(pdf_bytes, dpi=200, fmt="png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting PDF: {str(e)}")


def convert_to_images(content_type: str, file_bytes: bytes) -> List[Image.Image]:
    if content_type == "application/pdf":
        return convert_pdf_to_images(file_bytes)
    elif content_type.startswith("image/"):
        img = Image.open(io.BytesIO(file_bytes))
        return [img]
    else:
        raise HTTPException(
            status_code=415, detail=f"Unsupported file type: {content_type}"
        )


def img_to_baml_image(img: Image.Image) -> BamlImage:
    buffer = io.BytesIO()
    img.save(buffer, format=img.format or "PNG")
    base64_str = base64.b64encode(buffer.getvalue()).decode()
    return BamlImage.from_base64(
        f"image/{img.format.lower() if img.format else 'png'}", base64_str
    )


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()

        content_type = file.content_type or "application/pdf"

        # Convert to PIL Images
        images = convert_to_images(content_type, content)

        if not images:
            raise HTTPException(status_code=400, detail="No images could be extracted")

        # Convert first image to BAML Image
        baml_image = img_to_baml_image(images[0])

        # Call BAML function
        result = b.ExtractFromImage(baml_image)

        return {"result": result}

    except Exception as e:
        logging.error(f"Extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
