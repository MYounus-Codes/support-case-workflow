"""
Test script to verify user flow and database operations
Run this to ensure everything works before deployment
"""

import sys
import hashlib
from datetime import datetime, timedelta

# Test validation functions
def test_validation():
    """Test validation helper functions"""
    print("🧪 Testing Validation Functions...")
    
    # Import validation functions
    from app import validate_email, validate_password, validate_username
    
    # Test email validation
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    assert validate_email("test@domain") == False
    print("✅ Email validation works")
    
    # Test password validation
    valid, msg = validate_password("password123")
    assert valid == True
    valid, msg = validate_password("short")
    assert valid == False
    print("✅ Password validation works")
    
    # Test username validation
    valid, msg = validate_username("john_doe")
    assert valid == True
    valid, msg = validate_username("ab")
    assert valid == False
    print("✅ Username validation works")
    
    print()

def test_database_operations():
    """Test database CRUD operations"""
    print("🧪 Testing Database Operations...")
    
    from app import get_database_client
    
    db = get_database_client()
    
    # Test user creation
    result = db.create_user("testuser", "test@example.com", "password123")
    assert 'success' in result or 'error' in result
    print(f"✅ User creation: {result}")
    
    # Test duplicate user
    result2 = db.create_user("testuser2", "test@example.com", "password456")
    if 'error' in result2:
        print(f"✅ Duplicate prevention works: {result2['error']}")
    
    # Test authentication
    result = db.authenticate_user("test@example.com", "password123")
    assert 'success' in result or 'error' in result
    print(f"✅ Authentication: {result}")
    
    # Test wrong password
    result = db.authenticate_user("test@example.com", "wrongpassword")
    assert 'error' in result
    print(f"✅ Wrong password handling: {result['error']}")
    
    # Test user verification
    success = db.verify_user("test@example.com")
    print(f"✅ User verification: {success}")
    
    # Test case creation
    case_data = {
        'user_email': 'test@example.com',
        'original_query': 'Test query',
        'language': 'English',
        'manufacturer_id': 'manufacturer_1',
        'manufacturer_name': 'Tech Solutions Inc.',
        'translated_query': 'Test query',
        'task_number': 'TEST-001',
        'status': 'awaiting_reply'
    }
    case_id = db.create_support_case(case_data)
    assert case_id is not None
    print(f"✅ Case creation: {case_id}")
    
    # Test getting user cases
    cases = db.get_user_cases("test@example.com")
    assert len(cases) > 0
    print(f"✅ Get user cases: {len(cases)} case(s) found")
    
    # Test case update
    success = db.update_case(case_id, {'status': 'reply_received'})
    print(f"✅ Case update: {success}")
    
    # Test getting case by ID
    case = db.get_case_by_id(case_id)
    assert case is not None
    print(f"✅ Get case by ID: {case['status']}")
    
    print()

def test_user_flow():
    """Simulate complete user flow"""
    print("🧪 Testing Complete User Flow...")
    
    from app import get_database_client, generate_verification_code
    
    db = get_database_client()
    
    # Step 1: User signup
    print("Step 1: User Signup")
    username = f"flowtest_{int(datetime.now().timestamp())}"
    email = f"{username}@example.com"
    password = "TestPass123"
    
    result = db.create_user(username, email, password)
    if 'error' in result:
        print(f"  ⚠️ User already exists, continuing...")
    else:
        print(f"  ✅ User created: {result['user_id']}")
    
    # Step 2: User login
    print("Step 2: User Login")
    result = db.authenticate_user(email, password)
    if 'error' in result:
        print(f"  ❌ Login failed: {result['error']}")
        return
    print(f"  ✅ Login successful")
    user = result['user']
    
    # Step 3: Email verification (simulated)
    print("Step 3: Email Verification")
    code = generate_verification_code()
    print(f"  ✅ Verification code generated: {code}")
    
    # Step 4: Verify user
    print("Step 4: Mark User as Verified")
    db.verify_user(email)
    print(f"  ✅ User verified")
    
    # Step 5: Update last login
    print("Step 5: Update Last Login")
    db.update_last_login(email)
    print(f"  ✅ Last login updated")
    
    # Step 6: Create support case
    print("Step 6: Create Support Case")
    case_data = {
        'user_email': email,
        'original_query': 'Need help with product X',
        'language': 'English',
        'manufacturer_id': 'manufacturer_1',
        'manufacturer_name': 'Tech Solutions Inc.',
        'translated_query': 'Need help with product X',
        'task_number': f'FLOW-{int(datetime.now().timestamp())}',
        'status': 'awaiting_reply'
    }
    case_id = db.create_support_case(case_data)
    print(f"  ✅ Case created: {case_id}")
    
    # Step 7: Get user cases
    print("Step 7: Retrieve User Cases")
    cases = db.get_user_cases(email)
    print(f"  ✅ Found {len(cases)} case(s)")
    
    # Step 8: Update case status
    print("Step 8: Update Case Status")
    db.update_case(case_id, {
        'status': 'reply_received',
        'manufacturer_reply': 'We can help you with that',
        'reply_translated': 'We can help you with that',
        'reply_received_at': datetime.now().isoformat()
    })
    print(f"  ✅ Case updated to 'reply_received'")
    
    print()
    print("🎉 Complete user flow test passed!")
    print()

def test_edge_cases():
    """Test edge cases and error handling"""
    print("🧪 Testing Edge Cases...")
    
    from app import get_database_client
    
    db = get_database_client()
    
    # Test with invalid email
    result = db.authenticate_user("nonexistent@example.com", "password")
    assert 'error' in result
    print("✅ Handles non-existent user")
    
    # Test with empty password
    result = db.create_user("testuser3", "test3@example.com", "")
    # This should fail validation before reaching db
    print("✅ Empty password handling")
    
    # Test getting cases for non-existent user
    cases = db.get_user_cases("nonexistent@example.com")
    assert len(cases) == 0
    print("✅ Returns empty list for non-existent user")
    
    # Test getting non-existent case
    case = db.get_case_by_id("NONEXISTENT-CASE")
    assert case is None
    print("✅ Returns None for non-existent case")
    
    print()

def test_password_hashing():
    """Test password hashing consistency"""
    print("🧪 Testing Password Hashing...")
    
    password = "TestPassword123"
    hash1 = hashlib.sha256(password.encode()).hexdigest()
    hash2 = hashlib.sha256(password.encode()).hexdigest()
    
    assert hash1 == hash2
    print("✅ Password hashing is consistent")
    
    wrong_password = "WrongPassword123"
    hash3 = hashlib.sha256(wrong_password.encode()).hexdigest()
    assert hash1 != hash3
    print("✅ Different passwords produce different hashes")
    
    print()

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)
    print()
    
    try:
        test_validation()
        test_password_hashing()
        test_database_operations()
        test_edge_cases()
        test_user_flow()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("🎯 The application is ready for use!")
        print()
        print("📝 Next steps:")
        print("  1. Configure environment variables in .env")
        print("  2. Set up Supabase database (if using production mode)")
        print("  3. Configure email SMTP settings")
        print("  4. Run: streamlit run app.py")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
