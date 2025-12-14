"""
Streamlit Cloud Email Diagnostics
Add this to your app temporarily to debug email issues
"""
import streamlit as st
import os

st.title("🔍 Email Configuration Diagnostics")

# Check if secrets are loaded
st.header("1. Secrets Detection")
if hasattr(st, 'secrets') and len(st.secrets) > 0:
    st.success("✅ Streamlit secrets are loaded!")
    st.write(f"Number of secrets found: {len(st.secrets)}")
    
    # Show which keys exist (without values for security)
    st.subheader("Available secret keys:")
    for key in st.secrets.keys():
        st.write(f"- `{key}`")
else:
    st.error("❌ No Streamlit secrets found!")

st.divider()

# Check email configuration
st.header("2. Email Configuration")

try:
    from config import EMAIL_CONFIG, ENVIRONMENT, USE_STREAMLIT_SECRETS
    
    st.write(f"**Environment Mode:** {ENVIRONMENT}")
    st.write(f"**Using Streamlit Secrets:** {USE_STREAMLIT_SECRETS}")
    st.write(f"**Email Mock Mode:** {EMAIL_CONFIG['use_mock']}")
    
    if EMAIL_CONFIG['use_mock']:
        st.error("❌ Running in MOCK mode - emails won't be sent!")
        st.write("**Reasons for mock mode:**")
        
        sender_email = EMAIL_CONFIG.get('sender_email', '')
        sender_password = EMAIL_CONFIG.get('sender_password', '')
        
        if not sender_email:
            st.write("- ❌ SENDER_EMAIL is not set")
        else:
            st.write(f"- ✅ SENDER_EMAIL: {sender_email}")
            
        if not sender_password:
            st.write("- ❌ SENDER_PASSWORD is not set")
        else:
            st.write(f"- ✅ SENDER_PASSWORD: {'*' * len(sender_password)} (length: {len(sender_password)})")
    else:
        st.success("✅ Running in REAL email mode!")
        st.write(f"**SMTP Server:** {EMAIL_CONFIG['smtp_server']}")
        st.write(f"**SMTP Port:** {EMAIL_CONFIG['smtp_port']}")
        st.write(f"**Sender Email:** {EMAIL_CONFIG['sender_email']}")
        st.write(f"**Password Length:** {len(EMAIL_CONFIG['sender_password'])} characters")
        
except Exception as e:
    st.error(f"❌ Error loading config: {e}")

st.divider()

# Check individual secrets
st.header("3. Individual Secret Values (Nested Structure)")

if hasattr(st, 'secrets'):
    # Check email section
    st.subheader("📧 Email Configuration")
    if 'email' in st.secrets:
        email_keys = ['use_mock', 'sender_email', 'sender_password', 'smtp_server', 'smtp_port']
        for key in email_keys:
            if key in st.secrets['email']:
                value = st.secrets['email'][key]
                if 'password' in key.lower():
                    st.write(f"**email.{key}:** `{'*' * min(len(str(value)), 20)}` (length: {len(str(value))})")
                else:
                    st.write(f"**email.{key}:** `{value}`")
            else:
                st.error(f"❌ **email.{key}:** NOT FOUND!")
    else:
        st.error("❌ **[email] section NOT FOUND in secrets!**")
        st.warning("Your secrets need [email] section with nested keys!")
    
    # Check supabase section
    st.subheader("🗄️ Supabase Configuration")
    if 'supabase' in st.secrets:
        st.write(f"**supabase.url:** `{st.secrets['supabase'].get('url', 'NOT SET')}`")
        key_val = st.secrets['supabase'].get('key', '')
        st.write(f"**supabase.key:** `{'*' * min(len(str(key_val)), 20)}...`" if key_val else "❌ NOT SET")
    else:
        st.warning("⚠️ **[supabase] section not found**")
    
    # Check environment section
    st.subheader("⚙️ Environment Configuration")
    if 'environment' in st.secrets:
        st.write(f"**environment.mode:** `{st.secrets['environment'].get('mode', 'NOT SET')}`")
    else:
        st.warning("⚠️ **[environment] section not found**")

st.divider()

# Test email connection
st.header("4. Test SMTP Connection")

if st.button("🧪 Test SMTP Connection"):
    try:
        import smtplib
        from config import EMAIL_CONFIG
        
        if EMAIL_CONFIG['use_mock']:
            st.warning("⚠️ Email is in MOCK mode - cannot test SMTP connection")
        else:
            with st.spinner("Testing SMTP connection..."):
                with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                    st.write("✅ Connected to SMTP server")
                    server.starttls()
                    st.write("✅ TLS encryption started")
                    server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                    st.write("✅ Authentication successful!")
                    st.success("🎉 SMTP connection test passed! Emails should work.")
    except smtplib.SMTPAuthenticationError as e:
        st.error(f"❌ Authentication failed: {e}")
        st.write("**Possible issues:**")
        st.write("- Wrong Gmail App Password")
        st.write("- 2-Step Verification not enabled")
        st.write("- Need to generate new App Password")
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")

st.divider()

st.info("""
**Next Steps if email still not working:**
1. Make sure you clicked SAVE in Streamlit Cloud secrets
2. Make sure you REBOOTED the app (not just saved)
3. Check that USE_MOCK_EMAIL = "false" (lowercase)
4. Verify your Gmail App Password is correct (16 characters)
5. Generate a NEW Gmail App Password and update secrets
""")
