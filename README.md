# 🎫 Support Automation System - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Database Setup](#database-setup)
8. [API Integration](#api-integration)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

A comprehensive support case automation system that handles multilingual support requests, manufacturer communication, and automated follow-ups. Built with Streamlit and Supabase.

### Key Capabilities
- 🔐 **Secure Authentication** with email verification
- 🌐 **Multi-language Support** with automatic translation
- 🏭 **Multiple Manufacturers** integration
- ⏰ **Automated Reminders** (24-hour business hours)
- 📊 **Real-time Dashboard** for case tracking
- 💾 **Cloud Database** with Supabase
- 📧 **Email Notifications** at every step

---

## ✨ Features

### Authentication & Security
- ✅ User signup with validation
- ✅ Secure login with SHA-256 password hashing
- ✅ Email verification with 6-digit code
- ✅ Automatic redirect to dashboard after verification
- ✅ Session management
- ✅ Row Level Security (RLS) in database

### Support Case Management
- ✅ Create support cases in any language
- ✅ Automatic translation to English
- ✅ Forward to manufacturer with task tracking
- ✅ Real-time status updates
- ✅ Complete audit trail
- ✅ Case history tracking

### Automation
- ✅ 24-hour business hours reminder system
- ✅ Weekend exclusion (Saturday & Sunday)
- ✅ Automatic email notifications
- ✅ Background task processing
- ✅ Workflow orchestration

### Admin Panel
- ✅ System statistics dashboard
- ✅ View all cases
- ✅ Manage case statuses
- ✅ Configure system settings
- ✅ Monitor overdue cases

---

## 🚀 Quick Start

### Prerequisites
```bash
# Check Python version (3.8+ required)
python --version

# Check pip
pip --version
```

### 3-Step Installation

```bash
# 1. Create project folder
mkdir support_automation
cd support_automation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

### ⚡ New Features (December 2025)

#### 📧 Real Email Sending
- Verification codes sent to actual email inbox (not console)
- Case notifications delivered via email
- Works in both development and production
- Supports Gmail, Outlook, SendGrid, and custom SMTP

**Setup Instructions**: See [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md)

#### 🔄 Persistent Sessions
- User and admin sessions maintained on page reload
- 24-hour automatic session timeout
- No need to re-login after browser refresh
- Secure session management with timestamps

**Quick Test**:
```bash
# Test your email configuration
python test_email_config.py

# This will verify SMTP settings and send a test email
```

---

## 📦 Installation

### Option 1: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install streamlit==1.31.0 supabase==2.3.0 python-dotenv==1.0.0

# Save app.py and run
streamlit run app.py
```

### Option 2: Docker Setup (Coming Soon)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## ⚙️ Configuration

### 1. Environment Variables

Create `.env` file:

```env
# Environment Mode
ENVIRONMENT=development

# Email Configuration (IMPORTANT: Setup required for real emails)
USE_MOCK_EMAIL=false              # Set to 'true' for console output only
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password   # See EMAIL_SETUP_GUIDE.md
COMPANY_NAME=Support Automation System

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@supportautomation.com
ADMIN_PASSWORD=Admin@123456
ADMIN_ENABLED=true

# System Settings
REMINDER_HOURS=24
EXCLUDE_WEEKENDS=true
```

**📧 Email Setup**: Follow the [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) to configure Gmail SMTP with App Password.

### 2. Update app.py

```python
# Load from .env
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_CONFIG = {
    'url': os.getenv('SUPABASE_URL'),
    'key': os.getenv('SUPABASE_KEY')
}

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': int(os.getenv('SMTP_PORT')),
    'sender_email': os.getenv('SENDER_EMAIL'),
    'sender_password': os.getenv('SENDER_PASSWORD')
}
```

### 3. Gmail App Password Setup

1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Generate App Password:
   - Search "App passwords"
   - Select "Mail" and your device
   - Copy 16-digit password
   - Use this in `.env` file

---

## 🗄️ Database Setup

### Step 1: Create Supabase Account

1. Visit https://supabase.com
2. Create free account
3. Create new project
4. Note your credentials

### Step 2: Create Tables

Copy and run the SQL script in Supabase SQL Editor:

```sql
-- Run the complete SQL script from supabase_schema.sql
-- This creates all 6 tables with indexes and triggers
```

### Step 3: Enable Real Database

In `app.py`, find:

```python
self.use_mock = True  # Change to False
```

Change to:

```python
self.use_mock = False  # Now using real Supabase!
```

Uncomment:

```python
from supabase import create_client, Client
self.client: Client = create_client(
    SUPABASE_CONFIG['url'],
    SUPABASE_CONFIG['key']
)
```

---

## 🔧 API Integration

### Translation API

Choose and integrate one:

**Option 1: Google Translate API**
```python
from googletrans import Translator

def translate_to_english(text, source_lang):
    translator = Translator()
    result = translator.translate(text, src=source_lang, dest='en')
    return result.text
```

**Option 2: DeepL API**
```python
import deepl

def translate_to_english(text, source_lang):
    translator = deepl.Translator(DEEPL_API_KEY)
    result = translator.translate_text(text, target_lang="EN")
    return result.text
```

### Manufacturer API

Replace mock implementation:

```python
def submit_case(self, manufacturer_id: str, case_description: str) -> str:
    # Real API call
    response = requests.post(
        MANUFACTURERS[manufacturer_id]['api_url'],
        json={'description': case_description},
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    return response.json()['task_number']
```

---

## 💻 Usage

### For End Users

1. **Sign Up**
   ```
   Navigate to app → Sign Up tab
   Enter: Username, Email, Password
   Click "Sign Up"
   ```

2. **Login**
   ```
   Enter: Email, Password
   Receive verification code
   Enter code → Automatically redirected to dashboard
   ```

3. **Create Support Case**
   ```
   Dashboard → New Support Case tab
   Select: Language, Manufacturer
   Describe issue
   Submit → Receive task number
   ```

4. **Track Cases**
   ```
   Dashboard → My Cases tab
   View all cases with status
   ```

### For Administrators

```python
# Enable admin mode in sidebar
# View system statistics
# Manage all cases
# Configure settings
```

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Connect repository
4. Add secrets in Settings:
   ```toml
   [secrets]
   SUPABASE_URL = "your-url"
   SUPABASE_KEY = "your-key"
   ```
5. Deploy!

### Option 2: Heroku

```bash
# Create Procfile
web: streamlit run app.py --server.port=$PORT

# Create runtime.txt
python-3.10.12

# Deploy
heroku create your-app-name
git push heroku main
heroku config:set SUPABASE_URL=your-url
```

### Option 3: AWS/GCP/Azure

Use Docker container or VM with:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

---

## 🔍 Testing

### Test Flow

```bash
# 1. Create test user
Username: testuser
Email: test@example.com
Password: Test123!

# 2. Login and verify
Enter verification code (shown on screen)

# 3. Create test case
Language: Danish
Manufacturer: Tech Solutions Inc.
Query: "Test query for support"

# 4. Check database
# Verify case saved in Supabase
```

### Unit Tests (Coming Soon)

```python
def test_user_creation():
    db = SupabaseClient()
    result = db.create_user('test', 'test@test.com', 'pass123')
    assert result['success'] == True

def test_case_creation():
    # Test case creation workflow
    pass
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found: streamlit"**
```bash
# Solution:
pip install streamlit
```

**2. "Supabase connection failed"**
```bash
# Check credentials in .env
# Verify Supabase project is active
# Test connection in Supabase dashboard
```

**3. "Email not sending"**
```bash
# Verify SMTP settings
# Use App Password (not regular password)
# Check firewall/antivirus
```

**4. "Verification code incorrect"**
```bash
# Code shown on screen for testing
# Check console for code
# Ensure timing (expires in 10 min)
```

**5. "Port already in use"**
```bash
# Use different port:
streamlit run app.py --server.port 8502
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in Streamlit
st.write("Debug:", st.session_state)
```

---

## 📊 Project Structure

```
support_automation/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore file
├── README.md                   # This file
│
├── sql/
│   └── supabase_schema.sql    # Database schema
│
├── docs/
│   ├── setup_guide.md         # Setup instructions
│   └── api_docs.md            # API documentation
│
└── tests/                     # Unit tests (optional)
    ├── test_auth.py
    ├── test_cases.py
    └── test_workflow.py
```

---

## 🎓 Best Practices

### Security
- ✅ Never commit `.env` to git
- ✅ Use environment variables for secrets
- ✅ Enable RLS in Supabase
- ✅ Use HTTPS in production
- ✅ Implement rate limiting

### Performance
- ✅ Use database indexes
- ✅ Cache frequent queries
- ✅ Optimize images and assets
- ✅ Use connection pooling
- ✅ Monitor with logging

### Maintenance
- ✅ Regular database backups
- ✅ Monitor error logs
- ✅ Update dependencies
- ✅ Test before deployment
- ✅ Document changes

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📞 Support

- 📧 Email: support@example.com
- 💬 Discord: [Join Server]
- 📚 Docs: [Documentation]
- 🐛 Issues: [GitHub Issues]

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ User authentication
- ✅ Email verification
- ✅ Support case creation
- ✅ Multi-language support
- ✅ Automated reminders
- ✅ Basic dashboard

### Version 1.1 (Planned)
- 📋 Advanced analytics
- 📊 Export to PDF/Excel
- 🔔 Push notifications
- 🌙 Dark mode
- 📱 Mobile app
- 🤖 AI-powered responses

### Version 2.0 (Future)
- 🎯 ML-based routing
- 📈 Predictive analytics
- 🔗 Third-party integrations
- 🌍 Multi-tenant support
- 💬 Live chat
- 📞 VoIP integration

---

## 🎉 Acknowledgments

- Streamlit team for amazing framework
- Supabase for cloud database
- Community contributors
- Open source libraries

---

## 📈 Statistics

- ⭐ GitHub Stars: [Count]
- 🍴 Forks: [Count]
- 🐛 Issues: [Count]
- ✅ Pull Requests: [Count]

---

**Built with ❤️ using Streamlit and Supabase**

*Last Updated: December 2024*