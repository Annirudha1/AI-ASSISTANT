# Configuration Example for Dialogflow Integration
# Copy this to your settings.py or create a .env file

# ===========================================
# DIALOGFLOW API CONFIGURATION
# ===========================================

# Method 1: Environment Variables (Recommended)
# Create a .env file in your project root with:
"""
DIALOGFLOW_PROJECT_ID=your-dialogflow-project-id
DIALOGFLOW_CREDENTIALS_PATH=path/to/your/service-account-key.json
"""

# Method 2: Direct in settings.py
# Add these lines to chatbot_project/settings.py:
DIALOGFLOW_PROJECT_ID = "your-dialogflow-project-id-here"
DIALOGFLOW_CREDENTIALS_PATH = "path/to/your/service-account-key.json"

# ===========================================
# HOW TO GET YOUR DIALOGFLOW CREDENTIALS
# ===========================================

# Step 1: Go to Google Cloud Console
# https://console.cloud.google.com/

# Step 2: Create or select a project

# Step 3: Enable Dialogflow API
# - Go to "APIs & Services" > "Library"
# - Search for "Dialogflow API"
# - Click "Enable"

# Step 4: Create Service Account
# - Go to "IAM & Admin" > "Service Accounts"
# - Click "Create Service Account"
# - Name: "dialogflow-bot"
# - Role: "Dialogflow API Client"
# - Create Key > JSON
# - Download the JSON file

# Step 5: Set up Dialogflow Agent
# - Go to https://dialogflow.cloud.google.com/
# - Create new agent or use existing
# - Create intents for customer support

# ===========================================
# EXAMPLE VALUES (Replace with your actual values)
# ===========================================

# Example project ID: "my-chatbot-project-123456"
# Example credentials path: "C:/path/to/service-account-key.json"

# ===========================================
# TESTING
# ===========================================

# After adding your credentials:
# 1. Restart Django server: python manage.py runserver
# 2. Go to http://localhost:8000/chat/
# 3. Ask questions that match your Dialogflow intents
# 4. Check Django logs for any errors

# Priority order:
# 1. Dialogflow (if configured) - Most intelligent
# 2. OpenAI GPT-3.5 (if API key provided) - Good fallback  
# 3. Simple responses (always works) - Basic fallback



