# Gmail Stock Email Sender

A desktop application for sending stock update emails to customers using multiple Gmail accounts with automatic rotation to avoid sending limits.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- Send bulk emails (500-1000+ customers) using multiple Gmail accounts
- Automatic account rotation to stay within Gmail limits (450/day per account)
- Upload customers via CSV or Excel files (.csv, .xlsx, .xls)
- Customer selection and filtering capabilities
- Filter invalid emails and failed deliveries (2+ failures)
- Send stock files as attachments
- Track sent/failed status per customer
- Export customer emails
- Daily email counter at top of application
- Professional HTML email templates with bold formatting

## Requirements

- Windows 7/10/11 (64-bit)
- Python 3.8+ (if running from source)
- Gmail accounts with App Passwords

## Installation

### Option 1: Standalone Executable (Recommended)

1. Download `GmailStockSender_Package.zip` from [Releases](../../releases)
2. Extract the ZIP file
3. Double-click `install.bat`
4. Click "Yes" for administrator permission
5. Find "Gmail Stock Sender" on your desktop

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/gmail-stock-sender.git
cd gmail-stock-sender

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Gmail Setup

1. Go to https://myaccount.google.com/
2. Enable **2-Step Verification**
3. Go to **Security > App Passwords**
4. Generate new password for "Mail"
5. Copy the 16-character password
6. Use this password in the app (NOT your regular Gmail password)

## Usage

### Step 1: Add Gmail Accounts
- Go to **"Gmail Accounts"** tab
- Enter Gmail address and App Password
- Add multiple accounts for rotation

### Step 2: Add Customers
- Go to **"Customers"** tab
- Upload CSV/Excel file: `store_code, email, mobile_number`
- Or add manually

### Step 3: Add Stock Data
- Go to **"Stock Data"** tab
- Upload stock file (CSV, Excel, or TXT)

### Step 4: Send Emails
- Go to **"Send Emails"** tab
- Select stock file as attachment
- Configure batch size and delays
- Click **"Send Emails"**

## Customer File Format

**CSV Format:**
```csv
store_code,email,mobile_number
ST001,customer1@example.com,9876543210
ST002,customer2@example.com,9876543211
```

**Excel Format:**

| store_code | email | mobile_number |
|------------|-------|---------------|
| ST001 | customer1@example.com | 9876543210 |
| ST002 | customer2@example.com | 9876543211 |

**Note:** Only `email` is required. `store_code` and `mobile_number` are optional.

## Email Template

The application sends a professional HTML email with:
- "Dear Sir," greeting
- "Kindly find attached Stock details and send your Orders."
- "Many new and short items included in the list and marked."
- Stock file attachment
- Call-to-action button

## Gmail Limits

| Account Type | Daily Limit |
|--------------|-------------|
| Free Gmail | 500 emails/day |
| Google Workspace | 2,000 emails/day |

**App Setting:** 450 emails/day per account (safe margin)

## Project Structure

```
gmail-stock-sender/
├── main.py              # Main GUI application
├── database.py          # SQLite database operations
├── gmail_service.py     # Gmail SMTP service
├── templates.py         # HTML email templates
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── install.bat          # Windows installer
├── create_package.bat   # Package creator
├── build_exe.bat        # Build executable
├── README.md            # Documentation
├── LICENSE              # MIT License
└── .gitignore           # Git ignore file
```

## Troubleshooting

### Authentication Failed
- Make sure you're using **App Password**, not regular password
- Verify 2-Step Verification is enabled

### Emails Not Sending
- Check Gmail daily limit (max 500/day)
- Wait if accounts hit limit
- Check internet connection

### Invalid Emails
- Use **"Select Invalid Emails"** button to find bad addresses
- Delete invalid emails before sending

### Excel Upload Error
- The standalone executable includes openpyxl
- If running from source: `pip install openpyxl`

## Building from Source

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "GmailStockSender" --collect-all openpyxl main.py

# Create distribution package
.\create_package.bat
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created for bulk email sending with Gmail account rotation.

## Support

For issues and feature requests, please create an [Issue](../../issues).
