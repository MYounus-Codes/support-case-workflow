# 🚨 EMAIL NOT WORKING? - Quick Fix Checklist

## Run These Diagnostic Steps:

### Step 1: Deploy Diagnostics Page

1. **Commit and push the diagnostic file:**
   ```bash
   git add email_diagnostics.py
   git commit -m "Add email diagnostics"
   git push
   ```

2. **Access the diagnostics:**
   - Go to your Streamlit Cloud app
   - Add `?page=email_diagnostics` to the URL, OR
   - Run: `streamlit run email_diagnostics.py` in your app

3. **Check the diagnostics output** - it will tell you exactly what's wrong!

### Step 2: Common Issues & Fixes

#### ❌ Issue: "No Streamlit secrets found"
**Fix:** 
- Secrets weren't saved or app wasn't rebooted
- Go to Streamlit Cloud → Settings → Secrets
- Verify secrets are there
- Click **Reboot** (not just Save!)

#### ❌ Issue: "SENDER_EMAIL: NOT FOUND"
**Fix:**
Your secrets format is wrong. Use this EXACT format (no quotes around keys):

```toml
SENDER_EMAIL = "yousufhere.dev@gmail.com"
SENDER_PASSWORD = "aiabopxvronurxzw"
USE_MOCK_EMAIL = "false"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
```

NOT this:
```toml
"SENDER_EMAIL" = "yousufhere.dev@gmail.com"  ❌ Wrong!
```

#### ❌ Issue: "Running in MOCK mode"
**Fix:**
Either credentials are missing OR USE_MOCK_EMAIL is set to true

Check diagnostics page to see which credential is missing

#### ❌ Issue: "SMTP Authentication failed"
**Fix:**
Your Gmail App Password is wrong. Generate a NEW one:

1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already)
3. Scroll to "App passwords"
4. Click "App passwords"
5. Select app: **Mail**
6. Generate new password
7. Copy the 16-character code (NO SPACES)
8. Update `SENDER_PASSWORD` in Streamlit Cloud secrets
9. Save and **REBOOT**

#### ❌ Issue: "Less secure app access"
**Fix:**
You're trying to use your regular Gmail password instead of App Password!

You MUST use an App Password (see above)

### Step 3: Verify Secrets Format

Your Streamlit Cloud secrets should look EXACTLY like this:

```toml
ENVIRONMENT = "production"
USE_MOCK_EMAIL = "false"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SENDER_EMAIL = "yousufhere.dev@gmail.com"
SENDER_PASSWORD = "aiabopxvronurxzw"
COMPANY_NAME = "Support Automation System"
SUPABASE_URL = "https://eetdfpfojtktsicojqst.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVldGRmcGZvanRrdHNpY29qcXN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MzE0NzcsImV4cCI6MjA4MTIwNzQ3N30.m1ESYsxFBO-ECPK9vhfNrOVz9UCv29PVn3igwq5nqy4"
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@supportautomation.com"
ADMIN_PASSWORD = "Admin@123456"
ADMIN_ENABLED = "true"
```

**Key points:**
- NO quote marks around the key names (left side)
- YES quote marks around the values (right side)
- NO [sections] like `[email]` or `[general]`
- FLAT format only

### Step 4: After Updating Secrets

**YOU MUST REBOOT THE APP!**

1. Save secrets
2. Click the menu (⋮)
3. Select **Reboot app**
4. Wait for app to restart
5. Check logs for: `[CONFIG] Email mode: REAL`

### Step 5: Test in the App

1. Try to register/login
2. Should see: "✅ Verification code sent to [email]"
3. Check your email inbox
4. Enter verification code

## 🆘 Still Not Working?

Run the diagnostics page and share the output:
```bash
streamlit run email_diagnostics.py
```

Or check the **Streamlit Cloud logs**:
- Click "Manage app"
- View logs
- Look for `[CONFIG]` and `[EMAIL]` messages
- Share any error messages
