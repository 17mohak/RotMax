import os
import time
import edge_tts
from google import genai
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# We try these models in order. If one fails, we try the next.
MODEL_CANDIDATES = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

VOICE = "en-US-ChristopherNeural"
BACKGROUND_VIDEO = "background.mp4"

# --- BACKUP SCRIPT (Last Resort) ---
BACKUP_SCRIPT = (
    "Yo, the AI is taking a nap, but here's the tea. "
    "Newton's First Law is the law of laziness. "
    "Objects don't move unless you push them. "
    "It's called Inertia. Stay safe."
)


def get_viral_script(notes: str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    Rewrite these notes into a funny, fast-paced 'brainrot' script (max 30s). 
    Use slang: 'bet', 'no cap', 'cooked'. 
    NOTES: {notes}
    """

    # --- MODEL HOPPER LOGIC ---
    for model_name in MODEL_CANDIDATES:
        print(f"1. Trying Brain: {model_name}...")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            if response.text:
                clean_text = response.text.replace("*", "").replace("#", "")
                print(f"   ✅ Success with {model_name}!")
                return clean_text
        except Exception as e:
            print(f"   ❌ {model_name} failed: {e}")
            time.sleep(1)  # Short pause before next try

    print("   ⚠️ All AI models failed. Switching to BACKUP.")
    return BACKUP_SCRIPT


async def generate_brainrot(notes: str, output_filename: str = "final_brainrot.mp4"):
    # 1. Get Script (Model Hopper)
    script = get_viral_script(notes)

    # 2. Generate Audio
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