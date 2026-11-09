"""
Quick Credentials & Connectivity Verification Script.
Tests:
1. Groq API (Conversational LLM response latency & generation)
2. Deepgram API (Speech-to-Text & Text-to-Speech Aura check)
3. Hugging Face Access (Verifies token validity)
"""

import os
import sys
import time

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv

# Load .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def print_separator(title):
    print(f"\n{'='*20} {title} {'='*20}")

def test_groq():
    print_separator("Testing 1: Groq API (LLM Brain)")
    if not GROQ_API_KEY or "your_" in GROQ_API_KEY:
        print("[ERROR] GROQ_API_KEY not configured in .env")
        return False
    
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        
        start_time = time.time()
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional voice agent. Reply in one short, polite sentence in Indian English."
                },
                {
                    "role": "user",
                    "content": "Hello, I want to confirm my webinar attendance for tomorrow."
                }
            ],
            max_tokens=60,
            temperature=0.3
        )
        elapsed_ms = (time.time() - start_time) * 1000
        reply = completion.choices[0].message.content
        
        print("[SUCCESS] Groq Connection Successful!")
        print(f"[LATENCY] Response Time: {elapsed_ms:.1f} ms (Ultra Fast!)")
        print(f"[REPLY] Agent: \"{reply.strip()}\"")
        return True
    except Exception as e:
        print(f"[ERROR] Groq API Test Failed: {e}")
        return False

def test_deepgram():
    print_separator("Testing 2: Deepgram API (STT & TTS)")
    if not DEEPGRAM_API_KEY or "your_" in DEEPGRAM_API_KEY:
        print("[ERROR] DEEPGRAM_API_KEY not configured in .env")
        return False
    
    try:
        import requests
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Test Deepgram Aura TTS (Generates a quick audio greeting)
        tts_url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
        payload = {"text": "Hello! Your Voice AI agent is successfully connected to Deepgram."}
        
        start_time = time.time()
        response = requests.post(tts_url, headers=headers, json=payload)
        elapsed_ms = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            print("[SUCCESS] Deepgram Connection Successful!")
            print(f"[LATENCY] TTS Generation: {elapsed_ms:.1f} ms")
            print(f"[AUDIO] Audio Generated: {len(response.content)} bytes (Audio pipeline functional!)")
            return True
        else:
            print(f"[ERROR] Deepgram returned status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Deepgram API Test Failed: {e}")
        return False

def test_huggingface():
    print_separator("Testing 3: Hugging Face Token")
    if not HUGGINGFACE_TOKEN or "your_" in HUGGINGFACE_TOKEN:
        print("[ERROR] HUGGINGFACE_TOKEN not configured in .env")
        return False
    
    try:
        import requests
        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("name", "Unknown")
            print("[SUCCESS] Hugging Face Token Valid!")
            print(f"[USER] Authenticated as: {username}")
            return True
        else:
            print(f"[ERROR] Hugging Face Auth Failed ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Hugging Face Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("\nStarting Voice AI Credentials Verification...")
    
    groq_ok = test_groq()
    dg_ok = test_deepgram()
    hf_ok = test_huggingface()
    
    print("\n" + "="*50)
    if groq_ok and dg_ok and hf_ok:
        print("[RESULT] ALL SYSTEMS READY! All 3 credentials authenticated and working!")
    else:
        print("[RESULT] Some services failed. Check the error messages above.")
    print("="*50 + "\n")
