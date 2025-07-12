import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Email Configuration
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_IMAP_SERVER = os.getenv('EMAIL_IMAP_SERVER', 'imap.gmail.com')
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com:587')
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'email_segregation_db')
    
    # MonkeyLearn API Configuration
    MONKEYLEARN_API_KEY = os.getenv('MONKEYLEARN_API_KEY')
    MONKEYLEARN_MODEL_ID = os.getenv('MONKEYLEARN_MODEL_ID', 'cl_WtsrTkFc')
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Department Email Configuration
    DEPARTMENT_EMAILS = {
        'hardware': os.getenv('HARDWARE_EMAIL', 'hardware@company.com'),
        'software': os.getenv('SOFTWARE_EMAIL', 'software@company.com'),
        'order': os.getenv('ORDER_EMAIL', 'orders@company.com'),
        'payment': os.getenv('PAYMENT_EMAIL', 'accounts@company.com'),
        'general': os.getenv('GENERAL_EMAIL', 'general@company.com')
    }
    
    # Email Templates
    AUTO_REPLY_SUBJECT = "[Auto-Reply] Query Submitted"
    FORWARD_SUBJECT = "Forwarded message from company's mail-id"
    
    # Validation
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        # Only email credentials are required for the three-tier classifier
        required_fields = [
            'EMAIL_USERNAME', 'EMAIL_PASSWORD'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        
        # Optional API keys (for enhanced functionality)
        optional_fields = {
            'OPENAI_API_KEY': 'OpenAI classifier will be unavailable',
            'MONKEYLEARN_API_KEY': 'MonkeyLearn classifier will be unavailable (legacy)'
        }
        
        missing_optional = []
        for field, message in optional_fields.items():
            if not getattr(cls, field):
                missing_optional.append(f"{field}: {message}")
        
        if missing_optional:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Optional configuration missing:")
            for msg in missing_optional:
                logger.warning(f"  - {msg}")
        
        return True
