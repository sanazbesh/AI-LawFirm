import re
from typing import Dict, List

class AIAnalysisSystem:
    def __init__(self):
        pass
    
    def analyze_contract(self, document_text: str) -> Dict:
        analysis = {
            'risk_level': self._assess_risk_level(document_text),
            'key_clauses': self._identify_key_clauses(document_text),
            'missing_clauses': self._identify_missing_clauses(document_text),
            'recommendations': self._generate_recommendations(),
            'complexity_score': self._calculate_complexity(document_text)
        }
        return analysis
    
    def _assess_risk_level(self, text: str) -> str:
        risk_keywords = ['penalty', 'termination', 'breach', 'litigation', 'damages']
        text_lower = text.lower()
        high_count = sum(1 for word in risk_keywords if word in text_lower)
        
        if high_count >= 3:
            return 'high'
        elif high_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _identify_key_clauses(self, text: str) -> List[Dict]:
        clause_patterns = {
            'termination': r'(?:termination|terminate|end|cancel)[^.]*\.',
            'payment': r'(?:payment|pay|fee|cost|price)[^.]*\.',
            'liability': r'(?:liability|liable|responsible)[^.]*\.'
        }
        
        clauses = []
        for clause_type, pattern in clause_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:2]:
                clauses.append({
                    'type': clause_type,
                    'text': match.strip()[:100] + "...",
                    'importance': 'high' if clause_type in ['termination', 'liability'] else 'medium'
                })
        
        return clauses
    
    def _identify_missing_clauses(self, text: str) -> List[str]:
        standard_clauses = [
            'Force Majeure', 'Governing Law', 'Dispute Resolution',
            'Indemnification', 'Limitation of Liability', 'Confidentiality'
        ]
        
        text_lower = text.lower()
        missing = []
        
        for clause in standard_clauses:
            if clause.lower().replace(' ', '') not in text_lower.replace(' ', ''):
                missing.append(clause)
        
        return missing
    
    def _generate_recommendations(self) -> List[str]:
        return [
            "Consider adding explicit termination procedures",
            "Review payment terms for clarity",
            "Add force majeure clause for risk mitigation"
        ]
    
    def _calculate_complexity(self, text: str) -> float:
        words = text.split()
        sentences = text.split('.')
        
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        long_words = sum(1 for word in words if len(word) > 6)
        complexity = (avg_words_per_sentence * 0.4) + (long_words / len(words) * 100 * 0.6)
        
        return min(complexity, 100.0)
