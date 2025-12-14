"""
Quick verification script for local email setup
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*60)
print("📧 EMAIL CONFIGURATION CHECK")
print("="*60)

env_file_exists = os.path.exists('.env')
print(f"\n✓ .env file exists: {env_file_exists}")

if env_file_exists:
    sender_email = os.getenv('SENDER_EMAIL', '')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    use_mock = os.getenv('USE_MOCK_EMAIL', 'false')
    environment = os.getenv('ENVIRONMENT', 'development')
    
    print(f"✓ ENVIRONMENT: {environment}")
    print(f"✓ USE_MOCK_EMAIL: {use_mock}")
    print(f"✓ SENDER_EMAIL: {sender_email if sender_email else '❌ NOT SET'}")
    print(f"✓ SENDER_PASSWORD: {'✓ SET' if sender_password else '❌ NOT SET'}")
    
    print("\n" + "-"*60)
    
    if use_mock.lower() == 'false' and sender_email and sender_password:
        print("✅ CONFIGURATION IS CORRECT - Will send REAL emails")
        print(f"   Emails will be sent from: {sender_email}")
    elif use_mock.lower() == 'true':
        print("⚠️  MOCK MODE ENABLED - Emails will print to console only")
        print("   Set USE_MOCK_EMAIL=false in .env to send real emails")
    else:
        print("❌ MISSING CREDENTIALS - Will use mock mode")
        print("   Add SENDER_EMAIL and SENDER_PASSWORD to .env file")
    
    print("-"*60 + "\n")
else:
    print("\n❌ .env file not found!")
    print("   Run: copy .env.example .env")
    print("   Then edit .env with your credentials\n")
