# 🚀 Streamlit Cloud Deployment - Email Setup Guide

## ⚠️ Current Issue
Your app works locally but email verification doesn't work on Streamlit Cloud because the secrets are not configured properly.

## ✅ Step-by-Step Fix

### Step 1: Go to Streamlit Cloud Settings

1. Go to https://share.streamlit.io
2. Find your app: **support-case-workflow**
3. Click on your app
4. Click the **⚙️ Settings** (three dots menu or settings icon)
5. Select **Secrets**

### Step 2: Add These Secrets (FLAT FORMAT)

**Copy and paste this EXACTLY into your Streamlit Cloud Secrets:**

```toml
# General Configuration
ENVIRONMENT = "production"

# Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@supportautomation.com"
ADMIN_PASSWORD = "Admin@123456"
ADMIN_ENABLED = "true"

# Supabase Configuration
SUPABASE_URL = "https://eetdfpfojtktsicojqst.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVldGRmcGZvanRrdHNpY29qcXN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MzE0NzcsImV4cCI6MjA4MTIwNzQ3N30.m1ESYsxFBO-ECPK9vhfNrOVz9UCv29PVn3igwq5nqy4"

# Email Configuration - CRITICAL FOR VERIFICATION
USE_MOCK_EMAIL = "false"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SENDER_EMAIL = "yousufhere.dev@gmail.com"
SENDER_PASSWORD = "aiabopxvronurxzw"
COMPANY_NAME = "Support Automation System"
```

### Step 3: Save and Reboot

1. Click **Save** in Streamlit Cloud
2. **Reboot your app** from the Streamlit Cloud menu (⋮ → Reboot)

### Step 4: Verify It's Working

After rebooting, watch the app logs in Streamlit Cloud:

**You should see:**
```
[CONFIG] Running in Streamlit Cloud - using secrets
[CONFIG] Email sender configured: True
[CONFIG] Email password configured: True
[CONFIG] USE_MOCK_EMAIL setting: False
[CONFIG] Email mode: REAL
```

**If you see this instead (BAD):**
```
[CONFIG] Email mode: MOCK
```
Then your secrets weren't loaded properly - try rebooting again.

## 🔍 Troubleshooting

### Issue: Still seeing MOCK mode in Streamlit Cloud

**Solutions:**
1. Double-check all secrets are saved (no typos)
2. Make sure `USE_MOCK_EMAIL = "false"` (lowercase "false")
3. Verify `SENDER_EMAIL` and `SENDER_PASSWORD` are filled in
4. **Reboot the app** (not just save - you MUST reboot!)
5. Check the app logs for error messages

### Issue: "SMTP Authentication failed"

**Solutions:**
1. Your Gmail App Password might be wrong
2. Generate a **new** App Password:
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification (if not already)
   - Scroll to "App passwords"
   - Generate new password for "Mail"
   - Copy the 16-character code (no spaces)
3. Update `SENDER_PASSWORD` in Streamlit secrets
4. Save and **Reboot**

### Issue: Can't generate App Password

**Reason:** 2-Step Verification not enabled

**Solution:**
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow setup instructions
4. Once enabled, "App passwords" option will appear below it

## 📝 Important Notes

### Why Use Flat Format?

Streamlit Cloud secrets work best with **flat key-value pairs** (not nested sections). The format above uses:
```toml
KEY = "value"
```

NOT:
```toml
[section]
KEY = "value"
```

### Security Warning

The example above contains your **actual credentials**. They are:
- ✅ Safe in Streamlit Cloud Secrets (encrypted)
- ❌ NOT safe if you commit them to GitHub

Make sure your `.env` and `.streamlit/secrets.toml` files are in `.gitignore`!

## ✅ Quick Checklist

- [ ] Logged into Streamlit Cloud
- [ ] Opened app Settings → Secrets
- [ ] Pasted the secrets configuration
- [ ] Saved the secrets
- [ ] **Rebooted the app** (MUST DO THIS!)
- [ ] Checked app logs show "Email mode: REAL"
- [ ] Tested registration/login with email verification

## 🎯 Expected Behavior After Fix

1. User registers/logs in
2. App shows: "✅ Verification code sent to [email]"
3. User receives **actual email** with verification code
4. User enters code and gains access

## 📞 Still Not Working?

Check the **Streamlit Cloud app logs** (click on "Manage app" → View logs) and look for:
- `[CONFIG]` messages showing what mode it's in
- `[EMAIL]` messages showing if emails are being sent
- Any error messages with `[ERROR]`

Share those log messages if you need more help!
