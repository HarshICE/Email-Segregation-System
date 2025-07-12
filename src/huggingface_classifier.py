import logging
from typing import Dict, List, Optional
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class HuggingFaceClassifier:
    """Email classifier using Hugging Face transformers"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.classifier = None
        self.sentiment_classifier = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                # Use a general sentiment classifier that can help with classification
                self.sentiment_classifier = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    return_all_scores=True
                )
                self.logger.info("Hugging Face classifier initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Hugging Face classifier: {e}")
                self.sentiment_classifier = None
        else:
            self.logger.warning("Transformers library not available")
    
    def classify_email(self, email_content: str) -> str:
        """Classify email content using Hugging Face transformers"""
        if not TRANSFORMERS_AVAILABLE or not self.sentiment_classifier:
            return self._fallback_classification(email_content)
        
        try:
            # First, let's use keyword matching combined with sentiment analysis
            keyword_result = self._keyword_classification(email_content)
            
            # If keyword classification is uncertain, we could use sentiment
            # to help decide between categories
            if keyword_result != 'general':
                return keyword_result
            
            # For general emails, we can use more sophisticated analysis
            # This is a simplified example - you could train a custom model
            return self._advanced_classification(email_content)
                
        except Exception as e:
            self.logger.error(f"Hugging Face classification failed: {e}")
            return self._fallback_classification(email_content)
    
    def _keyword_classification(self, email_content: str) -> str:
        """Enhanced keyword classification with scoring"""
        keywords = {
            'hardware': {
                'primary': ['hardware', 'laptop', 'computer', 'device', 'monitor', 'printer', 'keyboard', 'mouse'],
                'secondary': ['broken', 'repair', 'replace', 'malfunction', 'defective', 'warranty']
            },
            'software': {
                'primary': ['software', 'program', 'application', 'app', 'system', 'bug', 'error'],
                'secondary': ['crash', 'install', 'update', 'download', 'license', 'virus']
            },
            'order': {
                'primary': ['order', 'purchase', 'buy', 'delivery', 'shipping', 'product'],
                'secondary': ['cart', 'checkout', 'tracking', 'arrived', 'dispatch', 'package']
            },
            'payment': {
                'primary': ['payment', 'bill', 'invoice', 'money', 'pay', 'charge'],
                'secondary': ['refund', 'transaction', 'card', 'bank', 'receipt', 'cost']
            }
        }
        
        content_lower = email_content.lower()
        scores = {}
        
        for category, keyword_groups in keywords.items():
            primary_score = sum(2 for keyword in keyword_groups['primary'] if keyword in content_lower)
            secondary_score = sum(1 for keyword in keyword_groups['secondary'] if keyword in content_lower)
            scores[category] = primary_score + secondary_score
        
        if max(scores.values()) > 0:
            result = max(scores, key=scores.get)
            self.logger.info(f"Email classified as: {result} (keyword-enhanced)")
            return result
        
        return 'general'
    
    def _advanced_classification(self, email_content: str) -> str:
        """Advanced classification using context analysis"""
        # This is where you could implement more sophisticated logic
        # For now, we'll use keyword-based classification
        return self._fallback_classification(email_content)
    
    def _fallback_classification(self, email_content: str) -> str:
        """Fallback to simple keyword-based classification"""
        keywords = {
            'hardware': ['hardware', 'laptop', 'computer', 'mouse', 'keyboard', 'screen', 'monitor', 'device'],
            'software': ['software', 'program', 'application', 'bug', 'error', 'crash', 'install', 'update'],
            'order': ['order', 'purchase', 'buy', 'delivery', 'shipping', 'product', 'item'],
            'payment': ['payment', 'bill', 'invoice', 'money', 'pay', 'charge', 'refund', 'transaction'],
        }
        
        content_lower = email_content.lower()
        scores = {}
        
        for category, category_keywords in keywords.items():
            score = sum(1 for keyword in category_keywords if keyword in content_lower)
            scores[category] = score
        
        if max(scores.values()) > 0:
            result = max(scores, key=scores.get)
            self.logger.info(f"Email classified as: {result} (fallback)")
            return result
        
        self.logger.info("Email classified as: general (fallback)")
        return 'general'
    
    def train_custom_classifier(self, training_data: List[Dict]):
        """Train a custom classifier with your email data"""
        # This would require a more complex implementation
        # For now, we'll use the keyword-based approach
        self.logger.info("Custom training not implemented yet")
        pass
