import os
import json
import streamlit as st
from groq import Groq

class DynamicGeopoliticalRiskAgent:
    """
    Evaluates maritime geopolitical risk indices for key transit corridors
    using Groq LLM inference with structured JSON responses.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        
        if not self.api_key:
            try:
                self.api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                self.api_key = os.getenv("GROQ_API_KEY")

        try:
            if self.api_key and "gsk_" in self.api_key:
                self.client = Groq(api_key=self.api_key)
                print("✅ [RiskAgent] Groq Client initialized successfully.")
            else:
                print("⚠️ [RiskAgent] No valid Groq key detected. Defaulting to local fallback.")
                self.client = None
        except Exception as e:
            print(f"❌ [RiskAgent] Groq Client Init Error: {e}")
            self.client = None

    def analyze_news_and_calculate_risk(self, news_text: str) -> dict:
        if not self.client:
            return self._heuristic_fallback(news_text)

        system_prompt = (
            "You are an expert maritime geopolitical risk intelligence engine. "
            "Analyze current news feeds and return your assessment strictly as a valid JSON object."
        )

        user_prompt = f"""
Evaluate geopolitical maritime transit corridor risks based on the news feed below.

Required Output JSON Schema:
{{
  "Strait of Hormuz": {{"score": 0.15, "rationale": "One concise sentence based on explicit news."}},
  "Red Sea / Bab-el-Mandeb": {{"score": 0.85, "rationale": "One concise sentence based on explicit news."}},
  "Cape of Good Hope": {{"score": 0.10, "rationale": "One concise sentence based on explicit news."}},
  "Malacca Strait": {{"score": 0.05, "rationale": "One concise sentence based on explicit news."}}
}}

Evaluation Rules:
- "score": Float value between 0.00 (Safe) and 1.00 (Critical Risk).
- Evaluate EACH corridor independently based ONLY on locations explicitly mentioned in the text.
- If a corridor is unaffected or unmentioned in the news, assign a low baseline score (0.05 - 0.20).
- "rationale": Single concise sentence explaining the reasoning.

News Feed Input:
{news_text}
"""

        try:
            print("🚀 [RiskAgent] Sending payload to Groq API via model `openai/gpt-oss-120b`...")
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )

            raw_content = response.choices[0].message.content.strip()
            parsed_data = json.loads(raw_content)

            required_keys = [
                "Strait of Hormuz", 
                "Red Sea / Bab-el-Mandeb", 
                "Cape of Good Hope", 
                "Malacca Strait"
            ]

            for key in required_keys:
                if key not in parsed_data:
                    raise KeyError(f"Missing corridor key in LLM JSON payload: {key}")

            print("✅ [RiskAgent] Groq API response successfully received and parsed.")
            return parsed_data

        except Exception as err:
            print(f"❌ [RiskAgent] API Request Failed: {err}. Executing local fallback logic.")
            return self._heuristic_fallback(news_text)

    def _heuristic_fallback(self, news_text: str) -> dict:
        text_lower = news_text.lower()
        threat_keywords = ["attack", "drone", "missile", "seized", "disruption", "war", "security", "deadly", "houthi"]

        def evaluate_location(location_keywords):
            has_location = any(kw in text_lower for kw in location_keywords)
            has_threat = any(kw in text_lower for kw in threat_keywords)

            if has_location and has_threat:
                return 0.85, "High operational threat detected via localized keyword analysis."
            elif has_location:
                return 0.40, "Elevated monitoring due to explicit regional references."
            return 0.10, "Standard operational parameters detected."

        hormuz_score, hormuz_reason = evaluate_location(["hormuz", "strait of hormuz", "iran", "persian gulf"])
        redsea_score, redsea_reason = evaluate_location(["red sea", "bab-el-mandeb", "yemen"])
        cape_score, cape_reason = evaluate_location(["cape of good hope", "africa", "cape route"])
        malacca_score, malacca_reason = evaluate_location(["malacca", "singapore", "malacca strait"])

        return {
            "Strait of Hormuz": {"score": hormuz_score, "rationale": hormuz_reason},
            "Red Sea / Bab-el-Mandeb": {"score": redsea_score, "rationale": redsea_reason},
            "Cape of Good Hope": {"score": cape_score, "rationale": cape_reason},
            "Malacca Strait": {"score": malacca_score, "rationale": malacca_reason}
        }