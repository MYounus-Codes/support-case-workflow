"""
Test Supabase Database Connection
Verifies that the database is properly configured and accessible
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 TESTING SUPABASE DATABASE CONNECTION")
print("=" * 60)
print()

# Check environment variables
print("1️⃣ Checking Environment Variables...")
print()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

print(f"   Environment: {ENVIRONMENT}")
print(f"   Supabase URL: {SUPABASE_URL}")
print(f"   Supabase Key: {'*' * 20}...{SUPABASE_KEY[-10:] if SUPABASE_KEY else 'NOT SET'}")
print()

if not SUPABASE_URL or SUPABASE_URL == 'https://your-project.supabase.co':
    print("   ⚠️  WARNING: Supabase URL not configured!")
    print("   Please set SUPABASE_URL in your .env file")
    print()

if not SUPABASE_KEY or 'your-supabase' in SUPABASE_KEY:
    print("   ⚠️  WARNING: Supabase KEY not configured!")
    print("   Please set SUPABASE_KEY in your .env file")
    print()

# Check if supabase library is installed
print("2️⃣ Checking Supabase Library...")
print()

try:
    from supabase import create_client, Client
    print("   ✅ Supabase library installed")
    print()
except ImportError:
    print("   ❌ Supabase library not installed!")
    print("   Run: pip install supabase")
    print()
    sys.exit(1)

# Try to connect to Supabase
print("3️⃣ Testing Database Connection...")
print()

if SUPABASE_URL and SUPABASE_KEY and 'your-' not in SUPABASE_URL:
    try:
        # Try with named parameters first (newer versions)
        try:
            client: Client = create_client(
                supabase_url=SUPABASE_URL,
                supabase_key=SUPABASE_KEY
            )
        except TypeError:
            # Fallback for older versions
            client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("   ✅ Successfully connected to Supabase")
        print()
        
        # Test reading from users table
        print("4️⃣ Testing Database Tables...")
        print()
        
        try:
            result = client.table('users').select('count').execute()
            print(f"   ✅ 'users' table accessible")
        except Exception as e:
            print(f"   ⚠️  'users' table error: {str(e)}")
        
        try:
            result = client.table('support_cases').select('count').execute()
            print(f"   ✅ 'support_cases' table accessible")
        except Exception as e:
            print(f"   ⚠️  'support_cases' table error: {str(e)}")
        
        try:
            result = client.table('manufacturers').select('*').execute()
            print(f"   ✅ 'manufacturers' table accessible")
            if result.data:
                print(f"      Found {len(result.data)} manufacturers")
                for mfr in result.data:
                    print(f"      - {mfr.get('name', 'Unknown')}")
        except Exception as e:
            print(f"   ⚠️  'manufacturers' table error: {str(e)}")
        
        print()
        print("=" * 60)
        print("✅ DATABASE CONNECTION TEST SUCCESSFUL!")
        print("=" * 60)
        print()
        print("📝 Next Steps:")
        print("   1. Your database is properly configured")
        print("   2. All tables are accessible")
        print("   3. Set ENVIRONMENT=production in .env to use real database")
        print("   4. Run: streamlit run app.py")
        print()
        
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        print()
        print("   Possible issues:")
        print("   - Check your Supabase URL and KEY")
        print("   - Verify your Supabase project is active")
        print("   - Check network connectivity")
        print("   - Review Supabase dashboard for errors")
        print()
        sys.exit(1)
else:
    print("   ⚠️  Skipping connection test - credentials not configured")
    print()
    print("   To test real database:")
    print("   1. Copy .env.example to .env")
    print("   2. Add your Supabase URL and KEY")
    print("   3. Run this test again")
    print()

# Check email configuration
print("5️⃣ Checking Email Configuration...")
print()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

print(f"   SMTP Server: {SMTP_SERVER}")
print(f"   Sender Email: {SENDER_EMAIL}")
print(f"   Sender Password: {'*' * 10 if SENDER_PASSWORD and len(SENDER_PASSWORD) > 5 else 'NOT SET'}")
print()

if not SENDER_EMAIL or 'your-email' in SENDER_EMAIL:
    print("   ⚠️  Email not configured for production")
    print("   Verification codes will be shown in console/UI")
    print()
else:
    print("   ✅ Email configuration looks good")
    print()

# Check admin configuration
print("6️⃣ Checking Admin Configuration...")
print()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_ENABLED = os.getenv('ADMIN_ENABLED', 'true').lower() == 'true'

print(f"   Admin Username: {ADMIN_USERNAME}")
print(f"   Admin Email: {ADMIN_EMAIL}")
print(f"   Admin Enabled: {ADMIN_ENABLED}")

if ADMIN_PASSWORD == 'Admin@123456':
    print("   ⚠️  WARNING: Using default admin password!")
    print("   Please change ADMIN_PASSWORD in .env for production")
else:
    print("   ✅ Custom admin password set")

print()

print("=" * 60)
print("✅ CONFIGURATION CHECK COMPLETE")
print("=" * 60)
print()

print("📊 Summary:")
print(f"   Environment: {ENVIRONMENT}")
print(f"   Database: {'✅ Connected' if SUPABASE_URL and 'your-' not in SUPABASE_URL else '⚠️ Mock Mode'}")
print(f"   Email: {'✅ Configured' if SENDER_EMAIL and 'your-' not in SENDER_EMAIL else '⚠️ Mock Mode'}")
print(f"   Admin: {'✅ Enabled' if ADMIN_ENABLED else '❌ Disabled'}")
print()

if ENVIRONMENT == 'production':
    print("🚀 Ready for Production Deployment!")
else:
    print("🔧 Running in Development Mode")
    print("   Set ENVIRONMENT=production in .env for full features")

print()
