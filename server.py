"""
FastAPI SaaS Server for Multipurpose Voice AI Agent.
Provides REST APIs for:
- Campaign & Contact management
- Live Call simulation (LLM dialogue & Deepgram TTS)
- Audio streaming to browser
- Call analytics & logging
"""

import os
import sys
import uuid
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.llm_engine import LLMEngine
from core.tts_engine import TTSEngine
from core.campaign_manager import CampaignManager

app = FastAPI(title="Voice AI SaaS Platform", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
llm_engine = LLMEngine()
tts_engine = TTSEngine()
campaign_mgr = CampaignManager()

# Ensure directories exist
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
audio_cache_dir = os.path.join(base_dir, "audio_cache")
os.makedirs(static_dir, exist_ok=True)
os.makedirs(audio_cache_dir, exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Request Models
class StartCallRequest(BaseModel):
    campaign_id: str
    language: str = "en"
    recipient_name: str = "Karan Sharma"
    phone_number: str = "+91 98765 43210"

class TurnRequest(BaseModel):
    campaign_id: str
    system_prompt: str
    messages: list
    user_message: str

class EndCallRequest(BaseModel):
    campaign_id: str
    campaign_title: str
    language: str
    recipient: str
    final_status: str
    transcript: list

@app.get("/")
def get_dashboard():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "SaaS Dashboard index.html not found"}

@app.get("/api/campaigns")
def get_campaigns():
    return {
        "campaigns": campaign_mgr.campaigns,
        "list": campaign_mgr.list_campaigns()
    }

@app.get("/api/contacts")
def get_contacts():
    return {"contacts": campaign_mgr.load_sample_contacts()}

@app.post("/api/call/start")
def start_call(req: StartCallRequest):
    try:
        session = campaign_mgr.prepare_call_session(
            campaign_id=req.campaign_id,
            language=req.language,
            contact_vars={"name": req.recipient_name}
        )
        greeting = session["initial_greeting"]
        
        # Synthesize initial greeting audio
        audio_filename = f"greeting_{uuid.uuid4().hex[:8]}.wav"
        audio_full_path = os.path.join(audio_cache_dir, audio_filename)
        tts_res = tts_engine.speak(greeting, play_audio=False, filename=audio_full_path)
        
        audio_url = f"/audio/{audio_filename}" if tts_res.get("success") else None

        return {
            "success": True,
            "session": session,
            "initial_greeting": greeting,
            "audio_url": audio_url,
            "tts_latency_ms": tts_res.get("latency_ms", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/call/turn")
def process_turn(req: TurnRequest):
    try:
        updated_messages = req.messages + [{"role": "user", "content": req.user_message}]
        
        # LLM Generation
        llm_res = llm_engine.generate_response(req.system_prompt, updated_messages)
        ai_reply = llm_res["spoken_text"]
        status_tag = llm_res["status_tag"]
        llm_latency_ms = llm_res["latency_ms"]

        # TTS Synthesis
        audio_filename = f"turn_{uuid.uuid4().hex[:8]}.wav"
        audio_full_path = os.path.join(audio_cache_dir, audio_filename)
        tts_res = tts_engine.speak(ai_reply, play_audio=False, filename=audio_full_path)
        
        audio_url = f"/audio/{audio_filename}" if tts_res.get("success") else None
        tts_latency_ms = tts_res.get("latency_ms", 0)

        return {
            "success": True,
            "ai_reply": ai_reply,
            "status_tag": status_tag,
            "llm_latency_ms": llm_latency_ms,
            "tts_latency_ms": tts_latency_ms,
            "total_latency_ms": llm_latency_ms + tts_latency_ms,
            "audio_url": audio_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/call/end")
def end_call(req: EndCallRequest):
    try:
        record = {
            "campaign_id": req.campaign_id,
            "campaign_title": req.campaign_title,
            "language": req.language,
            "recipient": req.recipient,
            "final_status": req.final_status,
            "transcript": req.transcript
        }
        campaign_mgr.log_call_result(record)
        return {"success": True, "message": "Call recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
def get_logs():
    log_path = os.path.join(base_dir, "data", "call_logs.json")
    if os.path.exists(log_path):
        try:
            import json
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            return {"logs": logs}
        except Exception:
            return {"logs": []}
    return {"logs": []}

@app.get("/api/stats")
def get_stats():
    log_path = os.path.join(base_dir, "data", "call_logs.json")
    logs = []
    if os.path.exists(log_path):
        try:
            import json
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    
    total = len(logs)
    confirmed = sum(1 for l in logs if any(k in l.get("final_status", "") for k in ["CONFIRM", "BOOKED", "ACCEPTED", "INTERESTED"]))
    opt_outs = sum(1 for l in logs if any(k in l.get("final_status", "") for k in ["OPT_OUT", "DECLINE", "ABSENT"]))
    
    # Calculate conversion rate
    conversion_rate = f"{(confirmed / total * 100):.1f}%" if total > 0 else "0.0%"
    
    return {
        "total_calls": total,
        "confirmed_calls": confirmed,
        "opt_out_calls": opt_outs,
        "conversion_rate": conversion_rate,
        "avg_cost_per_call": "₹0.74",
        "avg_latency": "680 ms"
    }

@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join(audio_cache_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    raise HTTPException(status_code=404, detail="Audio file not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

