# Email Segregation System

An intelligent email processing system that automatically classifies incoming emails using AI and routes them to appropriate departments with auto-replies and forwarding.

## 🎯 Overview

This system processes emails from `ouremailrepository@gmail.com`, classifies them using NLP/AI, sends auto-replies to customers, and forwards emails to the appropriate departments. The system ensures that only new emails are processed (no duplicates).

## ✨ Key Features

- **🔍 Intelligent Email Classification**: Uses AI (HuggingFace/OpenAI) to categorize emails into departments
- **📧 Auto-Reply System**: Sends personalized acknowledgment emails to senders
- **📬 Smart Email Forwarding**: Routes emails to appropriate department inboxes
- **🚫 Duplicate Prevention**: Only processes new emails, prevents duplicate replies/forwards
- **📊 Real-time Statistics**: Tracks processing statistics by department
- **🔒 Secure Authentication**: Gmail App Password support for enhanced security

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Email Inbox   │ - │ Email Processor │ - │   AI Classifier │
│ (Gmail IMAP)    │    │                 │    │ (HuggingFace)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                v                        v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Database     │ - │ Email Responder │ -<99> Department     │
│   (MongoDB)     │    │                 │    │ Classification  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                v
                  ┌─────────────────────────────┐
                  │     Auto-Reply + Forward    │
                  │  • hardware@company.com     │
                  │  • software@company.com     │
                  │  • orders@company.com       │
                  │  • accounts@company.com     │
                  │  • general@company.com      │
                  └─────────────────────────────┘
```

## 📁 Project Structure

```
Final Imp/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── .env.template              # Environment template
├── install.py                 # Dependency installer
├── setup.py                   # Package setup
├── run_email_system.bat       # Windows batch file to run system
├── email_segregation.log      # Application logs
│
├── src/                       # Source code
│   ├── email_processor.py     # Email fetching and processing
│   ├── email_responder.py     # Auto-reply and forwarding
│   ├── database.py           # MongoDB operations
│   ├── unified_classifier.py  # AI classification (main)
│   ├── huggingface_classifier.py  # HuggingFace NLP
│   ├── enhanced_keyword_classifier.py  # Keyword-based fallback
│   └── __init__.py
│
├── config/                    # Configuration
│   ├── settings.py           # Application settings
│   └── __init__.py
│
├── trash/                     # Moved unnecessary files
│   ├── old_documentation/    # Feature-specific docs
│   ├── test_scripts/        # Testing scripts
│   ├── old_features/        # Unused code
│   └── emails/              # Email dumps
│
└── Documentation/             # Important docs only
    ├── README.md             # This file
    ├── DEPLOYMENT_GUIDE.md   # Production deployment
    ├── PROJECT_STRUCTURE.md  # Code structure
    └── PROJECT_SUMMARY.md    # Project overview
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python install.py
```

### 2. Configure Environment
Copy `.env.template` to `.env` and configure:
```env
# Email Configuration
EMAIL_USERNAME=ouremailrepository@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_SMTP_SERVER=smtp.gmail.com:587

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=email_segregation_db

# Department Email Addresses
HARDWARE_EMAIL=hardware@company.com
SOFTWARE_EMAIL=software@company.com
ORDER_EMAIL=orders@company.com
PAYMENT_EMAIL=accounts@company.com
GENERAL_EMAIL=general@company.com

