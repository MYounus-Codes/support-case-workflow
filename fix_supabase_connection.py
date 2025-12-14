"""
Quick fix for Supabase connection compatibility issues
This script helps diagnose and fix the proxy parameter error
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("🔧 Supabase Connection Fix Tool")
print("=" * 60)
print()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

print("1️⃣ Checking Supabase library installation...")
print()

try:
    import supabase
    print(f"   ✅ Supabase library version: {supabase.__version__ if hasattr(supabase, '__version__') else 'Unknown'}")
except ImportError:
    print("   ❌ Supabase not installed!")
    print("   Run: pip install supabase")
    exit(1)

print()
print("2️⃣ Testing connection methods...")
print()

# Method 1: Named parameters (recommended for v2.x)
print("   Method 1: Named parameters...")
try:
    from supabase import create_client, Client
    client = create_client(
        supabase_url=SUPABASE_URL,
        supabase_key=SUPABASE_KEY
    )
    print("   ✅ SUCCESS with named parameters!")
    print()
    
    # Test a query
    print("3️⃣ Testing database query...")
    try:
        result = client.table('manufacturers').select('*').execute()
        print(f"   ✅ Query successful! Found {len(result.data)} manufacturers")
        print()
        print("=" * 60)
        print("✅ CONNECTION WORKING PERFECTLY!")
        print("=" * 60)
        print()
        print("Your database is ready to use.")
        print("Set ENVIRONMENT=production in .env to use it.")
        exit(0)
    except Exception as e:
        print(f"   ⚠️ Query failed: {str(e)}")
        
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")
    print()

# Method 2: Positional parameters (older versions)
print("   Method 2: Positional parameters...")
try:
    from supabase import create_client, Client
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("   ✅ SUCCESS with positional parameters!")
    print()
    
    # Test a query
    print("3️⃣ Testing database query...")
    try:
        result = client.table('manufacturers').select('*').execute()
        print(f"   ✅ Query successful! Found {len(result.data)} manufacturers")
        print()
        print("=" * 60)
        print("✅ CONNECTION WORKING!")
        print("=" * 60)
        print()
        print("Your database is ready to use.")
        print("Set ENVIRONMENT=production in .env to use it.")
        exit(0)
    except Exception as e:
        print(f"   ⚠️ Query failed: {str(e)}")
        
except Exception as e:
    print(f"   ❌ Failed: {str(e)}")
    print()

print()
print("=" * 60)
print("❌ CONNECTION FAILED")
print("=" * 60)
print()
print("🔧 Troubleshooting Steps:")
print()
print("1. Update Supabase library:")
print("   pip uninstall supabase -y")
print("   pip install supabase")
print()
print("2. Check your credentials:")
print(f"   URL: {SUPABASE_URL}")
print(f"   Key: {'*' * 20}...{SUPABASE_KEY[-10:] if SUPABASE_KEY else 'NOT SET'}")
print()
print("3. Verify Supabase project status:")
print("   - Go to https://supabase.com/dashboard")
print("   - Check if project is active")
print("   - Verify API keys")
print()
print("4. Try reinstalling from scratch:")
print("   pip uninstall supabase postgrest-py gotrue-py realtime-py storage3 -y")
print("   pip install supabase")
print()
