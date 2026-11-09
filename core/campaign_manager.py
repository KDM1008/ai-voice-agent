"""
Campaign Manager: Handles Multi-Domain Configurations, Contact Personalization & Call Logging.
"""

import os
import json
import csv
import time
from datetime import datetime

class CampaignManager:
    def __init__(self, config_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = config_path or os.path.join(base_dir, "configs", "campaigns.json")
        self.log_path = os.path.join(base_dir, "data", "call_logs.json")
        self.contacts_path = os.path.join(base_dir, "data", "contacts_sample.csv")
        self.campaigns = self._load_campaigns()

    def _load_campaigns(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Campaign config file not found at {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_campaigns(self) -> list:
        return [
            {"id": cid, "title": c["title"], "domain": c["domain"]}
            for cid, c in self.campaigns.items()
        ]

    def get_campaign(self, campaign_id: str) -> dict:
        return self.campaigns.get(campaign_id)

    def load_sample_contacts(self) -> list:
        contacts = []
        if os.path.exists(self.contacts_path):
            with open(self.contacts_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    contacts.append(row)
        return contacts

    def prepare_call_session(self, campaign_id: str, language: str = None, contact_vars: dict = None) -> dict:
        """
        Prepares personalized System Prompt & Initial Greeting for a call.
        """
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Unknown campaign: {campaign_id}")

        # Merge contact variables with campaign defaults
        vars_dict = campaign.get("default_vars", {}).copy()
        if contact_vars:
            vars_dict.update({k: v for k, v in contact_vars.items() if v})

        # Pick language (fallback if specified language is missing)
        available_languages = list(campaign["prompts"].keys())
        chosen_lang = language if language in available_languages else available_languages[0]

        raw_prompt = campaign["prompts"][chosen_lang]
        raw_greeting = campaign["greeting"][chosen_lang]

        # Interpolate variables safely
        system_prompt = raw_prompt
        greeting = raw_greeting
        for key, val in vars_dict.items():
            system_prompt = system_prompt.replace(f"{{{key}}}", str(val))
            greeting = greeting.replace(f"{{{key}}}", str(val))

        return {
            "campaign_id": campaign_id,
            "campaign_title": campaign["title"],
            "domain": campaign["domain"],
            "language": chosen_lang,
            "variables": vars_dict,
            "system_prompt": system_prompt,
            "initial_greeting": greeting
        }

    def log_call_result(self, call_data: dict):
        """
        Appends call outcome and transcript to data/call_logs.json.
        """
        logs = []
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except Exception:
                logs = []

        call_record = {
            "timestamp": datetime.now().isoformat(),
            **call_data
        }
        logs.append(call_record)

        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

