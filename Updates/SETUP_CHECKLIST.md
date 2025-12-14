# 🎯 Setup & Testing Checklist

## Pre-Deployment Checklist

### 1. Email Configuration ✉️

- [ ] **Enable 2-Step Verification** on your Google Account
  - Go to: https://myaccount.google.com/security
  - Click "2-Step Verification" and complete setup

- [ ] **Generate Gmail App Password**
  - Go to: https://myaccount.google.com/apppasswords
  - Select app: "Mail"
  - Select device: "Other (Custom name)"
  - Enter name: "Support Case Workflow"
  - Click "Generate"
  - **Copy the 16-character password** (no spaces)

- [ ] **Update .env file**
  ```env
  USE_MOCK_EMAIL=false
  SENDER_EMAIL=yousufhere.dev@gmail.com
  SENDER_PASSWORD=your-16-char-password-here
  ```

- [ ] **Test Email Configuration**
  ```bash
  python test_email_config.py
  ```
  - You should receive a test email
  - Check your inbox and spam folder

### 2. Session Management 🔐

- [ ] Session persistence code is implemented (✅ Already done)
- [ ] User sessions survive page reloads
- [ ] Admin sessions survive page reloads
- [ ] Sessions expire after 24 hours
- [ ] Clean logout functionality works

### 3. Application Testing 🧪

#### User Flow Test
- [ ] **Sign Up New User**
  - Click "Sign Up" tab
  - Enter username, email, password
  - Click "Sign Up"
  - **Check email inbox** for verification code
  - Enter code and verify
  - Should redirect to dashboard

- [ ] **Login Existing User**
  - Enter email and password
  - Click "Login"
  - **Check email inbox** for verification code
  - Enter code and verify
  - Should redirect to dashboard

- [ ] **Page Reload Test**
  - While logged in, press F5 or Ctrl+R
  - Should remain logged in
  - Dashboard should still be visible
  - No need to re-authenticate

- [ ] **Session Timeout Test**
  - Login and note the time
  - Wait 24 hours (or temporarily reduce timeout in config)
  - Reload page
  - Should be logged out automatically

- [ ] **Logout Test**
  - Click "Logout" button
  - Should redirect to login page
  - Session should be completely cleared
  - Reloading should stay on login page

#### Admin Flow Test
- [ ] **Admin Login**
  - Click "Admin Login" tab
  - Username: `admin`
  - Password: `Admin@123456` (or your configured password)
  - Should redirect to admin panel

- [ ] **Admin Page Reload**
  - While logged in as admin, press F5
  - Should remain logged in as admin
  - Admin panel should still be visible

- [ ] **Admin Logout**
  - Click logout
  - Should redirect to login page

#### Support Case Flow Test
- [ ] **Create Support Case**
  - Login as user
  - Go to "New Support Case" tab
  - Select language and manufacturer
  - Enter issue description
  - Click "Submit Support Request"
  - **Check email inbox** for case notification
  - Email should contain case ID and task number

- [ ] **View Cases**
  - Go to "My Cases" tab
  - Should see submitted cases
  - Case status should be visible

### 4. Email Content Verification 📧

Check that emails contain:

**Verification Email:**
- [ ] User's name in greeting
- [ ] 6-digit verification code
- [ ] Expiry time (10 minutes)
- [ ] Company name in signature

**Case Notification Email:**
- [ ] Case ID
- [ ] Task number
- [ ] Confirmation message
- [ ] Company name in signature

### 5. Console Output Check 🖥️

With `USE_MOCK_EMAIL=false`, you should **NOT** see:
- ❌ `[EMAIL MOCK] Sending verification code...`
- ❌ `[EMAIL MOCK] Verification Code: ...`
- ❌ `[EMAIL MOCK] Case notification sent...`

You should see:
- ✅ `[EMAIL] Verification code sent to ...`
- ✅ `[EMAIL] Case notification sent to ...`

### 6. Error Testing 🐛

- [ ] **Wrong Verification Code**
  - Enter incorrect code
  - Should show error message
  - Should allow retry

- [ ] **Expired Verification Code**
  - Wait 10+ minutes after code generation
  - Try to verify
  - Should show expiry error
  - Should allow requesting new code

- [ ] **Invalid Email**
  - Try signup with invalid email format
  - Should show validation error

- [ ] **Weak Password**
  - Try signup with short password (< 8 chars)
  - Should show password requirement error

### 7. Production Readiness 🚀

- [ ] **Environment Variables**
  - All sensitive data in .env (not hardcoded)
  - .env is in .gitignore
  - No credentials in git history

- [ ] **Email Sending**
  - Real emails working (not mock)
  - Emails deliver within 1-2 minutes
  - No emails in spam (check sender reputation)

- [ ] **Session Security**
  - Sessions timeout after 24 hours
  - Sessions clear on logout
  - No session data leakage

- [ ] **Database**
  - Supabase connected (if using production DB)
  - RLS policies enabled
  - Data persists correctly

## Quick Test Commands

```bash
# Test email configuration
python test_email_config.py

# Run the application
streamlit run app.py

# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Email:', os.getenv('SENDER_EMAIL')); print('Mock:', os.getenv('USE_MOCK_EMAIL'))"
```

## Troubleshooting

### ❌ No Email Received?

1. Check spam/junk folder
2. Verify `USE_MOCK_EMAIL=false` in .env
3. Run `python test_email_config.py`
4. Check console for error messages
5. Verify App Password (not regular password)
6. Ensure 2-Step Verification is enabled

### ❌ Session Not Persisting?

1. Check browser console for errors
2. Verify Streamlit version: `streamlit version`
3. Clear browser cache
4. Try incognito/private window
5. Check that `session_created_at` is set on login

### ❌ Authentication Failed?

1. Regenerate Gmail App Password
2. Copy password without spaces
3. Update SENDER_PASSWORD in .env
4. Restart application

### ❌ Emails Going to Spam?

1. Check sender reputation
2. Consider using SendGrid for production
3. Set up SPF/DKIM records (for custom domains)
4. Warm up new email addresses gradually

## Documentation Reference

- [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) - Detailed email setup instructions
- [SESSION_EMAIL_IMPLEMENTATION.md](SESSION_EMAIL_IMPLEMENTATION.md) - Technical implementation details
- [README.md](README.md) - Complete application documentation

## Support

If you encounter issues:
1. Check the documentation files listed above
2. Review console logs for error messages
3. Verify all environment variables are set correctly
4. Test with `USE_MOCK_EMAIL=true` first to isolate email issues

---

**Last Updated**: December 14, 2025  
**Status**: Ready for Testing ✅
