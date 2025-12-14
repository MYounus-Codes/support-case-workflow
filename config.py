"""
Configuration file for Support Case Automation System
Store sensitive credentials in environment variables for production
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# Try to load Streamlit secrets (Streamlit Cloud)
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        # Helper function to get config from Streamlit secrets or environment
        def get_secret(key: str, default: str = '', section: str = None):
            """Get secret from Streamlit secrets or environment variables"""
            try:
                if section:
                    return st.secrets[section].get(key, os.getenv(key, default))
                return st.secrets.get(key, os.getenv(key, default))
            except:
                return os.getenv(key, default)
    else:
        def get_secret(key: str, default: str = '', section: str = None):
            return os.getenv(key, default)
except ImportError:
    def get_secret(key: str, default: str = '', section: str = None):
        return os.getenv(key, default)

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

# Set to 'production' to use real Supabase, 'development' for mock
ENVIRONMENT = get_secret('ENVIRONMENT', 'development', 'general')

# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================

ADMIN_CONFIG = {
    'username': get_secret('ADMIN_USERNAME', 'admin', 'admin'),
    'email': get_secret('ADMIN_EMAIL', 'admin@supportautomation.com', 'admin'),
    'password': get_secret('ADMIN_PASSWORD', 'Admin@123456', 'admin'),
    'enabled': get_secret('ADMIN_ENABLED', 'true', 'admin').lower() == 'true'
}

# ============================================================================
# SUPABASE CONFIGURATION
# ============================================================================

SUPABASE_CONFIG = {
    'url': get_secret('SUPABASE_URL', '', 'supabase'),
    'key': get_secret('SUPABASE_KEY', '', 'supabase'),
    'use_mock': ENVIRONMENT == 'development'
}

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

EMAIL_CONFIG = {
    'smtp_server': get_secret('SMTP_SERVER', 'smtp.gmail.com', 'email'),
    'smtp_port': int(get_secret('SMTP_PORT', '587', 'email')),
    'sender_email': get_secret('SENDER_EMAIL', '', 'email'),
    'sender_password': get_secret('SENDER_PASSWORD', '', 'email'),
    'company_name': get_secret('COMPANY_NAME', 'Support Automation System', 'email'),
    # Use mock email only in development or if credentials are not set
    'use_mock': (
        ENVIRONMENT == 'development' or 
        get_secret('USE_MOCK_EMAIL', 'false', 'email').lower() == 'true' or
        not get_secret('SENDER_EMAIL', '', 'email') or 
        not get_secret('SENDER_PASSWORD', '', 'email')
    )
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
