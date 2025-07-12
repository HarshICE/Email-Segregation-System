import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from datetime import datetime
from typing import Dict, List, Optional
from config.settings import Config

class DatabaseManager:
    """Handles all MongoDB operations for the email segregation system"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(Config.MONGODB_URI)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[Config.MONGODB_DATABASE]
            self.collection = self.db.emails
            
            # Create indexes for better performance
            self._create_indexes()
            
            self.logger.info("Successfully connected to MongoDB")
            return True
        except ConnectionFailure as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def _create_indexes(self):
        """Create indexes for the emails collection to improve query performance"""
        try:
            # Create index on uid (unique to prevent duplicates)
            self.collection.create_index('uid', unique=True, background=True)
            # Create index on message_id (unique, sparse to allow null values)
            self.collection.create_index('message_id', unique=True, sparse=True, background=True)
            # Create compound index for fallback duplicate detection
            self.collection.create_index([('date', 1), ('from_email', 1), ('subject', 1)], background=True)
            self.logger.info("Database indexes created successfully")
        except PyMongoError as e:
            self.logger.warning(f"Could not create indexes (they may already exist): {e}")
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.logger.info("Disconnected from MongoDB")
    
    def email_exists(self, email_data: Dict) -> bool:
        """Check if email already exists in database using unique identifiers"""
        try:
            # Primary check: UID (most reliable)
            uid_query = {'uid': email_data.get('uid')}
            if self.collection.find_one(uid_query):
                return True
            
            # Secondary check: Message-ID (if available)
            message_id = email_data.get('message_id')
            if message_id:
                message_id_query = {'message_id': message_id}
                if self.collection.find_one(message_id_query):
                    return True
            
            # Fallback check: combination of date, sender, and subject
            fallback_query = {
                'date': email_data.get('date'),
                'from_email': email_data.get('from_email'),
                'subject': email_data.get('subject')
            }
            return self.collection.find_one(fallback_query) is not None
            
        except PyMongoError as e:
            self.logger.error(f"Error checking email existence: {e}")
            return False
    
    def insert_email(self, email_data: Dict) -> bool:
        """Insert new email into database"""
        try:
            # Add timestamp for when email was processed
            email_data['processed_at'] = datetime.now()
            
            result = self.collection.insert_one(email_data)
            if result.inserted_id:
                self.logger.info(f"Email inserted with ID: {result.inserted_id}")
                return True
            return False
        except PyMongoError as e:
            self.logger.error(f"Error inserting email: {e}")
            return False
    
    def get_all_emails(self) -> List[Dict]:
        """Retrieve all emails from database"""
        try:
            emails = list(self.collection.find())
            return emails
        except PyMongoError as e:
            self.logger.error(f"Error retrieving emails: {e}")
            return []
    
    def get_emails_by_department(self, department: str) -> List[Dict]:
        """Retrieve emails for a specific department"""
        try:
            emails = list(self.collection.find({'department': department}))
            return emails
        except PyMongoError as e:
            self.logger.error(f"Error retrieving emails for department {department}: {e}")
            return []
    
    def update_email_status(self, email_id: str, status: str) -> bool:
        """Update email processing status"""
        try:
            result = self.collection.update_one(
                {'_id': email_id},
                {'$set': {'status': status, 'updated_at': datetime.now()}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            self.logger.error(f"Error updating email status: {e}")
            return False
    
    def get_processed_uids(self) -> List[str]:
        """Get list of all processed email UIDs"""
        try:
            # Only get the uid field to minimize data transfer
            processed_emails = self.collection.find({}, {'uid': 1, '_id': 0})
            uids = [email.get('uid') for email in processed_emails if email.get('uid')]
            self.logger.info(f"Found {len(uids)} processed email UIDs")
            return uids
        except PyMongoError as e:
            self.logger.error(f"Error getting processed UIDs: {e}")
            return []
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            stats = {
                'total_emails': self.collection.count_documents({}),
                'hardware_emails': self.collection.count_documents({'department': 'hardware'}),
                'software_emails': self.collection.count_documents({'department': 'software'}),
                'order_emails': self.collection.count_documents({'department': 'order'}),
                'payment_emails': self.collection.count_documents({'department': 'payment'}),
                'general_emails': self.collection.count_documents({'department': 'general'})
            }
            return stats
        except PyMongoError as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {}
