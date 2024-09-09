from fastapi import FastAPI, File, UploadFile, HTTPException

# from dotenv import load_dotenv

# load_dotenv()
from typing import List
import imghdr
from baml_py import Image
from baml_client import b
from pydantic import BaseModel, Json
from typing import Any

# to import from 2 directories up you'd use "from ..my_module import MyClass"
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


class ExtractResponse(BaseModel):
    output: Json[Any]


@app.post("/extract/", response_model=ExtractResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    file_names = []
    output_data = {}
    for file in files:
        # Check if the file is an image
        contents = await file.read()
        file_type = imghdr.what(None, h=contents)

        if file_type in ["png", "jpeg", "gif"]:
            file_names.append(file.filename)
            import base64

            base64_image = base64.b64encode(contents).decode("utf-8")
            image = Image.from_base64(
                media_type=f"image/{file_type}", base64=base64_image
            )
            res = b.ExtractResume(
                "Aaron is a software engineer at Google.\n He studied at Stanford University."
            )
            print(res)
            # Process the image file
            # TODO: Implement image processing logic
        else:
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is not a supported image format",
            )

    return ExtractResponse(output="{}")