# Optional: OpenAI API (for enhanced classification)
OPENAI_API_KEY=your-openai-api-key
```

### 3. Run the System

#### Option 1: Continuous Mode (Recommended)
Runs continuously, checking for new emails every minute:
```bash
python main.py --mode continuous --interval 60
```

#### Option 2: Single Run Mode
Checks for emails once and exits:
```bash
python main.py --mode once
```

#### Option 3: Custom Interval
Continuous mode with custom check interval (in seconds):
```bash
python main.py --mode continuous --interval 30  # Check every 30 seconds
```

#### Option 4: Use Windows Batch Files
- **Interactive launcher**: `run_email_system.bat`
- **Direct continuous mode**: `run_continuous.bat`
- **Direct single run**: `run_once.bat`

## 🔧 Configuration

### Gmail Setup
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Use App Password** in `.env` file (not regular Gmail password)

### Department Configuration
The system classifies emails into these departments:

| Department | Description | Response Time | Default Email |
|------------|-------------|---------------|---------------|
| **Hardware** | Hardware support, technical issues | 24 hours | hardware@company.com |
| **Software** | Software support, bugs, features | 24 hours | software@company.com |
| **Order** | Sales, orders, product inquiries | 12 hours | orders@company.com |
| **Payment** | Billing, payments, accounts | 24 hours | accounts@company.com |
| **General** | General inquiries, other | 24 hours | general@company.com |

### MongoDB Setup
- **Local**: MongoDB running on localhost:27017
- **Cloud**: Update `MONGODB_URI` with your cloud connection string
- **Database**: `email_segregation_db` (auto-created)

## 🤖 AI Classification

The system uses a three-tier classification approach:

1. **Primary**: HuggingFace DistilBERT model (fast, accurate)
2. **Secondary**: OpenAI GPT (if API key provided)
3. **Fallback**: Enhanced keyword-based classification

### Classification Examples
- *"My laptop screen is flickering"* → **Hardware**
- *"The software crashes when I click save"* → **Software**
- *"I want to order 10 laptops"* → **Order**
- *"My payment was declined"* → **Payment**
- *"What are your business hours?"* → **General**

## 📧 Email Processing Workflow

### For Each New Email:
1. **Fetch**: System connects to Gmail IMAP and fetches only new emails
2. **Process**: Extract email content, sender, subject, date
3. **Classify**: AI determines appropriate department
4. **Store**: Email saved to MongoDB with classification
5. **Auto-Reply**: Personalized confirmation sent to sender
6. **Forward**: Email forwarded to department with context
7. **Log**: All operations logged for monitoring

### Auto-Reply Example
```
Subject: [Auto-Reply] Query Submitted

Thank you for contacting us regarding hardware support. 
Your query has been forwarded to our Hardware Support team 
and they will respond within 24 hours.

Best regards,
Email Segregation System
Your Company Name
```

### Forwarded Email Example
```
Subject: Forwarded message from company's mail-id - Hardware Department

This email has been automatically classified and forwarded to the Hardware Department.

--- ORIGINAL MESSAGE ---
From: customer@example.com
Date: 2025-01-12 10:30:00
Subject: Laptop screen issue
Classified as: Hardware Department

Message Content:
My laptop screen is flickering and making strange noises...

--- END OF ORIGINAL MESSAGE ---

This message was processed by the Email Segregation System.
Please respond to the original sender at: customer@example.com
```

## 🔄 Continuous Monitoring

### Default Behavior
By default, the system runs in **continuous mode**, checking for new emails every 60 seconds (1 minute). This ensures immediate processing of incoming emails without manual intervention.

### Continuous Mode Features
- **Persistent connections**: Database and email connections maintained for efficiency
- **Graceful shutdown**: Press Ctrl+C to stop the system safely
- **Error recovery**: Continues running even if individual cycles encounter errors
- **Real-time logging**: Detailed logs of each check cycle
- **Configurable intervals**: Customize how often to check for emails

### Example Continuous Mode Output
```
--- Email Check Cycle #1 at 2025-01-12 10:30:00 ---
Found 2 new emails to process
Successfully processed email from customer1@example.com -> hardware
Successfully processed email from customer2@example.com -> software
Successfully processed 2 out of 2 emails
Waiting 60 seconds until next check...

--- Email Check Cycle #2 at 2025-01-12 10:31:00 ---
No new emails to process
Waiting 60 seconds until next check...
```

### Stopping the System
- **Graceful shutdown**: Press `Ctrl+C` to stop safely
- **Automatic cleanup**: Connections closed and resources freed
- **Safe interruption**: Can be stopped at any time without data loss

## 📊 Monitoring & Logs

### Log Output Example
```
2025-01-12 10:30:15 - Starting Email Segregation System
2025-01-12 10:30:15 - Found 125 previously processed emails
2025-01-12 10:30:16 - Found 130 total emails, 5 new emails to process
2025-01-12 10:30:17 - Successfully processed email from customer@example.com - hardware
2025-01-12 10:30:17 - Auto-reply sent to customer@example.com for hardware department
2025-01-12 10:30:18 - Email forwarded to hardware@company.com for department: hardware
2025-01-12 10:30:20 - Successfully processed 5 out of 5 emails

