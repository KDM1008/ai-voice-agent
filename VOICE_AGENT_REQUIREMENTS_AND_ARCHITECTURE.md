# Multipurpose & Multilingual Voice AI Agent Platform: Architecture & Technical Blueprint
## Enterprise Outbound Calling for Webinars, Business, Advertising, Government Schemes & Education in 10+ Languages

---

## 1. Executive Summary & Core Feasibility

### Can you build a single Multipurpose & Multilingual Voice AI Agent?
**Yes, 100%.** Modern voice AI engines can handle both multiple business domains and multiple languages simultaneously. By decoupling:
1. **The Telephony Layer** (Exotel / Plivo / SIP),
2. **The Speech Engine** (Multilingual STT & Vernacular TTS), and
3. **The Intelligence Layer** (Dynamic Multilingual LLM Prompts & Campaign Data),

A single unified platform can handle:
* **Domains**: Webinars, Business Leads, Advertising, Government Schemes, and School Announcements.
* **Languages**: Hindi, English, Hinglish (code-mixed), Gujarati, Marathi, Tamil, Telugu, Bengali, Kannada, Punjabi, and Malayalam.
* **Voice Flow**: Seamless pre-configured language selection **plus** real-time dynamic language switching mid-call (e.g., citizen switches from Hindi to Gujarati).

---

## 2. Multipurpose Domain Matrix & Use Cases

A single backend server dynamically loads the campaign configuration (`campaign_type` + `target_language`):

```
                               ┌─────────────────────────────────────────┐
                               │   Multipurpose Voice AI Platform        │
                               │   (Telephony + Language Engine + LLM)   │
                               └────────────────────┬────────────────────┘
                                                    │
      ┌──────────────────┬──────────────────────────┼─────────────────────────┬──────────────────┐
      │                  │                          │                         │                  │
      ▼                  ▼                          ▼                         ▼                  ▼
 1. Webinars        2. Business                3. Advertising            4. Govt Schemes    5. Schools
 - Attendance       - Lead Qualification       - Discount Codes          - PM Kisan/Awas    - PTM Reminder
 - Slot Confirms    - EMI/Payment Reminders    - Product Launches        - Subsidy Status   - Fee Due Alerts
 - WhatsApp Links   - Customer Feedback        - DND Opt-Out Support     - Multi-lingual    - Exam/Holidays
```

---

## 3. Deep Dive: Multilingual & Vernacular Engine (Indic Languages)

In India, a voice agent restricted to pure English will fail for government schemes, rural citizens, small business owners, and regional school announcements. The system must support **native languages, regional accents, and colloquial code-mixing (Hinglish/Tanglish)**.

```
Incoming Audio (e.g. Gujarati / Hindi / Hinglish)
           │
           ▼
[1. Multilingual STT]  ──► Deepgram Nova-2 / Sarvam Saaras / Groq Whisper-v3
           │               (Transcribes speech to text in original script or romanized form)
           ▼
[2. Language Detector] ──► Confirms language (e.g., 'gu', 'hi', 'en') or detects language change
           │
           ▼
[3. Multilingual LLM]  ──► Groq Llama-3.1-8B / Qwen-2.5-7B / Sarvam
           │               (Reasons, maintains context, responds in matching language)
           ▼
[4. Vernacular TTS]    ──► Sarvam Bulbul / Azure Neural Indian / Bhashini / Kokoro
           │               (Synthesizes authentic regional Indian accent & cadence)
           ▼
Outgoing Audio Stream back to phone call
```

### 3.1 Supported Languages & Dialect Matrix

