"""
Rule-Based Engine for ScamShield AI
Provides deterministic, high-quality scambaiting responses when AI APIs are unavailable.
"""

import random
import re

class RuleEngine:
    def __init__(self):
        self.scam_types = {
            "loan": ["loan", "approved", "quickcash", "interest", "credit"],
            "prize": ["winner", "lottery", "big bazaar", "prize", "won", "gift"],
            "investment": ["investment", "trading", "returns", "profit", "stock", "guaranteed"],
            "kyc": ["kyc", "bank", "blocked", "frozen", "sbi", "otp", "aadhaar", "pan"]
        }
        
        # Responses meant to waste time and act like a believable victim
        self.responses = {
            "loan": [
                "Oh my god, I really need this money! My car broke down yesterday. How do I apply?",
                "Is it really instant? I've been rejected by 3 banks this week. Please help me.",
                "I'm looking at the processing fee... is there any discount? I only have 500 in my account right now.",
                "Okay, I'm trying to pay the fee but my GPay is showing 'Bank Server Busy'. Can you wait 5 minutes?",
                "I sent the money! Did you get it? My name is Ramesh. Check your account please."
            ],
            "prize": [
                "REALLY?! I never win anything! This is the best day of my life!",
                "iPhone 15 Pro Max? My daughter has been asking for one for her birthday! How do I get it?",
                "I went to the website but it says '404 not found'. Is the link correct?",
                "Wait, processing fee for a prize? Can't you just deduct it from the 5 lakh rupees?",
                "I'm at the bank now to withdraw the 5000. Give me 10 minutes, there's a long queue."
            ],
            "investment": [
                "25% monthly? That's way better than my FD! Tell me more please.",
                "I have 50,000 saved for my son's college. Can I invest all of it for the Platinum plan?",
                "Ramesh Kumar from Delhi? I think I know him! Is he the one with the blue car?",
                "I'm trying to add the UPI ID as a beneficiary but it says 'Invalid format'. Check it again?",
                "My husband is saying this might be too good to be true. Convince him please, he's very stubborn."
            ],
            "kyc": [
                "WHAT?! My account will be blocked? But I have my salary coming tomorrow!",
                "I'm trying to find my PAN card, I think my wife put it somewhere. One second...",
                "The 16 digit number... okay, it's 4592... wait, I dropped the card. Hold on.",
                "I got the OTP! It's... 7... 2... wait, another message came. Which one is it?",
                "Sir, why are you shouting? I'm trying my best! The internet is very slow in my village."
            ],
            "generic": [
                "Hello? Who is this? Are you from the government?",
                "I'm interested, but I'm a bit busy at work. Can we talk over chat instead of call?",
                "Can you send me your office address? I want to come and meet you in person.",
                "Wait, I think I know your voice. Did you call me last year about the LIC policy?",
                "I'm trying to follow your instructions but my phone screen is cracked. Can you type slowly?"
            ]
        }

    def detect_scam_type(self, message):
        message = message.lower()
        for scam_type, keywords in self.scam_types.items():
            if any(keyword in message for keyword in keywords):
                return scam_type
        return "generic"

    def get_response(self, message, history=None):
        scam_type = self.detect_scam_type(message)
        
        # If history exists, try to progress the "story"
        turn_number = len(history) // 2 if history else 0
        
        options = self.responses.get(scam_type, self.responses["generic"])
        
        # Pick response based on turn number if possible, else random
        index = min(turn_number, len(options) - 1)
        response = options[index]
        
        # Extraction logic using centralized utility
        from utils.extraction import extractor
        extracted_data = extractor.extract_all(message)
        
        risk_score = 30
        if scam_type != "generic":
            risk_score = 85
        if "otp" in message.lower() or "pay" in message.lower() or "cvv" in message.lower():
            risk_score = 98

        return {
            "success": True,
            "agent_response": response,
            "entities": extracted_data,
            "risk_score": risk_score,
            "scam_type": scam_type,
            "persona_used": "Rule-Based fallback"
        }

rule_engine = RuleEngine()
