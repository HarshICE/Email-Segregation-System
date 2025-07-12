import email
import imaplib
import logging
import os
from bs4 import BeautifulSoup
# from cleantext import clean  # Optional dependency
from typing import Dict, List, Optional
from config.settings import Config

class EmailProcessor:
    """Handles email fetching and processing operations"""
    
    def __init__(self):
        self.mail = None
        self.logger = logging.getLogger(__name__)
        
    def connect_to_email(self) -> bool:
        """Connect to email server using IMAP"""
        try:
            self.mail = imaplib.IMAP4_SSL(Config.EMAIL_IMAP_SERVER)
            self.mail.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
            self.mail.select("inbox")
            self.logger.info("Successfully connected to email server")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to email server: {e}")
            return False
    
    def disconnect_from_email(self):
        """Disconnect from email server"""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
                self.logger.info("Disconnected from email server")
            except:
                pass
    
    def _reconnect(self) -> bool:
        """Reconnect to email server"""
        try:
            # Close existing connection
            self.disconnect_from_email()
            
            # Establish new connection
            self.mail = imaplib.IMAP4_SSL(Config.EMAIL_IMAP_SERVER)
            self.mail.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
            self.mail.select("inbox")
            self.logger.info("Successfully reconnected to email server")
            return True
        except Exception as e:
            self.logger.error(f"Failed to reconnect to email server: {e}")
            return False
    
    def fetch_emails(self, processed_uids: List[str] = None) -> List[Dict]:
        """Fetch only new emails from inbox that haven't been processed"""
        if not self.mail:
            self.logger.error("No email connection established")
            return []
        
        try:
            # Refresh the mailbox to ensure we see the latest emails
            try:
                self.mail.select("inbox")
            except Exception as e:
                self.logger.warning(f"Failed to refresh inbox, attempting reconnection: {e}")
                # Attempt to reconnect if refresh fails
                if not self._reconnect():
                    self.logger.error("Failed to reconnect to email server")
                    return []
            
            result, data = self.mail.uid('search', None, "ALL")
            if result != 'OK':
                self.logger.error("Failed to search emails")
                return []
            
            all_email_uids = data[0].split()
            processed_uids = processed_uids or []
            
            # Convert processed UIDs to bytes for comparison
            processed_uids_bytes = [uid.encode('utf-8') if isinstance(uid, str) else uid for uid in processed_uids]
            
            # Filter out already processed emails
            new_email_uids = [uid for uid in all_email_uids if uid not in processed_uids_bytes]
            
            self.logger.info(f"Found {len(all_email_uids)} total emails, {len(new_email_uids)} new emails to process")
            
            emails = []
            for uid in new_email_uids:
                email_data = self._process_single_email(uid)
                if email_data:
                    emails.append(email_data)
            
            self.logger.info(f"Successfully fetched {len(emails)} new emails")
            return emails
            
        except Exception as e:
            self.logger.error(f"Error fetching emails: {e}")
            return []
    
    def _process_single_email(self, uid: bytes) -> Optional[Dict]:
        """Process a single email and extract relevant information"""
        try:
            result, email_data = self.mail.uid('fetch', uid, '(RFC822)')
            if result != 'OK':
                return None
            
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)
            
            # Extract email metadata
            from_header = email_message.get('From', '')
            to_header = email_message.get('To', '')
            subject = email_message.get('Subject', '')
            date = email_message.get('Date', '')
            message_id = email_message.get('Message-ID', '')
            
            # Extract sender email address
            from_email = self._extract_email_address(from_header)
            
            # Extract and clean email content
            email_content = self._extract_email_content(email_message)
            cleaned_content = self._clean_text(email_content)
            
            email_info = {
                'uid': uid.decode('utf-8'),
                'message_id': message_id,
                'from_header': from_header,
                'from_email': from_email,
                'to_header': to_header,
                'subject': subject,
                'date': date,
                'raw_content': email_content,
                'cleaned_content': cleaned_content,
                'status': 'unprocessed'
            }
            
            return email_info
            
        except Exception as e:
            self.logger.error(f"Error processing email {uid}: {e}")
            return None
    
    def _extract_email_address(self, from_header: str) -> str:
        """Extract email address from From header"""
        try:
            if '<' in from_header and '>' in from_header:
                start = from_header.find('<') + 1
                end = from_header.find('>')
                return from_header[start:end]
            else:
                # If no brackets, assume the whole string is the email
                return from_header.strip()
        except:
            return from_header
    
    def _extract_email_content(self, email_message) -> str:
        """Extract text content from email message"""
        content = ""
        
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            content += payload.decode('utf-8', errors='ignore')
                    elif part.get_content_type() == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            # Convert HTML to text
                            soup = BeautifulSoup(payload.decode('utf-8', errors='ignore'), 'html.parser')
                            content += soup.get_text()
            else:
                # Single part message
                payload = email_message.get_payload(decode=True)
                if payload:
                    content = payload.decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.error(f"Error extracting email content: {e}")
        
        return content
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        try:
            # Simple text cleaning without external dependencies
            if not text:
                return ""
            
            # Remove extra whitespace and normalize
            cleaned = ' '.join(text.split())
            
            # Convert to lowercase for classification
            cleaned = cleaned.lower()
            
            # Remove some common noise characters
            cleaned = cleaned.replace('\r', ' ').replace('\n', ' ')
            
            return cleaned
        except Exception as e:
            self.logger.error(f"Error cleaning text: {e}")
            return text
    
    def save_email_to_file(self, email_data: Dict, filename: str) -> bool:
        """Save email content to file (for debugging/backup)"""
        try:
            emails_dir = os.path.join(os.getcwd(), "emails")
            if not os.path.exists(emails_dir):
                os.makedirs(emails_dir)
            
            file_path = os.path.join(emails_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(email_data.get('cleaned_content', ''))
            
            return True
        except Exception as e:
            self.logger.error(f"Error saving email to file: {e}")
            return False
