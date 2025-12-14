"""
Configuration file for Support Case Automation System
Store sensitive credentials in environment variables for production
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# Check if running in Streamlit Cloud (has secrets) or locally (use .env)
USE_STREAMLIT_SECRETS = False
try:
    import streamlit as st
    if hasattr(st, 'secrets') and len(st.secrets) > 0:
        USE_STREAMLIT_SECRETS = True
        print("[CONFIG] Running in Streamlit Cloud - using secrets")
    else:
        print("[CONFIG] Running locally - using .env file")
except:
    print("[CONFIG] Running locally - using .env file")

# Helper function to get config with section support
def get_secret(key: str, default: str = '', section: str = None):
    """Get secret from Streamlit secrets (nested) or environment variables (flat)"""
    if USE_STREAMLIT_SECRETS:
        try:
            import streamlit as st
            # Try nested structure first: st.secrets["section"]["key"]
            if section and section in st.secrets:
                value = st.secrets[section].get(key, None)
                if value is not None:
                    return str(value)
            # Fallback to environment variable
            return os.getenv(key, default)
        except Exception as e:
            print(f"[CONFIG WARNING] Error reading secret [{section}]['{key}']: {e}")
            return os.getenv(key, default)
    else:
        # Running locally - use environment variables from .env
        return os.getenv(key, default)

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================

# Set to 'production' to use real Supabase, 'development' for mock
ENVIRONMENT = get_secret('mode', 'development', section='environment')

# ============================================================================
# ADMIN AUTHENTICATION
# ============================================================================

ADMIN_CONFIG = {
    'username': get_secret('username', 'admin', section='admin'),
    'email': get_secret('email', 'admin@supportautomation.com', section='admin'),
    'password': get_secret('password', 'Admin@123456', section='admin'),
    'enabled': get_secret('enabled', 'true', section='admin').lower() == 'true'
}

# ============================================================================
# SUPABASE CONFIGURATION
# ============================================================================

SUPABASE_CONFIG = {
    'url': get_secret('url', '', section='supabase'),
    'key': get_secret('key', '', section='supabase'),
    'use_mock': ENVIRONMENT == 'development'
}

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

_sender_email = get_secret('sender_email', '', section='email').strip()
_sender_password = get_secret('sender_password', '', section='email').strip()
_use_mock_env = get_secret('use_mock', 'false', section='email').lower().strip() == 'true'

# Convert port to int safely
try:
    _smtp_port = int(get_secret('smtp_port', '587', section='email'))
except (ValueError, TypeError):
    _smtp_port = 587
    print("[CONFIG WARNING] Invalid SMTP_PORT, using default 587")

EMAIL_CONFIG = {
    'smtp_server': get_secret('smtp_server', 'smtp.gmail.com', section='email').strip(),
    'smtp_port': _smtp_port,
    'sender_email': _sender_email,
    'sender_password': _sender_password,
    'company_name': get_secret('company_name', 'Support Automation System', section='email'),
    # Use mock email only if explicitly set to true OR if credentials are missing
    'use_mock': _use_mock_env or not _sender_email or not _sender_password
}

# Debug logging
print(f"[CONFIG] Email sender configured: {bool(_sender_email)}")
print(f"[CONFIG] Email password configured: {bool(_sender_password)}")
print(f"[CONFIG] USE_MOCK_EMAIL setting: {_use_mock_env}")
print(f"[CONFIG] Email mode: {'MOCK' if EMAIL_CONFIG['use_mock'] else 'REAL'}")

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
