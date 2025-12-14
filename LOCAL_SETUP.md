# Quick Setup Instructions

## ✅ Configuration is now fixed!

Your `.env` file should have these settings for **local development with real emails**:

```env
# Set to development for local, production for cloud
ENVIRONMENT=development

# Email settings - MUST have these for real emails
USE_MOCK_EMAIL=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=yousufhere.dev@gmail.com
SENDER_PASSWORD=aiabopxvronurxzw
COMPANY_NAME=Support Automation System

# Supabase
SUPABASE_URL=https://eetdfpfojtktsicojqst.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🚀 How to Run Locally

1. **Make sure your `.env` file exists** (not just `.env.example`)
   ```bash
   # If .env doesn't exist, copy from example:
   copy .env.example .env
   ```

2. **Edit `.env` file** and ensure:
   - `USE_MOCK_EMAIL=false`
   - `SENDER_EMAIL` has your Gmail address
   - `SENDER_PASSWORD` has your Gmail App Password

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

4. **Check the console** - you should see:
   ```
   [CONFIG] Running locally - using .env file
   [CONFIG] Email sender configured: True
   [CONFIG] Email password configured: True
   [CONFIG] USE_MOCK_EMAIL setting: False
   [CONFIG] Email mode: REAL
   ```

## 🔧 What Was Fixed

1. **No more secrets.toml error** - Config now gracefully detects if running locally or on Streamlit Cloud
2. **Proper .env loading** - Uses environment variables when not on Streamlit Cloud
3. **Better debug logging** - Shows exactly what mode it's running in
4. **Email mock detection** - Only uses mock if credentials are missing OR `USE_MOCK_EMAIL=true`

## 🎯 Testing

Run this to verify your config:
```bash
python test_config.py
```

You should see `Email mode: REAL` if everything is configured correctly.
