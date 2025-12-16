import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.staticfiles import StaticFiles

client = OpenAI()
app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "ballad"

@app.post("/tts")
def generate_tts(data: TTSRequest):
    filename = f"audio_{uuid.uuid4()}.mp3"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=data.voice,
        input=data.text,
        response_format="mp3",
    )

    with open(filename, "wb") as f:
        f.write(response)

    return {
        "audio_url": f"/audio/{filename}"
    }

app.mount("/audio", StaticFiles(directory="."), name="audio")
