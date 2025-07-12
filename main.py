#!/usr/bin/env python3
"""
Email Segregation System
Automatically processes incoming emails, classifies them using NLP, 
and forwards them to appropriate departments with auto-replies.
"""

import logging
import sys
import os
import csv
import time
import signal
from datetime import datetime
from typing import List, Dict

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

from src.email_processor import EmailProcessor
from src.unified_classifier import UnifiedClassifier
from src.email_responder import EmailResponder
from src.database import DatabaseManager
from config.settings import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_segregation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class EmailSegregationSystem:
    """Main class for the email segregation system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_processor = EmailProcessor()
        self.classifier = UnifiedClassifier(preferred_method='openai')
        self.responder = EmailResponder()
        self.db_manager = DatabaseManager()
        self.running = True
        self.check_interval = 60  # Check every 60 seconds (1 minute)
        
        # Validate configuration
        try:
            Config.validate_config()
            self.logger.info("Configuration validated successfully")
        except ValueError as e:
            self.logger.error(f"Configuration validation failed: {e}")
            sys.exit(1)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.running = False
    
    def run_continuous(self):
        """Run the system continuously, checking for emails every minute"""
        self.logger.info("Starting Email Segregation System in CONTINUOUS mode")
        self.logger.info(f"Will check for new emails every {self.check_interval} seconds")
        
        try:
            # Connect to database once
            if not self.db_manager.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Connect to email server once
            if not self.email_processor.connect_to_email():
                self.logger.error("Failed to connect to email server")
                return False
            
            self.logger.info("Email Segregation System is now running continuously...")
            self.logger.info("Press Ctrl+C to stop the system gracefully")
            
            cycle_count = 0
            while self.running:
                cycle_count += 1
                self.logger.info(f"\n--- Email Check Cycle #{cycle_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
                
                try:
                    # Check for new emails
                    self._check_and_process_emails()
                    
                    # Wait for the next check (with ability to interrupt)
                    if self.running:
                        self.logger.info(f"Waiting {self.check_interval} seconds until next check...")
                        for i in range(self.check_interval):
                            if not self.running:
                                break
                            time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error in email check cycle: {e}")
                    self.logger.info("Continuing with next cycle...")
                    time.sleep(5)  # Short delay before retrying
            
            self.logger.info("Email Segregation System stopped gracefully")
            return True
            
        except Exception as e:
            self.logger.error(f"Critical error in continuous mode: {e}")
            return False
        finally:
            self.cleanup()
    
    def run_once(self):
        """Run the system once and exit (original behavior)"""
        self.logger.info("Starting Email Segregation System in SINGLE-RUN mode")
        
        try:
            # Connect to database
            if not self.db_manager.connect():
                self.logger.error("Failed to connect to database")
                return False
            
            # Connect to email server
            if not self.email_processor.connect_to_email():
                self.logger.error("Failed to connect to email server")
                return False
            
            # Check and process emails once
            self._check_and_process_emails()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in single-run execution: {e}")
            return False
        finally:
            self.cleanup()
    
    def _check_and_process_emails(self):
        """Check for new emails and process them"""
        try:
            # Get list of already processed email UIDs from database
            processed_uids = self.db_manager.get_processed_uids()
            
            # Fetch only new emails that haven't been processed
            emails = self.email_processor.fetch_emails(processed_uids)
            
            if not emails:
                self.logger.info("No new emails to process")
                return
            
            self.logger.info(f"Found {len(emails)} new emails to process")
            
            # Process each email
            processed_count = 0
            for email_data in emails:
                if self.process_single_email(email_data):
                    processed_count += 1
            
            self.logger.info(f"Successfully processed {processed_count} out of {len(emails)} emails")
            
            # Display statistics only when emails were processed
            if processed_count > 0:
                self.display_statistics()
                
        except Exception as e:
            self.logger.error(f"Error in email check and process: {e}")
            raise
    
    def process_single_email(self, email_data: Dict) -> bool:
        """Process a single email through the entire pipeline"""
        try:
            # Check if email already exists in database
            if self.db_manager.email_exists(email_data):
                self.logger.info(f"Email from {email_data['from_email']} already processed, skipping")
                return False
            
            # Classify the email
            department = self.classifier.classify_email(email_data['cleaned_content'])
            email_data['department'] = department
            
            # Insert into database
            if not self.db_manager.insert_email(email_data):
                self.logger.error(f"Failed to insert email into database")
                return False
            
            # Send auto-reply to sender
            if not self.responder.send_auto_reply(email_data['from_email'], department):
                self.logger.warning(f"Failed to send auto-reply to {email_data['from_email']}")
            
            # Forward email to appropriate department
            if not self.responder.forward_email(
                email_data['from_email'], 
                department, 
                email_data['cleaned_content'],
                email_data.get('subject', ''),
                email_data.get('date', '')
            ):
                self.logger.warning(f"Failed to forward email to {department} department")
            
            self.logger.info(f"Successfully processed email from {email_data['from_email']} -> {department}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing email: {e}")
            return False
    
    def display_statistics(self):
        """Display processing statistics"""
        try:
            stats = self.db_manager.get_database_stats()
            self.logger.info("=== Email Processing Statistics ===")
            self.logger.info(f"Total emails processed: {stats.get('total_emails', 0)}")
            self.logger.info(f"Hardware department: {stats.get('hardware_emails', 0)}")
            self.logger.info(f"Software department: {stats.get('software_emails', 0)}")
            self.logger.info(f"Order department: {stats.get('order_emails', 0)}")
            self.logger.info(f"Payment department: {stats.get('payment_emails', 0)}")
            self.logger.info(f"General department: {stats.get('general_emails', 0)}")
            self.logger.info("===================================")
        except Exception as e:
            self.logger.error(f"Error displaying statistics: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.email_processor.disconnect_from_email()
            self.db_manager.disconnect()
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

def main():
    """Main entry point"""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Email Segregation System')
    parser.add_argument('--mode', choices=['continuous', 'once'], default='continuous',
                       help='Run mode: continuous (default) or once')
    parser.add_argument('--interval', type=int, default=60,
                       help='Check interval in seconds for continuous mode (default: 60)')
    
    args = parser.parse_args()
    
    try:
        # Create the system
        system = EmailSegregationSystem()
        
        # Set the check interval if provided
        if args.interval > 0:
            system.check_interval = args.interval
            
        # Run in the specified mode
        if args.mode == 'continuous':
            print(f"Starting Email Segregation System in CONTINUOUS mode (checking every {args.interval} seconds)")
            print("Press Ctrl+C to stop the system gracefully")
            success = system.run_continuous()
        else:
            print("Starting Email Segregation System in SINGLE-RUN mode")
            success = system.run_once()
        
        if success:
            print("Email segregation system completed successfully!")
            return 0
        else:
            print("Email segregation system failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
