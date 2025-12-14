"""
Support Case Automation System - Streamlit App
Complete workflow with Supabase authentication and email verification
Production-ready with proper error handling and modular design
"""

import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import hashlib
import json
from typing import Optional, Dict, List
import time
import re

# ============================================================================
# PAGE CONFIGURATION (MUST BE FIRST STREAMLIT COMMAND)
# ============================================================================

st.set_page_config(
    page_title="Support Automation System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# IMPORT CONFIGURATION (After set_page_config)
# ============================================================================

try:
    from config import (
        SUPABASE_CONFIG, 
        EMAIL_CONFIG, 
        MANUFACTURERS,
        TRANSLATION_CONFIG,
        SECURITY_CONFIG,
        BUSINESS_CONFIG,
        ADMIN_CONFIG,
        ENVIRONMENT,
        get_config_summary
    )
except ImportError:
    # Fallback if config.py is not available - provide defaults
    SUPABASE_CONFIG = {
        'url': 'https://eetdfpfojtktsicojqst.supabase.co',
        'key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVldGRmcGZvanRrdHNpY29qcXN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MzE0NzcsImV4cCI6MjA4MTIwNzQ3N30.m1ESYsxFBO-ECPK9vhfNrOVz9UCv29PVn3igwq5nqy4',
        'use_mock': True
    }
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': 'your-email@gmail.com',
        'sender_password': 'your-app-password',
        'company_name': 'Support Automation System',
        'use_mock': True
    }
    MANUFACTURERS = {
        'manufacturer_1': {
            'name': 'Tech Solutions Inc.',
            'api_url': 'https://api.techsolutions.com',
            'email': 'support@techsolutions.com'
        },
        'manufacturer_2': {
            'name': 'Global Parts Ltd.',
            'api_url': 'https://api.globalparts.com',
            'email': 'support@globalparts.com'
        },
        'manufacturer_3': {
            'name': 'Innovation Corp.',
            'api_url': 'https://api.innovation.com',
            'email': 'support@innovation.com'
        }
    }
    SECURITY_CONFIG = {
        'min_password_length': 8,
        'verification_code_expiry_minutes': 10,
        'max_login_attempts': 5,
        'session_timeout_hours': 24
    }
    BUSINESS_CONFIG = {
        'reminder_threshold_hours': 24,
        'exclude_weekends': True,
        'auto_approve_replies': False
    }
    TRANSLATION_CONFIG = {
        'provider': 'google',
        'api_key': '',
        'use_mock': True,
        'auto_detect_language': True,
        'supported_languages': {
            'en': 'English',
            'da': 'Danish',
            'de': 'German',
            'fr': 'French',
            'es': 'Spanish',
            'sv': 'Swedish',
            'no': 'Norwegian'
        }
    }
    ADMIN_CONFIG = {
        'username': 'admin',
        'email': 'admin@supportautomation.com',
        'password': 'Admin@123456',
        'enabled': True
    }
    ENVIRONMENT = 'development'

# ============================================================================
# CONFIGURATION (Legacy - kept for backwards compatibility)
# ============================================================================

# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    min_length = SECURITY_CONFIG.get('min_password_length', 8)
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def validate_username(username: str) -> tuple[bool, str]:
    """Validate username"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, hyphens, and underscores"
    return True, "Username is valid"

def authenticate_admin(username: str, password: str) -> bool:
    """Authenticate admin user"""
    if not ADMIN_CONFIG.get('enabled', False):
        return False
    
    return (username == ADMIN_CONFIG['username'] and 
            password == ADMIN_CONFIG['password'])

def is_admin_user() -> bool:
    """Check if current session user is admin"""
    if not st.session_state.get('authenticated', False):
        return False
    return st.session_state.get('is_admin', False)

# ============================================================================
# SUPABASE DATABASE CLIENT
# ============================================================================

@st.cache_resource
def get_database_client():
    """Get or create the database client instance (persists across sessions)"""
    return SupabaseClient()

class SupabaseClient:
    """
    Supabase Database Client
    Handles all database operations for users and support cases
    """
    
    def __init__(self):
        # For demo purposes, using in-memory storage
        # Replace with actual Supabase client in production
        self.users_table = {}
        self.cases_table = {}
        self.use_mock = SUPABASE_CONFIG.get('use_mock', True)
        self.use_rest_client = False
        
        # Initialize real Supabase client for production
        if not self.use_mock:
            # Try REST API client first (more reliable)
            try:
                from supabase_rest_client import SupabaseRESTClient
                self.client = SupabaseRESTClient(
                    SUPABASE_CONFIG['url'],
                    SUPABASE_CONFIG['key']
                )
                self.use_rest_client = True
                print("✅ Supabase REST API client initialized successfully")
            except Exception as e:
                # Fall back to SDK if REST client fails
                try:
                    from supabase import create_client, Client
                    
                    # Create client with proper configuration
                    self.client: Client = create_client(
                        supabase_url=SUPABASE_CONFIG['url'],
                        supabase_key=SUPABASE_CONFIG['key']
                    )
                    self.use_rest_client = False
                    print("✅ Supabase SDK client initialized successfully")
                except ImportError:
                    st.error("⚠️ Supabase library not installed. Run: pip install supabase")
                    st.info("💡 Falling back to mock database for development")
                    self.use_mock = True
                except TypeError as e:
                    # Handle version incompatibility - try REST client
                    if 'proxy' in str(e):
                        st.warning("⚠️ Supabase SDK has compatibility issues. Using REST API instead...")
                        try:
                            from supabase_rest_client import SupabaseRESTClient
                            self.client = SupabaseRESTClient(
                                SUPABASE_CONFIG['url'],
                                SUPABASE_CONFIG['key']
                            )
                            self.use_rest_client = True
                            print("✅ Switched to REST API client")
                        except:
                            st.error("⚠️ Failed to initialize any Supabase client. Falling back to mock database.")
                            self.use_mock = True
                    else:
                        st.error(f"⚠️ Failed to connect to Supabase: {str(e)}")
                        st.info("💡 Falling back to mock database for development")
                        self.use_mock = True
                except Exception as e:
                    st.error(f"⚠️ Failed to connect to Supabase: {str(e)}")
                    st.info("💡 Falling back to mock database for development")
                    self.use_mock = True
    
    # ========================================================================
    # USER TABLE OPERATIONS
    # ========================================================================
    
    def create_user(self, username: str, email: str, password: str) -> Dict:
        """
        Create new user in database
        
        SQL for Supabase table creation:
        
        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            verified BOOLEAN DEFAULT FALSE,
            last_login TIMESTAMP
        );
        
        CREATE INDEX idx_users_email ON users(email);
        CREATE INDEX idx_users_username ON users(username);
        """
        
        if self.use_mock:
            # Mock implementation
            if email in self.users_table:
                return {'error': 'Email already registered'}
            
            # Check if username already exists
            for user in self.users_table.values():
                if user['username'].lower() == username.lower():
                    return {'error': 'Username already taken'}
            
            user_id = f"user_{len(self.users_table) + 1}"
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            self.users_table[email] = {
                'id': user_id,
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'created_at': datetime.now().isoformat(),
                'verified': False,
                'last_login': None
            }
            
            return {'success': True, 'user_id': user_id}
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                # Using REST client
                return self.client.create_user(username, email, password)
            else:
                # Using SDK
                try:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    result = self.client.table('users').insert({
                        'username': username,
                        'email': email,
                        'password_hash': password_hash
                    }).execute()
                    
                    if result.data:
                        return {'success': True, 'user_id': result.data[0]['id']}
                    else:
                        return {'error': 'Failed to create user'}
                except Exception as e:
                    error_msg = str(e)
                    if 'duplicate key' in error_msg.lower() or 'unique' in error_msg.lower():
                        if 'email' in error_msg.lower():
                            return {'error': 'Email already registered'}
                        elif 'username' in error_msg.lower():
                            return {'error': 'Username already taken'}
                    return {'error': f'Registration failed: {error_msg}'}
    
    def authenticate_user(self, email: str, password: str) -> Dict:
        """Authenticate user with email and password"""
        
        if self.use_mock:
            # Mock implementation
            if email not in self.users_table:
                return {'error': 'Invalid email or password'}
            
            user = self.users_table[email]
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if user['password_hash'] != password_hash:
                return {'error': 'Invalid email or password'}
            
            return {'success': True, 'user': user}
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                # Using REST client
                return self.client.authenticate_user(email, password)
            else:
                # Using SDK
                try:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    result = self.client.table('users').select('*').eq(
                        'email', email
                    ).eq('password_hash', password_hash).execute()
                    
                    if not result.data or len(result.data) == 0:
                        return {'error': 'Invalid email or password'}
                    
                    return {'success': True, 'user': result.data[0]}
                except Exception as e:
                    return {'error': f'Authentication failed: {str(e)}'}
    
    def verify_user(self, email: str) -> bool:
        """Mark user as verified after email confirmation"""
        
        if self.use_mock:
            # Mock implementation
            if email in self.users_table:
                self.users_table[email]['verified'] = True
                return True
            return False
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                return self.client.verify_user(email)
            else:
                try:
                    self.client.table('users').update({
                        'verified': True
                    }).eq('email', email).execute()
                    return True
                except:
                    return False
    
    def update_last_login(self, email: str):
        """Update user's last login timestamp"""
        
        if self.use_mock:
            if email in self.users_table:
                self.users_table[email]['last_login'] = datetime.now().isoformat()
        else:
            if self.use_rest_client:
                self.client.update_last_login(email)
            else:
                try:
                    self.client.table('users').update({
                        'last_login': datetime.now().isoformat()
                    }).eq('email', email).execute()
                except:
                    pass
    
    # ========================================================================
    # SUPPORT CASES TABLE OPERATIONS
    # ========================================================================
    
    def create_support_case(self, case_data: Dict) -> str:
        """
        Create new support case in database
        
        SQL for Supabase table creation:
        
        CREATE TABLE support_cases (
            case_id TEXT PRIMARY KEY,
            user_email TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
            original_query TEXT NOT NULL,
            language TEXT NOT NULL,
            manufacturer_id TEXT NOT NULL,
            manufacturer_name TEXT NOT NULL,
            translated_query TEXT,
            task_number TEXT UNIQUE,
            status TEXT DEFAULT 'awaiting_reply',
            submitted_at TIMESTAMP DEFAULT NOW(),
            forwarded_at TIMESTAMP,
            manufacturer_reply TEXT,
            reply_translated TEXT,
            reply_received_at TIMESTAMP,
            reminder_sent BOOLEAN DEFAULT FALSE,
            reminder_sent_at TIMESTAMP,
            needs_approval BOOLEAN DEFAULT FALSE,
            approved BOOLEAN DEFAULT FALSE,
            approved_at TIMESTAMP,
            notes TEXT
        );
        
        CREATE INDEX idx_cases_user_email ON support_cases(user_email);
        CREATE INDEX idx_cases_task_number ON support_cases(task_number);
        CREATE INDEX idx_cases_status ON support_cases(status);
        CREATE INDEX idx_cases_submitted_at ON support_cases(submitted_at DESC);
        """
        
        case_id = f"CASE-{int(time.time())}-{random.randint(100, 999)}"
        case_data['case_id'] = case_id
        case_data['submitted_at'] = datetime.now().isoformat()
        case_data['forwarded_at'] = datetime.now().isoformat()
        
        if self.use_mock:
            # Mock implementation
            self.cases_table[case_id] = case_data
            return case_id
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                return self.client.create_support_case(case_data)
            else:
                try:
                    result = self.client.table('support_cases').insert(
                        case_data
                    ).execute()
                    return result.data[0]['case_id']
                except Exception as e:
                    print(f"Error creating case: {e}")
                    return None
    
    def get_user_cases(self, user_email: str) -> List[Dict]:
        """Get all support cases for a specific user"""
        
        if self.use_mock:
            # Mock implementation
            return [
                case for case in self.cases_table.values()
                if case.get('user_email') == user_email
            ]
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                return self.client.get_user_cases(user_email)
            else:
                try:
                    result = self.client.table('support_cases').select('*').eq(
                        'user_email', user_email
                    ).order('submitted_at', desc=True).execute()
                    return result.data
                except Exception as e:
                    print(f"Error fetching cases: {e}")
                    return []
    
    def get_case_by_id(self, case_id: str) -> Optional[Dict]:
        """Get specific case by case_id"""
        
        if self.use_mock:
            return self.cases_table.get(case_id)
        else:
            if self.use_rest_client:
                return self.client.get_case_by_id(case_id)
            else:
                try:
                    result = self.client.table('support_cases').select('*').eq(
                        'case_id', case_id
                    ).execute()
                    return result.data[0] if result.data else None
                except:
                    return None
    
    def update_case(self, case_id: str, updates: Dict) -> bool:
        """Update support case with new information"""
        
        if self.use_mock:
            # Mock implementation
            if case_id in self.cases_table:
                self.cases_table[case_id].update(updates)
                return True
            return False
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                return self.client.update_case(case_id, updates)
            else:
                try:
                    self.client.table('support_cases').update(updates).eq(
                        'case_id', case_id
                    ).execute()
                    return True
                except:
                    return False
    
    def get_overdue_cases(self) -> List[Dict]:
        """
        Get cases that are overdue for manufacturer response
        (No reply within 24 business hours, excluding weekends)
        """
        
        if self.use_mock:
            # Mock implementation
            overdue = []
            for case in self.cases_table.values():
                if case.get('status') == 'awaiting_reply' and not case.get('reminder_sent'):
                    forwarded_time = datetime.fromisoformat(case['forwarded_at'])
                    if self._is_overdue(forwarded_time):
                        overdue.append(case)
            return overdue
        else:
            # Real Supabase implementation
            if self.use_rest_client:
                # REST client doesn't have complex filtering, so get all and filter
                try:
                    all_cases = self.client.get_all_cases()
                    overdue = []
                    for case in all_cases:
                        if case.get('status') == 'awaiting_reply' and not case.get('reminder_sent'):
                            if case.get('forwarded_at'):
                                forwarded_time = datetime.fromisoformat(case['forwarded_at'])
                                if self._is_overdue(forwarded_time):
                                    overdue.append(case)
                    return overdue
                except:
                    return []
            else:
                try:
                    result = self.client.table('support_cases').select('*').eq(
                        'status', 'awaiting_reply'
                    ).eq('reminder_sent', False).execute()
                    
                    overdue = []
                    for case in result.data:
                        forwarded_time = datetime.fromisoformat(case['forwarded_at'])
                        if self._is_overdue(forwarded_time):
                            overdue.append(case)
                    return overdue
                except:
                    return []
    
    def _is_overdue(self, forwarded_time: datetime, hours: int = 24) -> bool:
        """Check if case is overdue (excluding weekends)"""
        current = forwarded_time
        business_hours_passed = 0
        
        while business_hours_passed < hours:
            current += timedelta(hours=1)
            # Skip weekends (Saturday=5, Sunday=6)
            if current.weekday() < 5:
                business_hours_passed += 1
        
        return datetime.now() > current