| Language | ISO Code | Script Supported | Best STT Provider | Best Vernacular TTS Voice |
| :--- | :---: | :--- | :--- | :--- |
| **English (Indian)** | `en-IN` | Latin | Deepgram Nova-2 / Groq Whisper | Kokoro / Deepgram Aura / Azure `en-IN-Neerja` |
| **Hindi (हिंदी)** | `hi-IN` | Devanagari | Sarvam Saaras / Deepgram / Groq | Sarvam Bulbul / Azure `hi-IN-Swara` |
| **Hinglish (Colloquial)**| `hi-Latn`| Latin / Devanagari | Groq Whisper Large-v3 / Deepgram | Sarvam Bulbul / Azure `hi-IN-Madhur` |
| **Gujarati (ગુજરાતી)** | `gu-IN` | Gujarati | Sarvam Saaras / Groq Whisper | Sarvam Bulbul / Azure `gu-IN-Dhwani` |
| **Marathi (मराठी)** | `mr-IN` | Devanagari | Sarvam Saaras / Groq Whisper | Sarvam Bulbul / Azure `mr-IN-Aarohi` |
| **Tamil (தமிழ்)** | `ta-IN` | Tamil | Sarvam Saaras / Groq Whisper | Sarvam Bulbul / Azure `ta-IN-Pallavi` |
| **Telugu (తెలుగు)** | `te-IN` | Telugu | Sarvam Saaras / Groq Whisper | Sarvam Bulbul / Azure `te-IN-Shruti` |
| **Kannada (ಕನ್ನಡ)** | `kn-IN` | Kannada | Sarvam Saaras / Groq Whisper | Sarvam Bulbul / Azure `kn-IN-Sapna` |
| **Bengali (বাংলা)** | `bn-IN` | Bengali | Sarvam Saaras / Groq Whisper | Sarvam Bulbul / Azure `bn-IN-Tanishaa` |
| **Punjabi (ਪੰਜਾਬੀ)** | `pa-IN` | Gurmukhi | Sarvam Saaras / Groq Whisper | Azure `pa-IN-Ojas` / Bhashini |

### 3.2 The Three Multilingual Calling Modes:
1. **Pre-Configured Mode (CRM Driven)**:
   * Each contact in your database has a `preferred_language` field (e.g., `hi` for Uttar Pradesh/MP, `gu` for Gujarat, `ta` for Tamil Nadu).
   * The call begins directly in that language with the appropriate regional greeting.
2. **Bilingual Opening with Auto-Detect Mode**:
   * Agent greets bilingually: *"Hello, Namaste! This is Priya calling from [Organization]. Main [Organization] se bol rahi hoon."*
   * The STT identifies which language the user responds in and locks into that language for the rest of the call.
3. **Mid-Call Dynamic Language Switching**:
   * If a citizen says in the middle of a call: *"Bhaiya Gujarati me baat karoge?"* or *"Can you speak in English please?"*
   * The LLM emits a control token `[SWITCH_LANG: gu]` or `[SWITCH_LANG: en]`.
   * The backend dynamically updates the STT language model and switches the TTS voice ID instantly without disconnecting.

---

## 4. Regulatory & Telephony Rules (India TRAI / DLT Critical Notice)

When making calls across business, government, school, and advertising domains, you must respect Indian telecom regulations:

```
                     ┌─────────────────────────────────────────┐
                     │   Outbound Call Route Classification    │
                     └────────────────────┬────────────────────┘
                                          │
            ┌─────────────────────────────┴─────────────────────────────┐
            ▼                                                           ▼
   Transactional / Service Route                               Promotional / Marketing Route
   (Webinars, Schools, Govt, Payment Alerts)                   (Discounts, Advertising, Product Launch)
   - Can call DND (Do Not Disturb) numbers                     - STRICTLY PROHIBITED to call DND numbers
   - Allowed 24/7 (or 8:00 AM - 9:00 PM)                       - Restricted strictly between 10:00 AM - 9:00 PM
   - Fixed DLT entity & sender ID required                     - Mandatory scrubbing against National DND registry
```

### Can You Use Your Personal Mobile Number?
* **Testing / Demo (1–5 calls)**: Technically possible using an Android GSM gateway app.
* **Commercial / Advertising / Bulk Calling**: **NEVER use a personal SIM**.
  * Under TRAI TCCCPR rules, telecom providers (Jio, Airtel, Vi) use AI to detect high-frequency outbound calling patterns on personal SIMs.
  * Your personal SIM will be blocked for spam within 24 to 48 hours.
* **Production Solution**: Use **Exotel**, **Plivo**, or **Tata Tele Business Services (TTBS)** with a verified DLT registration and virtual number (DID).

---

## 5. Domain & Multilingual System Prompts & Parameters

### 5.1 Universal Conversational Parameters
* **VAD Threshold**: `0.5`
* **Speech Silence Cutoff**: `400ms` (natural pauses without cutting the caller off).
* **Max Response Length**: `50 - 70 tokens` (1 to 2 short sentences per turn. Never read long paragraphs on a phone call).
* **Temperature**: `0.3` (Strict facts, zero hallucinations).

---

### 5.2 Prompt 1: Webinar Follow-up (Hinglish / English)

