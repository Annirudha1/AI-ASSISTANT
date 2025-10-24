# Dialogflow API Integration Guide

## 🔧 How to Add Your Dialogflow API Key

### Step 1: Install Dialogflow Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Dialogflow Credentials

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create or select a project**
3. **Enable Dialogflow API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Dialogflow API"
   - Click "Enable"

4. **Create Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "dialogflow-bot")
   - Grant "Dialogflow API Client" role
   - Click "Create Key" > "JSON"
   - Download the JSON file

### Step 3: Add Your Credentials

**Option A: Environment Variables (Recommended)**
Create a `.env` file in your project root:
```env
DIALOGFLOW_PROJECT_ID=your-project-id-here
DIALOGFLOW_CREDENTIALS_PATH=path/to/your/service-account-key.json
```

**Option B: Direct in Settings**
Add to `chatbot_project/settings.py`:
```python
DIALOGFLOW_PROJECT_ID = "your-project-id-here"
DIALOGFLOW_CREDENTIALS_PATH = "path/to/your/service-account-key.json"
```

### Step 4: Set Up Dialogflow Agent

1. **Go to Dialogflow Console**: https://dialogflow.cloud.google.com/
2. **Create a new agent** or use existing one
3. **Create intents** for common customer support questions:
   - "Business Hours"
   - "Password Reset"
   - "Return Policy"
   - "Shipping Information"
   - "Contact Support"

### Step 5: Test Integration

1. **Start your Django server**:
   ```bash
   python manage.py runserver
   ```

2. **Test in browser**: Go to http://localhost:8000/chat/
3. **Ask questions** that match your Dialogflow intents

## 🎯 API Priority Order

Your chatbot now uses this priority:
1. **Dialogflow** (if configured) - Most intelligent
2. **OpenAI GPT-3.5** (if API key provided) - Good fallback
3. **Simple responses** (always works) - Basic fallback

## 🔍 Troubleshooting

### Common Issues:
- **"Dialogflow API error"**: Check your project ID and credentials path
- **"Permission denied"**: Ensure service account has Dialogflow API Client role
- **"No intents found"**: Create intents in Dialogflow console

### Debug Mode:
Check Django logs for error messages when testing.

## 📁 File Structure
```
chatbot/
├── ai_helper.py          # Updated with Dialogflow integration
├── settings.py           # Added Dialogflow config
└── requirements.txt      # Added google-cloud-dialogflow
```

## 🚀 Ready to Use!

Once configured, your chatbot will automatically use Dialogflow for intelligent responses!



