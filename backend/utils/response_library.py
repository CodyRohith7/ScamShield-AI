"""
Enhanced Response Library - 50+ diverse, human-like response templates
Ensures agent never repeats and sounds completely natural
"""

from typing import List, Dict
import random


class ResponseLibrary:
    """Comprehensive library of human-like responses for different personas"""
    
    def __init__(self):
        self.responses = self._load_response_templates()
        self.used_responses = set()  # Track used responses to avoid repetition
    
    def _load_response_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load all response templates organized by persona and context"""
        
        return {
            "elderly_person": {
                "initial_interest": [
                    "Oh my! This sounds very good. Can you please explain more slowly?",
                    "Beta, I am not very good with these things. Can you help me understand?",
                    "My grandson usually helps me with such matters, but he is not here. Please guide me.",
                    "I am a senior citizen, so please bear with me if I ask too many questions.",
                    "This is very interesting. I want to make sure I understand correctly.",
                    "God bless you for helping me. Can you repeat that please?",
                ],
                "showing_interest": [
                    "Yes yes, I am listening carefully. Please continue.",
                    "This will really help me. My pension is not much, you know.",
                    "I have some savings for my medical expenses. Will this work for that?",
                    "My children don't give me much time. It's good that you are helping.",
                    "I trust you beta. You sound like a nice person.",
                    "Can I call my daughter and ask her also? She handles my money.",
                ],
                "asking_questions": [
                    "But how do I do this payment? I only know basic phone use.",
                    "Is this safe? I don't want to lose my money.",
                    "Can you come to my house and help me? I will give you chai.",
                    "My neighbor also got some call like this. Is it the same thing?",
                    "I need to withdraw money from bank first. Can we do this tomorrow?",
                    "Will I get a receipt? I keep all my papers very carefully.",
                ],
                "hesitation": [
                    "Let me think about it. I will discuss with my son tonight.",
                    "I am a bit scared. What if something goes wrong?",
                    "Can I get this in writing? My eyesight is weak but I will show someone.",
                    "How do I know this is real? So many frauds happen these days.",
                    "My bank manager told me to be careful with phone calls.",
                    "I will pray and decide. God will guide me.",
                ],
                "stalling": [
                    "Actually, I need to take my medicine now. Can you call after 1 hour?",
                    "My daughter is coming to visit. Let me ask her first.",
                    "I don't have my glasses. I cannot see the phone properly.",
                    "There is some pooja at home. Can we talk tomorrow?",
                    "I need to check my bank passbook first. It's somewhere in my cupboard.",
                    "Let me finish my lunch first. Old people need to eat on time.",
                ]
            },
            
            "young_professional": {
                "initial_interest": [
                    "Interesting! Tell me more about this opportunity.",
                    "I've been looking for something like this. What's the catch?",
                    "Sounds good, but I need to understand the details first.",
                    "I'm always open to good opportunities. Explain the process.",
                    "Cool! How does this work exactly?",
                    "I'm intrigued. What do I need to do?",
                ],
                "showing_interest": [
                    "This could be perfect timing. I just got my salary.",
                    "I've been wanting to invest. Is this legit?",
                    "My friends have been talking about such opportunities.",
                    "I'm tired of my 9-5. This could be a game-changer.",
                    "The returns sound amazing. Too good to be true?",
                    "I'm in if this is genuine. I can afford to take some risk.",
                ],
                "asking_questions": [
                    "Do you have a website? I want to check reviews.",
                    "Can I see some testimonials or success stories?",
                    "What's the company registration number?",
                    "Is this SEBI registered? I'm careful with investments.",
                    "Can I get this offer in an email? I want to read the fine print.",
                    "How many people have already joined this?",
                ],
                "hesitation": [
                    "Hmm, I need to do some research first.",
                    "Let me check with my CA. I don't make hasty decisions.",
                    "This sounds like MLM. Is it?",
                    "I've heard about scams like this. How is yours different?",
                    "Why the urgency? Good opportunities don't expire in hours.",
                    "I'll need to see some documentation before committing.",
                ],
                "stalling": [
                    "I'm in a meeting right now. Can you WhatsApp me the details?",
                    "Let me finish work and call you back in the evening.",
                    "I need to check my bank balance first.",
                    "Send me an email. I'll review and get back to you.",
                    "I'm traveling this week. Can we connect next Monday?",
                    "Let me discuss with my partner first. It's a joint decision.",
                ]
            },
            
            "student": {
                "initial_interest": [
                    "Wow, this sounds cool! Is it real?",
                    "I could really use some extra money for my fees.",
                    "My parents don't give me much pocket money. This could help!",
                    "Is this like those work-from-home things I see on Instagram?",
                    "Bro, this better not be a scam. I'm broke already lol",
                    "Tell me more! I have exams but this sounds important.",
                ],
                "showing_interest": [
                    "Yaar, I really need money. My laptop just broke.",
                    "If this works, I can finally buy that phone I wanted!",
                    "My friends will be so jealous if I make this much money.",
                    "I can work on this between classes, right?",
                    "This is better than my part-time job at the cafe.",
                    "I'm in! What do I need to do?",
                ],
                "asking_questions": [
                    "Do I need to invest anything? I only have 2000 rupees.",
                    "Is this legal? I don't want to get in trouble.",
                    "Can I do this from my hostel? Internet is slow here.",
                    "How long will it take? I have assignments to submit.",
                    "Will my parents find out? They'll kill me if this is risky.",
                    "Do you have an Instagram page or something I can check?",
                ],
                "hesitation": [
                    "Idk man, sounds too good to be true.",
                    "My senior told me about a scam like this last month.",
                    "Let me ask in my college group. Someone might know about this.",
                    "I'm scared. What if I lose my money?",
                    "Can I start with a smaller amount first?",
                    "My dad will be so angry if this is fake.",
                ],
                "stalling": [
                    "I have a class in 10 minutes. Can we talk later?",
                    "Let me finish my exam first. It's tomorrow.",
                    "I need to ask my roommate. He knows about these things.",
                    "Can you send me a message? I'll check after my lecture.",
                    "I'm in the library. Can't talk now. Text me the details.",
                    "Let me think about it over the weekend.",
                ]
            },
            
            "housewife": {
                "initial_interest": [
                    "Really? This could help with household expenses!",
                    "I've been looking for ways to earn from home.",
                    "My husband doesn't give me enough money. This sounds good.",
                    "Can I do this while managing home and kids?",
                    "This is exactly what I need! Tell me more.",
                    "I saw something like this on Facebook. Is it the same?",
                ],
                "showing_interest": [
                    "I want to surprise my husband with this income!",
                    "My kids' school fees are so expensive. This will help.",
                    "I can finally buy things without asking my husband.",
                    "My kitty party friends will be so impressed!",
                    "I have some jewelry I can sell if needed for investment.",
                    "This is better than those boring cooking classes.",
                ],
                "asking_questions": [
                    "Is this safe? I don't want my husband to know initially.",
                    "How much time will this take daily? I'm very busy.",
                    "Can I do this on my phone? I don't have a laptop.",
                    "Will I need to go anywhere? I can't leave home much.",
                    "Is this like those Tupperware or Amway things?",
                    "Can my sister also join? We can do it together.",
                ],
                "hesitation": [
                    "I need to think. My husband handles all money matters.",
                    "What if he finds out and gets angry?",
                    "I'm not very educated. Will I be able to do this?",
                    "Let me ask my neighbor. She knows about such things.",
                    "I'm worried. What if something goes wrong?",
                    "Can I start after my daughter's exams? She needs my attention now.",
                ],
                "stalling": [
                    "I need to cook lunch now. Can you call in the evening?",
                    "My kids are back from school. Very noisy. Call me at 2 PM.",
                    "Let me finish my household work first.",
                    "My mother-in-law is here. I can't talk freely. Message me.",
                    "I'll discuss with my husband tonight and let you know tomorrow.",
                    "Give me your number. I'll call you when I'm free.",
                ]
            },
            
            "businessman": {
                "initial_interest": [
                    "I'm always looking for good investment opportunities. Go on.",
                    "What's the ROI on this? I need specifics.",
                    "I deal with crores. Is this worth my time?",
                    "My CA handles most investments, but I'm listening.",
                    "I've seen many schemes. What makes yours special?",
                    "Time is money. Give me the bottom line.",
                ],
                "showing_interest": [
                    "I can invest significant amounts if this checks out.",
                    "I have multiple businesses. This could be another revenue stream.",
                    "My portfolio needs diversification. This might fit.",
                    "I'm meeting my financial advisor tomorrow. I'll discuss this.",
                    "If the numbers make sense, I'm in. I move fast.",
                    "I have liquid cash available. What's the minimum investment?",
                ],
                "asking_questions": [
                    "What's the legal structure? Private limited? Partnership?",
                    "Show me the balance sheet and P&L statements.",
                    "Who are the other investors? Any notable names?",
                    "What's the exit strategy? I don't like being locked in.",
                    "Is this audited? I need proper documentation.",
                    "What are the tax implications? I'm in the 30% bracket.",
                ],
                "hesitation": [
                    "I'll need my lawyer to review the agreement.",
                    "Send me a detailed proposal. I'll have my team analyze it.",
                    "I don't make decisions on phone calls. Email me everything.",
                    "I've been burned before. I need solid proof.",
                    "Why are you calling me? How did you get my number?",
                    "I'll do my due diligence. This will take a week minimum.",
                ],
                "stalling": [
                    "I'm in a board meeting. Call my secretary for an appointment.",
                    "I'm traveling to Dubai next week. We'll talk after that.",
                    "Send everything to my office email. I'll review when I can.",
                    "I have back-to-back meetings today. Try me tomorrow.",
                    "My accountant handles these calls. Let me transfer you.",
                    "I'm at the golf club. This isn't the right time.",
                ]
            }
        }
    
    def get_response(
        self,
        persona_type: str,
        context: str,
        conversation_history: List[str] = None
    ) -> str:
        """
        Get a unique, context-appropriate response
        
        Args:
            persona_type: Type of persona (elderly_person, young_professional, etc.)
            context: Current conversation context (initial_interest, hesitation, etc.)
            conversation_history: Previous responses to avoid repetition
        
        Returns:
            str: Human-like response
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get available responses for this persona and context
        persona_responses = self.responses.get(persona_type, {})
        context_responses = persona_responses.get(context, [])
        
        if not context_responses:
            # Fallback to generic response
            return "I see. Can you tell me more about this?"
        
        # Filter out already used responses
        available_responses = [r for r in context_responses if r not in conversation_history]
        
        # If all responses used, reset and use any
        if not available_responses:
            available_responses = context_responses
        
        # Select random response
        response = random.choice(available_responses)
        
        return response
    
    def get_all_personas(self) -> List[str]:
        """Get list of all available personas"""
        return list(self.responses.keys())
    
    def get_contexts_for_persona(self, persona_type: str) -> List[str]:
        """Get all available contexts for a persona"""
        return list(self.responses.get(persona_type, {}).keys())


# Singleton instance
response_library = ResponseLibrary()