```text
You are Priya from [University Name].
You are calling [Student Name] regarding their registration for the upcoming webinar: "[Webinar Title]" on [Date].

LANGUAGE & TONE:
Conversational Hinglish or Indian English (match the student's language). Polite and friendly.

FLOW:
1. Greet: "Hello [Student Name], main Priya bol rahi hoon [University Name] se. Aapne hamare [Webinar Title] webinar ke liye register kiya tha na?"
2. Check Attendance: "Hum final seats confirm kar rahe hain—kya aap live session attend kar payenge?"
3. Outlines:
   - If YES: "Great! Session link hum aapke WhatsApp aur email par 1 ghante pehle send kar denge. Thank you!" -> Mark: CONFIRMED.
   - If NO/BUSY: "Koi baat nahi! Kya aap chahte hain ki hum session ki recorded video aapko email kar dein?" -> Mark: RECORDING_REQUESTED or NOT_INTERESTED.
```

---

### 5.3 Prompt 2: Business & Payment Reminder (English & Hindi)

```text
You are Rahul, accounts manager at [Company Name].
You are speaking with [Client Name] regarding invoice #[Invoice_Number] of amount [Amount], which was due on [Due_Date].

OBJECTIVE:
Politely confirm when the payment will be initiated.

LANGUAGE:
Professional Indian English or Hindi.

FLOW:
- "Hello [Client Name], I am calling from [Company Name] regarding invoice #[Invoice_Number]. We haven't received the payment confirmation yet. Could you please share the expected date of transfer?"
- If client says already paid: "Thank you for the update! Please share the transaction ID or receipt on accounts@[company].com and I will update our records immediately."
- Record: PROMISE_TO_PAY_DATE | ALREADY_PAID | DISPUTE_RAISED.
```

---

### 5.4 Prompt 3: Advertising / Festive Promo Campaign (Hinglish)

```text
You are Ananya calling from [Brand / Store Name].
You are calling registered customer [Customer Name] with a special festival offer.

OBJECTIVE:
Share exclusive promo code [PROMO_CODE] for 30% OFF and offer to send the catalog link on WhatsApp.

RULES:
- Keep it under 30 seconds.
- DND Compliance: If the user says "Don't call me / Remove my number", immediately reply: "Apologies for the disturbance! I will remove your number from our promotional list right away. Have a nice day!" -> Status: OPT_OUT_DND.
- If interested: "Maine coupon code [PROMO_CODE] aur shopping link aapke WhatsApp par bhej diya hai. Happy shopping!" -> Status: CONVERTED.
```

---

### 5.5 Prompt 4: Government Scheme Awareness (Hindi - PM Awas / Kisan Yojana)

```text
Aap [Department Name] ki taraf se virtual sahayak Vikas hain.
Aap [Citizen Name] ji se [Scheme Name, e.g., PM Surya Ghar / Kisan Credit] ke baare me baat kar rahe hain.

OBJECTIVE:
Nagarik ko yojana ke labh (subsidy / financial assistance) ke baare me suchit karein aur pata karein ki kya unhe aavedan karne me sahayata chahiye.

SAMPLE CONVERSATION:
- "Namaste [Citizen Name] ji. Main sarkari yojana sahayata kendra se Vikas bol raha hoon. Kya main [Citizen Name] ji se baat kar raha hoon?"
- "Sarkar ki [Scheme Name] ke tahat aapko subsidy mil sakti hai. Kya aap is yojana ke labh aur aavedan ki jankari lena chahte hain?"
- Agar nagarik bole "Haan": "Bahut accha! Aapke phone par poori jankari ka SMS bhej diya gaya hai. Aap najdiki CSC kendra par jaakar aavedan kar sakte hain."
- Record: INTERESTED_SMS_SENT | ALREADY_BENEFICIARY | NOT_INTERESTED.
```

---

### 5.6 Prompt 5: School PTM & Fee Announcement (Gujarati / ગુજરાતી)

```text
You are Bhavna from the administrative office of [School Name].
You are calling [Parent Name], parent of student [Student Name] (Standard [Standard]).

LANGUAGE:
Pure polite Gujarati (ગુજરાતી).

PROMPT SCRIPT (GUJARATI):
- "નમસ્તે [Parent Name] જી, હું [School Name] માંથી ભાવના વાત કરું છું. આ શનિવારે, તારીખ [Date] ના રોજ શાળામાં વાલી-શિક્ષક મિટિંગ (PTM) રાખેલ છે. શું તમે હાજર રહી શકશો?"
- If parent says YES: "ખૂબ સરસ! તમારો સમય સવારે [Time] વાગ્યે નક્કી કરેલ છે. આભાર!" -> Mark: PTM_CONFIRMED.
- If parent asks about fee notice: "હાજી, આ સત્રની બાકી ફી ભરવાની છેલ્લી તારીખ [Due Date] છે. કૃપા કરીને સમયસર જમા કરાવી દેશો." -> Mark: FEE_NOTIFIED.
```

