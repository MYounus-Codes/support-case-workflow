"""Test configuration loading"""
from config import EMAIL_CONFIG, ENVIRONMENT

print(f"Environment: {ENVIRONMENT}")
print(f"Email Mock Mode: {EMAIL_CONFIG['use_mock']}")
print(f"Sender Email: {EMAIL_CONFIG['sender_email']}")
print(f"Password Set: {bool(EMAIL_CONFIG['sender_password'])}")
print(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}")
print(f"SMTP Port: {EMAIL_CONFIG['smtp_port']}")
