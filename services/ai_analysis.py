import re
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from collections import Counter
import math

class AIAnalysisSystem:
    def __init__(self):
        self.legal_terms_database = {
            'contract_types': {
                'employment': ['employment', 'employee', 'salary', 'benefits', 'job description', 'termination'],
                'service': ['services', 'consulting', 'professional', 'scope of work', 'deliverables'],
                'purchase': ['purchase', 'sale', 'goods', 'products', 'delivery', 'warranty'],
                'lease': ['lease', 'rent', 'tenant', 'landlord', 'premises', 'rental'],
                'nda': ['confidential', 'non-disclosure', 'proprietary', 'trade secret'],
                'licensing': ['license', 'intellectual property', 'royalty', 'trademark', 'copyright']
            },
            'risk_indicators': {
                'high': ['unlimited liability', 'personal guarantee', 'no termination clause', 'automatic renewal', 'penalty'],
                'medium': ['termination', 'breach', 'default', 'damages', 'indemnification'],
                'low': ['notice period', 'mutual consent', 'good faith', 'reasonable', 'standard terms']
            },
            'standard_clauses': [
                'force majeure', 'governing law', 'dispute resolution', 'indemnification',
                'limitation of liability', 'confidentiality', 'termination', 'payment terms',
                'intellectual property', 'warranties', 'non-compete', 'assignment'
            ]
        }
        
        self.compliance_frameworks = {
            'gdpr': ['data protection', 'privacy', 'personal data', 'consent', 'processing'],
            'hipaa': ['protected health information', 'phi', 'healthcare', 'medical records'],
            'sox': ['financial reporting', 'internal controls', 'audit', 'disclosure'],
            'pci': ['payment card', 'credit card', 'cardholder data', 'payment processing']
        }
    
    def analyze_contract(self, document_text: str, contract_type: str = None) -> Dict:
        """Comprehensive contract analysis using AI techniques."""
        analysis = {
            'risk_assessment': self._assess_risk_level(document_text),
            'key_clauses': self._identify_key_clauses(document_text),
            'missing_clauses': self._identify_missing_clauses(document_text, contract_type),
            'recommendations': self._generate_recommendations(document_text, contract_type),
            'complexity_score': self._calculate_complexity(document_text),
            'compliance_analysis': self._analyze_compliance(document_text),
            'financial_terms': self._extract_financial_terms(document_text),
            'timeline_analysis': self._analyze_timeline(document_text),
            'party_obligations': self._extract_obligations(document_text),
            'red_flags': self._identify_red_flags(document_text),
            'contract_type_prediction': self._predict_contract_type(document_text),
            'negotiation_points': self._identify_negotiation_points(document_text)
        }
        return analysis
    
    def _assess_risk_level(self, text: str) -> Dict[str, Any]:
        """Advanced risk assessment with detailed scoring."""
        text_lower = text.lower()
        
        high_risk_patterns = [
            r'unlimited\s+liability', r'personal\s+guarantee', r'no\s+termination',
            r'automatic\s+renewal', r'liquidated\s+damages', r'penalty\s+clause'
        ]
        
        medium_risk_patterns = [
            r'termination\s+for\s+convenience', r'breach\s+of\s+contract',
            r'indemnification', r'limitation\s+of\s+liability', r'force\s+majeure'
        ]
        
        low_risk_patterns = [
            r'mutual\s+consent', r'good\s+faith', r'reasonable\s+notice',
            r'standard\s+terms', r'industry\s+practice'
        ]
        
        high_risk_count = sum(len(re.findall(pattern, text_lower)) for pattern in high_risk_patterns)
        medium_risk_count = sum(len(re.findall(pattern, text_lower)) for pattern in medium_risk_patterns)
        low_risk_count = sum(len(re.findall(pattern, text_lower)) for pattern in low_risk_patterns)
        
        # Calculate weighted risk score
        risk_score = (high_risk_count * 3) + (medium_risk_count * 2) + (low_risk_count * 0.5)
        total_indicators = high_risk_count + medium_risk_count + low_risk_count
        
        if risk_score >= 6 or high_risk_count >= 2:
            risk_level = 'high'
        elif risk_score >= 3 or medium_risk_count >= 2:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'level': risk_level,
            'score': round(risk_score, 1),
            'high_risk_indicators': high_risk_count,
            'medium_risk_indicators': medium_risk_count,
            'low_risk_indicators': low_risk_count,
            'confidence': min(0.9, total_indicators / 10) if total_indicators > 0 else 0.5
        }
    
    def _identify_key_clauses(self, text: str) -> List[Dict]:
        """Advanced clause identification with context analysis."""
        clause_patterns = {
            'termination': {
                'pattern': r'(?:termination|terminate|end|cancel|dissolution)[^.!?]*[.!?]',
                'keywords': ['termination', 'notice period', 'cause', 'convenience'],
                'importance': 'critical'
            },
            'payment': {
                'pattern': r'(?:payment|pay|fee|cost|price|compensation|remuneration)[^.!?]*[.!?]',
                'keywords': ['amount', 'due date', 'currency', 'method'],
                'importance': 'critical'
            },
            'liability': {
                'pattern': r'(?:liability|liable|responsible|damages|harm)[^.!?]*[.!?]',
                'keywords': ['limitation', 'exclusion', 'cap', 'indemnify'],
                'importance': 'critical'
            },
            'confidentiality': {
                'pattern': r'(?:confidential|proprietary|non-disclosure|trade\s+secret)[^.!?]*[.!?]',
                'keywords': ['confidential', 'disclosure', 'proprietary'],
                'importance': 'high'
            },
            'intellectual_property': {
                'pattern': r'(?:intellectual\s+property|copyright|trademark|patent|proprietary\s+rights)[^.!?]*[.!?]',
                'keywords': ['ownership', 'license', 'infringement'],
                'importance': 'high'
            },
            'force_majeure': {
                'pattern': r'(?:force\s+majeure|act\s+of\s+god|unforeseeable\s+circumstances)[^.!?]*[.!?]',
                'keywords': ['force majeure', 'unforeseeable', 'beyond control'],
                'importance': 'medium'
            }
        }
        
        clauses = []
        for clause_type, config in clause_patterns.items():
            matches = re.findall(config['pattern'], text, re.IGNORECASE | re.DOTALL)
            for match in matches[:3]:  # Limit to first 3 matches per type
                # Calculate relevance score based on keywords
                match_lower = match.lower()
                keyword_score = sum(1 for keyword in config['keywords'] if keyword in match_lower)
                
                clauses.append({
                    'type': clause_type.replace('_', ' ').title(),
                    'text': match.strip()[:200] + "..." if len(match.strip()) > 200 else match.strip(),
                    'importance': config['importance'],
                    'relevance_score': keyword_score,
                    'location': text.find(match)
                })
        
        # Sort by importance and relevance
        importance_order = {'critical': 3, 'high': 2, 'medium': 1, 'low': 0}
        clauses.sort(key=lambda x: (importance_order.get(x['importance'], 0), x['relevance_score']), reverse=True)
        
        return clauses
    
    def _identify_missing_clauses(self, text: str, contract_type: str = None) -> List[Dict]:
        """Identify missing standard clauses with recommendations."""
        text_lower = text.lower().replace(' ', '').replace('-', '').replace('_', '')
        
        # Standard clauses based on contract type
        if contract_type:
            type_specific_clauses = {
                'employment': ['non-compete', 'severance', 'benefits', 'job description'],
                'service': ['scope of work', 'deliverables', 'acceptance criteria', 'change management'],
                'purchase': ['warranty', 'delivery terms', 'inspection', 'risk of loss'],
                'lease': ['maintenance obligations', 'utilities', 'security deposit', 'renewal options'],
                'nda': ['return of materials', 'survival', 'exceptions', 'remedies']
            }
            additional_clauses = type_specific_clauses.get(contract_type.lower(), [])
        else:
            additional_clauses = []
        
        all_standard_clauses = self.legal_terms_database['standard_clauses'] + additional_clauses
        
        missing_clauses = []
        for clause in all_standard_clauses:
            clause_variations = [
                clause.lower().replace(' ', ''),
                clause.lower().replace(' ', '_'),
                clause.lower().replace('_', ''),
                clause.lower()
            ]
            
            found = any(variation in text_lower for variation in clause_variations)
            
            if not found:
                # Determine criticality based on contract type and clause
                criticality = self._determine_clause_criticality(clause, contract_type)
                
                missing_clauses.append({
                    'clause': clause.title(),
                    'criticality': criticality,
                    'reason': self._get_clause_importance_reason(clause),
                    'suggested_language': self._get_suggested_clause_language(clause)
                })
        
        # Sort by criticality
        criticality_order = {'critical': 3, 'high': 2, 'medium': 1, 'low': 0}
        missing_clauses.sort(key=lambda x: criticality_order.get(x['criticality'], 0), reverse=True)
        
        return missing_clauses
    
    def _determine_clause_criticality(self, clause: str, contract_type: str) -> str:
        """Determine how critical a missing clause is."""
        critical_clauses = {
            'general': ['governing law', 'termination', 'limitation of liability'],
            'employment': ['termination', 'non-compete', 'confidentiality'],
            'service': ['scope of work', 'payment terms', 'deliverables'],
            'purchase': ['warranty', 'delivery terms', 'payment terms']
        }
        
        if clause in critical_clauses.get('general', []):
            return 'critical'
        elif contract_type and clause in critical_clauses.get(contract_type.lower(), []):
            return 'critical'
        elif clause in ['indemnification', 'dispute resolution', 'force majeure']:
            return 'high'
        else:
            return 'medium'
    
    def _get_clause_importance_reason(self, clause: str) -> str:
        """Provide reasoning for why a clause is important."""
        reasons = {
            'governing law': 'Determines which jurisdiction\'s laws apply to the contract',
            'dispute resolution': 'Establishes process for resolving conflicts',
            'termination': 'Defines how and when the contract can be ended',
            'limitation of liability': 'Limits exposure to damages and losses',
            'indemnification': 'Protects against third-party claims',
            'force majeure': 'Provides protection from unforeseeable circumstances',
            'confidentiality': 'Protects sensitive business information',
            'intellectual property': 'Clarifies ownership of IP rights'
        }
        
        return reasons.get(clause, f'Standard clause that provides important legal protection')
    
    def _get_suggested_clause_language(self, clause: str) -> str:
        """Provide suggested language for missing clauses."""
        suggestions = {
            'governing law': 'This Agreement shall be governed by and construed in accordance with the laws of [State/Country].',
            'termination': 'Either party may terminate this Agreement with [X] days written notice.',
            'limitation of liability': 'In no event shall either party be liable for indirect, incidental, or consequential damages.',
            'force majeure': 'Neither party shall be liable for delays caused by circumstances beyond their reasonable control.'
        }
        
        return suggestions.get(clause, 'Consult with legal counsel for appropriate language.')
    
    def _generate_recommendations(self, text: str, contract_type: str = None) -> List[Dict]:
        """Generate AI-powered recommendations for contract improvement."""
        recommendations = []
        text_lower = text.lower()
        
        # Analyze contract length and complexity
        word_count = len(text.split())
        if word_count < 500:
            recommendations.append({
                'category': 'Structure',
                'priority': 'medium',
                'recommendation': 'Consider expanding contract details for better clarity and protection',
                'rationale': f'Contract is relatively short ({word_count} words) and may lack important details'
            })
        
        # Check for vague language
        vague_terms = ['reasonable', 'appropriate', 'satisfactory', 'adequate', 'proper']
        vague_count = sum(1 for term in vague_terms if term in text_lower)
        if vague_count > 3:
            recommendations.append({
                'category': 'Language Clarity',
                'priority': 'high',
                'recommendation': 'Replace vague terms with specific, measurable criteria',
                'rationale': f'Found {vague_count} instances of potentially vague language'
            })
        
        # Check payment terms specificity
        if 'payment' in text_lower:
            if not re.search(r'\$[\d,]+|\d+\s*days?', text_lower):
                recommendations.append({
                    'category': 'Payment Terms',
                    'priority': 'high',
                    'recommendation': 'Specify exact payment amounts and due dates',
                    'rationale': 'Payment terms appear to lack specific amounts or timelines'
                })
        
        # Check for termination procedures
        if 'termination' in text_lower or 'terminate' in text_lower:
            if 'notice' not in text_lower:
                recommendations.append({
                    'category': 'Termination',
                    'priority': 'high',
                    'recommendation': 'Add specific notice requirements for termination',
                    'rationale': 'Termination clause lacks clear notice procedures'
                })
        
        # Check for dispute resolution
        dispute_terms = ['dispute', 'arbitration', 'mediation', 'litigation', 'court']
        if not any(term in text_lower for term in dispute_terms):
            recommendations.append({
                'category': 'Risk Management',
                'priority': 'high',
                'recommendation': 'Add dispute resolution clause specifying mediation or arbitration',
                'rationale': 'No dispute resolution mechanism specified'
            })
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _calculate_complexity(self, text: str) -> Dict[str, Any]:
        """Calculate contract complexity using multiple metrics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Basic readability metrics
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        long_words = sum(1 for word in words if len(word) > 6)
        very_long_words = sum(1 for word in words if len(word) > 10)
        
        # Legal complexity indicators
        legal_terms = ['whereas', 'heretofore', 'hereinafter', 'notwithstanding', 'pursuant']
        legal_term_count = sum(1 for term in legal_terms if term in text.lower())
        
        # Sentence complexity
        complex_sentences = sum(1 for sentence in sentences 
                               if len(sentence.split()) > 25 or sentence.count(',') > 3)
        
        # Calculate overall complexity score
        readability_score = (avg_words_per_sentence * 0.3) + (long_words / len(words) * 100 * 0.4)
        legal_complexity = (legal_term_count / len(words) * 100 * 0.2) + (very_long_words / len(words) * 100 * 0.1)
        structure_complexity = (complex_sentences / len(sentences) * 100) if sentences else 0
        
        total_complexity = min(readability_score + legal_complexity + structure_complexity, 100.0)
        
        # Determine complexity level
        if total_complexity >= 70:
            level = 'high'
        elif total_complexity >= 40:
            level = 'medium'
        else:
            level = 'low'
        
        return {
            'score': round(total_complexity, 1),
            'level': level,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'long_words_percentage': round(long_words / len(words) * 100, 1) if words else 0,
            'legal_term_density': round(legal_term_count / len(words) * 100, 2) if words else 0,
            'complex_sentences_percentage': round(complex_sentences / len(sentences) * 100, 1) if sentences else 0
        }
    
    def _analyze_compliance(self, text: str) -> Dict[str, Any]:
        """Analyze compliance with various regulatory frameworks."""
        text_lower = text.lower()
        compliance_analysis = {}
        
        for framework, keywords in self.compliance_frameworks.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            if keyword_matches > 0:
                compliance_level = 'full' if keyword_matches >= len(keywords) // 2 else 'partial'
                compliance_analysis[framework.upper()] = {
                    'applicable': True,
                    'compliance_level': compliance_level,
                    'matched_keywords': keyword_matches,
                    'total_keywords': len(keywords),
                    'recommendations': self._get_compliance_recommendations(framework, compliance_level)
                }
        
        return compliance_analysis
    
    def _get_compliance_recommendations(self, framework: str, level: str) -> List[str]:
        """Get compliance recommendations for specific frameworks."""
        recommendations = {
            'gdpr': [
                'Include explicit consent mechanisms for data processing',
                'Add data subject rights provisions',
                'Specify data retention periods'
            ],
            'hipaa': [
                'Include business associate agreement provisions',
                'Add breach notification requirements',
                'Specify minimum security safeguards'
            ],
            'sox': [
                'Include financial reporting accuracy requirements',
                'Add internal control provisions',
                'Specify audit trail requirements'
            ]
        }
        
        return recommendations.get(framework, [])
    
    def _extract_financial_terms(self, text: str) -> Dict[str, Any]:
        """Extract and analyze financial terms from the contract."""
        # Find monetary amounts
        money_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',
            r'USD\s*[\d,]+(?:\.\d{2})?',
            r'[\d,]+\s*dollars?'
        ]
        
        amounts = []
        for pattern in money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            amounts.extend(matches)
        
        # Find payment terms
        payment_pattern = r'(?:payment|pay|due|invoice)[^.]*(?:\d+\s*days?|\d+\s*months?)[^.]*\.'
        payment_terms = re.findall(payment_pattern, text, re.IGNORECASE)
        
        # Find interest rates
        interest_pattern = r'\d+(?:\.\d+)?%\s*(?:per\s*)?(?:annum|annual|yearly|month)'
        interest_rates = re.findall(interest_pattern, text, re.IGNORECASE)
        
        return {
            'monetary_amounts': list(set(amounts)),
            'payment_terms': [term.strip() for term in payment_terms],
            'interest_rates': list(set(interest_rates)),
            'currency_mentioned': 'USD' in text or '$' in text
        }
    
    def _analyze_timeline(self, text: str) -> Dict[str, Any]:
        """Analyze timeline and deadline information."""
        # Find time periods
        time_patterns = [
            r'\d+\s*(?:days?|weeks?|months?|years?)',
            r'(?:within|by|before|after)\s+\d+\s*(?:days?|weeks?|months?)',
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]
        
        timelines = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            timelines.extend(matches)
        
        # Find deadline-related terms
        deadline_pattern = r'(?:deadline|due date|expir[ei]\w*|terminat\w*)\s*[:\-]?\s*[^.]*\.'
        deadlines = re.findall(deadline_pattern, text, re.IGNORECASE)
        
        return {
            'time_periods': list(set(timelines)),
            'deadlines': [deadline.strip() for deadline in deadlines],
            'has_specific_dates': bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text))
        }
    
    def _extract_obligations(self, text: str) -> Dict[str, List[str]]:
        """Extract party obligations from the contract."""
        obligation_patterns = [
            r'(?:shall|must|will|agrees? to|responsible for|obligated to)\s+[^.]*\.',
            r'(?:party|client|contractor|vendor)\s+(?:shall|must|will)\s+[^.]*\.',
        ]
        
        obligations = []
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            obligations.extend([match.strip() for match in matches])
        
        # Categorize obligations (simplified)
        payment_obligations = [o for o in obligations if any(term in o.lower() for term in ['pay', 'payment', 'fee', 'cost'])]
        delivery_obligations = [o for o in obligations if any(term in o.lower() for term in ['deliver', 'provide', 'supply', 'perform'])]
        compliance_obligations = [o for o in obligations if any(term in o.lower() for term in ['comply', 'follow', 'adhere', 'conform'])]
        
        return {
            'payment_obligations': payment_obligations[:5],
            'delivery_obligations': delivery_obligations[:5],
            'compliance_obligations': compliance_obligations[:5],
            'total_obligations': len(obligations)
        }
    
    def _identify_red_flags(self, text: str) -> List[Dict[str, Any]]:
        """Identify potential red flags in the contract."""
        red_flags = []
        text_lower = text.lower()
        
        red_flag_patterns = {
            'Unlimited Liability': {
                'pattern': r'unlimited\s+liability|unlimited\s+damages',
                'severity': 'critical',
                'description': 'Contract may expose party to unlimited financial risk'
            },
            'No Termination Clause': {
                'pattern': r'(?!.*terminat)(?!.*end)(?!.*cancel)',
                'severity': 'high',
                'description': 'Lack of termination provisions may create binding obligation'
            },
            'Automatic Renewal': {
                'pattern': r'automatic(?:ally)?\s+renew|auto-renew',
                'severity': 'medium',
                'description': 'Contract may automatically renew without explicit consent'
            },
            'Personal Guarantee': {
                'pattern': r'personal\s+guarantee|personally\s+guarantee',
                'severity': 'high',
                'description': 'Personal assets may be at risk'
            },
            'Liquidated Damages': {
                'pattern': r'liquidated\s+damages|penalty\s+clause',
                'severity': 'medium',
                'description': 'Predetermined damage amounts may be excessive'
            }
        }
        
        for flag_name, config in red_flag_patterns.items():
            if re.search(config['pattern'], text_lower):
                red_flags.append({
                    'type': flag_name,
                    'severity': config['severity'],
                    'description': config['description'],
                    'recommendation': f'Review and consider negotiating {flag_name.lower()} terms'
                })
        
        return red_flags
    
    def _predict_contract_type(self, text: str) -> Dict[str, Any]:
        """Predict the most likely contract type using keyword analysis."""
        text_lower = text.lower()
        type_scores = {}
        
        for contract_type, keywords in self.legal_terms_database['contract_types'].items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            if score > 0:
                type_scores[contract_type] = score
        
        if not type_scores:
            return {'predicted_type': 'general', 'confidence': 0.5, 'scores': {}}
        
        # Find the type with highest score
        predicted_type = max(type_scores, key=type_scores.get)
        max_score = type_scores[predicted_type]
        total_score = sum(type_scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.5
        
        return {
            'predicted_type': predicted_type,
            'confidence': round(confidence, 2),
            'scores': type_scores
        }
    
    def _identify_negotiation_points(self, text: str) -> List[Dict[str, Any]]:
        """Identify potential negotiation points in the contract."""
        negotiation_points = []
        text_lower = text.lower()
        
        # Look for one-sided terms
        one_sided_patterns = [
            r'(?:client|party\s+a)(?:\s+shall|\s+must|\s+will)[^.]*(?:but|however|except)[^.]*(?:party\s+b|contractor)(?:\s+may|\s+can)',
            r'sole\s+discretion|absolute\s+discretion',
            r'without\s+limitation|unlimited\s+right'
        ]
        
        for pattern in one_sided_patterns:
            if re.search(pattern, text_lower):
                negotiation_points.append({
                    'type': 'One-sided Terms',
                    'priority': 'high',
                    'suggestion': 'Consider requesting mutual obligations or limitations',
                    'rationale': 'Terms appear to favor one party disproportionately'
                })
                break
        
        # Look for missing reciprocal obligations
        if 'indemnif' in text_lower and text_lower.count('indemnif') == 1:
            negotiation_points.append({
                'type': 'Indemnification',
                'priority': 'medium',
                'suggestion': 'Consider mutual indemnification clauses',
                'rationale': 'Indemnification appears to be one-sided'
            })
        
        # Check for broad IP assignments
        if re.search(r'(?:all|any).*intellectual\s+property.*(?:assign|transfer)', text_lower):
            negotiation_points.append({
                'type': 'Intellectual Property',
                'priority': 'high',
                'suggestion': 'Limit IP assignment to work specifically created for this contract',
                'rationale': 'Broad IP assignment may be overreaching'
            })
        
        return negotiation_points
    
    def analyze_document_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the overall sentiment and tone of the document."""
        positive_indicators = [
            'mutual', 'collaboration', 'partnership', 'good faith', 'reasonable',
            'fair', 'equitable', 'benefit', 'success', 'cooperation'
        ]
        
        negative_indicators = [
            'penalty', 'breach', 'default', 'violation', 'terminate', 'cancel',
            'liable', 'damages', 'forfeit', 'void', 'dispute', 'conflict'
        ]
        
        neutral_indicators = [
            'whereas', 'therefore', 'pursuant', 'herein', 'aforementioned',
            'notwithstanding', 'stipulate', 'covenant', 'provision'
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(text_lower.count(word) for word in positive_indicators)
        negative_count = sum(text_lower.count(word) for word in negative_indicators)
        neutral_count = sum(text_lower.count(word) for word in neutral_indicators)
        
        total_indicators = positive_count + negative_count + neutral_count
        
        if total_indicators == 0:
            sentiment = 'neutral'
            confidence = 0.5
        else:
            if positive_count > negative_count:
                sentiment = 'collaborative'
                confidence = positive_count / total_indicators
            elif negative_count > positive_count:
                sentiment = 'adversarial'
                confidence = negative_count / total_indicators
            else:
                sentiment = 'formal'
                confidence = neutral_count / total_indicators
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 2),
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'neutral_indicators': neutral_count,
            'tone_description': self._get_tone_description(sentiment, confidence)
        }
    
    def _get_tone_description(self, sentiment: str, confidence: float) -> str:
        """Get a description of the document's tone."""
        descriptions = {
            'collaborative': 'The document emphasizes partnership and mutual benefit',
            'adversarial': 'The document focuses heavily on penalties and enforcement',
            'formal': 'The document maintains a neutral, formal legal tone'
        }
        
        base_description = descriptions.get(sentiment, 'The document maintains a standard legal tone')
        
        if confidence > 0.8:
            return f"{base_description} with high confidence"
        elif confidence > 0.6:
            return f"{base_description} with moderate confidence"
        else:
            return f"{base_description} but analysis is uncertain due to mixed indicators"
    
    def generate_executive_summary(self, analysis_results: Dict) -> str:
        """Generate an executive summary of the AI analysis."""
        risk_level = analysis_results['risk_assessment']['level']
        complexity_level = analysis_results['complexity_score']['level']
        contract_type = analysis_results['contract_type_prediction']['predicted_type']
        
        summary_parts = []
        
        # Contract type and complexity
        summary_parts.append(f"This appears to be a {contract_type} contract with {complexity_level} complexity.")
        
        # Risk assessment
        risk_colors = {'low': 'minimal', 'medium': 'moderate', 'high': 'significant'}
        summary_parts.append(f"Risk assessment indicates {risk_colors[risk_level]} legal and financial risk.")
        
        # Key findings
        missing_count = len(analysis_results['missing_clauses'])
        if missing_count > 0:
            summary_parts.append(f"Analysis identified {missing_count} potentially missing standard clauses.")
        
        red_flags_count = len(analysis_results['red_flags'])
        if red_flags_count > 0:
            critical_flags = [f for f in analysis_results['red_flags'] if f['severity'] == 'critical']
            if critical_flags:
                summary_parts.append(f"Found {len(critical_flags)} critical red flag(s) requiring immediate attention.")
            else:
                summary_parts.append(f"Identified {red_flags_count} areas of concern for review.")
        
        # Recommendations
        high_priority_recs = [r for r in analysis_results['recommendations'] if r['priority'] == 'high']
        if high_priority_recs:
            summary_parts.append(f"Generated {len(high_priority_recs)} high-priority recommendations for improvement.")
        
        return " ".join(summary_parts)
    
    def compare_contracts(self, contract1_text: str, contract2_text: str) -> Dict[str, Any]:
        """Compare two contracts and identify key differences."""
        analysis1 = self.analyze_contract(contract1_text)
        analysis2 = self.analyze_contract(contract2_text)
        
        comparison = {
            'risk_comparison': {
                'contract1_risk': analysis1['risk_assessment']['level'],
                'contract2_risk': analysis2['risk_assessment']['level'],
                'risk_difference': self._compare_risk_levels(
                    analysis1['risk_assessment']['level'], 
                    analysis2['risk_assessment']['level']
                )
            },
            'complexity_comparison': {
                'contract1_complexity': analysis1['complexity_score']['score'],
                'contract2_complexity': analysis2['complexity_score']['score'],
                'complexity_difference': round(
                    analysis2['complexity_score']['score'] - analysis1['complexity_score']['score'], 1
                )
            },
            'clause_differences': self._compare_clauses(
                analysis1['key_clauses'], 
                analysis2['key_clauses']
            ),
            'missing_clause_comparison': {
                'contract1_missing': len(analysis1['missing_clauses']),
                'contract2_missing': len(analysis2['missing_clauses']),
                'unique_to_contract1': self._find_unique_missing_clauses(
                    analysis1['missing_clauses'], 
                    analysis2['missing_clauses']
                ),
                'unique_to_contract2': self._find_unique_missing_clauses(
                    analysis2['missing_clauses'], 
                    analysis1['missing_clauses']
                )
            },
            'financial_comparison': self._compare_financial_terms(
                analysis1['financial_terms'], 
                analysis2['financial_terms']
            ),
            'recommendation': self._generate_comparison_recommendation(analysis1, analysis2)
        }
        
        return comparison
    
    def _compare_risk_levels(self, risk1: str, risk2: str) -> str:
        """Compare risk levels between two contracts."""
        risk_order = {'low': 1, 'medium': 2, 'high': 3}
        
        score1 = risk_order[risk1]
        score2 = risk_order[risk2]
        
        if score1 == score2:
            return 'equal'
        elif score1 < score2:
            return 'contract2_higher_risk'
        else:
            return 'contract1_higher_risk'
    
    def _compare_clauses(self, clauses1: List[Dict], clauses2: List[Dict]) -> Dict[str, List[str]]:
        """Compare clauses between two contracts."""
        types1 = set(clause['type'] for clause in clauses1)
        types2 = set(clause['type'] for clause in clauses2)
        
        return {
            'common_clauses': list(types1 & types2),
            'unique_to_contract1': list(types1 - types2),
            'unique_to_contract2': list(types2 - types1)
        }
    
    def _find_unique_missing_clauses(self, missing1: List[Dict], missing2: List[Dict]) -> List[str]:
        """Find clauses missing from one contract but not the other."""
        clauses1 = set(clause['clause'] for clause in missing1)
        clauses2 = set(clause['clause'] for clause in missing2)
        
        return list(clauses1 - clauses2)
    
    def _compare_financial_terms(self, financial1: Dict, financial2: Dict) -> Dict[str, Any]:
        """Compare financial terms between contracts."""
        return {
            'contract1_amounts': len(financial1.get('monetary_amounts', [])),
            'contract2_amounts': len(financial2.get('monetary_amounts', [])),
            'contract1_payment_terms': len(financial1.get('payment_terms', [])),
            'contract2_payment_terms': len(financial2.get('payment_terms', [])),
            'both_specify_currency': (
                financial1.get('currency_mentioned', False) and 
                financial2.get('currency_mentioned', False)
            )
        }
    
    def _generate_comparison_recommendation(self, analysis1: Dict, analysis2: Dict) -> str:
        """Generate a recommendation based on contract comparison."""
        risk1 = analysis1['risk_assessment']['level']
        risk2 = analysis2['risk_assessment']['level']
        
        missing1 = len(analysis1['missing_clauses'])
        missing2 = len(analysis2['missing_clauses'])
        
        complexity1 = analysis1['complexity_score']['score']
        complexity2 = analysis2['complexity_score']['score']
        
        # Simple recommendation logic
        if risk1 == 'low' and risk2 == 'high':
            return "Contract 1 appears to have lower risk profile and may be preferable."
        elif risk2 == 'low' and risk1 == 'high':
            return "Contract 2 appears to have lower risk profile and may be preferable."
        elif missing1 < missing2:
            return "Contract 1 has fewer missing standard clauses and may be more complete."
        elif missing2 < missing1:
            return "Contract 2 has fewer missing standard clauses and may be more complete."
        elif abs(complexity1 - complexity2) > 20:
            if complexity1 < complexity2:
                return "Contract 1 is significantly less complex and may be easier to understand and manage."
            else:
                return "Contract 2 is significantly less complex and may be easier to understand and manage."
        else:
            return "Both contracts have similar risk profiles. Review specific terms and business requirements to determine preference."
    
    def extract_key_metrics(self, text: str) -> Dict[str, Any]:
        """Extract key performance metrics and benchmarks from contracts."""
        text_lower = text.lower()
        
        # Extract performance metrics
        metrics = {
            'performance_standards': [],
            'service_levels': [],
            'quality_metrics': [],
            'delivery_timeframes': [],
            'penalty_clauses': [],
            'bonus_clauses': []
        }
        
        # Performance standards
        performance_patterns = [
            r'(?:perform[a-z]*|standard[s]?|requirement[s]?)[^.]*(?:\d+%|\d+\s*percent)[^.]*\.',
            r'(?:accuracy|quality|completion)[^.]*(?:\d+%|\d+\s*percent)[^.]*\.',
        ]
        
        for pattern in performance_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metrics['performance_standards'].extend([m.strip() for m in matches])
        
        # Service level agreements
        sla_patterns = [
            r'(?:service\s+level|sla|uptime|availability)[^.]*(?:\d+(?:\.\d+)?%)[^.]*\.',
            r'(?:response\s+time|resolution\s+time)[^.]*(?:\d+\s*(?:hours?|days?|minutes?))[^.]*\.'
        ]
        
        for pattern in sla_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metrics['service_levels'].extend([m.strip() for m in matches])
        
        # Delivery timeframes
        delivery_pattern = r'(?:deliver|complete|finish)[^.]*(?:within|by|before)\s*\d+\s*(?:days?|weeks?|months?)[^.]*\.'
        delivery_matches = re.findall(delivery_pattern, text, re.IGNORECASE)
        metrics['delivery_timeframes'] = [m.strip() for m in delivery_matches]
        
        # Penalty clauses
        penalty_pattern = r'(?:penalty|fine|liquidated\s+damages)[^.]*\$[\d,]+(?:\.\d{2})?[^.]*\.'
        penalty_matches = re.findall(penalty_pattern, text, re.IGNORECASE)
        metrics['penalty_clauses'] = [m.strip() for m in penalty_matches]
        
        return metrics
    
    def analyze_contract_lifecycle(self, text: str) -> Dict[str, Any]:
        """Analyze contract lifecycle events and phases."""
        lifecycle_analysis = {
            'inception': self._extract_inception_terms(text),
            'performance_phase': self._extract_performance_terms(text),
            'modification': self._extract_modification_terms(text),
            'termination': self._extract_termination_terms(text),
            'post_termination': self._extract_post_termination_terms(text)
        }
        
        return lifecycle_analysis
    
    def _extract_inception_terms(self, text: str) -> Dict[str, Any]:
        """Extract contract inception and commencement terms."""
        inception_pattern = r'(?:effective|commence|begin|start)[^.]*(?:date|upon|when)[^.]*\.'
        inception_matches = re.findall(inception_pattern, text, re.IGNORECASE)
        
        return {
            'commencement_clauses': [m.strip() for m in inception_matches[:3]],
            'has_conditions_precedent': bool(re.search(r'condition[s]?\s+precedent|subject\s+to', text, re.IGNORECASE))
        }
    
    def _extract_performance_terms(self, text: str) -> Dict[str, Any]:
        """Extract performance phase terms."""
        performance_pattern = r'(?:perform|discharge|fulfill|execute)[^.]*obligation[s]?[^.]*\.'
        performance_matches = re.findall(performance_pattern, text, re.IGNORECASE)
        
        return {
            'performance_obligations': [m.strip() for m in performance_matches[:3]],
            'has_monitoring_provisions': bool(re.search(r'monitor|review|inspect|audit', text, re.IGNORECASE))
        }
    
    def _extract_modification_terms(self, text: str) -> Dict[str, Any]:
        """Extract contract modification terms."""
        modification_pattern = r'(?:modif[yi]|amend|change|alter)[^.]*(?:writing|written|signed)[^.]*\.'
        modification_matches = re.findall(modification_pattern, text, re.IGNORECASE)
        
        return {
            'modification_procedures': [m.strip() for m in modification_matches[:2]],
            'requires_written_consent': bool(re.search(r'(?:modif[yi]|amend).*writ(?:ten|ing)', text, re.IGNORECASE))
        }
    
    def _extract_termination_terms(self, text: str) -> Dict[str, Any]:
        """Extract termination terms."""
        termination_pattern = r'(?:terminat[ei]|end|expir[ei])[^.]*(?:notice|cause|breach)[^.]*\.'
        termination_matches = re.findall(termination_pattern, text, re.IGNORECASE)
        
        return {
            'termination_procedures': [m.strip() for m in termination_matches[:3]],
            'notice_required': bool(re.search(r'terminat.*notice', text, re.IGNORECASE)),
            'termination_for_cause': bool(re.search(r'terminat.*(?:cause|breach)', text, re.IGNORECASE))
        }
    
    def _extract_post_termination_terms(self, text: str) -> Dict[str, Any]:
        """Extract post-termination obligations."""
        survival_pattern = r'(?:surviv[ei]|remain\s+in\s+(?:force|effect))[^.]*(?:terminat|expir)[^.]*\.'
        survival_matches = re.findall(survival_pattern, text, re.IGNORECASE)
        
        return {
            'survival_clauses': [m.strip() for m in survival_matches[:2]],
            'has_return_obligations': bool(re.search(r'return|destroy.*(?:confidential|proprietary)', text, re.IGNORECASE)),
            'has_post_term_restrictions': bool(re.search(r'(?:after|following).*terminat.*(?:not|shall\s+not)', text, re.IGNORECASE))
        }
    
    def generate_contract_scorecard(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate a comprehensive contract scorecard."""
        scorecard = {
            'overall_score': 0,
            'category_scores': {},
            'strengths': [],
            'weaknesses': [],
            'grade': 'F'
        }
        
        # Risk Management Score (25 points)
        risk_level = analysis_results['risk_assessment']['level']
        risk_scores = {'low': 25, 'medium': 15, 'high': 5}
        risk_score = risk_scores.get(risk_level, 10)
        
        # Completeness Score (25 points)
        missing_critical = len([c for c in analysis_results['missing_clauses'] if c['criticality'] == 'critical'])
        completeness_score = max(0, 25 - (missing_critical * 5))
        
        # Clarity Score (20 points)
        complexity_score = analysis_results['complexity_score']['score']
        clarity_score = max(0, 20 - (complexity_score / 5))
        
        # Financial Terms Score (15 points)
        financial_terms = analysis_results['financial_terms']
        financial_score = 0
        if financial_terms['monetary_amounts']:
            financial_score += 5
        if financial_terms['payment_terms']:
            financial_score += 5
        if financial_terms['currency_mentioned']:
            financial_score += 5
        
        # Compliance Score (15 points)
        compliance_analysis = analysis_results['compliance_analysis']
        compliance_score = len(compliance_analysis) * 3  # 3 points per applicable framework
        compliance_score = min(compliance_score, 15)
        
        # Calculate total score
        total_score = risk_score + completeness_score + clarity_score + financial_score + compliance_score
        
        # Assign grade
        if total_score >= 85:
            grade = 'A'
        elif total_score >= 75:
            grade = 'B'
        elif total_score >= 65:
            grade = 'C'
        elif total_score >= 55:
            grade = 'D'
        else:
            grade = 'F'
        
        scorecard.update({
            'overall_score': total_score,
            'category_scores': {
                'risk_management': risk_score,
                'completeness': completeness_score,
                'clarity': clarity_score,
                'financial_terms': financial_score,
                'compliance': compliance_score
            },
            'grade': grade,
            'strengths': self._identify_contract_strengths(analysis_results),
            'weaknesses': self._identify_contract_weaknesses(analysis_results)
        })
        
        return scorecard
    
    def _identify_contract_strengths(self, analysis_results: Dict) -> List[str]:
        """Identify contract strengths based on analysis."""
        strengths = []
        
        if analysis_results['risk_assessment']['level'] == 'low':
            strengths.append("Low risk profile with appropriate protections")
        
        if len(analysis_results['missing_clauses']) < 3:
            strengths.append("Comprehensive clause coverage")
        
        if analysis_results['complexity_score']['score'] < 40:
            strengths.append("Clear and understandable language")
        
        if analysis_results['financial_terms']['payment_terms']:
            strengths.append("Well-defined payment terms")
        
        if not analysis_results['red_flags']:
            strengths.append("No critical red flags identified")
        
        return strengths
    
    def _identify_contract_weaknesses(self, analysis_results: Dict) -> List[str]:
        """Identify contract weaknesses based on analysis."""
        weaknesses = []
        
        if analysis_results['risk_assessment']['level'] == 'high':
            weaknesses.append("High risk exposure requires attention")
        
        critical_missing = [c for c in analysis_results['missing_clauses'] if c['criticality'] == 'critical']
        if critical_missing:
            weaknesses.append(f"Missing {len(critical_missing)} critical clause(s)")
        
        if analysis_results['complexity_score']['score'] > 70:
            weaknesses.append("Overly complex language may cause confusion")
        
        critical_flags = [f for f in analysis_results['red_flags'] if f['severity'] == 'critical']
        if critical_flags:
            weaknesses.append("Contains critical red flags")
        
        if len(analysis_results['recommendations']) > 5:
            weaknesses.append("Multiple areas identified for improvement")
        
        return weaknesses