# Initialize database client (persists across all sessions)
# Using @st.cache_resource decorator ensures single instance
db = get_database_client()

# ============================================================================
# EMAIL SERVICE
# ============================================================================

class EmailService:
    """Email service for sending verification codes and notifications"""
    
    @staticmethod
    def send_verification_email(to_email: str, code: str, username: str) -> bool:
        """Send verification code email"""
        try:
            subject = f"Verify Your Account - {EMAIL_CONFIG['company_name']}"
            body = f"""
Hello {username},

Thank you for signing up with {EMAIL_CONFIG['company_name']}!

Your verification code is: {code}

Please enter this code to complete your login.

This code will expire in {SECURITY_CONFIG['verification_code_expiry_minutes']} minutes.

Best regards,
{EMAIL_CONFIG['company_name']} Team
            """
            
            # Debug logging
            is_mock = EMAIL_CONFIG.get('use_mock', True)
            print(f"[EMAIL DEBUG] Mock mode: {is_mock}")
            print(f"[EMAIL DEBUG] ENVIRONMENT: {ENVIRONMENT}")
            print(f"[EMAIL DEBUG] Sender email configured: {bool(EMAIL_CONFIG.get('sender_email'))}")
            print(f"[EMAIL DEBUG] Sender password configured: {bool(EMAIL_CONFIG.get('sender_password'))}")
            
            # Use mock or real email based on configuration
            if is_mock:
                print(f"[EMAIL MOCK] Sending verification code to {to_email}")
                print(f"[EMAIL MOCK] Verification Code: {code}")
                st.warning("⚠️ Running in MOCK mode - No actual email sent. Check your Streamlit Cloud secrets!")
                st.info(f"Mock Verification Code: **{code}**")
                return True
            else:
                # Real email sending
                print(f"[EMAIL] Attempting to send real email to {to_email}")
                message = MIMEMultipart()
                message['From'] = EMAIL_CONFIG['sender_email']
                message['To'] = to_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                    server.starttls()
                    print(f"[EMAIL] Connected to SMTP server")
                    server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                    print(f"[EMAIL] Logged in successfully")
                    server.send_message(message)
                    print(f"[EMAIL] Email sent successfully")
                
                st.success(f"✅ Verification code sent to {to_email}")
                return True
                
        except smtplib.SMTPAuthenticationError as e:
            print(f"[ERROR] SMTP Authentication failed: {e}")
            st.error("❌ Email authentication failed. Please check your Gmail App Password in Streamlit secrets.")
            return False
        except smtplib.SMTPException as e:
            print(f"[ERROR] SMTP error: {e}")
            st.error(f"❌ Email sending failed: {str(e)}")
            return False
        except Exception as e:
            print(f"[ERROR] Email sending failed: {e}")
            st.error(f"❌ Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_case_notification(to_email: str, case_id: str, task_number: str):
        """Send case submission notification"""
        try:
            subject = f"Support Case {case_id} Submitted"
            body = f"""
Your support case has been successfully submitted.

Case ID: {case_id}
Task Number: {task_number}

You will receive updates via email when the manufacturer responds.

Best regards,
{EMAIL_CONFIG['company_name']} Team
            """
            
            if EMAIL_CONFIG.get('use_mock', True):
                print(f"[EMAIL MOCK] Case notification sent to {to_email}")
                return True
            else:
                message = MIMEMultipart()
                message['From'] = EMAIL_CONFIG['sender_email']
                message['To'] = to_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                    server.starttls()
                    server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                    server.send_message(message)
                
                print(f"[EMAIL] Case notification sent to {to_email}")
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to send case notification: {e}")
            return False

# ============================================================================
# TRANSLATION SERVICE
# ============================================================================

class TranslationService:
    """Translation service with automatic language detection"""
    
    # Supported languages mapping (code: name)
    LANGUAGES = TRANSLATION_CONFIG.get('supported_languages', {
        'en': 'English',
        'da': 'Danish',
        'de': 'German',
        'fr': 'French',
        'es': 'Spanish',
        'sv': 'Swedish',
        'no': 'Norwegian'
    })
    
    @staticmethod
    def detect_language(text: str) -> tuple[str, str]:
        """Detect language from text using langdetect
        
        Returns:
            tuple: (language_code, language_name)
            e.g., ('da', 'Danish') or ('en', 'English')
        """
        try:
            # Import langdetect only when needed
            from langdetect import detect, DetectorFactory
            # Set seed for consistent results
            DetectorFactory.seed = 0
            
            # Detect language
            detected_code = detect(text)
            
            # Get language name from code
            language_name = TranslationService.LANGUAGES.get(
                detected_code, 
                'English'  # Default to English if not in supported list
            )
            
            print(f"[LANGUAGE DETECTION] Detected: {detected_code} ({language_name})")
            return detected_code, language_name
            
        except ImportError:
            print("[WARNING] langdetect not installed, defaulting to English")
            return 'en', 'English'
        except Exception as e:
            print(f"[WARNING] Language detection failed: {e}, defaulting to English")
            return 'en', 'English'
    
    @staticmethod
    def translate_to_english(text: str, source_lang_code: str = None) -> tuple[str, str, str]:
        """Translate text to English with auto-detection
        
        Args:
            text: The text to translate
            source_lang_code: Optional source language code. If not provided, auto-detect.
        
        Returns:
            tuple: (translated_text, detected_lang_code, detected_lang_name)
        """
        # Auto-detect language if not provided
        if source_lang_code is None:
            source_lang_code, source_lang_name = TranslationService.detect_language(text)
        else:
            source_lang_name = TranslationService.LANGUAGES.get(source_lang_code, 'Unknown')
        
        # If already in English, no translation needed
        if source_lang_code == 'en':
            return text, source_lang_code, source_lang_name
        
        # Use mock translation if configured
        if TRANSLATION_CONFIG.get('use_mock', True):
            translated = f"[Translated from {source_lang_name} to English] {text}"
            return translated, source_lang_code, source_lang_name
        
        # Use real translation API
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source=source_lang_code, target='en')
            translated = translator.translate(text)
            return translated, source_lang_code, source_lang_name
        except ImportError:
            print("[WARNING] deep_translator not installed, using mock translation")
            return f"[Mock Translation] {text}", source_lang_code, source_lang_name
        except Exception as e:
            print(f"[ERROR] Translation failed: {e}")
            return text, source_lang_code, source_lang_name
    
    @staticmethod
    def translate_from_english(text: str, target_lang_code: str) -> str:
        """Translate from English to target language
        
        Args:
            text: The English text to translate
            target_lang_code: Target language code (e.g., 'da', 'de')
        
        Returns:
            str: Translated text
        """
        # If target is English, no translation needed
        if target_lang_code == 'en':
            return text
        
        target_lang_name = TranslationService.LANGUAGES.get(target_lang_code, 'Unknown')
        
        # Use mock translation if configured
        if TRANSLATION_CONFIG.get('use_mock', True):
            return f"[Translated to {target_lang_name}] {text}"
        
        # Use real translation API
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source='en', target=target_lang_code)
            return translator.translate(text)
        except ImportError:
            print("[WARNING] deep_translator not installed, using mock translation")
            return f"[Mock Translation to {target_lang_name}] {text}"
        except Exception as e:
            print(f"[ERROR] Translation failed: {e}")
            return text

