# Email Configuration Guide

This guide provides a step-by-step process to configure Gmail with the Email Segregation System.

## Step-by-Step Setup

### 1. Enable Two-Factor Authentication (2FA)
- Log in to your Gmail account.
- Navigate to [Google Account Security](https://myaccount.google.com/security).
- Under "Signing in to Google," click "2-Step Verification" and follow the instructions to enable it.

### 2. Create an App-Specific Password
- After enabling 2FA, go to the [Security](https://myaccount.google.com/security) section.
- Select "App passwords."
- Choose "Mail" as the app and "Windows Computer" as the device.
- Generate the password and store it securely.

### 3. Configure the `.env` File
- Copy the `.env.template` file to `.env`.
- Edit the `.env` file and input your email and the app-specific password:
  ```env
  EMAIL_USERNAME=your_email@gmail.com
  EMAIL_PASSWORD=your_app_password
  EMAIL_IMAP_SERVER=imap.gmail.com
  EMAIL_SMTP_SERVER=smtp.gmail.com:587
  ```

### 4. Verify IMAP/SMTP Settings
- Ensure IMAP is enabled in your Gmail settings:
  - Go to Gmail.
  - Click the gear icon, then "See all settings."
  - Go to the "Forwarding and POP/IMAP" tab.
  - Enable "IMAP access."

### 5. Run the Email Segregation System
- Test the configuration by running the main application:
  ```sh
  python main.py
  ```
- Use keywords in test emails to see classification results.

## Security Considerations

- **Protect Your `.env` File**: Ensure the `.env` file isn't committed to version control. Add it to `.gitignore`.
- **Rotate App Passwords**: Regularly update your app-specific passwords.

This setup secures Gmail integration, enabling the system to fetch and classify incoming emails efficiently.
