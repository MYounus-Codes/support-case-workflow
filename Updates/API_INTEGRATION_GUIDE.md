# API Integration Guide

This guide explains how to integrate real APIs and services when moving to production.

## ✅ System Architecture - Production Ready

The system is designed with **clear separation** between mock/development and production implementations:

- **Configuration centralized** in `config.py`
- **Environment-based switching** via `ENVIRONMENT` variable
- **Minimal code changes** required for production

---

## 🔄 What Changes When Going Live?

When you have real APIs and users, you only need to update:

1. **API credentials in `.env` file**
2. **Manufacturer information in `config.py`**
3. **Environment setting from `development` to `production`**

**NO need to change the core workflow or application logic!**

---

## 📝 Step-by-Step Integration

### 1. Language Detection (Already Integrated)

**Current Setup:**
- Uses `langdetect` library (already installed)
- Automatically detects language from user's message
- No user selection required

**Status:** ✅ **Production Ready** - No changes needed!

---

### 2. Translation Service

**Location:** `config.py` → `TRANSLATION_CONFIG`

**Current (Development):**
```python
TRANSLATION_CONFIG = {
    'provider': 'google',
    'api_key': '',
    'use_mock': True  # Using mock translations
}
```

**For Production - Option A: Google Translate API**

1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Update `.env`:
   ```bash
   ENVIRONMENT=production
   TRANSLATION_PROVIDER=google
   TRANSLATION_API_KEY=your-google-translate-api-key
   ```
3. Code in `app.py` and `workflow.py` already supports it!

**For Production - Option B: DeepL API**

1. Get API key from [DeepL](https://www.deepl.com/pro-api)
2. Update `.env`:
   ```bash
   ENVIRONMENT=production
   TRANSLATION_PROVIDER=deepl
   TRANSLATION_API_KEY=your-deepl-api-key
   ```
3. Update `TranslationService` to use DeepL library

**Implementation Example (add to TranslationService):**
```python
# In translate_to_english method:
if TRANSLATION_CONFIG['provider'] == 'deepl':
    import deepl
    translator = deepl.Translator(TRANSLATION_CONFIG['api_key'])
    result = translator.translate_text(
        text, 
        source_lang=source_lang_code.upper(),
        target_lang='EN'
    )
    return result.text, source_lang_code, source_lang_name
```

---

### 3. Manufacturer API Integration

**Location:** `config.py` → `MANUFACTURERS`

**Current Configuration:**
```python
MANUFACTURERS = {
    'manufacturer_1': {
        'name': 'Tech Solutions Inc.',
        'api_url': 'https://api.techsolutions.com',
        'email': 'raufa7951@gmail.com',
        'api_key': ''
    }
}
```

**For Production:**

1. Update manufacturer details in `config.py`:
   ```python
   MANUFACTURERS = {
       'manufacturer_1': {
           'name': 'Real Manufacturer Name',
           'api_url': os.getenv('MANUFACTURER_1_API', 'https://api.realmanufacturer.com'),
           'email': os.getenv('MANUFACTURER_1_EMAIL', 'support@realmanufacturer.com'),
           'api_key': os.getenv('MANUFACTURER_1_KEY', '')
       }
   }
   ```

2. Add to `.env`:
   ```bash
   MANUFACTURER_1_API=https://api.realmanufacturer.com
   MANUFACTURER_1_EMAIL=support@realmanufacturer.com
   MANUFACTURER_1_KEY=your-api-key
   ```

3. Update `ManufacturerAPI` class in `app.py`:

**Current (Mock):**
```python
def submit_case(self, manufacturer_id: str, case_description: str) -> str:
    self.task_counter += 1
    task_number = f"{manufacturer_id.upper()}-TASK-{self.task_counter}"
    # Simulate API call
    return task_number
```

**Production Implementation:**
```python
def submit_case(self, manufacturer_id: str, case_description: str) -> str:
    """Submit case to manufacturer via their API"""
    manufacturer = MANUFACTURERS.get(manufacturer_id)
    
    # Real API call
    import requests
    response = requests.post(
        f"{manufacturer['api_url']}/cases",
        headers={
            'Authorization': f"Bearer {manufacturer['api_key']}",
            'Content-Type': 'application/json'
        },
        json={
            'description': case_description,
            'priority': 'normal'
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['task_number']  # Or whatever their API returns
    else:
        raise Exception(f"API Error: {response.status_code}")
```

---

### 4. Email Service (Already Configured)

**Location:** `config.py` → `EMAIL_CONFIG`

**Current Setup:**
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',
    'use_mock': False  # Can use real email now!
}
```

**For Production:**

1. Update `.env`:
   ```bash
   SENDER_EMAIL=your-company-email@company.com
   SENDER_PASSWORD=your-app-specific-password
   SMTP_SERVER=smtp.gmail.com  # or your email provider
   SMTP_PORT=587
   USE_MOCK_EMAIL=false
   ```

**Status:** ✅ Already integrated in `app.py` (EmailService class)

---

### 5. Database (Supabase)

**Location:** `config.py` → `SUPABASE_CONFIG`

**Current Setup:**
```python
SUPABASE_CONFIG = {
    'url': 'https://eetdfpfojtktsicojqst.supabase.co',
    'key': 'your-key-here',
    'use_mock': True  # Currently using in-memory storage
}
```

**For Production:**

1. Create tables using `tables.sql`
2. Update `.env`:
   ```bash
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_KEY=your-supabase-anon-key
   ENVIRONMENT=production  # This will set use_mock=False
   ```

**Status:** ✅ Already integrated with REST client fallback

---

## 🎯 Quick Production Checklist

When you're ready to go live, just:

- [ ] **Update `.env` file** with production credentials
- [ ] **Set `ENVIRONMENT=production`** in `.env`
- [ ] **Update manufacturer information** in `config.py`
- [ ] **Test translation API** with real credentials
- [ ] **Verify manufacturer API endpoints** work correctly
- [ ] **Run `tables.sql`** in Supabase to create database schema
- [ ] **Test end-to-end flow** with real services

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Enable rate limiting** on APIs
5. **Use HTTPS** for all API calls
6. **Validate manufacturer responses** before processing

---

## 📊 Monitoring & Logging

The system already includes logging at key points:

```python
print(f"[LANGUAGE DETECTION] Detected: {detected_code}")
print(f"[TRANSLATION] Translating from {source_lang_name}")
print(f"[MANUFACTURER API] Submitting to {manufacturer_id}")
```

**For Production:**
- Replace `print()` with proper logging library
- Set up error tracking (e.g., Sentry)
- Monitor API usage and costs
- Track translation accuracy

---

## 🚀 Deployment

The system is designed to be deployed as:

1. **Streamlit Cloud** - Easiest option
2. **Docker Container** - For custom hosting
3. **Cloud Platform** - AWS, Azure, GCP

All configurations are centralized, making deployment straightforward!

---

## 📞 Support

If you need help integrating specific APIs:
1. Check manufacturer's API documentation
2. Update the `ManufacturerAPI` class accordingly
3. Test with mock data first
4. Gradually roll out to production

**Remember:** The system is designed so you only change API endpoints and credentials, not the core workflow!