# ============================================================================
# MANUFACTURER API
# ============================================================================

class ManufacturerAPI:
    """Manufacturer API integration"""
    
    def __init__(self):
        self.task_counter = 1000
    
    def submit_case(self, manufacturer_id: str, case_description: str) -> str:
        """Submit case to manufacturer and get task number"""
        self.task_counter += 1
        task_number = f"{manufacturer_id.upper()}-TASK-{self.task_counter}"
        
        print(f"[MANUFACTURER API] Submitting to {manufacturer_id}")
        print(f"[MANUFACTURER API] Task Number: {task_number}")
        
        # Simulate API call (replace with actual manufacturer API)
        time.sleep(0.5)
        
        return task_number
    
    def send_reminder(self, task_number: str, manufacturer_id: str):
        """Send reminder to manufacturer"""
        print(f"[MANUFACTURER API] Sending reminder for {task_number}")

# ============================================================================
# WORKFLOW AUTOMATION
# ============================================================================

class WorkflowAutomation:
    """Main workflow automation engine"""
    
    def __init__(self):
        self.translator = TranslationService()
        self.manufacturer_api = ManufacturerAPI()
        self.email_service = EmailService()
    
    def process_support_case(
        self, 
        user_email: str,
        query: str, 
        manufacturer_id: str
    ) -> Dict:
        """Process complete support case workflow with automatic language detection"""
        
        # Step 1: Receive query
        st.info("📥 Step 1: Processing your support request...")
        
        # Step 2: Auto-detect language and translate to English
        st.info("🌐 Step 2: Detecting language and translating to English...")
        translated_query, lang_code, lang_name = self.translator.translate_to_english(query)
        st.success(f"✓ Detected language: **{lang_name}**")
        time.sleep(0.5)
        
        # Step 3: Forward to manufacturer
        st.info(f"📤 Step 3: Forwarding to {MANUFACTURERS[manufacturer_id]['name']}...")
        
        # Step 4: Get task number
        st.info("🎫 Step 4: Receiving task number...")
        task_number = self.manufacturer_api.submit_case(manufacturer_id, translated_query)
        time.sleep(0.5)
        
        # Save to database
        case_data = {
            'user_email': user_email,
            'original_query': query,
            'language': lang_name,
            'language_code': lang_code,
            'manufacturer_id': manufacturer_id,
            'manufacturer_name': MANUFACTURERS[manufacturer_id]['name'],
            'translated_query': translated_query,
            'task_number': task_number,
            'status': 'awaiting_reply'
        }
        
        case_id = db.create_support_case(case_data)
        
        # Send confirmation email
        self.email_service.send_case_notification(user_email, case_id, task_number)
        
        st.success(f"✅ Support case submitted successfully!")
        st.success(f"🎫 Task Number: **{task_number}**")
        st.success(f"📧 Confirmation email sent to {user_email}")
        
        return {
            'case_id': case_id,
            'task_number': task_number,
            'status': 'submitted'
        }

