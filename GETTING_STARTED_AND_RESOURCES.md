# Voice AI Agent: Getting Started & Resources Guide
## Step-by-Step Onboarding, Account Setup, Free Credits & Project Starter Checklist

---

## 1. Executive Setup Roadmap

To start building your Voice AI Agent without buying expensive hardware or paying heavy platform fees, follow these **4 sequential stages**:

```
[Stage 1: AI & Speech Accounts]
  ├── Hugging Face (Model Hub & LoRA storage)
  ├── Groq Cloud (Ultra-fast LLM brain - Free tier)
  ├── Deepgram ($200 free credit for Real-time STT)
  └── Sarvam AI (Indian Vernacular TTS & STT)
         │
         ▼
[Stage 2: Compute & Storage Setup]
  ├── Google Colab (Free T4 Cloud GPU for fine-tuning)
  └── Google Drive (Free 15 GB storage for weights & datasets)
         │
         ▼
[Stage 3: Local Dev & Security Environment]
  ├── Python 3.10 / 3.11 Virtual Environment
  └── Secure `.env` configuration file
         │
         ▼
[Stage 4: Telephony Provider (When Ready for Real Calls)]
  └── Plivo / Exotel (Outbound SIP & WebSocket streaming)
```

---

## 2. Platform Accounts & Resource Sign-Up Directory

Here is the exact list of websites, what they do, their free tier allowances, and where to get your API keys:

