import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import Config

class EmailResponder:
    """Handles email response and forwarding operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def send_auto_reply(self, to_email: str, department: str) -> bool:
        """Send an automatic reply to the sender based on the department"""
        try:
            # Construct email message
            subject = Config.AUTO_REPLY_SUBJECT
            
            # Create department-specific auto-reply messages
            department_messages = {
                'hardware': "Thank you for contacting us regarding hardware support. Your query has been forwarded to our Hardware Support team and they will respond within 24 hours.",
                'software': "Thank you for contacting us regarding software support. Your query has been forwarded to our Software Development team and they will respond within 24 hours.",
                'order': "Thank you for your order inquiry. Your query has been forwarded to our Order Management team and they will respond within 12 hours.",
                'payment': "Thank you for contacting us regarding payment matters. Your query has been forwarded to our Accounts team and they will respond within 24 hours.",
                'general': "Thank you for contacting us. Your query has been forwarded to our General Support team and they will respond within 24 hours."
            }
            
            body = department_messages.get(department, department_messages['general'])
            body += "\n\nBest regards,\nEmail Segregation System\nYour Company Name"
            
            msg = self._construct_email_message(to_email, Config.EMAIL_USERNAME, subject, body)
            
            # Send email
            self._send_email(msg, to_email)
            
            self.logger.info(f"Auto-reply sent to {to_email} for {department} department")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send auto-reply to {to_email}: {e}")
            return False
    
    def forward_email(self, from_email: str, department: str, email_content: str, original_subject: str = "", date: str = "") -> bool:
        """Forward an email to the appropriate department"""
        try:
            department_mapping = Config.DEPARTMENT_EMAILS
            to_email = department_mapping.get(department, Config.DEPARTMENT_EMAILS['general'])
            
            # Construct email message with better formatting
            subject = f"{Config.FORWARD_SUBJECT} - {department.title()} Department"
            if original_subject:
                subject += f" - {original_subject}"
            
            # Create a well-formatted forwarded email body
            body = f"""This email has been automatically classified and forwarded to the {department.title()} Department.

--- ORIGINAL MESSAGE ---
From: {from_email}
Date: {date if date else 'Not specified'}
Subject: {original_subject if original_subject else 'No subject'}
Classified as: {department.title()} Department

Message Content:
{email_content}

--- END OF ORIGINAL MESSAGE ---

This message was processed by the Email Segregation System.
Please respond to the original sender at: {from_email}
"""
            
            msg = self._construct_email_message(to_email, Config.EMAIL_USERNAME, subject, body)
            
            # Send email
            self._send_email(msg, to_email)
            
            self.logger.info(f"Email forwarded to {to_email} for department: {department}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to forward email to {department} department: {e}")
            return False
    
    def _construct_email_message(self, to_email: str, from_email: str, subject: str, body: str) -> MIMEMultipart:
        """Construct email message with given parameters"""
        msg = MIMEMultipart()
        msg['To'] = to_email
        msg['From'] = from_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        return msg
    
    def _send_email(self, msg: MIMEMultipart, to_email: str) -> bool:
        """Send the constructed email message"""
        try:
            # Set up SMTP server
            smtp_server, smtp_port = Config.EMAIL_SMTP_SERVER.split(':')
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()
            server.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
            
            # Send the email message
            server.send_message(msg, from_addr=Config.EMAIL_USERNAME, to_addrs=[to_email])
            server.quit()
            
            self.logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending email to {to_email}: {e}")
            return False

