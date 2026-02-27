"""
Extraction Utility for ScamShield AI
Provides robust regex-based extraction for financial identifiers and phishing links.
"""

import re
from typing import Dict, List

class EntityExtractor:
    def __init__(self):
        # Compiled Regex Patterns for better performance
        self.patterns = {
            # standard 10-digit Indian mobile numbers
            "phone_number": re.compile(r'\b[6-9]\d{9}\b'),
            
            # UPI IDs: username@bankname or username@upi
            "upi_id": re.compile(r'\b[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}\b'),
            
            # Bank Account: 9-18 digits (covers most Indian banks)
            # We look for context like "account", "ac no", "acc" to avoid false positive random numbers
            "bank_account": re.compile(r'(?:account|ac|no|number|a/c)[\s:.-]*(\d{9,18})\b', re.IGNORECASE),
            
            # IFSC Code: 4 chars + 0 + 6 chars (e.g., SBIN0001234)
            "ifsc_code": re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b'),
            
            # Phishing Links: http/https or www matches
            "phishing_links": re.compile(r'(https?://\S+|www\.\S+)', re.IGNORECASE)
        }

    def extract_all(self, text: str) -> Dict[str, List[str]]:
        """
        Extract all known entities from the text.
        Returns a dictionary with lists of found entities.
        """
        entities = {}
        
        # 1. Standard Pattern Matching
        for key, pattern in self.patterns.items():
            matches = pattern.findall(text)
            # Remove duplicates while preserving order
            entities[key] = list(dict.fromkeys(matches))
            
        # 2. Heuristic Cleanup for Bank Accounts 
        # (If regex missed the capture group but matched the whole string, fix it)
        # Actually our bank regex captures the number in group 1.
        # Let's run a simpler regex for pure numbers if the context-aware one fails, 
        # but only if we are sure it looks like a bank request context.
        
        # Simpler bank account fallback (just long strings of digits if 'bank' is mentioned)
        if "bank" in text.lower() or "transfer" in text.lower():
            simple_accs = re.findall(r'\b\d{9,18}\b', text)
            # Filter out phone numbers (10 digits starting with 6-9) from bank accounts
            filtered_accs = [
                acc for acc in simple_accs 
                if not (len(acc) == 10 and int(acc[0]) >= 6)
            ]
            
            # Formatting Note: The previous context-aware regex returns tuples if groups exist.
            # findall with groups returns the group.
            
            # Let's merge standard capture with fallback
            current_accs = entities.get("bank_account", [])
            merged_accs = list(set(current_accs + filtered_accs))
            entities["bank_account"] = merged_accs

        return entities

# Singleton instance
extractor = EntityExtractor()
