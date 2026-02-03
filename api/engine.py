import os
import time
import edge_tts
from google import genai
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
MODEL_NAME = "gemini-2.0-flash"
VOICE = "en-US-ChristopherNeural"
BACKGROUND_VIDEO = "background.mp4"

# --- BACKUP SCRIPT (Used if AI fails) ---
BACKUP_SCRIPT = (
    "Yo, listen up! The AI is taking a nap right now, but I got you. "
    "Newton's First Law is basically the law of being lazy. "
    "Objects don't wanna move unless you push them. No cap. "
    "It's called Inertia. Stay safe out there."
)


def get_viral_script(notes: str):
    print(f"1. Asking Gemini ({MODEL_NAME}) to write a script...")

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are a Gen Z TikTok creator. Rewrite the following study notes into a funny, 
    fast-paced 'brainrot' style script (max 30 seconds). 
    Use slang like 'bet', 'no cap', 'cooked'. 

    NOTES:
    {notes}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        if response.text:
            return response.text.replace("*", "").replace("#", "")

    except Exception as e:
        print(f"   ⚠️ AI Error: {e}")
        print("   ⚠️ Switching to BACKUP SCRIPT to save the demo!")
        return BACKUP_SCRIPT


async def generate_brainrot(notes: str, output_filename: str = "final_brainrot.mp4"):
    # 1. Get Script (AI or Backup)
    script = get_viral_script(notes)
    print(f"   Script used: {script[:50]}...")

    print(f"2. Generating Audio...")
    communicate = edge_tts.Communicate(script, VOICE)
    await communicate.save("temp_voice.mp3")

    # 3. Processing Video
    voice_clip = AudioFileClip("temp_voice.mp3")
    game_clip = VideoFileClip(BACKGROUND_VIDEO)

    audio_duration = voice_clip.duration
    if game_clip.duration < audio_duration:
        n_loops = int(audio_duration // game_clip.duration) + 1
        final_video = concatenate_videoclips([game_clip] * n_loops)
    else:
        final_video = game_clip

    final_video = final_video.subclip(0, audio_duration)

    game_audio = final_video.audio.volumex(0.1)
    final_audio = CompositeAudioClip([game_audio, voice_clip])
    final_video = final_video.set_audio(final_audio)

    print("3. Rendering Video...")
    final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac", preset="ultrafast")

    return output_filename