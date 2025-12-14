"""
Configuration file for Support Case Automation System
Store sensitive credentials in environment variables for production
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

# Set to 'production' to use real Supabase, 'development' for mock
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================

ADMIN_CONFIG = {
    'username': os.getenv('ADMIN_USERNAME', 'admin'),
    'email': os.getenv('ADMIN_EMAIL', 'admin@supportautomation.com'),
    'password': os.getenv('ADMIN_PASSWORD', 'Admin@123456'),  # Change in production!
    'enabled': os.getenv('ADMIN_ENABLED', 'true').lower() == 'true'
}

# ============================================================================
# SUPABASE CONFIGURATION
# ============================================================================

SUPABASE_CONFIG = {
    'url': os.getenv('SUPABASE_URL', 'https://eetdfpfojtktsicojqst.supabase.co'),
    'key': os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVldGRmcGZvanRrdHNpY29qcXN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MzE0NzcsImV4cCI6MjA4MTIwNzQ3N30.m1ESYsxFBO-ECPK9vhfNrOVz9UCv29PVn3igwq5nqy4'),
    'use_mock': ENVIRONMENT == 'development'
}

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'sender_email': os.getenv('SENDER_EMAIL', 'your-email@gmail.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', 'your-app-password'),
    'company_name': os.getenv('COMPANY_NAME', 'Support Automation System'),
    # Use real email if credentials are properly configured, regardless of environment
    'use_mock': os.getenv('USE_MOCK_EMAIL', 'false').lower() == 'true'
}

# ============================================================================
# MANUFACTURERS CONFIGURATION
# ============================================================================

MANUFACTURERS = {
    'manufacturer_1': {
        'name': 'Tech Solutions Inc.',
        'api_url': os.getenv('MANUFACTURER_1_API', 'https://api.techsolutions.com'),
        'email': 'raufa7951@gmail.com',
        'api_key': os.getenv('MANUFACTURER_1_KEY', '')
    },
    'manufacturer_2': {
        'name': 'Global Parts Ltd.',
        'api_url': os.getenv('MANUFACTURER_2_API', 'https://api.globalparts.com'),
        'email': 'support@globalparts.com',
        'api_key': os.getenv('MANUFACTURER_2_KEY', '')
    },
    'manufacturer_3': {
        'name': 'Innovation Corp.',
        'api_url': os.getenv('MANUFACTURER_3_API', 'https://api.innovation.com'),
        'email': 'support@innovation.com',
        'api_key': os.getenv('MANUFACTURER_3_KEY', '')
    }
}

# ============================================================================
# TRANSLATION API CONFIGURATION
# ============================================================================

TRANSLATION_CONFIG = {
    'provider': os.getenv('TRANSLATION_PROVIDER', 'google'),  # 'google', 'deepl', or 'deep_translator'
    'api_key': os.getenv('TRANSLATION_API_KEY', ''),
    'use_mock': ENVIRONMENT == 'development',
    'auto_detect_language': True,  # Automatically detect language instead of user selection
    # Language code mapping for translation services
    'supported_languages': {
        'en': 'English',
        'da': 'Danish',
        'de': 'German',
        'fr': 'French',
        'es': 'Spanish',
        'sv': 'Swedish',
        'no': 'Norwegian',
        'nl': 'Dutch',
        'it': 'Italian',
        'pt': 'Portuguese'
    }
}

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

SECURITY_CONFIG = {
    'min_password_length': 8,
    'verification_code_expiry_minutes': 10,
    'max_login_attempts': 5,
    'session_timeout_hours': 24
}

# ============================================================================
# BUSINESS LOGIC CONFIGURATION
# ============================================================================

BUSINESS_CONFIG = {
    'reminder_threshold_hours': 24,
    'exclude_weekends': True,
    'auto_approve_replies': False  # Set to True to skip manual approval
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_config_summary() -> Dict:
    """Get configuration summary for debugging"""
    return {
        'environment': ENVIRONMENT,
        'using_mock_db': SUPABASE_CONFIG['use_mock'],
        'using_mock_email': EMAIL_CONFIG['use_mock'],
        'using_mock_translation': TRANSLATION_CONFIG['use_mock'],
        'supabase_url': SUPABASE_CONFIG['url'],
        'smtp_server': EMAIL_CONFIG['smtp_server']
    }

def validate_production_config() -> tuple[bool, list]:
    """Validate that all production settings are configured"""
    errors = []
    
    if ENVIRONMENT == 'production':
        if SUPABASE_CONFIG['url'] == 'your-supabase-url':
            errors.append('SUPABASE_URL not configured')
        
        if SUPABASE_CONFIG['key'] == 'your-supabase-anon-key':
            errors.append('SUPABASE_KEY not configured')
        
        if EMAIL_CONFIG['sender_email'] == 'your-email@gmail.com':
            errors.append('SENDER_EMAIL not configured')
        
        if EMAIL_CONFIG['sender_password'] == 'your-app-password':
            errors.append('SENDER_PASSWORD not configured')
        
        if TRANSLATION_CONFIG['api_key'] == '':
            errors.append('TRANSLATION_API_KEY not configured')
    
    return len(errors) == 0, errors
