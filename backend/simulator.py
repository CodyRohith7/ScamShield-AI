"""
Traffic Simulator Module
Generates synthetic background noise (scam conversations) to populate the honeypot.
Useful for demonstrations and testing graph visualization.
"""

import random
import time
from simple_agent import SimpleScamAgent
from database import db
from datetime import datetime

class TrafficSimulator:
    def __init__(self):
        self.agent = SimpleScamAgent() # The Victim
        
    def generate_scam_opener(self):
        """Generate a random scam opening message"""
        scams = [
            ("Dear customer, your SBI account is blocked. update PAN immediately at http://sbi-kyc-update.com", "loan_approval"),
            ("Congratulation! You won Rs. 25 Lakhs in KBC Lottery. Call Mr. Rana 9876543210 for claim.", "prize_lottery"),
            ("Hello sir, I am calling from FedEx. Investigating parcel with illegal items sent to Taiwan.", "digital_arrest"),
            ("Work from home job offer. Earn 5000/day. Just like videos. Message on Telegram.", "job_offer"),
            ("Urgent electricity bill unpaid. Power cut in 2 hours. Pay 15 rs verification.", "impersonation")
        ]
        return random.choice(scams)

    def run_simulation(self, count=3):
        """Run a simulation of N conversations"""
        results = []
        
        for i in range(count):
            opener_text, scam_type = self.generate_scam_opener()
            
            # Start new conversation
            conv_id = db.create_conversation(scam_type)
            
            # Message 1: Scammer
            db.add_message(conv_id, "scammer", opener_text)
            
            # Message 2: Agent (Victim) response
            # We re-init agent to get a fresh random persona
            agent = SimpleScamAgent() 
            response = agent.generate_response(opener_text, [])
            
            db.add_message(
                conv_id, 
                "agent", 
                response['agent_response'], 
                response.get('internal_reasoning', ''),
                response.get('persona_used', 'Unknown'),
                response.get('risk_score', 0)
            )
            
            # Extract and save entities
            if response.get('entities'):
                for entity_type, values in response['entities'].items():
                    for value in values:
                        db.add_entity(conv_id, entity_type, value)
            
            # Simulate a short back-and-forth (Mocking the scammer's 2nd reply)
            scammer_reply = "Yes correct sir. Please send UPI payment to 9876543210@ybl for processing."
            db.add_message(conv_id, "scammer", scammer_reply)
            
            # Message 3: Agent Response to Reply
            response_2 = agent.generate_response(scammer_reply, [
                {"role": "scammer", "content": opener_text},
                {"role": "model", "content": response['agent_response']}
            ])
            
            db.add_message(
                 conv_id, 
                "agent", 
                response_2['agent_response'], 
                response_2.get('internal_reasoning', ''),
                response_2.get('persona_used', 'Unknown'),
                response_2.get('risk_score', 0.8)
            )
            
            if response_2.get('entities'):
                for entity_type, values in response_2['entities'].items():
                    for value in values:
                        db.add_entity(conv_id, entity_type, value)
            
            results.append(f"Simulated Chat #{conv_id} ({scam_type})")
            
        return results

# Singleton
simulator = TrafficSimulator()
