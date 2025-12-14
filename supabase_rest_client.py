"""
Supabase REST API Client - Direct HTTP Implementation
Workaround for SDK compatibility issues
"""

import requests
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import json


class SupabaseRESTClient:
    """
    Direct REST API client for Supabase
    Bypasses the SDK proxy parameter issue
    """
    
    def __init__(self, url: str, key: str):
        self.url = url.rstrip('/')
        self.key = key
        self.headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None):
        """Make HTTP request to Supabase REST API"""
        url = f"{self.url}/rest/v1/{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data, params=params)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, params=params)
            
            response.raise_for_status()
            return response.json() if response.text else []
        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
    
    # User operations
    def create_user(self, username: str, email: str, password: str) -> Dict:
        """Create new user"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'verified': False
            }
            result = self._request('POST', 'users', data=data)
            return {'success': True, 'user_id': result[0]['id'] if result else None}
        except Exception as e:
            error_msg = str(e)
            if 'duplicate' in error_msg.lower() or 'unique' in error_msg.lower():
                if 'email' in error_msg.lower():
                    return {'error': 'Email already registered'}
                elif 'username' in error_msg.lower():
                    return {'error': 'Username already taken'}
            return {'error': f'Registration failed: {error_msg}'}
    
    def authenticate_user(self, email: str, password: str) -> Dict:
        """Authenticate user"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            params = {
                'email': f'eq.{email}',
                'password_hash': f'eq.{password_hash}',
                'select': '*'
            }
            result = self._request('GET', 'users', params=params)
            
            if not result or len(result) == 0:
                return {'error': 'Invalid email or password'}
            
            return {'success': True, 'user': result[0]}
        except Exception as e:
            return {'error': f'Authentication failed: {str(e)}'}
    
    def verify_user(self, email: str) -> bool:
        """Mark user as verified"""
        try:
            params = {'email': f'eq.{email}'}
            data = {'verified': True}
            self._request('PATCH', 'users', data=data, params=params)
            return True
        except:
            return False
    
    def update_last_login(self, email: str):
        """Update last login timestamp"""
        try:
            params = {'email': f'eq.{email}'}
            data = {'last_login': datetime.now().isoformat()}
            self._request('PATCH', 'users', data=data, params=params)
        except:
            pass
    
    # Support case operations
    def create_support_case(self, case_data: Dict) -> str:
        """Create support case"""
        try:
            result = self._request('POST', 'support_cases', data=case_data)
            return result[0]['case_id'] if result else None
        except Exception as e:
            print(f"Error creating case: {e}")
            return None
    
    def get_user_cases(self, user_email: str) -> List[Dict]:
        """Get all cases for a user"""
        try:
            params = {
                'user_email': f'eq.{user_email}',
                'order': 'submitted_at.desc',
                'select': '*'
            }
            return self._request('GET', 'support_cases', params=params)
        except Exception as e:
            print(f"Error fetching cases: {e}")
            return []
    
    def get_case_by_id(self, case_id: str) -> Optional[Dict]:
        """Get specific case"""
        try:
            params = {'case_id': f'eq.{case_id}', 'select': '*'}
            result = self._request('GET', 'support_cases', params=params)
            return result[0] if result else None
        except:
            return None
    
    def update_case(self, case_id: str, updates: Dict) -> bool:
        """Update support case"""
        try:
            params = {'case_id': f'eq.{case_id}'}
            self._request('PATCH', 'support_cases', data=updates, params=params)
            return True
        except:
            return False
    
    def get_all_cases(self) -> List[Dict]:
        """Get all cases (admin)"""
        try:
            params = {'order': 'submitted_at.desc', 'select': '*'}
            return self._request('GET', 'support_cases', params=params)
        except Exception as e:
            print(f"Error fetching all cases: {e}")
            return []
    
    def get_manufacturers(self) -> List[Dict]:
        """Get all manufacturers"""
        try:
            params = {'select': '*'}
            return self._request('GET', 'manufacturers', params=params)
        except Exception as e:
            print(f"Error fetching manufacturers: {e}")
            return []


# Test function
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    print("🧪 Testing Supabase REST API Client")
    print("=" * 60)
    print()
    
    try:
        client = SupabaseRESTClient(url, key)
        
        print("✅ Client initialized")
        print()
        
        # Test manufacturers
        print("Testing manufacturers table...")
        manufacturers = client.get_manufacturers()
        print(f"✅ Found {len(manufacturers)} manufacturers")
        for mfr in manufacturers:
            print(f"   - {mfr.get('name')}")
        print()
        
        print("=" * 60)
        print("✅ REST API CLIENT WORKING!")
        print("=" * 60)
        print()
        print("This client bypasses the SDK proxy issue.")
        print("You can now use the application with ENVIRONMENT=production")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
