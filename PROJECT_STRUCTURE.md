# Project Structure

## Directory Structure

```
Final Imp/
├── config/                 # Configuration module
│   ├── __init__.py
│   └── settings.py        # Application settings and configuration
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── classifier.py      # NLP email classification
│   ├── database.py        # MongoDB operations
│   ├── email_processor.py # Email fetching and processing
│   └── email_responder.py # Email response and forwarding
├── testing_utilities/     # Testing and development utilities
│   ├── generate_emails.py
│   ├── generate_enhanced_emails.py
│   ├── generated_emails.csv
│   └── enhanced_emails_dataset.csv
├── emails/                # Email backups (auto-created)
├── __pycache__/          # Python cache (auto-created)
├── .env                  # Environment variables (not in git)
├── .env.template         # Template for environment variables
├── .gitignore           # Git ignore rules
├── DEPLOYMENT_GUIDE.md  # Deployment instructions
├── email_segregation.log # Log file (auto-created)
├── install.py           # Installation script
├── main.py              # Main application entry point
├── MONKEYLEARN_SETUP.md # MonkeyLearn setup guide
├── PROJECT_STRUCTURE.md # This file
├── PROJECT_SUMMARY.md   # Project summary
├── README.md            # Main documentation
├── requirements.txt     # Python dependencies
├── setup.py             # Package setup
├── simple_demo.py       # Simple demo without dependencies
└── test_setup.py        # System setup test
```

## Key Files

### Main Application Files
- **main.py**: Main application entry point with full functionality
- **simple_demo.py**: Simplified demo version for testing
- **test_setup.py**: System setup verification script

### Configuration
- **.env**: Environment variables (credentials, API keys)
- **.env.template**: Template for environment setup
- **config/settings.py**: Application configuration management

### Core Modules
- **src/email_processor.py**: Email fetching, parsing, and processing
- **src/classifier.py**: NLP-based email classification
- **src/database.py**: MongoDB operations and data management
- **src/email_responder.py**: Email response and forwarding logic

### Documentation
- **README.md**: Complete user documentation
- **PROJECT_SUMMARY.md**: Project overview and accomplishments
- **DEPLOYMENT_GUIDE.md**: Step-by-step deployment instructions
- **MONKEYLEARN_SETUP.md**: MonkeyLearn API setup guide

### Installation & Setup
- **requirements.txt**: Python package dependencies
- **setup.py**: Package installation setup
- **install.py**: Automated installation script

## Module Dependencies

```
main.py
├── src/email_processor.py
├── src/classifier.py
├── src/email_responder.py
├── src/database.py
└── config/settings.py

simple_demo.py (standalone)

test_setup.py
├── src/* (all modules)
└── config/settings.py
```

## Data Flow

1. **Email Fetching**: `email_processor.py` connects to Gmail via IMAP
2. **Email Processing**: Parses and cleans email content
3. **Classification**: `classifier.py` categorizes emails by department
4. **Database Storage**: `database.py` stores processed emails in MongoDB
5. **Response**: `email_responder.py` sends auto-replies and forwards emails
6. **Logging**: All operations logged to `email_segregation.log`

## Configuration Files

### .env
Contains sensitive configuration:
- Email credentials
- MongoDB connection string
- MonkeyLearn API key
- Department email addresses

### config/settings.py
Loads and validates configuration from .env file and provides application-wide settings.

## Testing & Utilities

### testing_utilities/
Contains data generation scripts for testing:
- Email dataset generators
- Sample email data
- Development utilities

### test_setup.py
Verifies system setup:
- Module imports
- Configuration loading
- Database connectivity
- Classifier initialization