# ============================================================================
# STREAMLIT UI
# ============================================================================

def init_session_state():
    """Initialize session state variables with persistence support"""
    # Core authentication state - persist across reloads
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'session_created_at' not in st.session_state:
        st.session_state.session_created_at = None
    
    # Verification-related state (temporary)
    if 'verification_code' not in st.session_state:
        st.session_state.verification_code = None
    if 'verification_email' not in st.session_state:
        st.session_state.verification_email = None
    if 'verification_expiry' not in st.session_state:
        st.session_state.verification_expiry = None
    if 'temp_user' not in st.session_state:
        st.session_state.temp_user = None
    
    # Page navigation
    if 'page' not in st.session_state:
        # If user is authenticated, go to dashboard, else login
        st.session_state.page = 'dashboard' if st.session_state.authenticated else 'login'
    
    # Session timeout check - maintain session for 24 hours
    if st.session_state.authenticated and st.session_state.session_created_at:
        session_age_hours = (datetime.now() - st.session_state.session_created_at).total_seconds() / 3600
        if session_age_hours > SECURITY_CONFIG.get('session_timeout_hours', 24):
            # Session expired
            st.session_state.authenticated = False
            st.session_state.is_admin = False
            st.session_state.user = None
            st.session_state.user_id = None
            st.session_state.session_created_at = None
            st.session_state.page = 'login'

def generate_verification_code() -> str:
    """Generate 6-digit verification code"""
    return str(random.randint(100000, 999999))

