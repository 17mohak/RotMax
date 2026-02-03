from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import generate_brainrot
import os

app = FastAPI()

# Allow the frontend to talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    notes: str


@app.get("/")
def read_root():
    return {"status": "RotMax API is running"}


@app.post("/generate-video")
async def create_video(request: VideoRequest):
    try:
        # Generate the video
        output_file = await generate_brainrot(request.notes, "output.mp4")

        # Return the video file directly to the browser
        return FileResponse(output_file, media_type="video/mp4", filename="brainrot.mp4")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))