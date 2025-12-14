"""
Quick Email Configuration Test
Tests SMTP connection without running the full app
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_config():
    """Test email configuration"""
    
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Get config from environment
    use_mock = os.getenv('USE_MOCK_EMAIL', 'false').lower() == 'true'
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL', '')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    
    print(f"\n📧 Email Mode: {'MOCK' if use_mock else 'REAL'}")
    print(f"📮 SMTP Server: {smtp_server}:{smtp_port}")
    print(f"👤 Sender Email: {sender_email}")
    print(f"🔑 Password Set: {'Yes' if sender_password and sender_password != 'your-gmail-app-password' else 'No'}")
    
    if use_mock:
        print("\n⚠️  Mock email mode is enabled.")
        print("   Emails will be printed to console, not sent.")
        print("   To enable real email, set USE_MOCK_EMAIL=false in .env")
        return
    
    # Check if credentials are configured
    if not sender_email or sender_email == 'your-email@gmail.com':
        print("\n❌ ERROR: SENDER_EMAIL not configured in .env")
        print("   Please set your Gmail address in .env file")
        return
    
    if not sender_password or sender_password == 'your-gmail-app-password':
        print("\n❌ ERROR: SENDER_PASSWORD not configured in .env")
        print("   Please set your Gmail App Password in .env file")
        print("\n📖 Setup Instructions:")
        print("   1. Go to: https://myaccount.google.com/apppasswords")
        print("   2. Enable 2-Step Verification if not already enabled")
        print("   3. Generate App Password for 'Mail'")
        print("   4. Copy the 16-character password")
        print("   5. Update SENDER_PASSWORD in .env file")
        return
    
    # Test SMTP connection
    print("\n🔌 Testing SMTP connection...")
    
    try:
        # Create test message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = sender_email  # Send to self for testing
        message['Subject'] = "Test Email - Support Automation System"
        
        body = """
This is a test email from your Support Automation System.

If you received this email, your SMTP configuration is working correctly!

Configuration:
- SMTP Server: {}
- SMTP Port: {}
- Sender Email: {}

You can now use real email sending in your application.

Best regards,
Support Automation System
        """.format(smtp_server, smtp_port, sender_email)
        
        message.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        print(f"   Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            print("   Starting TLS encryption...")
            server.starttls()
            
            print("   Authenticating...")
            server.login(sender_email, sender_password)
            
            print("   Sending test email...")
            server.send_message(message)
        
        print("\n✅ SUCCESS! Email configuration is working!")
        print(f"   A test email has been sent to: {sender_email}")
        print("   Check your inbox (and spam folder)")
        print("\n✅ You can now run: streamlit run app.py")
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ ERROR: Authentication failed")
        print("   Your email or password is incorrect")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify SENDER_EMAIL is correct")
        print("   2. Ensure you're using Gmail App Password (not regular password)")
        print("   3. Regenerate App Password and try again")
        print("   4. Make sure 2-Step Verification is enabled")
        
    except smtplib.SMTPConnectError:
        print("\n❌ ERROR: Cannot connect to SMTP server")
        print("   Check your internet connection")
        print(f"   Verify SMTP_SERVER ({smtp_server}) and SMTP_PORT ({smtp_port})")
        
    except TimeoutError:
        print("\n❌ ERROR: Connection timeout")
        print("   Check if port 587 is blocked by firewall")
        print("   Try a different network if on restricted network")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your .env file configuration")
        print("   2. Ensure all credentials are correct")
        print("   3. Try regenerating your Gmail App Password")

if __name__ == "__main__":
    test_email_config()
