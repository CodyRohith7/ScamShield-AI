import re
from typing import List, Dict, Optional
from models.schemas import ExtractedEntities, BankAccount


class EntityExtractor:
    """Extract fraud-related entities from text using regex and NLP"""
    
    # Regex patterns for entity extraction
    UPI_PATTERN = r'\b[\w\.-]+@[\w\.-]+\b'  # username@bank or phone@paytm
    PHONE_PATTERN = r'(?:\+91|91)?[\s-]?[6-9]\d{9}'  # Indian phone numbers
    ACCOUNT_NUMBER_PATTERN = r'\b\d{10,18}\b'  # Bank account numbers
    IFSC_PATTERN = r'\b[A-Z]{4}0[A-Z0-9]{6}\b'  # IFSC codes
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'  # URLs
    
    # Common UPI handles
    UPI_HANDLES = ['paytm', 'ybl', 'oksbi', 'okhdfcbank', 'okicici', 'okaxis', 'ibl', 'axl']
    
    def __init__(self):
        self.extracted_all_time: ExtractedEntities = ExtractedEntities()
    
    def extract_from_text(self, text: str) -> ExtractedEntities:
        """Extract all entities from a single text message"""
        entities = ExtractedEntities()
        
        # Extract UPI IDs
        entities.upi_ids = self._extract_upi_ids(text)
        
        # Extract phone numbers
        entities.phone_numbers = self._extract_phone_numbers(text)
        
        # Extract bank accounts and IFSC
        entities.bank_accounts = self._extract_bank_accounts(text)
        
        # Extract URLs (phishing links)
        entities.phishing_links = self._extract_urls(text)
        
        # Extract names (simple heuristic)
        entities.aliases = self._extract_names(text)
        
        # Extract organization names
        entities.fake_organizations = self._extract_organizations(text)
        
        return entities
    
    def _extract_upi_ids(self, text: str) -> List[str]:
        """Extract UPI IDs from text"""
        upi_ids = []
        
        # Find all potential UPI IDs
        matches = re.findall(self.UPI_PATTERN, text, re.IGNORECASE)
        
        for match in matches:
            # Check if it's a valid UPI format
            if '@' in match:
                parts = match.split('@')
                if len(parts) == 2:
                    handle = parts[1].lower()
                    # Check if it's a known UPI handle or looks like one
                    if any(h in handle for h in self.UPI_HANDLES) or len(handle) <= 15:
                        upi_ids.append(match.lower())
        
        # Also check for phone@bank format
        phone_upi_pattern = r'\b[6-9]\d{9}@\w+\b'
        phone_upis = re.findall(phone_upi_pattern, text, re.IGNORECASE)
        upi_ids.extend([u.lower() for u in phone_upis])
        
        return list(set(upi_ids))  # Remove duplicates
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract Indian phone numbers from text"""
        phones = []
        
        matches = re.findall(self.PHONE_PATTERN, text)
        
        for match in matches:
            # Clean up the phone number
            phone = re.sub(r'[\s-]', '', match)
            
            # Normalize to +91 format
            if phone.startswith('91') and len(phone) == 12:
                phone = '+' + phone
            elif phone.startswith('+91'):
                pass
            elif len(phone) == 10:
                phone = '+91' + phone
            
            if phone.startswith('+91') and len(phone) == 13:
                phones.append(phone)
        
        return list(set(phones))
    
    def _extract_bank_accounts(self, text: str) -> List[BankAccount]:
        """Extract bank account numbers and IFSC codes"""
        accounts = []
        
        # Find account numbers
        account_numbers = re.findall(self.ACCOUNT_NUMBER_PATTERN, text)
        
        # Find IFSC codes
        ifsc_codes = re.findall(self.IFSC_PATTERN, text, re.IGNORECASE)
        
        # Try to pair them
        if account_numbers and ifsc_codes:
            for i, acc_num in enumerate(account_numbers):
                ifsc = ifsc_codes[i] if i < len(ifsc_codes) else None
                bank_name = self._get_bank_name_from_ifsc(ifsc) if ifsc else None
                
                accounts.append(BankAccount(
                    account_number=acc_num,
                    ifsc=ifsc.upper() if ifsc else None,
                    bank_name=bank_name,
                    confidence=0.9 if ifsc else 0.7
                ))
        elif account_numbers:
            # Account numbers without IFSC
            for acc_num in account_numbers:
                accounts.append(BankAccount(
                    account_number=acc_num,
                    confidence=0.6
                ))
        
        return accounts
    
    def _get_bank_name_from_ifsc(self, ifsc: str) -> Optional[str]:
        """Get bank name from IFSC code"""
        if not ifsc or len(ifsc) < 4:
            return None
        
        bank_codes = {
            'SBIN': 'State Bank of India',
            'HDFC': 'HDFC Bank',
            'ICIC': 'ICICI Bank',
            'AXIS': 'Axis Bank',
            'PUNB': 'Punjab National Bank',
            'UBIN': 'Union Bank of India',
            'CNRB': 'Canara Bank',
            'BARB': 'Bank of Baroda',
            'IDIB': 'Indian Bank',
            'IOBA': 'Indian Overseas Bank',
            'UTIB': 'Axis Bank',
            'KKBK': 'Kotak Mahindra Bank',
            'YESB': 'Yes Bank',
        }
        
        code = ifsc[:4].upper()
        return bank_codes.get(code, f"Unknown Bank ({code})")
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs (potential phishing links)"""
        urls = re.findall(self.URL_PATTERN, text, re.IGNORECASE)
        return list(set(urls))
    
    def _extract_names(self, text: str) -> List[str]:
        """Extract potential names (simple heuristic)"""
        names = []
        
        # Look for common patterns like "I am X" or "My name is X" or "Mr./Ms. X"
        patterns = [
            r'(?:I am|my name is|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:Mr\.|Ms\.|Mrs\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:contact|call)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            names.extend(matches)
        
        # Filter out common words that aren't names
        common_words = {'Sir', 'Madam', 'Hello', 'Please', 'Thank', 'Welcome'}
        names = [n for n in names if n not in common_words and len(n) > 2]
        
        return list(set(names))
    
    def _extract_organizations(self, text: str) -> List[str]:
        """Extract organization/company names"""
        orgs = []
        
        # Look for patterns like "X Pvt Ltd", "X Limited", "X Bank", etc.
        patterns = [
            r'([A-Z][A-Za-z\s]+(?:Pvt\.?\s+Ltd\.?|Limited|Bank|Finance|Loans?|Services?))',
            r'([A-Z][A-Za-z\s]+(?:Company|Corporation|Enterprises?))',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            orgs.extend(matches)
        
        # Clean up
        orgs = [org.strip() for org in orgs if len(org.strip()) > 5]
        
        return list(set(orgs))
    
    def merge_entities(self, new_entities: ExtractedEntities) -> ExtractedEntities:
        """Merge new entities with existing ones"""
        merged = ExtractedEntities()
        
        # Merge UPI IDs
        all_upi = set(self.extracted_all_time.upi_ids + new_entities.upi_ids)
        merged.upi_ids = list(all_upi)
        
        # Merge phone numbers
        all_phones = set(self.extracted_all_time.phone_numbers + new_entities.phone_numbers)
        merged.phone_numbers = list(all_phones)
        
        # Merge bank accounts (more complex - avoid duplicates)
        all_accounts = self.extracted_all_time.bank_accounts + new_entities.bank_accounts
        seen_accounts = set()
        unique_accounts = []
        for acc in all_accounts:
            if acc.account_number not in seen_accounts:
                seen_accounts.add(acc.account_number)
                unique_accounts.append(acc)
        merged.bank_accounts = unique_accounts
        
        # Merge URLs
        all_urls = set(self.extracted_all_time.phishing_links + new_entities.phishing_links)
        merged.phishing_links = list(all_urls)
        
        # Merge aliases
        all_aliases = set(self.extracted_all_time.aliases + new_entities.aliases)
        merged.aliases = list(all_aliases)
        
        # Merge organizations
        all_orgs = set(self.extracted_all_time.fake_organizations + new_entities.fake_organizations)
        merged.fake_organizations = list(all_orgs)
        
        # Update all-time extracted
        self.extracted_all_time = merged
        
        return merged
    
    def get_extraction_summary(self) -> Dict[str, int]:
        """Get summary of all extracted entities"""
        return {
            "upi_ids": len(self.extracted_all_time.upi_ids),
            "phone_numbers": len(self.extracted_all_time.phone_numbers),
            "bank_accounts": len(self.extracted_all_time.bank_accounts),
            "phishing_links": len(self.extracted_all_time.phishing_links),
            "aliases": len(self.extracted_all_time.aliases),
            "fake_organizations": len(self.extracted_all_time.fake_organizations),
        }
