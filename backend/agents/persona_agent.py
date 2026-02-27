import os
from typing import Optional
from models.schemas import PersonaType, ScamType, ConversationPhase
from utils.prompts import get_persona_agent_prompt

# Check which AI provider to use
USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None
USE_GEMINI = os.getenv("GEMINI_API_KEY") is not None

if USE_OPENAI:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class PersonaAgent:
    """
    Persona Agent: Engages with scammers using believable personas
    to extract intelligence while maintaining cover
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model if USE_OPENAI else "gemini-pro"
    
    async def generate_response(
        self,
        scammer_message: str,
        persona: PersonaType,
        scam_type: ScamType,
        phase: ConversationPhase,
        turn_number: int,
        conversation_context: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Generate a persona-based response to scammer
        
        Returns:
            (response_message, internal_reasoning)
        """
        
        # Get dynamic prompt based on context
        system_prompt = get_persona_agent_prompt(
            persona=persona,
            scam_type=scam_type,
            phase=phase.value,
            turn_number=turn_number
        )
        
        # Build user prompt
        user_prompt = f"SCAMMER'S MESSAGE: {scammer_message}\n\n"
        
        if conversation_context:
            user_prompt += f"PREVIOUS CONVERSATION:\n{conversation_context}\n\n"
        
        user_prompt += "Your response (stay in character, keep it natural and short):"
        
        try:
            if USE_OPENAI:
                response, reasoning = await self._call_openai(system_prompt, user_prompt)
            elif USE_GEMINI:
                response, reasoning = await self._call_gemini(system_prompt, user_prompt)
            else:
                response, reasoning = self._fallback_response(scammer_message, persona, phase)
            
            return response, reasoning
            
        except Exception as e:
            print(f"Persona Agent error: {e}")
            # Fallback response
            return self._fallback_response(scammer_message, persona, phase)
    
    async def _call_openai(self, system_prompt: str, user_prompt: str) -> tuple[str, str]:
        """Call OpenAI API"""
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,  # Higher temperature for more natural, varied responses
            max_tokens=150
        )
        
        message = response.choices[0].message.content.strip()
        
        # Generate reasoning (what the agent is thinking)
        reasoning = f"Persona: {system_prompt.split('You are playing the role of')[1].split('.')[0] if 'You are playing' in system_prompt else 'Unknown'}. Strategy: Engaging naturally to extract information."
        
        return message, reasoning
    
    async def _call_gemini(self, system_prompt: str, user_prompt: str) -> tuple[str, str]:
        """Call Google Gemini API"""
        model = genai.GenerativeModel(self.model)
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = model.generate_content(full_prompt)
        
        message = response.text.strip()
        reasoning = "Gemini-powered persona response generated"
        
        return message, reasoning
    
    def _fallback_response(
        self,
        scammer_message: str,
        persona: PersonaType,
        phase: ConversationPhase
    ) -> tuple[str, str]:
        """Generate fallback response when AI is unavailable"""
        
        message_lower = scammer_message.lower()
        
        # Phase-based responses
        if phase == ConversationPhase.TRUST_BUILDING:
            responses = {
                PersonaType.CAUTIOUS_MIDDLE_AGED: [
                    "This sounds interesting, but can you tell me more about how this works?",
                    "Hmm, I'm not sure I understand. Is this really genuine?",
                    "My son told me to be careful with these things. Can you explain properly?"
                ],
                PersonaType.EAGER_YOUNG_ADULT: [
                    "Wow really?? That sounds amazing! Tell me more!",
                    "OMG this is so cool! How does it work?",
                    "Yes yes! I'm interested! What do I need to do?"
                ],
                PersonaType.BUSY_PROFESSIONAL: [
                    "Interesting. I'm quite busy though. Can you send me the details?",
                    "I might be interested. What's the process?",
                    "Okay, but I need this to be quick. What are the next steps?"
                ],
                PersonaType.SENIOR_CITIZEN: [
                    "Beta, I don't understand properly. Can you explain slowly?",
                    "What is this? I am old person, please tell me clearly",
                    "My grandson usually helps me with these things. Is this safe?"
                ],
                PersonaType.TECH_SAVVY_STUDENT: [
                    "Interesting concept. What's the technology behind this?",
                    "Sounds good but I need to verify first. Got any official links?",
                    "I'm a student so budget is tight. Tell me more about this"
                ]
            }
        
        elif phase == ConversationPhase.INFORMATION_GATHERING:
            responses = {
                PersonaType.CAUTIOUS_MIDDLE_AGED: [
                    "Okay, I think I want to proceed. What payment method do you accept?",
                    "How do I send the money? I have Paytm and Google Pay",
                    "Can you send me your account details? I will transfer"
                ],
                PersonaType.EAGER_YOUNG_ADULT: [
                    "Alright let's do this! Where should I send the payment?",
                    "Cool! What's your UPI ID? I'll pay right now",
                    "Send me the link or account number, I'm ready!"
                ],
                PersonaType.BUSY_PROFESSIONAL: [
                    "Just send me your UPI ID or account details, I'll handle it",
                    "What's the payment method? I prefer UPI",
                    "Send me the details directly, I have a meeting soon"
                ],
                PersonaType.SENIOR_CITIZEN: [
                    "How to send money? I have phone pe, my grandson installed it",
                    "Please tell me step by step. What is your account number?",
                    "I will ask my son to help me pay. Send me the details"
                ],
                PersonaType.TECH_SAVVY_STUDENT: [
                    "Alright, what's your UPI? I'll send it",
                    "Do you accept crypto? Or just UPI/bank transfer?",
                    "Send me the payment link or QR code"
                ]
            }
        
        elif phase == ConversationPhase.INTELLIGENCE_EXTRACTION:
            responses = {
                PersonaType.CAUTIOUS_MIDDLE_AGED: [
                    "I tried to pay but it's not working. Can you send another UPI ID?",
                    "My bank is asking for IFSC code also. What is your IFSC?",
                    "The payment failed. Do you have another account number?"
                ],
                PersonaType.EAGER_YOUNG_ADULT: [
                    "Bro the UPI is not working! Send me another one quick!",
                    "Payment failed yaar. Got any other account?",
                    "This link is not opening. Send me a different link?"
                ],
                PersonaType.BUSY_PROFESSIONAL: [
                    "Transaction failed. Send alternative payment details",
                    "Your UPI seems inactive. Provide another method",
                    "I need your bank account and IFSC for NEFT"
                ],
                PersonaType.SENIOR_CITIZEN: [
                    "Beta it's showing error. What to do now?",
                    "I am trying but not working. Give me your phone number, my son will call",
                    "This is too confusing. Send me simple account number"
                ],
                PersonaType.TECH_SAVVY_STUDENT: [
                    "Getting an error. Is your UPI verified?",
                    "Send me your website link, I want to check reviews first",
                    "Payment gateway seems down. Got a backup method?"
                ]
            }
        
        else:  # SAFE_EXIT
            responses = {
                PersonaType.CAUTIOUS_MIDDLE_AGED: [
                    "Let me check with my family first. I will call you back",
                    "I need to think about this. Give me some time",
                    "My network is having issues. I will try later"
                ],
                PersonaType.EAGER_YOUNG_ADULT: [
                    "Okay let me talk to my parents first. Will get back to you!",
                    "My phone battery is dying. I'll message you later",
                    "Got to go now, will do this tomorrow for sure!"
                ],
                PersonaType.BUSY_PROFESSIONAL: [
                    "I have to jump on a call. Will handle this later",
                    "Something urgent came up. I'll get back to you",
                    "Let me check my account balance first. Will update you"
                ],
                PersonaType.SENIOR_CITIZEN: [
                    "Beta I am tired now. I will do tomorrow",
                    "My grandson is coming, he will help me later",
                    "I need to rest now. Thank you beta"
                ],
                PersonaType.TECH_SAVVY_STUDENT: [
                    "Got a class now. Will ping you later",
                    "Need to verify a few things first. Catch you later",
                    "Let me do some research. Will get back"
                ]
            }
        
        # Select appropriate response
        persona_responses = responses.get(persona, responses[PersonaType.CAUTIOUS_MIDDLE_AGED])
        
        # Simple selection based on message content
        if 'pay' in message_lower or 'money' in message_lower or 'transfer' in message_lower:
            response = persona_responses[0]
        elif 'account' in message_lower or 'upi' in message_lower:
            response = persona_responses[1] if len(persona_responses) > 1 else persona_responses[0]
        else:
            response = persona_responses[-1]
        
        reasoning = f"Fallback response for {persona.value} in {phase.value} phase"
        
        return response, reasoning
