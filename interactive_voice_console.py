"""
Interactive Voice AI Console:
Simulate real phone calls across 5 domains in English, Hindi, Gujarati, or Hinglish.
Features:
- Real-time LLM dialogue with Groq (< 500ms)
- Realistic voice synthesis through Deepgram Aura (played via laptop speakers)
- Dynamic campaign personalization & call outcome logging
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

from core.llm_engine import LLMEngine
from core.tts_engine import TTSEngine
from core.campaign_manager import CampaignManager

def print_header():
    print("\n" + "="*65)
    print("      🎙️  MULTIPURPOSE VOICE AI AGENT CONSOLE  🎙️")
    print("="*65)
    print(" Domains: Webinar | Business | Advertising | Govt Scheme | School")
    print(" Powered by: Groq (LPU) + Deepgram Aura TTS + Dynamic Campaigns")
    print("="*65 + "\n")

def run_simulation(session: dict, play_voice: bool = True):
    llm = LLMEngine()
    tts = TTSEngine()
    campaign_mgr = CampaignManager()

    print(f"\n[CALL CONNECTED] 📞 Dialing {session['variables'].get('name', 'User')}...")
    print(f"Domain    : {session['domain']}")
    print(f"Campaign  : {session['campaign_title']}")
    print(f"Language  : {session['language'].upper()}")
    print("-" * 65)

    greeting = session["initial_greeting"]
    print(f"\n🤖 AI Agent: \"{greeting}\"")
    
    # Speak greeting
    if play_voice:
        print("🔊 [Speaking through speakers...]")
        tts.speak(greeting, play_audio=True)

    messages = [{"role": "assistant", "content": greeting}]
    final_status = "INCOMPLETE"

    print("\n💡 (Type your response naturally, or type 'bye' / 'exit' to hang up)")
    
    while True:
        try:
            user_input = input("\n👤 You (Caller): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[Call Disconnected by user]")
            break

        if not user_input:
            continue

        if user_input.lower() in ["bye", "exit", "quit", "hangup", "alvida", "aavjo"]:
            print("\n[CALL ENDED] Caller hung up.")
            final_status = "CALL_TERMINATED_BY_USER"
            break

        messages.append({"role": "user", "content": user_input})

        # LLM Generation
        llm_result = llm.generate_response(session["system_prompt"], messages)
        ai_reply = llm_result["spoken_text"]
        status_tag = llm_result["status_tag"]
        llm_ms = llm_result["latency_ms"]

        print(f"\n🤖 AI Agent: \"{ai_reply}\"")
        print(f"   ⏱️ LLM Latency: {llm_ms:.1f} ms", end="")

        # Voice Synthesis & Playback
        if play_voice:
            tts_res = tts.speak(ai_reply, play_audio=True)
            tts_ms = tts_res.get("latency_ms", 0)
            total_latency = llm_ms + tts_ms
            print(f" | TTS: {tts_ms:.1f} ms | Total Turn: {total_latency:.1f} ms")
        else:
            print()

        messages.append({"role": "assistant", "content": ai_reply})

        # Check if conversation reached a natural conclusion
        if status_tag:
            final_status = status_tag
            print(f"\n🎯 [Outcome Detected: {status_tag}]")
            break

    # Log call result
    log_payload = {
        "campaign_id": session["campaign_id"],
        "campaign_title": session["campaign_title"],
        "language": session["language"],
        "recipient": session["variables"].get("name", "Unknown"),
        "final_status": final_status,
        "transcript": messages
    }
    campaign_mgr.log_call_result(log_payload)
    print(f"\n📝 Call summary logged to: data/call_logs.json (Status: {final_status})")
    print("=" * 65)

def main():
    print_header()
    campaign_mgr = CampaignManager()
    campaigns = campaign_mgr.list_campaigns()

    print("Select a Campaign to Test:")
    for idx, c in enumerate(campaigns, 1):
        print(f"  [{idx}] {c['title']} ({c['domain']})")
    print("  [6] Test with Sample CSV Contacts")
    print("  [0] Exit")

    choice = input("\nEnter choice (0-6) [Default: 1]: ").strip() or "1"

    if choice == "0":
        print("Goodbye!")
        return

    play_audio_input = input("Enable audio playback through speakers? (Y/n) [Default: Y]: ").strip().lower()
    play_audio = play_audio_input != "n"

    if choice == "6":
        # Load from CSV
        contacts = campaign_mgr.load_sample_contacts()
        if not contacts:
            print("No contacts found in data/contacts_sample.csv")
            return
        print("\nContacts loaded from CSV:")
        for idx, ct in enumerate(contacts, 1):
            print(f"  [{idx}] {ct['name']} - {ct['campaign_type']} ({ct['preferred_language']})")
        
        c_choice = input(f"Select contact (1-{len(contacts)}) [Default: 1]: ").strip() or "1"
        try:
            selected_contact = contacts[int(c_choice) - 1]
            session = campaign_mgr.prepare_call_session(
                campaign_id=selected_contact["campaign_type"],
                language=selected_contact["preferred_language"],
                contact_vars={"name": selected_contact["name"]}
            )
            run_simulation(session, play_voice=play_audio)
        except Exception as e:
            print(f"Error preparing session: {e}")
        return

    # Direct Campaign selection
    campaign_index = int(choice) - 1 if choice.isdigit() and 1 <= int(choice) <= 5 else 0
    selected_campaign = campaigns[campaign_index]
    camp_details = campaign_mgr.get_campaign(selected_campaign["id"])

    # Language selection
    avail_langs = list(camp_details["prompts"].keys())
    print(f"\nAvailable Languages for {selected_campaign['title']}:")
    for idx, l in enumerate(avail_langs, 1):
        print(f"  [{idx}] {l.upper()}")
    l_choice = input(f"Select language (1-{len(avail_langs)}) [Default: 1]: ").strip() or "1"
    chosen_lang = avail_langs[int(l_choice) - 1] if l_choice.isdigit() and 1 <= int(l_choice) <= len(avail_langs) else avail_langs[0]

    # Custom Name (optional)
    custom_name = input(f"\nEnter recipient name [Default: {camp_details['default_vars'].get('name')}]: ").strip()
    contact_vars = {"name": custom_name} if custom_name else None

    session = campaign_mgr.prepare_call_session(
        campaign_id=selected_campaign["id"],
        language=chosen_lang,
        contact_vars=contact_vars
    )

    run_simulation(session, play_voice=play_audio)

if __name__ == "__main__":
    main()