def login_page():
    """Login and signup page"""
    st.title("🔐 Support Automation System")
    
    # Show environment mode
    if ENVIRONMENT == 'production':
        st.info("🚀 Running in PRODUCTION mode")
    else:
        st.warning("🔧 Running in DEVELOPMENT mode")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Admin Login"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    if not validate_email(email):
                        st.error("Please enter a valid email address")
                        return
                    
                    result = db.authenticate_user(email, password)
                    
                    if 'error' in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        # Generate and send verification code
                        code = generate_verification_code()
                        st.session_state.verification_code = code
                        st.session_state.verification_email = email
                        st.session_state.verification_expiry = datetime.now() + timedelta(minutes=10)
                        st.session_state.temp_user = result['user']
                        
                        # Send verification email
                        EmailService.send_verification_email(
                            email, 
                            code, 
                            result['user']['username']
                        )
                        
                        st.success("✅ Verification code sent to your email!")
                        st.info(f"📧 Check your email: {email}")
                        st.info(f"🔑 Demo Code (for testing): **{code}**")
                        st.session_state.page = 'verify'
                        st.rerun()
    
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("signup_form"):
            username = st.text_input("Username", key="signup_username")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if not username or not email or not password:
                    st.error("Please fill in all fields")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                elif '@' not in email or '.' not in email:
                    st.error("Please enter a valid email address")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters")
                else:
                    # Validate inputs
                    is_valid_username, username_msg = validate_username(username)
                    if not is_valid_username:
                        st.error(username_msg)
                        return
                    
                    if not validate_email(email):
                        st.error("Please enter a valid email address")
                        return
                    
                    is_valid_password, password_msg = validate_password(password)
                    if not is_valid_password:
                        st.error(password_msg)
                        return
                    
                    result = db.create_user(username, email, password)
                    
                    if 'error' in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success("✅ Account created successfully!")
                        st.info("👉 Please login with your credentials")
    
    with tab3:
        st.subheader("🔐 Admin Access")
        
        if not ADMIN_CONFIG.get('enabled', False):
            st.warning("⚠️ Admin access is currently disabled")
            st.info("Enable in configuration: ADMIN_ENABLED=true")
            return
        
        with st.form("admin_login_form"):
            admin_username = st.text_input("Admin Username", key="admin_username")
            admin_password = st.text_input("Admin Password", type="password", key="admin_password")
            admin_submit = st.form_submit_button("Admin Login", use_container_width=True, type="primary")
            
            if admin_submit:
                if not admin_username or not admin_password:
                    st.error("Please fill in all fields")
                elif authenticate_admin(admin_username, admin_password):
                    # Set admin session with timestamp
                    st.session_state.authenticated = True
                    st.session_state.is_admin = True
                    st.session_state.user = {
                        'username': admin_username,
                        'email': ADMIN_CONFIG['email'],
                        'id': 'admin',
                        'is_admin': True
                    }
                    st.session_state.user_id = 'admin'
                    st.session_state.session_created_at = datetime.now()
                    st.session_state.page = 'dashboard'
                    st.success("✅ Admin authenticated successfully!")
                    st.success("🎉 Redirecting to admin dashboard...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid admin credentials")

