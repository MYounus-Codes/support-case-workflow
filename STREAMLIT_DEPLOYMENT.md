# Streamlit Cloud Deployment Guide

## 🚨 URGENT: Your credentials are currently exposed!

Your Supabase keys and other credentials are hardcoded in `config.py` and visible in your GitHub repository. Follow these steps immediately:

## 🔒 Step 1: Secure Your Credentials on Streamlit Cloud

1. **Go to your Streamlit Cloud app**: https://share.streamlit.io
2. **Click on your app** → Click **Settings (⚙️)** → Select **Secrets**
3. **Copy the contents** from `.streamlit/secrets.toml.template`
4. **Paste into Streamlit Secrets** and **update with your real values**:

```toml
[general]
ENVIRONMENT = "production"

[admin]
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@supportautomation.com"
ADMIN_PASSWORD = "YourSecurePassword123!"
ADMIN_ENABLED = "true"

[supabase]
SUPABASE_URL = "https://eetdfpfojtktsicojqst.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

[email]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-actual-email@gmail.com"
SENDER_PASSWORD = "your-gmail-app-password"
COMPANY_NAME = "Support Automation System"
USE_MOCK_EMAIL = "false"
```

5. **Click Save** in Streamlit Cloud
6. **Reboot the app** from the Streamlit Cloud dashboard

## 📧 Step 2: Get Gmail App Password

Your regular Gmail password **will NOT work**. You need an App Password:

1. Go to https://myaccount.google.com
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google", click **2-Step Verification** (enable if not enabled)
4. Scroll to the bottom and click **App passwords**
5. Select:
   - **App**: Mail
   - **Device**: Choose your device or "Other"
6. Click **Generate**
7. **Copy the 16-character password** (displayed without spaces)
8. Use this as `SENDER_PASSWORD` in Streamlit secrets

## ✅ Step 3: Verify Email is Working

After setting up secrets and rebooting:

1. Try to register/login
2. You should see: "✅ Verification code sent to [email]"
3. Check your email inbox
4. If you see "⚠️ Running in MOCK mode", your secrets aren't loaded correctly

## 🔍 Troubleshooting

### Problem: Still seeing MOCK mode
**Solution**: 
- Double-check Streamlit Cloud secrets are saved
- Reboot the app from Streamlit Cloud dashboard
- Make sure `USE_MOCK_EMAIL = "false"` (not "False" or "FALSE")

### Problem: "SMTP Authentication failed"
**Solution**:
- You're using your regular Gmail password (wrong!)
- Generate a new App Password following Step 2
- Update `SENDER_PASSWORD` in Streamlit secrets

### Problem: Email still not sending
**Solution**:
- Make sure 2-Step Verification is enabled on Gmail
- Try generating a fresh App Password
- Check that SENDER_EMAIL matches the Gmail account
- Verify SMTP_PORT is 587 (number, not string "587")

## 🔐 Step 4: Clean Up Exposed Credentials (DO THIS!)

Your credentials are currently in GitHub history. You need to:

1. **Rotate your Supabase keys** (generate new ones in Supabase dashboard)
2. **Update the keys** in Streamlit Cloud secrets
3. **Change your admin password**
4. Consider using `git filter-branch` or BFG Repo Cleaner to remove secrets from Git history

## 📝 What Changed

1. **config.py** now reads from Streamlit secrets first, then environment variables
2. **Better error messages** show exactly what's wrong with email configuration  
3. **Mock mode detection** automatically enabled if credentials are missing
4. **.gitignore** updated to prevent committing secrets
5. **Secrets template** provided for easy setup

## 🎯 Next Steps

1. ✅ Configure Streamlit Cloud secrets
2. ✅ Get Gmail App Password
3. ✅ Reboot app and test email
4. ✅ Rotate exposed credentials
5. ✅ Update README with setup instructions
