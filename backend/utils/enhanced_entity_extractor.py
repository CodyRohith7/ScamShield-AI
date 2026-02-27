"""
Enhanced Entity Extractor - Extracts all entity types with separate fields
"""

import re
from typing import Dict, List, Set
from dataclasses import dataclass, asdict


@dataclass
class ExtractedEntities:
    """Structured entity extraction results"""
    names: List[str]
    emails: List[str]
    upi_ids: List[str]
    account_numbers: List[str]
    ifsc_codes: List[str]
    phone_numbers: List[str]
    phishing_links: List[str]
    bank_names: List[str]
    addresses: List[str]
    aadhaar_numbers: List[str]
    pan_numbers: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def count(self) -> int:
        """Total number of entities extracted"""
        return sum([
            len(self.names),
            len(self.emails),
            len(self.upi_ids),
            len(self.account_numbers),
            len(self.ifsc_codes),
            len(self.phone_numbers),
            len(self.phishing_links),
            len(self.bank_names),
            len(self.addresses),
            len(self.aadhaar_numbers),
            len(self.pan_numbers)
        ])


class EnhancedEntityExtractor:
    """Extract all types of entities from conversation text"""
    
    # Regex patterns for all entity types
    PATTERNS = {
        'upi_id': r'\b[\w\.-]+@[\w\.-]+\b',
        'phone': r'\+?91[-\s]?\d{10}|\b\d{10}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'url': r'https?://[^\s]+|www\.[^\s]+|bit\.ly/[^\s]+',
        'account_number': r'\b\d{9,18}\b',
        'ifsc': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
        'aadhaar': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        'pan': r'\b[A-Z]{5}\d{4}[A-Z]\b'
    }
    
    # Common Indian bank names
    BANK_NAMES = [
        'SBI', 'State Bank', 'HDFC', 'ICICI', 'Axis', 'Kotak', 'PNB', 'Punjab National',
        'Bank of Baroda', 'BOB', 'Canara', 'Union Bank', 'Indian Bank', 'Bank of India',
        'Central Bank', 'IDBI', 'Yes Bank', 'IndusInd', 'Federal Bank', 'RBL', 'Bandhan',
        'IDFC', 'Paytm Payments Bank', 'Airtel Payments Bank', 'Fino Payments Bank'
    ]
    
    # Common Indian names (for pattern matching)
    COMMON_NAMES = [
        'Rajesh', 'Amit', 'Suresh', 'Ramesh', 'Vijay', 'Kumar', 'Sharma', 'Singh',
        'Patel', 'Gupta', 'Verma', 'Agarwal', 'Jain', 'Reddy', 'Rao', 'Nair',
        'Priya', 'Anjali', 'Neha', 'Pooja', 'Ravi', 'Sanjay', 'Manoj', 'Deepak'
    ]
    
    def __init__(self):
        self.extracted_cache = {}
    
    def extract_all(self, text: str) -> ExtractedEntities:
        """Extract all entity types from text"""
        
        # Initialize empty lists
        entities = ExtractedEntities(
            names=[],
            emails=[],
            upi_ids=[],
            account_numbers=[],
            ifsc_codes=[],
            phone_numbers=[],
            phishing_links=[],
            bank_names=[],
            addresses=[],
            aadhaar_numbers=[],
            pan_numbers=[]
        )
        
        if not text:
            return entities
        
        # Extract each entity type
        entities.upi_ids = self._extract_upi_ids(text)
        entities.phone_numbers = self._extract_phone_numbers(text)
        entities.emails = self._extract_emails(text)
        entities.phishing_links = self._extract_urls(text)
        entities.account_numbers = self._extract_account_numbers(text)
        entities.ifsc_codes = self._extract_ifsc_codes(text)
        entities.aadhaar_numbers = self._extract_aadhaar(text)
        entities.pan_numbers = self._extract_pan(text)
        entities.bank_names = self._extract_bank_names(text)
        entities.names = self._extract_names(text)
        entities.addresses = self._extract_addresses(text)
        
        return entities
    
    def extract_from_conversation(self, messages: List[Dict]) -> ExtractedEntities:
        """Extract entities from entire conversation"""
        
        # Combine all messages
        full_text = " ".join([msg.get('content', '') for msg in messages])
        
        return self.extract_all(full_text)
    
    def _extract_upi_ids(self, text: str) -> List[str]:
        """Extract UPI IDs"""
        matches = re.findall(self.PATTERNS['upi_id'], text, re.IGNORECASE)
        
        # Filter to only valid UPI patterns
        upi_ids = []
        for match in matches:
            # Check if it has @ and common UPI handles
            if '@' in match and any(handle in match.lower() for handle in 
                ['paytm', 'ybl', 'okaxis', 'okicici', 'oksbi', 'okhdfcbank', 'okbizaxis', 'ibl', 'axl']):
                upi_ids.append(match)
        
        return list(set(upi_ids))  # Remove duplicates
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers"""
        matches = re.findall(self.PATTERNS['phone'], text)
        
        # Normalize phone numbers
        phones = []
        for match in matches:
            # Remove spaces and hyphens
            clean = re.sub(r'[-\s]', '', match)
            # Remove +91 prefix if present
            clean = re.sub(r'^\+?91', '', clean)
            
            # Validate length (should be 10 digits)
            if len(clean) == 10 and clean.isdigit():
                phones.append(clean)
        
        return list(set(phones))
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        matches = re.findall(self.PATTERNS['email'], text)
        
        # Filter out UPI IDs (they also match email pattern)
        emails = [m for m in matches if not any(handle in m.lower() for handle in 
            ['paytm', 'ybl', 'okaxis', 'okicici', 'oksbi', 'okhdfcbank'])]
        
        return list(set(emails))
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs/phishing links"""
        matches = re.findall(self.PATTERNS['url'], text, re.IGNORECASE)
        return list(set(matches))
    
    def _extract_account_numbers(self, text: str) -> List[str]:
        """Extract bank account numbers"""
        matches = re.findall(self.PATTERNS['account_number'], text)
        
        # Filter to likely account numbers (9-18 digits)
        accounts = []
        for match in matches:
            if 9 <= len(match) <= 18:
                # Exclude phone numbers (10 digits) and Aadhaar (12 digits)
                if len(match) not in [10, 12]:
                    accounts.append(match)
        
        return list(set(accounts))
    
    def _extract_ifsc_codes(self, text: str) -> List[str]:
        """Extract IFSC codes"""
        matches = re.findall(self.PATTERNS['ifsc'], text)
        return list(set(matches))
    
    def _extract_aadhaar(self, text: str) -> List[str]:
        """Extract Aadhaar numbers"""
        matches = re.findall(self.PATTERNS['aadhaar'], text)
        
        # Normalize format
        aadhaar = []
        for match in matches:
            # Remove spaces and hyphens
            clean = re.sub(r'[-\s]', '', match)
            if len(clean) == 12 and clean.isdigit():
                # Format as XXXX-XXXX-XXXX
                formatted = f"{clean[0:4]}-{clean[4:8]}-{clean[8:12]}"
                aadhaar.append(formatted)
        
        return list(set(aadhaar))
    
    def _extract_pan(self, text: str) -> List[str]:
        """Extract PAN numbers"""
        matches = re.findall(self.PATTERNS['pan'], text)
        return list(set(matches))
    
    def _extract_bank_names(self, text: str) -> List[str]:
        """Extract bank names"""
        banks = []
        text_upper = text.upper()
        
        for bank in self.BANK_NAMES:
            if bank.upper() in text_upper:
                banks.append(bank)
        
        return list(set(banks))
    
    def _extract_names(self, text: str) -> List[str]:
        """Extract person names"""
        names = []
        
        # Look for common Indian names
        for name in self.COMMON_NAMES:
            pattern = r'\b' + re.escape(name) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                names.append(name)
        
        # Look for name patterns (Mr./Mrs./Ms. followed by name)
        title_pattern = r'\b(Mr\.?|Mrs\.?|Ms\.?|Dr\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        title_matches = re.findall(title_pattern, text)
        for match in title_matches:
            names.append(match[1])  # Get the name part
        
        # Look for "I am [Name]" or "My name is [Name]"
        intro_pattern = r'\b(?:I am|my name is|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        intro_matches = re.findall(intro_pattern, text, re.IGNORECASE)
        names.extend(intro_matches)
        
        return list(set(names))
    
    def _extract_addresses(self, text: str) -> List[str]:
        """Extract addresses (basic pattern matching)"""
        addresses = []
        
        # Look for patterns like "123 Street Name, City"
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Nagar|Colony),?\s+[A-Za-z\s]+'
        matches = re.findall(address_pattern, text, re.IGNORECASE)
        addresses.extend(matches)
        
        # Look for Indian city names
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        for city in cities:
            if city in text:
                # Extract surrounding context as potential address
                pattern = r'[^.!?]*' + re.escape(city) + r'[^.!?]*'
                city_matches = re.findall(pattern, text, re.IGNORECASE)
                addresses.extend(city_matches)
        
        return list(set(addresses))[:5]  # Limit to 5 addresses
    
    def validate_entities(self, entities: ExtractedEntities) -> ExtractedEntities:
        """Validate and clean extracted entities"""
        
        # Remove invalid UPI IDs
        entities.upi_ids = [upi for upi in entities.upi_ids if self._is_valid_upi(upi)]
        
        # Remove invalid phone numbers
        entities.phone_numbers = [phone for phone in entities.phone_numbers if self._is_valid_phone(phone)]
        
        # Remove invalid emails
        entities.emails = [email for email in entities.emails if self._is_valid_email(email)]
        
        return entities
    
    def _is_valid_upi(self, upi: str) -> bool:
        """Validate UPI ID"""
        if '@' not in upi:
            return False
        parts = upi.split('@')
        return len(parts) == 2 and len(parts[0]) > 0 and len(parts[1]) > 0
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone number"""
        return len(phone) == 10 and phone.isdigit() and phone[0] in '6789'
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email"""
        return '@' in email and '.' in email.split('@')[1]


# Global instance
entity_extractor = EnhancedEntityExtractor()


def extract_entities(text: str) -> Dict:
    """Convenience function to extract entities"""
    entities = entity_extractor.extract_all(text)
    validated = entity_extractor.validate_entities(entities)
    return validated.to_dict()


def extract_from_conversation(messages: List[Dict]) -> Dict:
    """Extract entities from conversation messages"""
    entities = entity_extractor.extract_from_conversation(messages)
    validated = entity_extractor.validate_entities(entities)
    return validated.to_dict()
