import re
import hashlib
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json

class DocumentProcessor:
    
    def __init__(self):
        self.legal_entities = [
            'corporation', 'llc', 'partnership', 'limited liability company',
            'inc', 'corp', 'co', 'ltd', 'company', 'firm', 'associates',
            'law firm', 'legal services', 'attorneys at law'
        ]
        
        self.legal_terms = [
            'whereas', 'heretofore', 'aforementioned', 'pursuant to',
            'notwithstanding', 'thereunder', 'hereinafter', 'stipulate',
            'covenant', 'indemnify', 'breach', 'default', 'remedy',
            'jurisdiction', 'governing law', 'force majeure', 'liability'
        ]
        
        self.contract_types = {
            'employment': ['employment', 'job', 'salary', 'benefits', 'termination', 'resignation'],
            'service': ['services', 'consulting', 'professional', 'engagement', 'scope of work'],
            'purchase': ['purchase', 'sale', 'buy', 'sell', 'goods', 'products', 'delivery'],
            'lease': ['lease', 'rent', 'rental', 'tenant', 'landlord', 'premises'],
            'nda': ['non-disclosure', 'confidentiality', 'confidential', 'proprietary', 'trade secret'],
            'license': ['license', 'licensing', 'intellectual property', 'copyright', 'trademark']
        }
    
    @staticmethod
    def extract_key_information(text: str) -> Dict:
        """Extract key information from document text using advanced regex patterns."""
        key_info = {}
        
        # Extract dates with multiple formats
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY, M/D/YY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
            r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b'  # YYYY-MM-DD
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        key_info['dates'] = list(set(dates))[:10]
        
        # Extract monetary amounts with various formats
        money_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # $1,000.00
            r'USD\s*[\d,]+(?:\.\d{2})?',  # USD 1000.00
            r'[\d,]+\s*dollars?',  # 1000 dollars
            r'[\d,]+\s*USD'  # 1000 USD
        ]
        
        amounts = []
        for pattern in money_patterns:
            amounts.extend(re.findall(pattern, text, re.IGNORECASE))
        key_info['monetary_amounts'] = list(set(amounts))[:10]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        key_info['email_addresses'] = list(set(emails))
        
        # Extract phone numbers with various formats
        phone_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 123-456-7890, 123.456.7890, 123 456 7890
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}\b',  # (123) 456-7890
            r'\+1[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'  # +1-123-456-7890
        ]
        
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        key_info['phone_numbers'] = list(set(phones))
        
        # Extract addresses
        address_pattern = r'\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Court|Ct|Place|Pl)'
        addresses = re.findall(address_pattern, text, re.IGNORECASE)
        key_info['addresses'] = list(set(addresses))[:5]
        
        # Extract company names and entities
        entity_patterns = [
            r'[A-Za-z0-9\s&,.-]+\s+(?:Inc|Corp|LLC|Co|Ltd|Company|Corporation|Limited)\b',
            r'\b[A-Z][A-Za-z0-9\s&,.-]*\s+(?:Law\s+Firm|Associates|Legal\s+Services)\b'
        ]
        
        entities = []
        for pattern in entity_patterns:
            entities.extend(re.findall(pattern, text, re.IGNORECASE))
        key_info['entities'] = list(set(entities))[:10]
        
        # Extract case numbers and docket numbers
        case_pattern = r'(?:Case\s+No\.?|Docket\s+No\.?|Civil\s+Action\s+No\.?)\s*:?\s*[\w\d-]+(?:\s*\([A-Z]{2,}\))?'
        case_numbers = re.findall(case_pattern, text, re.IGNORECASE)
        key_info['case_numbers'] = list(set(case_numbers))
        
        # Extract signatures (lines that look like signature blocks)
        signature_pattern = r'(?:Signed|Signature|By:)\s*[^\n]*(?:\n\s*[A-Za-z\s,.-]+){1,3}'
        signatures = re.findall(signature_pattern, text, re.IGNORECASE | re.MULTILINE)
        key_info['signature_blocks'] = signatures[:5]
        
        return key_info
    
    @staticmethod
    def classify_document(filename: str, text: str) -> str:
        """Classify document type based on filename and content analysis."""
        filename_lower = filename.lower()
        text_lower = text.lower()
        
        # Check first 2000 characters for classification (more comprehensive than original)
        text_sample = text_lower[:2000]
        
        # Contract/Agreement classification
        contract_keywords = [
            'contract', 'agreement', 'terms and conditions', 'hereby agree',
            'parties agree', 'consideration', 'obligations', 'covenants'
        ]
        if any(word in filename_lower for word in ['contract', 'agreement']) or \
           sum(1 for word in contract_keywords if word in text_sample) >= 2:
            return 'Contract/Agreement'
        
        # Court Filing classification
        court_keywords = [
            'motion', 'complaint', 'petition', 'brief', 'order', 'judgment',
            'court', 'honorable', 'civil action', 'case no', 'docket',
            'plaintiff', 'defendant', 'respondent', 'petitioner'
        ]
        if any(word in filename_lower for word in ['motion', 'complaint', 'petition', 'brief']) or \
           sum(1 for word in court_keywords if word in text_sample) >= 3:
            return 'Court Filing'
        
        # Corporate Document classification
        corporate_keywords = [
            'llc', 'corporation', 'incorporation', 'bylaws', 'board of directors',
            'shareholders', 'articles of incorporation', 'operating agreement',
            'board resolution', 'corporate', 'entity'
        ]
        if any(word in filename_lower for word in ['bylaws', 'incorporation', 'corporate']) or \
           sum(1 for word in corporate_keywords if word in text_sample) >= 2:
            return 'Corporate Document'
        
        # Real Estate classification
        real_estate_keywords = [
            'lease', 'deed', 'mortgage', 'property', 'real estate', 'premises',
            'landlord', 'tenant', 'rent', 'purchase agreement', 'title',
            'escrow', 'closing', 'conveyance'
        ]
        if any(word in filename_lower for word in ['lease', 'deed', 'mortgage']) or \
           sum(1 for word in real_estate_keywords if word in text_sample) >= 3:
            return 'Real Estate'
        
        # Family Law classification
        family_keywords = [
            'divorce', 'custody', 'prenuptial', 'marriage', 'child support',
            'alimony', 'spousal support', 'parenting plan', 'dissolution',
            'domestic relations', 'family court'
        ]
        if any(word in filename_lower for word in ['divorce', 'custody', 'prenup']) or \
           sum(1 for word in family_keywords if word in text_sample) >= 2:
            return 'Family Law'
        
        # Employment Law classification
        employment_keywords = [
            'employment', 'employee', 'employer', 'job', 'salary', 'wages',
            'benefits', 'termination', 'resignation', 'workplace', 'hr',
            'human resources', 'discrimination', 'harassment'
        ]
        if any(word in filename_lower for word in ['employment', 'employee', 'job']) or \
           sum(1 for word in employment_keywords if word in text_sample) >= 3:
            return 'Employment Law'
        
        # Intellectual Property classification
        ip_keywords = [
            'patent', 'trademark', 'copyright', 'intellectual property',
            'trade secret', 'licensing', 'infringement', 'royalty'
        ]
        if any(word in filename_lower for word in ['patent', 'trademark', 'copyright']) or \
           sum(1 for word in ip_keywords if word in text_sample) >= 2:
            return 'Intellectual Property'
        
        # Invoice/Billing classification
        billing_keywords = [
            'invoice', 'bill', 'payment', 'due date', 'amount due',
            'services rendered', 'billing', 'charges', 'fees'
        ]
        if any(word in filename_lower for word in ['invoice', 'bill']) or \
           sum(1 for word in billing_keywords if word in text_sample) >= 3:
            return 'Invoice/Billing'
        
        # Correspondence classification
        correspondence_keywords = [
            'dear', 'sincerely', 'regards', 'letter', 'correspondence',
            'memo', 'memorandum', 're:', 'subject:'
        ]
        if any(word in filename_lower for word in ['letter', 'memo', 'correspondence']) or \
           sum(1 for word in correspondence_keywords if word in text_sample) >= 2:
            return 'Correspondence'
        
        return 'General Document'
    
    def extract_parties(self, text: str) -> List[str]:
        """Extract party names from legal documents."""
        parties = []
        
        # Look for party identification patterns
        party_patterns = [
            r'(?:plaintiff|defendant|petitioner|respondent):\s*([A-Za-z\s,.-]+?)(?:\n|\.|,)',
            r'between\s+([A-Za-z\s,.-]+?)\s+and\s+([A-Za-z\s,.-]+?)(?:\s|,|\.|$)',
            r'(?:party|client):\s*([A-Za-z\s,.-]+?)(?:\n|\.|,)',
            r'(?:^|\n)\s*([A-Z][A-Za-z\s&,.-]+(?:Inc|Corp|LLC|Co|Ltd|Company|Corporation))\s*(?:\n|,|\.|$)'
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if isinstance(matches[0], tuple) if matches else False:
                # Handle patterns that return tuples
                for match in matches:
                    parties.extend([party.strip() for party in match if party.strip()])
            else:
                parties.extend([match.strip() for match in matches])
        
        # Clean up and deduplicate
        cleaned_parties = []
        for party in parties:
            party = party.strip().strip(',.')
            if len(party) > 2 and party not in cleaned_parties:
                cleaned_parties.append(party)
        
        return cleaned_parties[:10]  # Limit to first 10 parties
    
    def calculate_document_hash(self, text: str) -> str:
        """Calculate SHA-256 hash of document content for duplicate detection."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on common legal terms."""
        # Sample text for analysis (first 1000 characters)
        sample = text.lower()[:1000]
        
        # English legal terms
        english_terms = ['the', 'and', 'agreement', 'contract', 'shall', 'party', 'rights']
        english_score = sum(1 for term in english_terms if term in sample)
        
        # Spanish legal terms
        spanish_terms = ['el', 'la', 'y', 'contrato', 'acuerdo', 'parte', 'derechos']
        spanish_score = sum(1 for term in spanish_terms if term in sample)
        
        # French legal terms
        french_terms = ['le', 'la', 'et', 'contrat', 'accord', 'partie', 'droits']
        french_score = sum(1 for term in french_terms if term in sample)
        
        if spanish_score > english_score and spanish_score > french_score:
            return 'Spanish'
        elif french_score > english_score and french_score > spanish_score:
            return 'French'
        else:
            return 'English'
    
    def extract_contract_terms(self, text: str) -> Dict[str, Any]:
        """Extract key contract terms and clauses."""
        terms = {}
        
        # Extract effective dates
        effective_pattern = r'effective\s+(?:date|as\s+of)\s*:?\s*([^.;\n]+)'
        effective_dates = re.findall(effective_pattern, text, re.IGNORECASE)
        terms['effective_dates'] = [date.strip() for date in effective_dates]
        
        # Extract termination clauses
        termination_pattern = r'terminat[ei]\w*[^.]*\.(?:[^.]*\.)*'
        termination_clauses = re.findall(termination_pattern, text, re.IGNORECASE)
        terms['termination_clauses'] = termination_clauses[:3]
        
        # Extract governing law
        law_pattern = r'governed\s+by\s+(?:the\s+)?laws?\s+of\s+([^.;\n]+)'
        governing_law = re.findall(law_pattern, text, re.IGNORECASE)
        terms['governing_law'] = [law.strip() for law in governing_law]
        
        # Extract payment terms
        payment_pattern = r'payment[^.]*\$[\d,]+(?:\.\d{2})?[^.]*\.'
        payment_terms = re.findall(payment_pattern, text, re.IGNORECASE)
        terms['payment_terms'] = payment_terms[:5]
        
        return terms
    
    def analyze_document_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis for legal documents."""
        # Positive indicators
        positive_words = [
            'agree', 'consent', 'approve', 'accept', 'beneficial', 'favorable',
            'satisfactory', 'successful', 'resolved', 'settlement'
        ]
        
        # Negative indicators
        negative_words = [
            'dispute', 'breach', 'violation', 'default', 'reject', 'deny',
            'fail', 'unable', 'refuse', 'terminate', 'cancel', 'void'
        ]
        
        # Neutral/formal indicators
        neutral_words = [
            'whereas', 'therefore', 'pursuant', 'herein', 'aforementioned',
            'notwithstanding', 'stipulate', 'covenant'
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        neutral_count = sum(1 for word in neutral_words if word in text_lower)
        
        total_indicators = positive_count + negative_count + neutral_count
        
        if total_indicators == 0:
            sentiment = 'neutral'
            confidence = 0.0
        else:
            if positive_count > negative_count:
                sentiment = 'positive'
                confidence = positive_count / total_indicators
            elif negative_count > positive_count:
                sentiment = 'negative'
                confidence = negative_count / total_indicators
            else:
                sentiment = 'neutral'
                confidence = neutral_count / total_indicators
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 2),
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'neutral_indicators': neutral_count
        }
    
    def extract_deadlines_and_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract deadlines and important dates with context."""
        deadlines = []
        
        # Deadline patterns with context
        deadline_patterns = [
            (r'(?:due|deadline|expires?|must\s+be\s+(?:filed|submitted|completed))\s+(?:by|on|before)\s*:?\s*([^.;\n]+)', 'deadline'),
            (r'(?:effective|starting|commencing)\s+(?:date|on)\s*:?\s*([^.;\n]+)', 'effective_date'),
            (r'(?:termination|expiration|end)\s+(?:date|on)\s*:?\s*([^.;\n]+)', 'termination_date'),
            (r'(?:court\s+date|hearing|trial)\s*:?\s*([^.;\n]+)', 'court_date'),
            (r'(?:payment\s+due|invoice\s+due)\s*:?\s*([^.;\n]+)', 'payment_due')
        ]
        
        for pattern, date_type in deadline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                deadlines.append({
                    'type': date_type,
                    'date_text': match.strip(),
                    'context': date_type.replace('_', ' ').title()
                })
        
        return deadlines[:10]
    
    def detect_sensitive_information(self, text: str) -> Dict[str, Any]:
        """Detect potentially sensitive information in documents."""
        sensitive_info = {
            'social_security_numbers': [],
            'credit_card_numbers': [],
            'bank_account_numbers': [],
            'driver_license_numbers': [],
            'passport_numbers': [],
            'tax_id_numbers': []
        }
        
        # SSN pattern
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        sensitive_info['social_security_numbers'] = re.findall(ssn_pattern, text)
        
        # Credit card pattern (basic)
        cc_pattern = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
        sensitive_info['credit_card_numbers'] = re.findall(cc_pattern, text)
        
        # Bank account pattern (basic)
        bank_pattern = r'\b\d{8,17}\b'
        potential_accounts = re.findall(bank_pattern, text)
        sensitive_info['bank_account_numbers'] = potential_accounts[:5]  # Limit false positives
        
        # Tax ID pattern
        tax_id_pattern = r'\b\d{2}-\d{7}\b'
        sensitive_info['tax_id_numbers'] = re.findall(tax_id_pattern, text)
        
        return sensitive_info
    
    def generate_document_summary(self, text: str, max_length: int = 500) -> str:
        """Generate a summary of the document content."""
        # Simple extractive summarization
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) <= 3:
            return ' '.join(sentences)
        
        # Score sentences based on keyword frequency
        word_freq = {}
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            for word in words:
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
            sentence_scores.append((score, sentence))
        
        # Sort by score and take top sentences
        sentence_scores.sort(reverse=True, key=lambda x: x[0])
        
        summary_sentences = []
        current_length = 0
        
        for score, sentence in sentence_scores:
            if current_length + len(sentence) <= max_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)
            else:
                break
        
        return '. '.join(summary_sentences) + '.' if summary_sentences else text[:max_length]
    
    def process_document_complete(self, filename: str, text: str) -> Dict[str, Any]:
        """Complete document processing with all available analysis."""
        return {
            'filename': filename,
            'document_type': self.classify_document(filename, text),
            'key_information': self.extract_key_information(text),
            'parties': self.extract_parties(text),
            'contract_terms': self.extract_contract_terms(text),
            'deadlines': self.extract_deadlines_and_dates(text),
            'sentiment_analysis': self.analyze_document_sentiment(text),
            'language': self.detect_language(text),
            'sensitive_info': self.detect_sensitive_information(text),
            'document_hash': self.calculate_document_hash(text),
            'summary': self.generate_document_summary(text),
            'word_count': len(text.split()),
            'character_count': len(text),
            'processing_date': datetime.now().isoformat()
        }