def verification_page():
    """Email verification page"""
    st.title("📧 Email Verification")
    
    # Check if code is expired
    if st.session_state.verification_expiry and datetime.now() > st.session_state.verification_expiry:
        st.error("⏰ Verification code has expired. Please request a new one.")
        if st.button("← Back to Login"):
            st.session_state.page = 'login'
            st.session_state.verification_code = None
            st.session_state.verification_email = None
            st.session_state.verification_expiry = None
            st.session_state.temp_user = None
            st.rerun()
        return
    
    st.info(f"A verification code has been sent to: **{st.session_state.verification_email}**")
    
    # Show time remaining
    if st.session_state.verification_expiry:
        time_remaining = (st.session_state.verification_expiry - datetime.now()).total_seconds() / 60
        st.write(f"⏰ Code expires in: {int(time_remaining)} minutes")
    
    st.write("Please enter the 6-digit code from your email:")
    
    # Create a form for verification
    with st.form("verification_form"):
        entered_code = st.text_input(
            "Verification Code", 
            max_chars=6,
            placeholder="Enter 6-digit code"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            verify_button = st.form_submit_button("✅ Verify", use_container_width=True, type="primary")
        with col2:
            back_button = st.form_submit_button("← Back to Login", use_container_width=True)
        
        if verify_button:
            if not entered_code:
                st.error("❌ Please enter the verification code")
            elif entered_code == st.session_state.verification_code:
                # Mark user as verified
                db.verify_user(st.session_state.verification_email)
                db.update_last_login(st.session_state.verification_email)
                
                # Set user as authenticated with session tracking
                st.session_state.user = st.session_state.temp_user
                st.session_state.user_id = st.session_state.temp_user.get('id')
                st.session_state.authenticated = True
                st.session_state.session_created_at = datetime.now()
                st.session_state.page = 'dashboard'
                
                # Clear temporary data
                st.session_state.verification_code = None
                st.session_state.verification_expiry = None
                st.session_state.temp_user = None
                
                st.success("✅ Email verified successfully!")
                st.success("🎉 Redirecting to dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Code is incorrect. Please try again.")
        
        if back_button:
            st.session_state.page = 'login'
            st.session_state.verification_code = None
            st.session_state.verification_email = None
            st.session_state.verification_expiry = None
            st.session_state.temp_user = None
            st.rerun()
    
    # Resend code button outside form
    st.write("")
    if st.button("📧 Resend Verification Code", use_container_width=True):
        code = generate_verification_code()
        st.session_state.verification_code = code
        st.session_state.verification_expiry = datetime.now() + timedelta(minutes=10)
        
        EmailService.send_verification_email(
            st.session_state.verification_email,
            code,
            st.session_state.temp_user['username']
        )
        
        st.success("✅ New verification code sent!")
        st.info(f"🔑 Demo Code (for testing): **{code}**")
        st.rerun()

def dashboard_page():
    """Main dashboard page"""
    st.title("📊 Support Dashboard")
    
    # Header with user info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"### Welcome, {st.session_state.user['username']}! 👋")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.is_admin = False
            st.session_state.user = None
            st.session_state.user_id = None
            st.session_state.session_created_at = None
            st.session_state.page = 'login'
            st.rerun()
    
    st.divider()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📝 New Support Case", "📋 My Cases", "ℹ️ Info"])
    
    with tab1:
        new_support_case_form()
    
    with tab2:
        my_cases_view()
    
    with tab3:
        info_view()

def new_support_case_form():
    """Form to create new support case"""
    st.subheader("Create New Support Request")
    
    # Information banner
    st.info("💡 **Tip:** Write your message in any language! Our system will automatically detect and translate it.")
    
    with st.form("support_case_form"):
        # Manufacturer selection
        manufacturer_options = {
            key: value['name'] 
            for key, value in MANUFACTURERS.items()
        }
        
        manufacturer = st.selectbox(
            "Select Manufacturer",
            list(manufacturer_options.keys()),
            format_func=lambda x: manufacturer_options[x],
            key="case_manufacturer"
        )
        
        # Support query
        query = st.text_area(
            "Describe Your Issue (in any language)",
            height=150,
            placeholder="Please describe your issue in detail in any language...",
            key="case_query",
            help="Write in your preferred language - Danish, German, French, Spanish, English, or any other language we support!"
        )
        
        # Submit button
        submit = st.form_submit_button("Submit Support Request", use_container_width=True, type="primary")
        
        if submit:
            if not query.strip():
                st.error("Please describe your issue")
            else:
                with st.spinner("Processing your request..."):
                    workflow = WorkflowAutomation()
                    result = workflow.process_support_case(
                        user_email=st.session_state.user['email'],
                        query=query,
                        manufacturer_id=manufacturer
                    )
                
                st.balloons()
                
                # Show next steps
                st.write("### 📋 Next Steps:")
                st.write("1. ✅ Your case has been forwarded to the manufacturer")
                st.write("2. 📧 You'll receive email updates on progress")
                st.write("3. 🔔 We'll notify you when manufacturer responds")
                st.write("4. ⏰ Automatic reminder will be sent if no response in 24 hours (excluding weekends)")

def my_cases_view():
    """View user's support cases"""
    st.subheader("Your Support Cases")
    
    cases = db.get_user_cases(st.session_state.user['email'])
    
    if not cases:
        st.info("📭 You don't have any support cases yet.")
        st.write("Create your first support case in the 'New Support Case' tab!")
    else:
        st.write(f"**Total Cases:** {len(cases)}")
        st.write("")
        
        for case in cases:
            with st.expander(
                f"🎫 {case['case_id']} - {case['manufacturer_name']} - {case['status'].replace('_', ' ').title()}",
                expanded=False
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Case ID:** {case['case_id']}")
                    st.write(f"**Task Number:** {case['task_number']}")
                    st.write(f"**Language:** {case['language']}")
                
                with col2:
                    st.write(f"**Manufacturer:** {case['manufacturer_name']}")
                    st.write(f"**Status:** {case['status'].replace('_', ' ').title()}")
                    submitted_time = datetime.fromisoformat(case['submitted_at'])
                    st.write(f"**Submitted:** {submitted_time.strftime('%Y-%m-%d %H:%M')}")
                
                st.write("**Original Query:**")
                st.text_area("", value=case['original_query'], height=100, disabled=True, key=f"query_{case['case_id']}")
                
                # Status indicator
                status_map = {
                    'awaiting_reply': ('🟡', 'Waiting for manufacturer response'),
                    'reply_received': ('🟢', 'Manufacturer has responded'),
                    'pending_approval': ('🟠', 'Awaiting manual approval'),
                    'approved': ('✅', 'Approved and sent to you'),
                    'reminder_sent': ('🔔', 'Reminder sent to manufacturer')
                }
                
                if case['status'] in status_map:
                    icon, text = status_map[case['status']]
                    st.info(f"{icon} {text}")

def info_view():
    """Information and help view"""
    st.subheader("ℹ️ How It Works")
    
    st.write("""
    ### 📋 Support Case Workflow
    
    **Step 1: Submit Request**
    - Write your support query in your preferred language
    - Select the manufacturer
    - Submit the request
    
    **Step 2: Automatic Translation**
    - Your query is automatically translated to English
    - Ensures clear communication with manufacturers
    
    **Step 3: Forward to Manufacturer**
    - Case is forwarded to manufacturer's system
    - You receive a unique task number for tracking
    
    **Step 4: Email Notification**
    - Confirmation email sent to you
    - Task number provided for reference
    
    **Step 5: Manufacturer Response**
    - When manufacturer replies, you'll be notified
    - Response is translated back to your language
    
    **Step 6: Manual Approval**
    - Response is prepared for your review
    - You'll receive the translated response via email
    
    **⏰ Automatic Reminders**
    - If no response within 24 business hours
    - Automatic reminder sent to manufacturer
    - Excludes weekends (Saturday & Sunday)
    """)
    
    st.write("---")
    st.write("### 👥 Available Manufacturers")
    
    for key, mfr in MANUFACTURERS.items():
        st.write(f"**{mfr['name']}**")
        st.write(f"  - Contact: {mfr['email']}")
    
    st.write("---")
    st.write("### 📊 Workflow Status")
    
    status_info = {
        "🟡 Awaiting Reply": "Your case has been forwarded to the manufacturer. Waiting for their response.",
        "🟢 Reply Received": "Manufacturer has responded. Reply is being translated back to your language.",
        "🟠 Pending Approval": "Translated response is ready for manual review and approval.",
        "✅ Approved": "Response has been approved and sent to you via email.",
        "🔔 Reminder Sent": "Automatic reminder has been sent to manufacturer due to delayed response."
    }
    
    for status, description in status_info.items():
        st.write(f"**{status}**")
        st.write(f"  {description}")
        st.write("")

# ============================================================================
# BACKGROUND TASKS (For Production)
# ============================================================================

def check_overdue_cases_background():
    """
    Background task to check for overdue cases and send reminders
    This should run as a scheduled job in production
    """
    overdue_cases = db.get_overdue_cases()
    
    for case in overdue_cases:
        # Send reminder to manufacturer
        manufacturer_api = ManufacturerAPI()
        manufacturer_api.send_reminder(
            case['task_number'],
            case['manufacturer_id']
        )
        
        # Update case status
        db.update_case(case['case_id'], {
            'reminder_sent': True,
            'reminder_sent_at': datetime.now().isoformat(),
            'status': 'reminder_sent'
        })
        
        # Send notification email to user
        EmailService.send_case_notification(
            case['user_email'],
            case['case_id'],
            f"Reminder sent for task {case['task_number']}"
        )

# ============================================================================
# ADMIN PANEL (Optional)
# ============================================================================

def admin_panel():
    """Admin panel for managing cases and monitoring system"""
    st.title("🔧 Admin Panel")
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 All Cases", "⚙️ Settings"])
    
    with tab1:
        st.subheader("System Statistics")
        
        # Get all cases
        all_cases = []
        for user_email in db.users_table.keys():
            all_cases.extend(db.get_user_cases(user_email))
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", len(db.users_table))
        
        with col2:
            st.metric("Total Cases", len(all_cases))
        
        with col3:
            active_cases = [c for c in all_cases if c['status'] == 'awaiting_reply']
            st.metric("Active Cases", len(active_cases))
        
        with col4:
            overdue = db.get_overdue_cases()
            st.metric("Overdue Cases", len(overdue))
    
    with tab2:
        st.subheader("All Support Cases")
        
        if not all_cases:
            st.info("No cases in the system yet.")
        else:
            for case in sorted(all_cases, key=lambda x: x['submitted_at'], reverse=True):
                with st.expander(f"{case['case_id']} - {case['user_email']} - {case['status']}"):
                    st.json(case)
                    
                    if st.button(f"Mark as Replied", key=f"reply_{case['case_id']}"):
                        db.update_case(case['case_id'], {
                            'status': 'reply_received',
                            'reply_received_at': datetime.now().isoformat(),
                            'manufacturer_reply': 'Mock manufacturer reply',
                            'reply_translated': 'Mock translated reply',
                            'needs_approval': True
                        })
                        st.success("Case updated!")
                        st.rerun()
    
    with tab3:
        st.subheader("System Settings")
        st.write("Configure system-wide settings here")
        
        reminder_hours = st.number_input(
            "Reminder Threshold (hours)",
            min_value=1,
            max_value=168,
            value=24
        )
        
        exclude_weekends = st.checkbox("Exclude weekends from business hours", value=True)
        
        if st.button("Save Settings"):
            st.success("Settings saved!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stAlert {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        div[data-testid="stExpander"] {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🎫 Support System")
        st.write("")
        
        # Show environment info
        env_icon = "🚀" if ENVIRONMENT == 'production' else "🔧"
        st.caption(f"{env_icon} {ENVIRONMENT.upper()} MODE")
        st.write("")
        
        if st.session_state.authenticated:
            # Show role badge
            if st.session_state.is_admin:
                st.error("🔐 ADMIN ACCESS")
            else:
                st.success(f"👤 User: {st.session_state.user['username']}")
            
            st.write(f"📧 {st.session_state.user['email']}")
            st.write("")
            
            # Show user stats (not for admin viewing all cases)
            if not st.session_state.is_admin:
                user_cases = db.get_user_cases(st.session_state.user['email'])
                st.metric("My Cases", len(user_cases))
                
                active = [c for c in user_cases if c['status'] == 'awaiting_reply']
                st.metric("Active Cases", len(active))
            else:
                # Show system-wide stats for admin
                all_cases = []
                if db.use_mock:
                    all_cases = list(db.cases_table.values())
                else:
                    # Get all cases from database
                    try:
                        if db.use_rest_client:
                            all_cases = db.client.get_all_cases()
                        else:
                            result = db.client.table('support_cases').select('*').execute()
                            all_cases = result.data
                    except:
                        pass
                
                st.metric("Total Cases", len(all_cases))
                st.metric("Total Users", len(db.users_table) if db.use_mock else "N/A")
            
            st.write("")
            st.write("---")
        else:
            st.info("Please login to continue")
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        if st.session_state.page == 'verify':
            verification_page()
        else:
            login_page()
    else:
        # Route based on user role
        if st.session_state.is_admin:
            admin_panel()
        else:
            dashboard_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Support Automation System v1.0</p>
            <p>Powered by Streamlit & Supabase</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    