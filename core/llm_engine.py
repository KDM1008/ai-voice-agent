"""
LLM Engine: Groq-powered Conversational Core with Dynamic Multi-Domain Context.
"""

import os
import re
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLMEngine:
    def __init__(self, model_name=None):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in .env")
        
        self.model = model_name or os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, system_prompt: str, messages: list) -> dict:
        """
        Generates a concise, conversational voice response.
        Returns dict with:
        - 'spoken_text': Clean text to speak aloud (without internal tags)
        - 'status_tag': Extracted call status (e.g., CONFIRMED, OPT_OUT, etc.)
        - 'latency_ms': Generation time in milliseconds
        """
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        start_time = time.time()
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            max_tokens=80,
            temperature=0.3
        )
        latency_ms = (time.time() - start_time) * 1000
        raw_reply = completion.choices[0].message.content.strip()

        # Extract [STATUS: XYZ] tag if present
        status_match = re.search(r"\[STATUS:\s*([A-Z_]+)\]", raw_reply)
        status_tag = status_match.group(1) if status_match else None

        # Clean text for speech synthesis (remove status tags, brackets, and markdown)
        clean_text = re.sub(r"\[STATUS:[^\]]+\]", "", raw_reply)
        clean_text = clean_text.replace("*", "").replace("#", "").strip()

        return {
            "raw_reply": raw_reply,
            "spoken_text": clean_text,
            "status_tag": status_tag,
            "latency_ms": latency_ms
        }

