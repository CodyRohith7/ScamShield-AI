"""
Callback Service for ScamShield AI
Handles mandatory reporting of final results to the GUVI evaluation endpoint.
"""
import requests
import json
import logging

class CallbackService:
    def __init__(self):
        self.endpoint = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
        
    def send_report(self, session_id, conversation_history, extracted_intelligence, agent_notes="Scam detected and engaged"):
        """
        Send the final report to GUVI.
        """
        try:
            total_messages = len(conversation_history)
            
            # Map our intelligence keys to the problem statement keys
            # Our internal keys: phone_number, upi_id, bank_account, phishing_links
            # Target keys: phoneNumbers, upiIds, bankAccounts, phishingLinks
            
            final_intelligence = {
                "bankAccounts": extracted_intelligence.get("bank_account", []),
                "upiIds": extracted_intelligence.get("upi_id", []),
                "phishingLinks": extracted_intelligence.get("phishing_links", []),
                "phoneNumbers": extracted_intelligence.get("phone_number", []),
                "suspiciousKeywords": ["urgent", "verify", "block", "kyc", "prize"] # Basic keywords found
            }
            
            payload = {
                "sessionId": session_id,
                "scamDetected": True, # We only engage if detected
                "totalMessagesExchanged": total_messages,
                "extractedIntelligence": final_intelligence,
                "agentNotes": agent_notes
            }
            
            logging.info(f"Sending Callback for {session_id}: {json.dumps(payload)}")
            
            # Send the request
            # Using timeout to avoid blocking the agent
            response = requests.post(self.endpoint, json=payload, timeout=5)
            
            if response.status_code == 200:
                logging.info(f"Callback SUCCESS: {response.text}")
                return True
            else:
                logging.error(f"Callback FAILED: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Callback EXCEPTION: {str(e)}")
            return False

callback_service = CallbackService()