=== Email Processing Statistics ===
Total emails processed: 130
Hardware department: 45
Software department: 32
Order department: 28
Payment department: 15
General department: 10
===================================
```

### Database Statistics
The system provides real-time statistics:
- Total emails processed
- Emails per department
- Processing success rate
- Error tracking

## 🛠️ Development

### Adding New Departments
1. **Update Configuration**: Add new department to `DEPARTMENT_EMAILS` in `config/settings.py`
2. **Update Classifier**: Modify classification logic in `src/unified_classifier.py`
3. **Update Auto-Reply**: Add department message in `src/email_responder.py`
4. **Update Statistics**: Add new department to stats in `src/database.py`

### Customizing Auto-Reply Messages
Edit the `department_messages` dictionary in `src/email_responder.py`:

```python
department_messages = {
    'hardware': "Your custom hardware message...",
    'software': "Your custom software message...",
    # ... other departments
}
```

### Customizing Email Forwarding
Modify the email body template in the `forward_email` method in `src/email_responder.py`.

## 🔒 Security

### Email Security
- ✅ Gmail App Password authentication (more secure than regular passwords)
- ✅ Environment variable storage for credentials
- ✅ No hardcoded sensitive information
- ✅ TLS/SSL encryption for email communication

### Data Security
- ✅ MongoDB for secure data storage
- ✅ Email content cleaning and sanitization
- ✅ Comprehensive audit logging
- ✅ No sensitive data in auto-replies

## 🚨 Troubleshooting

### Common Issues

#### "Failed to connect to email server"
- **Check Gmail credentials** in `.env` file
- **Use App Password** instead of regular Gmail password
- **Verify IMAP is enabled** in Gmail settings

#### "Failed to send auto-reply/forward"
- **Check SMTP server settings**
- **Verify email credentials**
- **Check network connectivity**

#### "No new emails found"
- **Verify emails exist** in Gmail inbox
- **Check email connection** is working
- **Review processed email logs**

#### "Database connection failed"
- **Ensure MongoDB is running**
- **Check connection string** in `.env`
- **Verify database permissions**

### Performance Optimization
- **MongoDB Indexing**: Automatic indexing on email UIDs for fast duplicate detection
- **Email Filtering**: Only new emails are processed, reducing bandwidth
- **Connection Pooling**: Efficient database and email server connections
- **Background Processing**: Non-blocking email operations

## 🔧 Maintenance

### Regular Tasks
- **Monitor logs** for errors or issues
- **Check email quotas** and limits
- **Rotate credentials** periodically
- **Update dependencies** regularly
- **Clean up old logs** and temporary files

### Backup & Recovery
- **Database Backups**: Regular MongoDB backups recommended
- **Configuration Backup**: Keep `.env` file securely backed up
- **Log Archival**: Rotate and archive log files

## 📈 Scaling

### For High Volume
- **Database Clustering**: Use MongoDB replica sets
- **Load Balancing**: Multiple processing instances
- **Queue Management**: Implement email processing queues
- **Monitoring**: Add application performance monitoring

### Enterprise Features
- **Multiple Email Accounts**: Support for multiple source emails
- **Advanced Classification**: Custom ML models for specific domains
- **Reporting Dashboard**: Web interface for statistics and monitoring
- **API Integration**: REST API for external system integration

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **MongoDB**: 4.0 or higher
- **Memory**: 2GB RAM minimum
- **Disk**: 1GB free space
- **Network**: Internet connection for email and AI services

### Python Dependencies
See `requirements.txt` for complete list:
- `transformers` - HuggingFace AI models
- `torch` - PyTorch for ML
- `pymongo` - MongoDB driver
- `python-dotenv` - Environment management
- `beautifulsoup4` - HTML email processing
- `openai` - OpenAI API (optional)

## 📞 Support

For questions or issues:
1. **Check Logs**: Review `email_segregation.log` for errors
2. **Verify Configuration**: Ensure `.env` is properly configured
3. **Test Components**: Use individual test scripts in `trash/test_scripts/`
4. **Check Documentation**: Review this README and other docs

## 📄 License

This project is proprietary software. All rights reserved.

---

**Email Segregation System** - Intelligent email processing with AI classification, auto-replies, and smart forwarding.
