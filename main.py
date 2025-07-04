from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
from PIL import Image
import io
import os

app = FastAPI()

@app.get("/")
def ping():
    return {"message": "Background Remover API is Live!"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        input_data = await file.read()

        # Open as PIL image and ensure RGBA
        input_image = Image.open(io.BytesIO(input_data)).convert("RGBA")

        # Resize if needed (optional)
        # input_image = input_image.resize((1024, 1024))  # optional limit

        # Remove background
        output_image = remove(input_image)

        # Convert to bytes
        img_bytes = io.BytesIO()
        output_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return StreamingResponse(img_bytes, media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

