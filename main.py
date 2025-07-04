from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()

    input_image = Image.open(io.BytesIO(input_bytes)).convert("RGBA")
    output_image = remove(input_image)

    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    return StreamingResponse(output_bytes, media_type="image/png")

