"""
Advanced Scam Detection Agent
Supports Mistral, OpenAI, Gemini and Rule-Based Fallback.
Clean, production-ready implementation for Hackathon Submission.
"""

import os
import requests
import json
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from persona_engine import persona_engine
from utils.extraction import extractor

load_dotenv(override=True)

class SimpleScamAgent:
    """
    The Core Agent Logic.
    """
    
    def __init__(self):
        # Load Keys
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        
        # Initialize Clients
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
            
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')

        # Load Persona Engine
        self.persona_engine = persona_engine

    def _call_mistral(self, messages):
        """Native HTTP call to Mistral API"""
        try:
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.mistral_key}",
                "Content-Type": "application/json"
            }
            # Adjust messages to ensure roles are strictly user/assistant/system
            mistral_messages = []
            for m in messages:
                # Mistral prefers standard roles
                mistral_messages.append({"role": m["role"], "content": m["content"]})

            data = {
                "model": "mistral-tiny",
                "messages": mistral_messages,
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=data, timeout=8)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Mistral Error: {e}")
            return None

    def _call_openai(self, messages):
        """Call OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return None

    def generate_response(self, user_message, history=None):
        """
        Generate response using Multi-LLM Waterfall
        1. Check if we should use a pre-canned response (Persona Engine)
        2. Try Mistral
        3. Try OpenAI
        4. Try Gemini
        5. Fallback to Rule Engine
        """
        extracted_data = extractor.extract_all(user_message)
        
        # 1. PERSONA ENGINE - Random Injection
        # For this hackathon, we prioritize believability.
        # Simple heuristic: If history is short, trust building. If long, information gathering.
        phase = "trust_building"
        if history and len(history) > 4:
            phase = "information_gathering"
        if "upi" in user_message.lower() or "pay" in user_message.lower() or "bank" in user_message.lower():
            phase = "extraction"
            
        # 10% chance to just force a canned response for "human-ness", or if key keywords match
        canned_response = self.persona_engine.get_random_response(phase=phase)
        
        # 2. AI GENERATION
        system_prompt = (
            "You are a naive, slightly confused victim being targeted by a scammer. "
            "Your goal is to waste their time. Act interested but incompetent. "
            "Never reveal you are an AI. Use Indian English context. "
            "If they ask for money, start making excuses about technical issues. "
            "Keep responses short (1-2 sentences)."
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for msg in history:
                role = "assistant" if msg['role'] == 'agent' else "user"
                messages.append({"role": role, "content": msg['content']})
        messages.append({"role": "user", "content": user_message})

        agent_response = None
        provider_used = "none"
        
        # PROVIDER WATERFALL
        if not agent_response and self.mistral_key:
            # print("Trying Mistral...")
            agent_response = self._call_mistral(messages)
            if agent_response: provider_used = "mistral"
            
        if not agent_response and self.openai_key:
            # print("Mistral failed. Trying OpenAI...")
            agent_response = self._call_openai(messages)
            if agent_response: provider_used = "openai"
            
        # If AI generation worked, we stick with it. 
        # If it failed, we MUST use canned response.
        if not agent_response:
             print("AI failed. Using Canned Response.")
             agent_response = canned_response
             provider_used = "persona_engine_fallback"
             
        # FALLBACK: Rule Engine (Absolute last resort)
        if not agent_response:
            try:
                from rule_engine import rule_engine
                fallback = rule_engine.get_response(user_message, history)
                agent_response = fallback["agent_response"]
                provider_used = "rule_engine"
            except:
                agent_response = "I'm sorry, I didn't hear you. Can you repeat?"

        # Final Formatting
        return {
            "success": True,
            "agent_response": agent_response,
            "entities": extracted_data,
            "risk_score": 85 if "otp" in user_message.lower() else 40,
            "provider": provider_used
        }
