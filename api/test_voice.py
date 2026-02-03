import asyncio
import edge_tts

TEXT = "Welcome to Rot Max. I am your zero rupee AI narrator. Let's get these grades."
VOICE = "en-US-ChristopherNeural"  # This is a high-quality free male voice
OUTPUT_FILE = "test_audio.mp3"

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"Success! Audio saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())