import re
from typing import Dict

class DocumentProcessor:
    @staticmethod
    def extract_key_information(text: str) -> Dict:
        key_info = {}
        
        # Extract dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        key_info['dates'] = list(set(dates))[:10]
        
        # Extract dollar amounts
        money_pattern = r'\$[\d,]+(?:\.\d{2})?'
        amounts = re.findall(money_pattern, text)
        key_info['monetary_amounts'] = list(set(amounts))[:10]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        key_info['email_addresses'] = list(set(emails))
        
        # Extract phone numbers
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        key_info['phone_numbers'] = list(set(phones))
        
        return key_info
    
    @staticmethod
    def classify_document(filename: str, text: str) -> str:
        filename_lower = filename.lower()
        text_lower = text.lower()
        
        if any(word in filename_lower or word in text_lower[:1000] for word in 
               ['contract', 'agreement', 'terms', 'conditions']):
            return 'Contract/Agreement'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['motion', 'complaint', 'petition', 'brief', 'order', 'judgment']):
            return 'Court Filing'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['llc', 'corporation', 'incorporation', 'bylaws', 'board']):
            return 'Corporate Document'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['lease', 'deed', 'mortgage', 'property', 'real estate']):
            return 'Real Estate'
        elif any(word in filename_lower or word in text_lower[:1000] for word in 
                ['divorce', 'custody', 'prenuptial', 'marriage', 'child support']):
            return 'Family Law'
        else:
            return 'General Document'
