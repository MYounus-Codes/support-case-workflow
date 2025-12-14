# Email Setup Guide

## Gmail SMTP Configuration

To enable real email sending in the application, you need to configure Gmail SMTP with an App Password.

### Step-by-Step Guide

#### 1. Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** in the left sidebar
3. Scroll down to **How you sign in to Google**
4. Click on **2-Step Verification** and follow the setup process

#### 2. Generate App Password

1. Once 2-Step Verification is enabled, go back to: https://myaccount.google.com/security
2. Scroll down to **How you sign in to Google**
3. Click on **App passwords**
4. You may need to sign in again
5. In the "Select app" dropdown, choose **Mail**
6. In the "Select device" dropdown, choose **Other (Custom name)**
7. Enter a name like "Support Case Workflow"
8. Click **Generate**
9. Google will display a 16-character password
10. **Copy this password** (you won't be able to see it again)

#### 3. Update .env File

Edit your `.env` file and update these settings:

```env
# Enable real email sending
USE_MOCK_EMAIL=false

# Your Gmail address
SENDER_EMAIL=your-email@gmail.com

# The 16-character app password (without spaces)
SENDER_PASSWORD=abcdabcdabcdabcd
```

#### 4. Restart the Application

After updating the `.env` file, restart your Streamlit application:

```bash
streamlit run app.py
```

### Testing Email Delivery

1. Sign up with a new account or log in with an existing one
2. Check your email inbox for the verification code
3. If you don't receive it, check your spam folder
4. Verify that case notifications are also sent to your email

### Troubleshooting

#### Email not sending?

1. **Check App Password**: Make sure you copied it correctly without spaces
2. **SMTP Settings**: Verify `SMTP_SERVER=smtp.gmail.com` and `SMTP_PORT=587`
3. **2-Step Verification**: Ensure it's enabled on your Google Account
4. **Less Secure Apps**: App passwords only work when 2-Step Verification is enabled
5. **Firewall**: Check if port 587 is blocked by your firewall

#### Common Errors

- **"Authentication failed"**: Your app password is incorrect
- **"Connection refused"**: Port 587 might be blocked
- **"No such user"**: Verify your `SENDER_EMAIL` is correct

### Alternative Email Services

If you prefer not to use Gmail, you can use other SMTP services:

#### SendGrid
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SENDER_EMAIL=apikey
SENDER_PASSWORD=your-sendgrid-api-key
```

#### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your-email@outlook.com
SENDER_PASSWORD=your-password
```

#### Custom SMTP Server
Update these values in `.env` with your SMTP provider's details:
```env
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
SENDER_EMAIL=your-email@domain.com
SENDER_PASSWORD=your-password
```

### Security Best Practices

1. **Never commit `.env` file**: It's already in `.gitignore`
2. **Use App Passwords**: Never use your actual Gmail password
3. **Rotate passwords**: Periodically regenerate app passwords
4. **Monitor usage**: Check Google Account activity for suspicious email sending
5. **Rate limiting**: Be aware of Gmail's sending limits (500 emails per day for regular accounts)

### Development vs Production

- **Development**: You can set `USE_MOCK_EMAIL=true` to print codes to console instead of sending emails
- **Production**: Always set `USE_MOCK_EMAIL=false` and configure proper SMTP credentials

The application is now configured to work seamlessly in both environments.
