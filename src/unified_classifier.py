import logging
from typing import Dict, List, Optional
from config.settings import Config

class UnifiedClassifier:
    """Unified classifier that can use multiple classification methods"""
    
    def __init__(self, preferred_method: str = 'huggingface'):
        self.logger = logging.getLogger(__name__)
        self.preferred_method = preferred_method
        self.classifiers = {}
        
        # Initialize available classifiers
        self._initialize_classifiers()
        
        self.logger.info(f"Unified classifier initialized with method: {preferred_method}")
    
    def _initialize_classifiers(self):
        """Initialize all available classifiers"""
        
        # 1. Enhanced Keyword Classifier (always available)
        try:
            from src.enhanced_keyword_classifier import EnhancedKeywordClassifier
            self.classifiers['enhanced_keyword'] = EnhancedKeywordClassifier()
            self.logger.info("Enhanced keyword classifier loaded")
        except Exception as e:
            self.logger.error(f"Failed to load enhanced keyword classifier: {e}")
        
        # 2. OpenAI Classifier (if API key available)
        try:
            if hasattr(Config, 'OPENAI_API_KEY') and Config.OPENAI_API_KEY:
                from src.openai_classifier import OpenAIClassifier
                self.classifiers['openai'] = OpenAIClassifier()
                self.logger.info("OpenAI classifier loaded")
        except Exception as e:
            self.logger.warning(f"OpenAI classifier not available: {e}")
        
        # 3. Hugging Face Classifier (if transformers available)
        try:
            from src.huggingface_classifier import HuggingFaceClassifier
            self.classifiers['huggingface'] = HuggingFaceClassifier()
            self.logger.info("Hugging Face classifier loaded")
        except Exception as e:
            self.logger.warning(f"Hugging Face classifier not available: {e}")
        
        # 4. Original MonkeyLearn Classifier (fallback)
        try:
            from src.classifier import EmailClassifier
            self.classifiers['monkeylearn'] = EmailClassifier()
            self.logger.info("MonkeyLearn classifier loaded")
        except Exception as e:
            self.logger.warning(f"MonkeyLearn classifier not available: {e}")
    
    def classify_email(self, email_content: str) -> str:
        """Classify email using the preferred method or fallback"""
        
        # Try preferred method first
        if self.preferred_method in self.classifiers:
            try:
                result = self.classifiers[self.preferred_method].classify_email(email_content)
                self.logger.info(f"Classification successful with {self.preferred_method}: {result}")
                return result
            except Exception as e:
                self.logger.error(f"Failed with preferred method {self.preferred_method}: {e}")
        
        # Try fallback methods in order of preference: Hugging Face -> OpenAI -> Enhanced keyword -> MonkeyLearn
        fallback_order = ['huggingface', 'openai', 'enhanced_keyword', 'monkeylearn']
        
        for method in fallback_order:
            if method in self.classifiers and method != self.preferred_method:
                try:
                    result = self.classifiers[method].classify_email(email_content)
                    self.logger.info(f"Classification successful with fallback {method}: {result}")
                    return result
                except Exception as e:
                    self.logger.error(f"Failed with fallback method {method}: {e}")
        
        # Ultimate fallback - simple keyword classification
        self.logger.warning("All classifiers failed, using simple fallback")
        return self._simple_fallback(email_content)
    
    def _simple_fallback(self, email_content: str) -> str:
        """Simple fallback classification method"""
        keywords = {
            'hardware': ['hardware', 'computer', 'laptop', 'device', 'monitor', 'printer'],
            'software': ['software', 'program', 'app', 'bug', 'error', 'install'],
            'order': ['order', 'delivery', 'shipping', 'product', 'tracking'],
            'payment': ['payment', 'bill', 'invoice', 'refund', 'charge']
        }
        
        content_lower = email_content.lower()
        scores = {}
        
        for category, category_keywords in keywords.items():
            score = sum(1 for keyword in category_keywords if keyword in content_lower)
            scores[category] = score
        
        if max(scores.values()) > 0:
            result = max(scores, key=scores.get)
            self.logger.info(f"Simple fallback classification: {result}")
            return result
        
        self.logger.info("Simple fallback classification: general")
        return 'general'
    
    def get_available_methods(self) -> List[str]:
        """Get list of available classification methods"""
        return list(self.classifiers.keys())
    
    def set_preferred_method(self, method: str) -> bool:
        """Set the preferred classification method"""
        if method in self.classifiers:
            self.preferred_method = method
            self.logger.info(f"Preferred method changed to: {method}")
            return True
        else:
            self.logger.error(f"Method {method} not available")
            return False
    
    def get_classification_details(self, email_content: str) -> Dict:
        """Get detailed classification results from all available methods"""
        results = {}
        
        for method_name, classifier in self.classifiers.items():
            try:
                result = classifier.classify_email(email_content)
                results[method_name] = {
                    'classification': result,
                    'status': 'success'
                }
                
                # Get confidence if available
                if hasattr(classifier, 'get_classification_confidence'):
                    try:
                        confidence = classifier.get_classification_confidence(email_content)
                        results[method_name]['confidence'] = confidence
                    except:
                        pass
                        
            except Exception as e:
                results[method_name] = {
                    'classification': 'error',
                    'status': 'failed',
                    'error': str(e)
                }
        
        return results
    
    def get_supported_departments(self) -> List[str]:
        """Get list of supported departments"""
        return ['hardware', 'software', 'order', 'payment', 'general']
    
    def validate_department(self, department: str) -> bool:
        """Validate if department is supported"""
        return department in self.get_supported_departments()
