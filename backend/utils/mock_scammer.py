"""
Mock Scammer API - Simulates realistic scammer behavior
Generates AI-powered scammer responses for testing
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class MockScammerAPI:
    """Simulates realistic scammer responses for testing"""
    
    def __init__(self):
        self.scam_scenarios = self._load_scam_scenarios()
        self.response_templates = self._load_response_templates()
        
    def _load_scam_scenarios(self) -> Dict:
        """Load 2026 trending scam scenarios"""
        return {
            "ai_deepfake": {
                "name": "AI Deepfake Scam",
                "description": "Using AI-generated voices/videos to impersonate family members",
                "tactics": ["urgency", "emotional_manipulation", "voice_cloning"],
                "target_amount": "50000-500000"
            },
            "crypto_investment": {
                "name": "Cryptocurrency Investment Fraud",
                "description": "Fake crypto trading platforms promising guaranteed returns",
                "tactics": ["greed", "fomo", "fake_testimonials"],
                "target_amount": "10000-1000000"
            },
            "digital_arrest": {
                "name": "Digital Arrest Scam",
                "description": "Impersonating police/CBI claiming legal issues",
                "tactics": ["fear", "authority", "urgency"],
                "target_amount": "20000-200000"
            },
            "upi_qr": {
                "name": "UPI QR Code Scam",
                "description": "Sending payment QR instead of receiving money",
                "tactics": ["confusion", "technical_jargon", "urgency"],
                "target_amount": "500-50000"
            },
            "govt_scheme": {
                "name": "Fake Government Scheme",
                "description": "Fake PM schemes, subsidies, or benefits",
                "tactics": ["authority", "legitimacy", "limited_time"],
                "target_amount": "1000-100000"
            },
            "job_offer": {
                "name": "Fake Job Offer Scam",
                "description": "Work from home, data entry, or high-paying jobs",
                "tactics": ["greed", "desperation", "fake_documents"],
                "target_amount": "5000-50000"
            },
            "romance": {
                "name": "Romance/Dating Scam",
                "description": "Building fake relationships for financial gain",
                "tactics": ["emotional_manipulation", "long_game", "trust_building"],
                "target_amount": "10000-500000"
            },
            "tech_support": {
                "name": "Tech Support Scam",
                "description": "Fake Microsoft/Google support claiming virus/hack",
                "tactics": ["fear", "technical_jargon", "remote_access"],
                "target_amount": "5000-100000"
            },
            "courier_parcel": {
                "name": "Courier/Parcel Scam",
                "description": "Fake delivery notifications with customs/fees",
                "tactics": ["urgency", "legitimacy", "small_initial_payment"],
                "target_amount": "500-20000"
            },
            "social_media": {
                "name": "Social Media Impersonation",
                "description": "Fake celebrity/influencer accounts",
                "tactics": ["trust", "exclusivity", "giveaways"],
                "target_amount": "1000-100000"
            },
            "loan_approval": {
                "name": "Instant Loan Approval",
                "description": "Pre-approved loans requiring processing fees",
                "tactics": ["desperation", "urgency", "fake_documents"],
                "target_amount": "2000-50000"
            },
            "prize_lottery": {
                "name": "Prize/Lottery Scam",
                "description": "Fake KBC, lottery, or contest winnings",
                "tactics": ["greed", "excitement", "urgency"],
                "target_amount": "5000-50000"
            },
            "investment_scheme": {
                "name": "Ponzi/MLM Investment",
                "description": "Multi-level marketing or pyramid schemes",
                "tactics": ["greed", "social_proof", "fomo"],
                "target_amount": "10000-500000"
            },
            "rental_fraud": {
                "name": "Rental/Real Estate Fraud",
                "description": "Fake property listings or advance payments",
                "tactics": ["urgency", "scarcity", "fake_documents"],
                "target_amount": "10000-200000"
            },
            "charity_fraud": {
                "name": "Fake Charity Scam",
                "description": "Impersonating NGOs or disaster relief",
                "tactics": ["emotional_manipulation", "urgency", "legitimacy"],
                "target_amount": "500-50000"
            }
        }
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load diverse, human-like scammer response templates"""
        return {
            "initial_hook": [
                "Hello sir/madam, I have very good news for you!",
                "Congratulations! You have been selected for a special offer.",
                "URGENT: Your account requires immediate attention.",
                "Dear customer, this is regarding your recent application.",
                "Good news! Your request has been approved.",
                "Hello, I'm calling from {organization}. We have an important update.",
                "Sir, your {service} subscription is expiring today!",
                "Madam, we noticed suspicious activity on your account.",
            ],
            "urgency": [
                "This offer is valid only for today!",
                "You must act within the next 2 hours.",
                "If you don't respond now, your account will be blocked.",
                "Limited slots available, only 3 left!",
                "This is your last chance to claim this benefit.",
                "Immediate action required to avoid penalties.",
            ],
            "trust_building": [
                "We are a government-registered company.",
                "You can verify our details on our website.",
                "We have helped over 10,000 customers already.",
                "Your information is completely safe with us.",
                "We are authorized by RBI/SEBI/Government of India.",
                "Many of your neighbors have already benefited from this.",
            ],
            "payment_request": [
                "Just pay a small processing fee of Rs. {amount}.",
                "Transfer Rs. {amount} to this UPI ID: {upi}",
                "Send {amount} to confirm your booking.",
                "Pay {amount} as registration charges.",
                "Deposit {amount} for verification purposes.",
                "Transfer {amount} to activate your account.",
            ],
            "resistance_handling": [
                "Sir, I understand your concern, but this is 100% genuine.",
                "Madam, you can verify everything after payment.",
                "Don't worry, we will refund if you're not satisfied.",
                "This is a limited-time offer, you'll regret missing it.",
                "Other people are already benefiting, why miss out?",
                "I can show you proof if you want.",
            ],
            "pressure": [
                "Sir, the system will automatically cancel in 10 minutes.",
                "Madam, I'm trying to help you, but you need to decide now.",
                "If you don't pay now, you'll lose this opportunity forever.",
                "Your account will be permanently blocked if you delay.",
                "Legal action will be taken if you don't comply.",
            ],
            "fake_authority": [
                "I'm calling from Cyber Crime Department.",
                "This is Reserve Bank of India speaking.",
                "I'm from Income Tax Department.",
                "This is CBI investigation team.",
                "I'm calling from Supreme Court.",
                "This is Prime Minister's Office.",
            ],
            "emotional": [
                "Sir, your family member is in trouble!",
                "Your son has met with an accident.",
                "Your daughter is in police custody.",
                "Your mother is admitted in hospital.",
                "This money will help poor children.",
                "You're helping someone's life by doing this.",
            ]
        }
    
    def generate_scammer_response(
        self,
        victim_message: str,
        conversation_history: List[Dict],
        scam_type: str,
        turn_number: int
    ) -> Dict:
        """
        Generate realistic scammer response based on conversation context
        
        Returns structured JSON with scammer's message and metadata
        """
        
        # Determine scammer's strategy based on turn number
        if turn_number == 1:
            strategy = "initial_hook"
        elif turn_number <= 3:
            strategy = "trust_building"
        elif turn_number <= 5:
            strategy = "payment_request"
        elif turn_number <= 7:
            strategy = "resistance_handling"
        else:
            strategy = "pressure"
        
        # Check if victim is showing resistance
        resistance_keywords = ["no", "not interested", "scam", "fraud", "police", "report"]
        is_resistant = any(keyword in victim_message.lower() for keyword in resistance_keywords)
        
        if is_resistant:
            strategy = random.choice(["resistance_handling", "pressure", "fake_authority"])
        
        # Generate response
        response_template = random.choice(self.response_templates.get(strategy, ["Hello"]))
        
        # Add context-specific details
        scam_info = self.scam_scenarios.get(scam_type, {})
        response = self._customize_response(response_template, scam_type, scam_info)
        
        return {
            "scammer_message": response,
            "scam_type": scam_type,
            "strategy_used": strategy,
            "turn_number": turn_number,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "tactics": scam_info.get("tactics", []),
                "is_resistant_victim": is_resistant,
                "escalation_level": min(turn_number, 10)
            }
        }
    
    def _customize_response(self, template: str, scam_type: str, scam_info: Dict) -> str:
        """Customize response template with scam-specific details"""
        
        # Sample data for customization
        organizations = ["HDFC Bank", "State Bank", "Paytm", "PhonePe", "Google Pay", "Amazon", "Flipkart"]
        services = ["Prime membership", "credit card", "debit card", "UPI", "account"]
        amounts = ["999", "1999", "2999", "4999", "9999"]
        upi_ids = [
            f"{random.choice(['raj', 'amit', 'priya', 'suresh'])}@paytm",
            f"{random.choice(['kumar', 'singh', 'sharma', 'verma'])}{random.randint(100,999)}@phonepe",
            f"{random.randint(9000000000, 9999999999)}@ybl"
        ]
        
        response = template.replace("{organization}", random.choice(organizations))
        response = response.replace("{service}", random.choice(services))
        response = response.replace("{amount}", random.choice(amounts))
        response = response.replace("{upi}", random.choice(upi_ids))
        
        return response
    
    def get_scam_scenario_info(self, scam_type: str) -> Optional[Dict]:
        """Get detailed information about a scam scenario"""
        return self.scam_scenarios.get(scam_type)
    
    def list_all_scam_types(self) -> List[Dict]:
        """List all available scam scenarios"""
        return [
            {
                "type": key,
                "name": value["name"],
                "description": value["description"]
            }
            for key, value in self.scam_scenarios.items()
        ]


# Singleton instance
mock_scammer_api = MockScammerAPI()
