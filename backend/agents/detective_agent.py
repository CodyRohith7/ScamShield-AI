import json
import os
from typing import Dict, Optional
from models.schemas import ScamType, PersonaType
from utils.prompts import DETECTIVE_AGENT_SYSTEM_PROMPT

# Check which AI provider to use
USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None
USE_GEMINI = os.getenv("GEMINI_API_KEY") is not None

if USE_OPENAI:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class DetectiveAgent:
    """
    Detective Agent: Analyzes incoming messages to classify scam type,
    assess risk, and recommend appropriate persona
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model if USE_OPENAI else "gemini-pro"
        self.system_prompt = DETECTIVE_AGENT_SYSTEM_PROMPT
    
    async def analyze_message(self, message: str, conversation_history: Optional[str] = None) -> Dict:
        """
        Analyze a scam message and return classification
        
        Returns:
        {
            "scam_type": ScamType,
            "risk_score": float,
            "red_flags": List[str],
            "recommended_persona": PersonaType,
            "reasoning": str
        }
        """
        
        # Build analysis prompt
        analysis_prompt = f"""Analyze this message for scam detection:

MESSAGE: {message}
"""
        
        if conversation_history:
            analysis_prompt += f"\nPREVIOUS CONTEXT: {conversation_history}\n"
        
        analysis_prompt += "\nProvide your analysis in JSON format as specified."
        
        try:
            if USE_OPENAI:
                response = await self._call_openai(analysis_prompt)
            elif USE_GEMINI:
                response = await self._call_gemini(analysis_prompt)
            else:
                # No API key - use rule-based fallback
                response = self._fallback_analysis(message)
            
            # Parse JSON response
            result = json.loads(response)
            
            # Validate and normalize
            result["scam_type"] = ScamType(result.get("scam_type", "other"))
            result["recommended_persona"] = PersonaType(result.get("recommended_persona", "cautious_middle_aged"))
            result["risk_score"] = float(result.get("risk_score", 0.5))
            result["red_flags"] = result.get("red_flags", [])
            result["reasoning"] = result.get("reasoning", "")
            
            return result
            
        except Exception as e:
            print(f"Detective Agent error: {e}")
            print("Falling back to rule-based analysis...")
            # Use fallback on ANY error
            try:
                response = self._fallback_analysis(message)
                result = json.loads(response)
                result["scam_type"] = ScamType(result.get("scam_type", "other"))
                result["recommended_persona"] = PersonaType(result.get("recommended_persona", "cautious_middle_aged"))
                result["risk_score"] = float(result.get("risk_score", 0.5))
                result["red_flags"] = result.get("red_flags", [])
                result["reasoning"] = result.get("reasoning", "")
                return result
            except:
                # Last resort defaults
                return {
                    "scam_type": ScamType.OTHER,
                    "risk_score": 0.7,
                    "red_flags": ["Unable to fully analyze"],
                    "recommended_persona": PersonaType.CAUTIOUS_MIDDLE_AGED,
                    "reasoning": f"Analysis error: {str(e)}"
                }
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API"""
        model = genai.GenerativeModel(self.model)
        full_prompt = f"{self.system_prompt}\n\n{prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    
    def _fallback_analysis(self, message: str) -> str:
        """Rule-based fallback analysis when no AI is available"""
        message_lower = message.lower()
        
        # Detect scam type based on keywords
        scam_type = ScamType.OTHER
        risk_score = 0.5
        red_flags = []
        persona = PersonaType.CAUTIOUS_MIDDLE_AGED
        
        # Loan scam detection
        if any(word in message_lower for word in ['loan', 'credit', 'processing fee', 'instant approval']):
            scam_type = ScamType.LOAN_SCAM
            risk_score = 0.85
            red_flags = ["Loan offer", "Processing fee mention"]
            persona = PersonaType.CAUTIOUS_MIDDLE_AGED
        
        # Prize scam detection
        elif any(word in message_lower for word in ['won', 'prize', 'lottery', 'congratulations', 'winner']):
            scam_type = ScamType.PRIZE_SCAM
            risk_score = 0.9
            red_flags = ["Prize claim", "Congratulations message"]
            persona = PersonaType.EAGER_YOUNG_ADULT
        
        # Investment fraud detection
        elif any(word in message_lower for word in ['investment', 'returns', 'profit', 'trading', 'stock']):
            scam_type = ScamType.INVESTMENT_FRAUD
            risk_score = 0.8
            red_flags = ["Investment opportunity", "High returns promise"]
            persona = PersonaType.BUSY_PROFESSIONAL
        
        # Job scam detection
        elif any(word in message_lower for word in ['job', 'hiring', 'work from home', 'earn money']):
            scam_type = ScamType.JOB_SCAM
            risk_score = 0.75
            red_flags = ["Job offer", "Work from home"]
            persona = PersonaType.EAGER_YOUNG_ADULT
        
        # Tech support scam
        elif any(word in message_lower for word in ['technical support', 'virus', 'account blocked', 'verify']):
            scam_type = ScamType.TECH_SUPPORT
            risk_score = 0.8
            red_flags = ["Tech support claim", "Account issue"]
            persona = PersonaType.SENIOR_CITIZEN
        
        # Cryptocurrency scam
        elif any(word in message_lower for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain']):
            scam_type = ScamType.CRYPTOCURRENCY
            risk_score = 0.85
            red_flags = ["Cryptocurrency mention"]
            persona = PersonaType.TECH_SAVVY_STUDENT
        
        # Additional red flags
        if any(word in message_lower for word in ['urgent', 'limited time', 'act now', 'hurry']):
            red_flags.append("Urgency tactics")
            risk_score = min(1.0, risk_score + 0.1)
        
        if any(word in message_lower for word in ['send money', 'transfer', 'payment', 'upi', 'account']):
            red_flags.append("Payment request")
            risk_score = min(1.0, risk_score + 0.1)
        
        result = {
            "scam_type": scam_type.value,
            "risk_score": risk_score,
            "red_flags": red_flags,
            "recommended_persona": persona.value,
            "reasoning": f"Rule-based analysis detected {scam_type.value} with {len(red_flags)} red flags"
        }
        
        return json.dumps(result)