---

## 6. Model Training & Hosting Strategy (Without Laptop GPU)

To handle 5 domains and 10+ languages without local GPU hardware:

```
[Google Drive Storage]
  └── /multilingual_adapters/
        ├── lora_hindi_govt_v1/      (35 MB LoRA weights)
        ├── lora_gujarati_school_v1/ (25 MB LoRA weights)
        └── lora_hinglish_promo_v1/  (30 MB LoRA weights)
```

### Execution Strategy:
1. **Google Colab (Free T4 GPU)**:
   * Fine-tune `Qwen/Qwen2.5-7B-Instruct` or `meta-llama/Llama-3.2-3B-Instruct` using **QLoRA** on your multilingual dialogue pairs.
   * Save the tiny **LoRA adapter (30MB)** to your **Google Drive** or upload to a private **Hugging Face Hub** repository.
2. **Zero-Training Option (Instant Deployment & Lowest Cost)**:
   * **Groq API (`llama-3.1-8b-instant`)**: Already understands Hindi, Gujarati, Marathi, Tamil, Telugu, and English fluently.
   * Speed: **300+ tokens/second** (crucial for maintaining voice call response latency under 300ms).
   * Cost: **$0.05 per 1 Million tokens** (less than ₹0.002 per call).

---

## 7. Multilingual Cost Analysis (Per 1-Minute Call)

Comparing the cost of standard English calls vs. regional Indian vernacular calls:

| Call Type | Telephony (Exotel/Plivo) | STT Provider | LLM (Groq) | Vernacular TTS | Total Cost / Call |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **English / Hinglish** | ₹0.35 – ₹0.40 | Deepgram / Groq (₹0.15) | ₹0.002 | Kokoro / Aura (₹0.15) | **~₹0.65 – ₹0.70** |
| **Hindi (Government)** | ₹0.35 – ₹0.40 | Sarvam / Deepgram (₹0.20) | ₹0.002 | Sarvam Bulbul (₹0.18) | **~₹0.73 – ₹0.80** |
| **Gujarati / Marathi** | ₹0.35 – ₹0.40 | Sarvam Saaras (₹0.20) | ₹0.003 | Sarvam Bulbul (₹0.18) | **~₹0.73 – ₹0.80** |
| **Tamil / Telugu** | ₹0.35 – ₹0.40 | Sarvam Saaras (₹0.22) | ₹0.003 | Sarvam / Azure (₹0.20) | **~₹0.77 – ₹0.82** |

*(Standard commercial platforms like Retell or Vapi charge ₹12 to ₹16 per call for Indian vernacular voices. Our self-hosted pipeline delivers this at **under ₹0.85 per call**, an ~94% cost reduction).*

---

## 8. Multi-Tenant Campaign JSON Payload Specification

Here is how your backend dispatches any campaign in any language using a single standard format:

```json
{
  "call_id": "CALL_982341",
  "phone_number": "+919876543210",
  "domain": "government_scheme",
  "campaign_name": "PM_SURYA_GHAR_SOLAR",
  "telephony_route": "transactional",
  "language_config": {
    "primary_language": "gu-IN",
    "fallback_language": "hi-IN",
    "allow_dynamic_switch": true,
    "stt_model": "sarvam-saaras",
    "tts_voice": "sarvam-bulbul-female-gujarati"
  },
  "recipient_data": {
    "name": "Kishore Patel",
    "district": "Ahmedabad",
    "subsidy_amount": "₹78,000"
  },
  "post_call_webhook": "https://api.yourdomain.com/webhooks/call-results"
}
```

---

## 9. Next Steps to Build This

1. **Step 1: Campaign Dispatcher** — Set up a database / Google Sheet table with `phone_number`, `recipient_name`, `domain`, and `preferred_language`.
2. **Step 2: Audio Server with Dynamic Language Routing** — Build a FastAPI WebSocket server that initializes Deepgram/Sarvam STT and Sarvam/Kokoro TTS based on the incoming call's language tag.
3. **Step 3: Test Dynamic Switching** — Simulate a call where the user transitions from English to Hindi or Gujarati to verify the language switch trigger.
4. **Step 4: Exotel / Plivo Integration** — Connect real telephone numbers with DLT approval for commercial or transactional routes.