### 1. Hugging Face (Model Hub & Open-Source Community)
* **Website**: [https://huggingface.co/join](https://huggingface.co/join)
* **Purpose**:
  * Download pre-trained base models (e.g., `meta-llama/Llama-3.2-3B-Instruct`, `Qwen/Qwen2.5-7B-Instruct`).
  * Upload your fine-tuned LoRA dialogue adapters into private repositories.
  * Access open-source datasets for Indian dialects and conversational transcripts.
* **Cost / Free Tier**: **100% Free** for model storage, downloads, and community datasets.
* **Action Required**:
  1. Sign up with your email or GitHub.
  2. Go to **Settings** → **Access Tokens** (`https://huggingface.co/settings/tokens`).
  3. Click **Create New Token**, set Type to `Write` (or `Read`), name it `voice-agent-token`, and copy the token.
  4. *(Optional)* If using Llama models: Visit the [Llama 3.2 3B Model Page](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) and click **Agree and access repository** to accept Meta's free license.

---

### 2. Groq Cloud (Ultra-Fast Real-Time LLM Inference)
* **Website**: [https://console.groq.com/](https://console.groq.com/)
* **Purpose**:
  * Serves as the real-time conversational "brain" of the agent.
  * Provides inference speeds of **300 to 500 tokens/second** using custom LPU hardware (essential so callers don't experience awkward silence).
* **Cost / Free Tier**: **Generous Free Tier** (Thousands of free requests per day, perfect for development and testing).
* **Action Required**:
  1. Sign in with Google or GitHub.
  2. Click **API Keys** on the left menu (`https://console.groq.com/keys`).
  3. Click **Create API Key**, name it `voice-agent-groq`, and copy the key (starts with `gsk_...`).

---

### 3. Deepgram (Real-Time Streaming Speech-to-Text)
* **Website**: [https://console.deepgram.com/signup](https://console.deepgram.com/signup)
* **Purpose**:
  * Real-time WebSocket audio transcription with latency under 200ms.
  * Accurately transcribes Indian English, Hindi, and code-mixed Hinglish.
* **Cost / Free Tier**: **$200 Free Credit** upon signup (covers ~45,000+ minutes of live phone calls for free!).
* **Action Required**:
  1. Sign up with email or Google.
  2. Navigate to **API Keys** on the dashboard.
  3. Click **Create a New API Key**, grant `Admin` or `Member` role, and save the key securely.

---

### 4. Sarvam AI (Indian Vernacular STT & TTS)
* **Website**: [https://dashboard.sarvam.ai/](https://dashboard.sarvam.ai/)
* **Purpose**:
  * **Bulbul (TTS)**: High-quality, natural Indian accents in Hindi, Gujarati, Marathi, Tamil, Telugu, Bengali, Kannada, and Indian English.
  * **Saaras (STT)**: High-accuracy regional speech recognition for non-English speakers.
* **Cost / Free Tier**: Offers free trial credits upon developer account creation.
* **Action Required**:
  1. Sign up on the Sarvam dashboard.
  2. Generate an API Key under the **API Keys** section and copy it.

---

### 5. Google Colab & Google Drive (Cloud GPU Training - No Laptop GPU Needed)
* **Website**: [https://colab.research.google.com/](https://colab.research.google.com/)
* **Purpose**:
  * Provides a free **NVIDIA T4 GPU** (16 GB VRAM) to fine-tune Hugging Face models using QLoRA.
  * Stores datasets, checkpoints, and export files in your connected Google Drive without consuming your laptop's local disk space.
* **Cost / Free Tier**: **100% Free** with standard Google account (up to 15 GB free Drive storage).
* **Action Required**:
  1. Ensure you are signed in to your primary Google account.
  2. Create a dedicated folder in Google Drive: `My Drive/Voice_AI_Agent/models/`.

---

### 6. Telephony: Plivo & Exotel (Outbound Phone Calling)
*(Note: You can build and test the entire speech pipeline on your laptop using microphone/speakers before buying a phone number).*

* **Plivo**: [https://console.plivo.com/](https://console.plivo.com/)
  * *Why Plivo*: Super developer-friendly, instant sandbox testing, provides **$10 free test credits**, and supports WebSocket audio streaming (Zentrunk).
* **Exotel**: [https://my.exotel.com/](https://my.exotel.com/)
  * *Why Exotel*: The dominant enterprise cloud telephony provider in India, pre-integrated with Indian telecom DLT headers. Requires enterprise or registered entity verification.
* **Action for now**: Sign up for a **Plivo developer trial account** to get test credits and virtual numbers for testing.

---

## 3. Recommended Workspace Project Structure

Here is how we will organize the codebase inside `d:\Voice AI Agent`:

```
d:\Voice AI Agent\
├── configs/
│   ├── settings.py              # Loads API keys and audio settings
│   └── campaigns.json           # Stores multi-domain campaign configurations
├── core/
│   ├── stt_engine.py            # Deepgram & Sarvam real-time STT
│   ├── llm_engine.py            # Groq & Hugging Face prompt orchestrator
│   ├── tts_engine.py            # Kokoro & Sarvam Indian TTS
│   └── audio_router.py          # Duplex WebSocket pipeline & VAD handler
├── prompts/
│   ├── webinar_prompts.py       # Follow-up & attendance verification
│   ├── business_prompts.py      # Lead qualification & payment reminders
│   ├── marketing_prompts.py     # Advertising & promotional offers
│   ├── govt_prompts.py          # Multilingual welfare schemes (Hindi/Vernacular)
│   └── school_prompts.py        # PTM & fee announcements (Gujarati/Regional)
├── telephony/
│   ├── plivo_bridge.py          # Plivo SIP & WebSocket integration
│   └── exotel_bridge.py         # Exotel voice webhook integration
├── training/
│   └── colab_finetune_lora.ipynb # Google Colab notebook for Hugging Face fine-tuning
├── tests/
│   └── test_local_voice.py      # Test AI agent using your laptop mic/speakers
├── .env                         # Secrets (NEVER commit to GitHub)
├── .env.example                 # Template for required environment variables
├── requirements.txt             # Python libraries
├── main.py                      # FastAPI server entry point
├── VOICE_AGENT_REQUIREMENTS_AND_ARCHITECTURE.md
└── GETTING_STARTED_AND_RESOURCES.md
```

---

## 4. Environment Secrets Template (`.env.example`)

Create a `.env` file in your project root and paste the API keys you collect from the platforms above:

```ini
# ==========================================
# 1. LLM Brain (Groq & Hugging Face)
# ==========================================
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

HUGGINGFACE_TOKEN=hf_your_huggingface_access_token_here

# ==========================================
# 2. Speech-to-Text (STT)
# ==========================================
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# ==========================================
# 3. Text-to-Speech (TTS)
# ==========================================
SARVAM_API_KEY=your_sarvam_api_key_here
# Optional: Kokoro TTS runs locally with zero API key!

# ==========================================
# 4. Telephony (Plivo / Exotel)
# ==========================================
PLIVO_AUTH_ID=your_plivo_auth_id_here
PLIVO_AUTH_TOKEN=your_plivo_auth_token_here
PLIVO_PHONE_NUMBER=+91XXXXXXXXXX

EXOTEL_API_KEY=your_exotel_key_here
EXOTEL_API_TOKEN=your_exotel_token_here
EXOTEL_SUBDOMAIN=your_exotel_subdomain

# ==========================================
# 5. Server Configuration
# ==========================================
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ENVIRONMENT=development
```

---

## 5. Step-by-Step Action Plan (What to do right now)

### Phase 1: Collect Accounts & Keys (Today's Goal)
- [ ] **Step 1.1**: Sign up at [Groq Console](https://console.groq.com/) and copy your `GROQ_API_KEY`.
- [ ] **Step 1.2**: Sign up at [Deepgram Console](https://console.deepgram.com/signup) and copy your `DEEPGRAM_API_KEY` ($200 free credit).
- [ ] **Step 1.3**: Sign up at [Hugging Face](https://huggingface.co/join) and create an Access Token with `Write` access.
- [ ] **Step 1.4**: Sign up at [Sarvam AI](https://dashboard.sarvam.ai/) for Indian regional language voice synthesis.

### Phase 2: Python Environment Setup
1. Open PowerShell in `d:\Voice AI Agent`.
2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install the core real-time dependencies:
   ```powershell
   pip install fastapi uvicorn websockets deepgram-sdk groq python-dotenv requests sounddevice numpy
   ```

### Phase 3: Run the Local Microphone Test (Zero Telephony Cost)
* Before spending a single rupee on telephony, we will run a local test script that lets you talk into your laptop microphone and hear the AI respond in under 500ms in English, Hindi, or Gujarati!

