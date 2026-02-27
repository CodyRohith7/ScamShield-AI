import json
import os
from typing import List
from models.schemas import ExtractedEntities
from utils.prompts import (
    INTELLIGENCE_AGENT_SYSTEM_PROMPT,
    SUMMARY_GENERATION_PROMPT,
    RED_FLAGS_PROMPT,
    RECOMMENDED_ACTIONS_PROMPT
)

# Check which AI provider to use
USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None
USE_GEMINI = os.getenv("GEMINI_API_KEY") is not None

if USE_OPENAI:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class IntelligenceAgent:
    """
    Intelligence Agent: Extracts and structures fraud intelligence
    from conversations using AI-powered entity recognition
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model if USE_OPENAI else "gemini-pro"
    
    async def extract_entities_ai(self, conversation_text: str) -> ExtractedEntities:
        """
        Use AI to extract entities from conversation
        (Complements regex-based extraction)
        """
        
        prompt = f"""Extract fraud-related entities from this conversation:

{conversation_text}

Respond in JSON format as specified."""
        
        try:
            if USE_OPENAI:
                response = await self._call_openai(INTELLIGENCE_AGENT_SYSTEM_PROMPT, prompt)
            elif USE_GEMINI:
                response = await self._call_gemini(INTELLIGENCE_AGENT_SYSTEM_PROMPT, prompt)
            else:
                return ExtractedEntities()  # Return empty if no AI
            
            # Parse response
            data = json.loads(response)
            
            # Convert to ExtractedEntities model
            from models.schemas import BankAccount
            
            entities = ExtractedEntities(
                upi_ids=data.get("upi_ids", []),
                bank_accounts=[
                    BankAccount(**acc) if isinstance(acc, dict) else BankAccount(account_number=acc)
                    for acc in data.get("bank_accounts", [])
                ],
                phishing_links=data.get("phishing_links", []),
                phone_numbers=data.get("phone_numbers", []),
                aliases=data.get("aliases", []),
                fake_organizations=data.get("fake_organizations", [])
            )
            
            return entities
            
        except Exception as e:
            print(f"Intelligence Agent extraction error: {e}")
            return ExtractedEntities()
    
    async def generate_summary(self, conversation_text: str) -> str:
        """Generate conversation summary"""
        
        prompt = f"""Conversation transcript:

{conversation_text}

Generate a concise summary."""
        
        try:
            if USE_OPENAI:
                response = await self._call_openai(SUMMARY_GENERATION_PROMPT, prompt)
            elif USE_GEMINI:
                response = await self._call_gemini(SUMMARY_GENERATION_PROMPT, prompt)
            else:
                return "Conversation summary unavailable (AI not configured)"
            
            return response.strip()
            
        except Exception as e:
            print(f"Summary generation error: {e}")
            return f"Summary generation failed: {str(e)}"
    
    async def identify_red_flags(self, conversation_text: str) -> List[str]:
        """Identify red flags in conversation"""
        
        prompt = f"""Analyze this conversation for red flags:

{conversation_text}

Return JSON array of red flags."""
        
        try:
            if USE_OPENAI:
                response = await self._call_openai(RED_FLAGS_PROMPT, prompt)
            elif USE_GEMINI:
                response = await self._call_gemini(RED_FLAGS_PROMPT, prompt)
            else:
                return self._fallback_red_flags(conversation_text)
            
            # Parse JSON array
            red_flags = json.loads(response)
            return red_flags if isinstance(red_flags, list) else []
            
        except Exception as e:
            print(f"Red flags identification error: {e}")
            return self._fallback_red_flags(conversation_text)
    
    async def recommend_actions(self, entities: ExtractedEntities, conversation_text: str) -> List[str]:
        """Recommend actions based on extracted intelligence"""
        
        prompt = f"""Based on this intelligence:

Extracted Entities:
- UPI IDs: {entities.upi_ids}
- Bank Accounts: {[acc.account_number for acc in entities.bank_accounts]}
- Phishing Links: {entities.phishing_links}
- Phone Numbers: {entities.phone_numbers}

Conversation:
{conversation_text}

Recommend specific actions for law enforcement."""
        
        try:
            if USE_OPENAI:
                response = await self._call_openai(RECOMMENDED_ACTIONS_PROMPT, prompt)
            elif USE_GEMINI:
                response = await self._call_gemini(RECOMMENDED_ACTIONS_PROMPT, prompt)
            else:
                return self._fallback_actions(entities)
            
            # Parse JSON array
            actions = json.loads(response)
            return actions if isinstance(actions, list) else []
            
        except Exception as e:
            print(f"Action recommendation error: {e}")
            return self._fallback_actions(entities)
    
    async def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API"""
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"} if "JSON" in system_prompt else None
        )
        return response.choices[0].message.content
    
    async def _call_gemini(self, system_prompt: str, user_prompt: str) -> str:
        """Call Google Gemini API"""
        model = genai.GenerativeModel(self.model)
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    
    def _fallback_red_flags(self, conversation_text: str) -> List[str]:
        """Fallback red flag detection"""
        text_lower = conversation_text.lower()
        red_flags = []
        
        if any(word in text_lower for word in ['fee', 'charge', 'payment', 'deposit']):
            red_flags.append("Upfront fee request")
        
        if any(word in text_lower for word in ['urgent', 'hurry', 'limited time', 'act now', 'today only']):
            red_flags.append("Urgency tactics")
        
        if any(word in text_lower for word in ['guaranteed', '100%', 'risk-free', 'assured']):
            red_flags.append("Too good to be true claims")
        
        if any(word in text_lower for word in ['account', 'password', 'otp', 'pin', 'cvv']):
            red_flags.append("Requests for sensitive information")
        
        if any(word in text_lower for word in ['upi', 'paytm', 'phonepe', 'gpay']):
            red_flags.append("Personal payment methods instead of business accounts")
        
        if any(word in text_lower for word in ['secret', 'don\'t tell', 'confidential', 'private']):
            red_flags.append("Secrecy requests")
        
        return red_flags if red_flags else ["Suspicious conversation pattern"]
    
    def _fallback_actions(self, entities: ExtractedEntities) -> List[str]:
        """Fallback action recommendations"""
        actions = []
        
        if entities.upi_ids:
            for upi in entities.upi_ids:
                actions.append(f"Block UPI ID: {upi}")
                actions.append(f"Report UPI ID {upi} to NPCI")
        
        if entities.phishing_links:
            for link in entities.phishing_links:
                actions.append(f"Report phishing link to CERT-In: {link}")
                actions.append(f"Request takedown of {link}")
        
        if entities.phone_numbers:
            for phone in entities.phone_numbers:
                actions.append(f"Alert telecom provider about {phone}")
                actions.append(f"Add {phone} to DND/spam registry")
        
        if entities.bank_accounts:
            for acc in entities.bank_accounts:
                actions.append(f"Investigate bank account {acc.account_number}")
                if acc.ifsc:
                    actions.append(f"Alert {acc.bank_name or 'bank'} about suspicious account")
        
        if entities.fake_organizations:
            for org in entities.fake_organizations:
                actions.append(f"Investigate fake organization: {org}")
        
        if not actions:
            actions.append("Monitor for additional intelligence")
            actions.append("Continue conversation to extract more details")
        
        return actions
