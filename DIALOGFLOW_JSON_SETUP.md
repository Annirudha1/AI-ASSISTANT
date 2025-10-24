# 🤖 Dialogflow AI Agent Setup Guide

## 📁 **Where to Add Your Dialogflow JSON File**

### **Step 1: Get Your Dialogflow JSON Credentials**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select your project** (or create a new one)
3. **Enable Dialogflow API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Dialogflow API"
   - Click "Enable"

4. **Create Service Account**:
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Name: `dialogflow-agent`
   - Description: `AI Agent for chatbot`
   - Click "Create and Continue"
   - Role: `Dialogflow API Client`
   - Click "Continue" → "Done"

5. **Download JSON Key**:
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Download the file

### **Step 2: Add JSON to Your Project**

1. **Place the JSON file** in the `credentials` folder:
   ```
   chatbot/
   ├── credentials/
   │   └── dialogflow-service-account.json  ← Your JSON file goes here
   ├── chatbot/
   ├── chatbot_project/
   └── manage.py
   ```

2. **Update settings.py** with your project details:
   ```python
   # In chatbot_project/settings.py
   DIALOGFLOW_PROJECT_ID = "your-actual-project-id"  # Replace this
   DIALOGFLOW_CREDENTIALS_PATH = "credentials/dialogflow-service-account.json"
   ```

### **Step 3: Set Up Dialogflow Agent**

1. **Go to Dialogflow Console**: https://dialogflow.cloud.google.com/
2. **Create a new agent**:
   - Agent name: `AI Chatbot Agent`
   - Default language: `English`
   - Google Project: Select your project
   - Click "Create"

3. **Create Intents** for conversations:
   - **Welcome Intent**: "Hello", "Hi", "Hey"
   - **Goodbye Intent**: "Bye", "Goodbye", "See you later"
   - **Help Intent**: "Help", "What can you do?", "How can you help?"
   - **Weather Intent**: "What's the weather?", "Is it raining?"
   - **Time Intent**: "What time is it?", "What's the current time?"

### **Step 4: Test Your AI Agent**

1. **Start the server**:
   ```bash
   python manage.py runserver
   ```

2. **Go to chat**: http://localhost:8000/chat/

3. **Test conversations**:
   - "Hello" → Should get welcome response
   - "What can you help me with?" → Should get help response
   - "What's the weather?" → Should get weather response

## 🔧 **Configuration Example**

Your `credentials` folder should look like this:
```
credentials/
└── dialogflow-service-account.json
```

Your `settings.py` should have:
```python
DIALOGFLOW_PROJECT_ID = "my-chatbot-project-123456"
DIALOGFLOW_CREDENTIALS_PATH = "credentials/dialogflow-service-account.json"
```

## 🎯 **What This Creates**

- **Conversational AI Agent** that can have natural conversations
- **Intent Recognition** based on your Dialogflow setup
- **Context Awareness** for better responses
- **Fallback System** if Dialogflow fails

## 🚀 **Ready to Chat!**

Once you add your JSON file and update the project ID, your AI agent will be ready for conversations!



