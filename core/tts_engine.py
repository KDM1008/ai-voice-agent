"""
TTS Engine: Synthesizes realistic human-like voice audio using Deepgram Aura.
Plays directly through laptop speakers on Windows using built-in winsound.
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Check for Windows native audio player
HAS_WINSOUND = False
if sys.platform == "win32":
    try:
        import winsound
        HAS_WINSOUND = True
    except ImportError:
        pass

class TTSEngine:
    def __init__(self, voice_model="aura-asteria-en"):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY is not set in .env")
        
        self.voice_model = voice_model
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "audio_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def speak(self, text: str, play_audio: bool = True, filename: str = None) -> dict:
        """
        Synthesizes text to speech using Deepgram Aura (Linear16 PCM WAV).
        Plays the audio through speakers if play_audio is True.
        """
        if not text or not text.strip():
            return {"success": False, "error": "Empty text"}

        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

        # Request linear16 WAV format for instant Windows playback
        url = f"https://api.deepgram.com/v1/speak?model={self.voice_model}&encoding=linear16&container=wav"
        payload = {"text": text}

        start_time = time.time()
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            latency_ms = (time.time() - start_time) * 1000

            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Deepgram TTS API returned {response.status_code}: {response.text}",
                    "latency_ms": latency_ms
                }

            # Save WAV audio
            target_file = filename or os.path.join(self.cache_dir, f"reply_{int(time.time()*1000)}.wav")
            with open(target_file, "wb") as f:
                f.write(response.content)

            # Play audio through speakers
            if play_audio and HAS_WINSOUND:
                try:
                    winsound.PlaySound(target_file, winsound.SND_FILENAME)
                except Exception as audio_err:
                    print(f"  [Notice] Audio playback skipped: {audio_err}")

            return {
                "success": True,
                "audio_path": target_file,
                "audio_bytes": len(response.content),
                "latency_ms": latency_ms
            }

        except Exception as e:
            return {"success": False, "error": str(e), "latency_ms": 0}

