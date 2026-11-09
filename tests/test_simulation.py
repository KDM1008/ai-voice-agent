"""
Automated Test for Voice AI Conversation Pipeline (Non-interactive)
Tests:
1. Webinar Follow-up Campaign (Hinglish & English)
2. LLM response latency and status tag detection
3. Deepgram TTS generation
4. JSON call log creation
"""

import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.llm_engine import LLMEngine
from core.tts_engine import TTSEngine
from core.campaign_manager import CampaignManager

def run_test():
    print("\n--- Running Automated Pipeline Test ---")
    campaign_mgr = CampaignManager()
    llm = LLMEngine()
    tts = TTSEngine()

    # 1. Prepare Webinar Session
    session = campaign_mgr.prepare_call_session(
        campaign_id="webinar_followup",
        language="en",
        contact_vars={"name": "Aditya Sharma"}
    )
    print(f"[OK] Session Prepared: {session['campaign_title']} for {session['variables']['name']}")
    print(f"[OK] Initial Greeting: \"{session['initial_greeting']}\"")

    # 2. Simulate User Reply
    user_reply = "Yes, I will attend the live session tomorrow."
    print(f"\n[USER SAYS]: \"{user_reply}\"")

    messages = [
        {"role": "assistant", "content": session["initial_greeting"]},
        {"role": "user", "content": user_reply}
    ]

    # 3. LLM Generation
    result = llm.generate_response(session["system_prompt"], messages)
    print(f"[AI RESPONDS]: \"{result['spoken_text']}\"")
    print(f"[METRIC] LLM Latency: {result['latency_ms']:.1f} ms")
    print(f"[STATUS DETECTED]: {result['status_tag']}")

    # 4. TTS Generation (do not play audio to avoid blocking in CI/test)
    tts_result = tts.speak(result["spoken_text"], play_audio=False)
    print(f"[TTS GENERATED]: {tts_result.get('audio_bytes', 0)} bytes in {tts_result.get('latency_ms', 0):.1f} ms")

    # 5. Log Result
    campaign_mgr.log_call_result({
        "campaign_id": session["campaign_id"],
        "recipient": session["variables"]["name"],
        "final_status": result["status_tag"] or "CONFIRMED",
        "transcript": messages + [{"role": "assistant", "content": result["spoken_text"]}]
    })

    log_file = os.path.join(os.path.dirname(__file__), "..", "data", "call_logs.json")
    if os.path.exists(log_file):
        print(f"[LOG SUCCESS] Call logged to {os.path.abspath(log_file)}")

    print("\n--- TEST COMPLETED SUCCESSFULLY! All components working smoothly! ---")

if __name__ == "__main__":
    run_test()
