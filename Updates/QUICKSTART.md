# 🚀 Quick Start Guide

## Get Running in 2 Minutes

### Step 1: Install Dependencies (30 seconds)
```bash
pip install streamlit
```

### Step 2: Run the Application (10 seconds)
```bash
streamlit run app.py
```

### Step 3: Open Browser
The app will automatically open at: **http://localhost:8501**

---

## 🎮 Try It Out

### Demo User Flow

1. **Signup** (New Account)
   - Click "Sign Up" tab
   - Username: `john_doe`
   - Email: `john@example.com`
   - Password: `password123`
   - Click "Sign Up"

2. **Login** 
   - Go to "Login" tab
   - Email: `john@example.com`
   - Password: `password123`
   - Click "Login"

3. **Verify Email**
   - Look for verification code in the UI (6 digits)
   - Example: `123456`
   - Enter the code
   - Click "Verify"

4. **Create Support Case**
   - Select "New Support Case" tab
   - Language: `English`
   - Manufacturer: `Tech Solutions Inc.`
   - Issue: `Need help with product setup`
   - Click "Submit Support Request"

5. **Track Your Case**
   - Go to "My Cases" tab
   - See your case with status and task number
   - Expand to view details

---

## 📱 What You'll See

### Login Screen
- Clean, professional interface
- Tabs for Login and Sign Up
- Email verification flow

### Dashboard
- Welcome message with your username
- Three main tabs:
  - 📝 New Support Case
  - 📋 My Cases
  - ℹ️ Info

### Case Creation
- Language selection (7 languages)
- Manufacturer selection (3 options)
- Issue description field
- Real-time workflow feedback

### My Cases
- List of all your cases
- Status indicators with emojis
- Expandable details view
- Task numbers for tracking

---

## 🎯 Key Features to Test

✅ **User Management**
- Signup validation
- Login authentication
- Email verification
- Session persistence

✅ **Case Management**
- Create cases
- Track status
- View history
- Multi-language support

✅ **Automation**
- Auto-translation
- Task number generation
- Email notifications (mock)
- Status updates

---

## 🔧 Development Mode Features

The app runs in **development mode** by default:

- ✅ **Mock Database** - Data stored in memory (persists across sessions)
- ✅ **Mock Emails** - Verification codes shown in UI
- ✅ **Mock Translation** - Simulated translation service
- ✅ **Mock Manufacturer API** - Simulated API calls
- ✅ **No External Dependencies** - Works out of the box

**All user flows work exactly as they would in production!**

---

## 📊 Test Multiple Users

Open multiple browser tabs to test different users:

**Tab 1**: User john@example.com
**Tab 2**: User jane@example.com
**Tab 3**: User admin@example.com

Each user has independent sessions and can:
- Create their own accounts
- Login independently
- Create separate cases
- View only their own cases

---

## 🎨 UI Features

### Color-Coded Status
- 🟡 **Awaiting Reply** - Waiting for manufacturer
- 🟢 **Reply Received** - Manufacturer responded
- 🟠 **Pending Approval** - Awaiting manual approval
- ✅ **Approved** - Sent to user
- 🔔 **Reminder Sent** - Follow-up sent

### Interactive Elements
- Expandable case details
- Form validation
- Real-time feedback
- Loading spinners
- Success messages

### Responsive Design
- Works on desktop
- Sidebar navigation
- Tabbed interface
- Clean layout

---

## 🧪 Quick Tests

### Test 1: Signup Flow
```
1. Click "Sign Up"
2. Fill form
3. Click "Sign Up"
4. ✅ Should see "Account created successfully!"
```

### Test 2: Login Flow
```
1. Click "Login"
2. Enter credentials
3. Click "Login"
4. Enter verification code
5. ✅ Should redirect to dashboard
```

### Test 3: Case Creation
```
1. Go to "New Support Case"
2. Select language and manufacturer
3. Enter issue description
4. Click "Submit"
5. ✅ Should see task number and confirmation
```

### Test 4: View Cases
```
1. Go to "My Cases"
2. ✅ Should see list of your cases
3. Click to expand
4. ✅ Should see full details
```

---

## 💡 Tips

### Development
- Verification codes are displayed in UI
- Check terminal for email "sending" logs
- Database persists while app is running
- Restart app to reset database

### Testing
- Use different email addresses for each test user
- Username must be unique
- Password must be 8+ characters
- All validations work in real-time

### Troubleshooting
- **Port in use**: Stop other Streamlit apps
- **Module not found**: Run `pip install streamlit`
- **Code not working**: Check it matches the displayed code
- **Cases not showing**: Refresh the page

---

## 📚 Learn More

- Full documentation: See [README.md](README.md)
- Production setup: See [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)
- Project review: See [PROJECT_REVIEW.md](PROJECT_REVIEW.md)
- Run tests: `python test_user_flow.py`

---

## 🆘 Need Help?

### Common Issues

**Q: Can't see my cases**  
A: Refresh the page or check "My Cases" tab

**Q: Verification code not working**  
A: Make sure to copy the exact 6-digit code shown

**Q: Want to reset data**  
A: Restart the Streamlit app

**Q: Multiple users not working**  
A: Each user needs a unique email address

### Still Stuck?

1. Check the terminal for error messages
2. Review the code comments
3. Run the test suite: `python test_user_flow.py`
4. Check [PROJECT_REVIEW.md](PROJECT_REVIEW.md)

---

## 🎉 You're Ready!

The app is fully functional in development mode. When ready for production:

1. Copy `.env.example` to `.env`
2. Configure Supabase, email, etc.
3. Set `ENVIRONMENT=production`
4. Deploy using guides in [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)

**Happy Testing! 🚀**
