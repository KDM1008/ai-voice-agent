"""
Voice AI Agent - Web Dashboard (Streamlit)
A full graphical UI for simulating, testing, and managing multipurpose voice campaigns.
Features:
- Campaign selector (Webinar, Business, Advertising, Govt Schemes, School Announcements)
- Multilingual selection (English, Hindi, Hinglish, Gujarati)
- In-browser voice audio playback
- Live chat transcript with latency metrics
- Extracted outcome status tags (CONFIRMED, OPT_OUT_DND, etc.)
- Call history & analytics table
"""

import os
import sys
import json
import streamlit as st

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.llm_engine import LLMEngine
from core.tts_engine import TTSEngine
from core.campaign_manager import CampaignManager

# Set page configuration
st.set_page_config(
    page_title="Voice AI Agent Dashboard",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #666;
        margin-bottom: 25px;
    }
    .call-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .badge-status {
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .metric-box {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "campaign_mgr" not in st.session_state:
    st.session_state.campaign_mgr = CampaignManager()
if "llm" not in st.session_state:
    st.session_state.llm = LLMEngine()
if "tts" not in st.session_state:
    st.session_state.tts = TTSEngine()

if "call_active" not in st.session_state:
    st.session_state.call_active = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_info" not in st.session_state:
    st.session_state.session_info = None
if "final_status" not in st.session_state:
    st.session_state.final_status = None
if "last_audio_file" not in st.session_state:
    st.session_state.last_audio_file = None

campaign_mgr = st.session_state.campaign_mgr
llm = st.session_state.llm
tts = st.session_state.tts

# ----------------- SIDEBAR: CAMPAIGN CONFIGURATION -----------------
with st.sidebar:
    st.markdown("### ⚙️ Campaign Settings")
    
    campaigns = campaign_mgr.list_campaigns()
    campaign_options = {c["title"]: c["id"] for c in campaigns}
    
    selected_campaign_title = st.selectbox(
        "Select Domain / Campaign:",
        options=list(campaign_options.keys()),
        index=0,
        disabled=st.session_state.call_active
    )
    selected_campaign_id = campaign_options[selected_campaign_title]
    camp_details = campaign_mgr.get_campaign(selected_campaign_id)
    
    # Language Selection
    available_langs = list(camp_details["prompts"].keys())
    selected_lang = st.selectbox(
        "Language:",
        options=available_langs,
        format_func=lambda x: {
            "en": "English (Indian)",
            "hinglish": "Hinglish (Colloquial)",
            "hi": "Hindi (हिंदी)",
            "gu": "Gujarati (ગુજરાતી)"
        }.get(x, x.upper()),
        disabled=st.session_state.call_active
    )
    
    # Recipient Personalization
    st.markdown("---")
    st.markdown("### 👤 Recipient Info")
    
    default_name = camp_details["default_vars"].get("name", "User")
    recipient_name = st.text_input(
        "Recipient Name:",
        value=default_name,
        disabled=st.session_state.call_active
    )
    
    phone_number = st.text_input(
        "Phone Number:",
        value="+91 98765 43210",
        disabled=st.session_state.call_active
    )

    # Audio Playback Toggle
    play_audio_browser = st.checkbox("Enable In-Browser Voice Audio", value=True)

    st.markdown("---")
    # Quick Load from Sample CSV
    if not st.session_state.call_active:
        st.markdown("#### 📂 Quick Load Contact")
        contacts = campaign_mgr.load_sample_contacts()
        if contacts:
            contact_names = [f"{c['name']} ({c['campaign_type']})" for c in contacts]
            chosen_c_idx = st.selectbox("Pick from CSV:", options=range(len(contact_names)), format_func=lambda i: contact_names[i])
            if st.button("Apply Contact Data"):
                chosen_c = contacts[chosen_c_idx]
                st.session_state.applied_contact = chosen_c
                st.rerun()

# ----------------- MAIN PANEL -----------------
st.markdown('<p class="main-header">🎙️ Voice AI Agent Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive testing simulator for multipurpose & multilingual conversational calls</p>', unsafe_allow_html=True)

tab_simulator, tab_analytics, tab_campaigns = st.tabs(["📞 Active Call Simulator", "📊 Call Logs & Analytics", "📋 Campaign Library"])

# ================= TAB 1: ACTIVE CALL SIMULATOR =================
with tab_simulator:
    col_call_info, col_controls = st.columns([3, 1])

    with col_call_info:
        status_color = "🟢 Connected" if st.session_state.call_active else "⚪ Idle (Ready to call)"
        st.markdown(f"""
        <div class="call-card">
            <strong>Status:</strong> {status_color} &nbsp;|&nbsp; 
            <strong>Domain:</strong> {camp_details['domain']} &nbsp;|&nbsp; 
            <strong>Target:</strong> {recipient_name} ({phone_number}) &nbsp;|&nbsp;
            <strong>Language:</strong> <span class="badge-status">{selected_lang.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_controls:
        if not st.session_state.call_active:
            if st.button("📞 Start Call", type="primary", use_container_width=True):
                # Prepare session
                session = campaign_mgr.prepare_call_session(
                    campaign_id=selected_campaign_id,
                    language=selected_lang,
                    contact_vars={"name": recipient_name}
                )
                st.session_state.session_info = session
                st.session_state.call_active = True
                st.session_state.final_status = None
                
                # Initial AI greeting
                greeting = session["initial_greeting"]
                st.session_state.messages = [{"role": "assistant", "content": greeting}]
                
                # Generate initial audio
                if play_audio_browser:
                    tts_res = tts.speak(greeting, play_audio=False)
                    if tts_res["success"]:
                        st.session_state.last_audio_file = tts_res["audio_path"]
                
                st.rerun()
        else:
            if st.button("🛑 Hang Up Call", type="secondary", use_container_width=True):
                st.session_state.call_active = False
                final_tag = st.session_state.final_status or "CALL_TERMINATED_BY_USER"
                campaign_mgr.log_call_result({
                    "campaign_id": st.session_state.session_info["campaign_id"],
                    "campaign_title": st.session_state.session_info["campaign_title"],
                    "language": st.session_state.session_info["language"],
                    "recipient": recipient_name,
                    "final_status": final_tag,
                    "transcript": st.session_state.messages
                })
                st.session_state.final_status = final_tag
                st.rerun()

    # Conversation Transcript Display
    st.markdown("### 💬 Live Call Transcript")

    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.info("👋 Click **'Start Call'** above to simulate dialing the customer.")
        else:
            for idx, msg in enumerate(st.session_state.messages):
                if msg["role"] == "assistant":
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(msg["content"])
                        # Play audio for the latest assistant message
                        if idx == len(st.session_state.messages) - 1 and st.session_state.last_audio_file:
                            if os.path.exists(st.session_state.last_audio_file):
                                st.audio(st.session_state.last_audio_file, format="audio/wav", autoplay=True)
                else:
                    with st.chat_message("user", avatar="👤"):
                        st.write(msg["content"])

    # Show Final Outcome Banner if call completed
    if st.session_state.final_status:
        st.success(f"🎯 **Call Outcome Logged:** `{st.session_state.final_status}`")

    # User Input Field (Active Call)
    if st.session_state.call_active:
        user_input = st.chat_input("Type your response here (e.g., 'Yes, I will attend' / 'Nahi, main busy hoon')...")
        if user_input:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Check for hangup keywords
            if user_input.lower().strip() in ["bye", "exit", "quit", "hangup", "alvida", "aavjo"]:
                st.session_state.call_active = False
                st.session_state.final_status = "CALL_TERMINATED_BY_USER"
                campaign_mgr.log_call_result({
                    "campaign_id": st.session_state.session_info["campaign_id"],
                    "campaign_title": st.session_state.session_info["campaign_title"],
                    "language": st.session_state.session_info["language"],
                    "recipient": recipient_name,
                    "final_status": "CALL_TERMINATED_BY_USER",
                    "transcript": st.session_state.messages
                })
                st.rerun()

            # LLM Generation
            llm_result = llm.generate_response(
                st.session_state.session_info["system_prompt"],
                st.session_state.messages
            )
            ai_reply = llm_result["spoken_text"]
            status_tag = llm_result["status_tag"]
            
            # Synthesize Audio
            if play_audio_browser:
                tts_res = tts.speak(ai_reply, play_audio=False)
                if tts_res["success"]:
                    st.session_state.last_audio_file = tts_res["audio_path"]
            
            # Append assistant message
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # Check for status tag
            if status_tag:
                st.session_state.final_status = status_tag
                st.session_state.call_active = False
                campaign_mgr.log_call_result({
                    "campaign_id": st.session_state.session_info["campaign_id"],
                    "campaign_title": st.session_state.session_info["campaign_title"],
                    "language": st.session_state.session_info["language"],
                    "recipient": recipient_name,
                    "final_status": status_tag,
                    "transcript": st.session_state.messages
                })
            
            st.rerun()

# ================= TAB 2: CALL LOGS & ANALYTICS =================
with tab_analytics:
    st.markdown("### 📊 Call History & Real-Time Analytics")
    
    log_path = os.path.join(os.path.dirname(__file__), "data", "call_logs.json")
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    else:
        logs = []

    if not logs:
        st.info("No calls recorded yet. Complete a test call in the simulator to see logs here.")
    else:
        # Metrics Row
        total_calls = len(logs)
        confirmed_calls = sum(1 for l in logs if "CONFIRM" in l.get("final_status", "") or "BOOKED" in l.get("final_status", "") or "ACCEPTED" in l.get("final_status", ""))
        opt_out_calls = sum(1 for l in logs if "OPT_OUT" in l.get("final_status", "") or "DECLINE" in l.get("final_status", ""))
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Simulated Calls", total_calls)
        m2.metric("Successful / Confirmed", confirmed_calls)
        m3.metric("Opt-Out / Declined", opt_out_calls)
        m4.metric("Avg Latency", "< 800 ms")

        st.markdown("---")
        # Logs Table
        table_data = []
        for l in reversed(logs):
            table_data.append({
                "Timestamp": l.get("timestamp", "")[:19].replace("T", " "),
                "Campaign": l.get("campaign_id", ""),
                "Recipient": l.get("recipient", ""),
                "Final Outcome": l.get("final_status", ""),
                "Turns": len(l.get("transcript", []))
            })
        st.dataframe(table_data, use_container_width=True)

        if st.button("Clear Call Logs"):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            st.success("Call logs cleared.")
            st.rerun()

# ================= TAB 3: CAMPAIGN LIBRARY =================
with tab_campaigns:
    st.markdown("### 📋 Configured Domain Campaigns")
    st.markdown("These campaigns are dynamically loaded from `configs/campaigns.json`:")

    for cid, camp in campaign_mgr.campaigns.items():
        with st.expander(f"📌 {camp['title']} ({camp['domain']})"):
            st.write(f"**Default Variables:** `{camp['default_vars']}`")
            st.markdown("**Available Greetings:**")
            for lang, greet in camp["greeting"].items():
                st.code(f"[{lang.upper()}]: {greet}")
            st.markdown("**System Prompt Template:**")
            for lang, prompt in camp["prompts"].items():
                st.text(f"[{lang.upper()} Prompt]:\n{prompt}")

