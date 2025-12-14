# Production Setup Guide

## 🚀 Production Deployment Checklist

### ✅ Pre-Deployment

#### 1. Install Production Dependencies
```bash
pip install -r requirements.txt
pip install supabase python-dotenv
```

#### 2. Environment Configuration
Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` with production values:
```bash
ENVIRONMENT=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
COMPANY_NAME=Your Company Name
```

#### 3. Database Setup

**Step 1: Create Supabase Project**
1. Go to [https://supabase.com](https://supabase.com)
2. Create a new project
3. Copy your Project URL and anon/public key

**Step 2: Create Tables**

Run these SQL commands in Supabase SQL Editor:

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Support Cases Table
CREATE TABLE support_cases (
    case_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    original_query TEXT NOT NULL,
    language TEXT NOT NULL,
    manufacturer_id TEXT NOT NULL,
    manufacturer_name TEXT NOT NULL,
    translated_query TEXT,
    task_number TEXT UNIQUE,
    status TEXT DEFAULT 'awaiting_reply',
    submitted_at TIMESTAMP DEFAULT NOW(),
    forwarded_at TIMESTAMP,
    manufacturer_reply TEXT,
    reply_translated TEXT,
    reply_received_at TIMESTAMP,
    reminder_sent BOOLEAN DEFAULT FALSE,
    reminder_sent_at TIMESTAMP,
    needs_approval BOOLEAN DEFAULT FALSE,
    approved BOOLEAN DEFAULT FALSE,
    approved_at TIMESTAMP,
    notes TEXT
);

CREATE INDEX idx_cases_user_email ON support_cases(user_email);
CREATE INDEX idx_cases_task_number ON support_cases(task_number);
CREATE INDEX idx_cases_status ON support_cases(status);
CREATE INDEX idx_cases_submitted_at ON support_cases(submitted_at DESC);
```

**Step 3: Enable Row Level Security (RLS)**

```sql
-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE support_cases ENABLE ROW LEVEL SECURITY;

-- Users can read their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own data
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Users can view their own cases
CREATE POLICY "Users can view own cases" ON support_cases
    FOR SELECT USING (user_email = (SELECT email FROM users WHERE id = auth.uid()));

-- Users can create their own cases
CREATE POLICY "Users can create own cases" ON support_cases
    FOR INSERT WITH CHECK (user_email = (SELECT email FROM users WHERE id = auth.uid()));
```

#### 4. Email Setup (Gmail)

1. **Enable 2-Factor Authentication**
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this as `SENDER_PASSWORD` in `.env`

3. **Test Email Configuration**
   ```python
   python -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   print('✅ Email configuration successful')
   server.quit()
   "
   ```

#### 5. Translation API Setup

**Option A: Google Cloud Translation**
1. Create Google Cloud Project
2. Enable Cloud Translation API
3. Create API Key
4. Add to `.env`: `TRANSLATION_API_KEY=your-key`

**Option B: DeepL**
1. Sign up at [https://www.deepl.com/pro-api](https://www.deepl.com/pro-api)
2. Get API key
3. Add to `.env`: `TRANSLATION_API_KEY=your-key`
4. Set: `TRANSLATION_PROVIDER=deepl`

### 🌐 Deployment Options

#### Option 1: Streamlit Cloud (Recommended for Quick Deploy)

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [https://share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select branch and main file: `app.py`
   - Add secrets in "Advanced settings":
     ```toml
     [env]
     ENVIRONMENT = "production"
     SUPABASE_URL = "your-url"
     SUPABASE_KEY = "your-key"
     SMTP_SERVER = "smtp.gmail.com"
     SENDER_EMAIL = "your-email@gmail.com"
     SENDER_PASSWORD = "your-app-password"
     ```

3. **Deploy**

#### Option 2: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**
   ```bash
   docker build -t support-automation .
   docker run -p 8501:8501 --env-file .env support-automation
   ```

#### Option 3: Traditional Server (Ubuntu)

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   pip3 install -r requirements.txt
   ```

2. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/support-automation.service
   ```

   ```ini
   [Unit]
   Description=Support Automation System
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/var/www/support-automation
   Environment="PATH=/usr/bin"
   EnvironmentFile=/var/www/support-automation/.env
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable support-automation
   sudo systemctl start support-automation
   ```

4. **Configure Nginx Reverse Proxy**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

### 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` to version control
   - Use `.env.example` as template
   - Rotate credentials regularly

2. **Database Security**
   - Enable RLS on all tables
   - Use anon key for client-side
   - Use service key only for server-side operations

3. **Password Security**
   - Minimum 8 characters
   - Require letters + numbers
   - Consider adding special character requirement
   - Implement rate limiting on login attempts

4. **Session Security**
   - Set session timeout (default 24 hours)
   - Clear session on logout
   - Implement CSRF protection

### 📊 Monitoring & Logging

1. **Application Logs**
   ```python
   import logging
   logging.basicConfig(
       filename='app.log',
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s'
   )
   ```

2. **Error Tracking**
   - Integrate Sentry for error tracking
   - Set up alerts for critical errors

3. **Performance Monitoring**
   - Monitor database query performance
   - Track API response times
   - Monitor email delivery rates

### 🧪 Testing Before Production

1. **Test User Flow**
   ```bash
   # Signup → Verify → Login → Create Case
   python test_user_flow.py
   ```

2. **Test Database Operations**
   ```bash
   # Create, Read, Update, Delete operations
   python test_database.py
   ```

3. **Test Email Sending**
   ```bash
   # Send test verification email
   python test_email.py
   ```

### 📈 Scaling Considerations

1. **Database**
   - Supabase Free tier: 500MB database, 2GB bandwidth/month
   - Upgrade to Pro for production: $25/month
   - Consider connection pooling for high traffic

2. **Email Sending**
   - Gmail: 500 emails/day
   - Consider SendGrid/AWS SES for higher volume
   - Implement email queue system

3. **Translation API**
   - Google: $20 per 1M characters
   - DeepL: Free tier 500,000 characters/month
   - Cache translations to reduce costs

### 🔄 Backup & Recovery

1. **Database Backups**
   ```bash
   # Supabase automatic backups (Pro plan)
   # Or manual backup via dashboard
   ```

2. **Application Backup**
   ```bash
   # Regular code commits
   git push origin main
   ```

3. **Configuration Backup**
   ```bash
   # Backup .env securely (encrypted)
   gpg -c .env
   ```

### ✅ Post-Deployment Checklist

- [ ] Database tables created and verified
- [ ] RLS policies enabled
- [ ] Environment variables configured
- [ ] Email sending tested
- [ ] Translation API tested
- [ ] SSL certificate installed (for custom domain)
- [ ] Backup system configured
- [ ] Monitoring and logging enabled
- [ ] Error tracking setup
- [ ] User documentation updated
- [ ] Support contacts configured

### 🆘 Troubleshooting

**Database Connection Failed**
- Verify Supabase URL and key
- Check network connectivity
- Review Supabase project status

**Email Not Sending**
- Verify SMTP credentials
- Check Gmail App Password
- Ensure 2FA enabled
- Check spam folder

**Translation Not Working**
- Verify API key
- Check API quota
- Review API logs

**Performance Issues**
- Enable database connection pooling
- Optimize database queries
- Implement caching
- Consider upgrading server resources

### 📞 Support

For production issues:
- Check logs first
- Review error messages
- Consult documentation
- Contact support team

---

**Last Updated:** December 2025
**Version:** 1.0.0
