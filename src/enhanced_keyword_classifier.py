import logging
import re
from typing import Dict, List, Optional
from collections import Counter

class EnhancedKeywordClassifier:
    """Enhanced keyword-based email classifier with advanced features"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Enhanced keyword dictionary with weights and context
        self.keyword_patterns = {
            'hardware': {
                'primary': {
                    'computer': 3, 'laptop': 3, 'desktop': 3, 'pc': 2,
                    'hardware': 4, 'device': 2, 'machine': 2,
                    'monitor': 3, 'screen': 2, 'display': 2,
                    'keyboard': 3, 'mouse': 3, 'printer': 3,
                    'scanner': 3, 'webcam': 3, 'camera': 2,
                    'headset': 2, 'microphone': 2, 'speaker': 2
                },
                'secondary': {
                    'broken': 2, 'repair': 2, 'replace': 2, 'fix': 2,
                    'malfunction': 3, 'defective': 3, 'faulty': 3,
                    'warranty': 2, 'maintenance': 2, 'service': 1,
                    'physical': 1, 'hardware': 2, 'component': 2
                },
                'negative': ['software', 'program', 'app', 'code']
            },
            'software': {
                'primary': {
                    'software': 4, 'program': 3, 'application': 3, 'app': 2,
                    'system': 2, 'platform': 2, 'tool': 1,
                    'bug': 4, 'error': 3, 'crash': 3, 'freeze': 3,
                    'install': 3, 'update': 3, 'upgrade': 2,
                    'download': 2, 'license': 2, 'version': 2
                },
                'secondary': {
                    'virus': 3, 'malware': 3, 'antivirus': 2,
                    'backup': 2, 'restore': 2, 'sync': 2,
                    'login': 2, 'password': 2, 'access': 1,
                    'database': 2, 'server': 1, 'cloud': 1
                },
                'negative': ['hardware', 'device', 'physical']
            },
            'order': {
                'primary': {
                    'order': 4, 'purchase': 3, 'buy': 3, 'bought': 3,
                    'delivery': 3, 'shipping': 3, 'ship': 2,
                    'product': 3, 'item': 2, 'goods': 2,
                    'package': 2, 'parcel': 2, 'box': 1,
                    'tracking': 3, 'status': 2, 'when': 1
                },
                'secondary': {
                    'cart': 2, 'checkout': 3, 'shop': 2,
                    'arrived': 2, 'dispatch': 2, 'sent': 1,
                    'receive': 2, 'delivered': 3, 'delivery': 2,
                    'warehouse': 2, 'supplier': 1, 'vendor': 1
                },
                'negative': ['payment', 'bill', 'invoice', 'refund']
            },
            'payment': {
                'primary': {
                    'payment': 4, 'pay': 3, 'paid': 3, 'bill': 3,
                    'invoice': 4, 'money': 3, 'amount': 2,
                    'charge': 3, 'cost': 2, 'price': 2,
                    'refund': 4, 'transaction': 3, 'receipt': 3
                },
                'secondary': {
                    'card': 2, 'credit': 2, 'debit': 2, 'bank': 2,
                    'account': 2, 'balance': 2, 'finance': 2,
                    'billing': 3, 'subscription': 2, 'fee': 2,
                    'discount': 2, 'coupon': 2, 'promo': 1
                },
                'negative': ['order', 'product', 'shipping']
            }
        }
        
        # Common patterns that might indicate categories
        self.regex_patterns = {
            'order': [
                r'order\s*#?\s*\d+',
                r'tracking\s*#?\s*\d+',
                r'delivery\s*date',
                r'shipped\s*on'
            ],
            'payment': [
                r'\$\d+\.?\d*',
                r'invoice\s*#?\s*\d+',
                r'bill\s*#?\s*\d+',
                r'transaction\s*#?\s*\d+'
            ],
            'hardware': [
                r'model\s*#?\s*\w+',
                r'serial\s*#?\s*\w+',
                r'part\s*#?\s*\w+'
            ]
        }
        
        self.logger.info("Enhanced keyword classifier initialized")
    
    def classify_email(self, email_content: str) -> str:
        """Classify email content using enhanced keyword analysis"""
        try:
            # Clean and prepare content
            content = self._preprocess_content(email_content)
            
            # Get keyword scores
            keyword_scores = self._calculate_keyword_scores(content)
            
            # Get pattern scores
            pattern_scores = self._calculate_pattern_scores(content)
            
            # Get context scores
            context_scores = self._calculate_context_scores(content)
            
            # Combine all scores
            final_scores = self._combine_scores(keyword_scores, pattern_scores, context_scores)
            
            # Determine best category
            result = self._determine_category(final_scores)
            
            self.logger.info(f"Email classified as: {result} (enhanced keyword)")
            return result
            
        except Exception as e:
            self.logger.error(f"Enhanced classification failed: {e}")
            return self._simple_fallback(email_content)
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess email content for better analysis"""
        # Convert to lowercase
        content = content.lower()
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove common email signatures and footers
        content = re.sub(r'sent from my \w+', '', content)
        content = re.sub(r'unsubscribe.*', '', content)
        
        return content.strip()
    
    def _calculate_keyword_scores(self, content: str) -> Dict[str, float]:
        """Calculate scores based on keyword matching"""
        scores = {}
        
        for category, keywords in self.keyword_patterns.items():
            score = 0
            
            # Primary keywords (higher weight)
            for keyword, weight in keywords['primary'].items():
                count = content.count(keyword)
                score += count * weight
            
            # Secondary keywords (lower weight)
            for keyword, weight in keywords['secondary'].items():
                count = content.count(keyword)
                score += count * weight * 0.5
            
            # Negative keywords (reduce score)
            for keyword in keywords['negative']:
                count = content.count(keyword)
                score -= count * 1.5
            
            scores[category] = max(0, score)  # Don't allow negative scores
        
        return scores
    
    def _calculate_pattern_scores(self, content: str) -> Dict[str, float]:
        """Calculate scores based on regex patterns"""
        scores = {category: 0 for category in self.keyword_patterns.keys()}
        
        for category, patterns in self.regex_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content)
                scores[category] += len(matches) * 2  # Pattern matches get high score
        
        return scores
    
    def _calculate_context_scores(self, content: str) -> Dict[str, float]:
        """Calculate scores based on context analysis"""
        scores = {category: 0 for category in self.keyword_patterns.keys()}
        
        # Look for question words that might indicate categories
        question_patterns = {
            'order': ['when will', 'where is', 'has my', 'track my'],
            'payment': ['how much', 'why was', 'refund for', 'charged for'],
            'hardware': ['not working', 'broken', 'wont turn on', 'problem with'],
            'software': ['cant login', 'error message', 'wont install', 'crashes when']
        }
        
        for category, patterns in question_patterns.items():
            for pattern in patterns:
                if pattern in content:
                    scores[category] += 1.5
        
        return scores
    
    def _combine_scores(self, keyword_scores: Dict[str, float], 
                       pattern_scores: Dict[str, float], 
                       context_scores: Dict[str, float]) -> Dict[str, float]:
        """Combine all scoring methods"""
        combined = {}
        
        for category in keyword_scores.keys():
            combined[category] = (
                keyword_scores[category] * 1.0 +
                pattern_scores[category] * 1.5 +
                context_scores[category] * 1.2
            )
        
        return combined
    
    def _determine_category(self, scores: Dict[str, float]) -> str:
        """Determine the best category based on scores"""
        if not scores or max(scores.values()) == 0:
            return 'general'
        
        # Get the category with highest score
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # If score is too low, classify as general
        if best_score < 1.0:
            return 'general'
        
        # If multiple categories have similar scores, be more conservative
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1 and sorted_scores[0] - sorted_scores[1] < 0.5:
            return 'general'
        
        return best_category
    
    def _simple_fallback(self, email_content: str) -> str:
        """Simple fallback classification"""
        simple_keywords = {
            'hardware': ['hardware', 'computer', 'laptop', 'device', 'monitor', 'printer'],
            'software': ['software', 'program', 'app', 'bug', 'error', 'install'],
            'order': ['order', 'delivery', 'shipping', 'product', 'tracking'],
            'payment': ['payment', 'bill', 'invoice', 'refund', 'charge']
        }
        
        content_lower = email_content.lower()
        scores = {}
        
        for category, keywords in simple_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            scores[category] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return 'general'
    
    def get_classification_confidence(self, email_content: str) -> Dict[str, float]:
        """Get confidence scores for all categories"""
        content = self._preprocess_content(email_content)
        keyword_scores = self._calculate_keyword_scores(content)
        pattern_scores = self._calculate_pattern_scores(content)
        context_scores = self._calculate_context_scores(content)
        final_scores = self._combine_scores(keyword_scores, pattern_scores, context_scores)
        
        # Normalize scores to percentages
        total_score = sum(final_scores.values())
        if total_score > 0:
            return {cat: (score / total_score) * 100 for cat, score in final_scores.items()}
        else:
            return {cat: 0 for cat in final_scores.keys()}
