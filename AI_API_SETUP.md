# 🤖 AI API Setup Guide

Your chatbot now supports multiple high-quality AI services! Here's how to set them up for the best possible responses.

## 🚀 Available AI Services

### 1. **Claude 3.5 Sonnet** (Recommended - Best Quality)
- **Provider**: Anthropic
- **Quality**: ⭐⭐⭐⭐⭐ Excellent conversational AI
- **Cost**: ~$3 per 1M input tokens, $15 per 1M output tokens
- **Setup**: Get API key from [console.anthropic.com](https://console.anthropic.com)

### 2. **GPT-4 Turbo** (High Quality)
- **Provider**: OpenAI
- **Quality**: ⭐⭐⭐⭐⭐ Excellent reasoning and creativity
- **Cost**: ~$10 per 1M input tokens, $30 per 1M output tokens
- **Setup**: Get API key from [platform.openai.com](https://platform.openai.com)

### 3. **Gemini Pro** (Good Quality, Free Tier)
- **Provider**: Google
- **Quality**: ⭐⭐⭐⭐ Very good performance
- **Cost**: Free tier available, then $0.50 per 1M tokens
- **Setup**: Get API key from [makersuite.google.com](https://makersuite.google.com)

### 4. **Google Custom Search** (Real-Time Information)
- **Provider**: Google
- **Quality**: ⭐⭐⭐⭐⭐ Perfect for current information
- **Cost**: 100 free searches per day, then $5 per 1000 queries
- **Setup**: Already configured with your API key `AIzaSyBdsiaIjIM2yDYH6YeyQPLmfuw84VL73Fs`

### 5. **Dialogflow** (Conversational AI)
- **Provider**: Google Cloud
- **Quality**: ⭐⭐⭐ Good for specific intents
- **Cost**: Free tier, then pay-per-use
- **Setup**: Already configured with your JSON file

## 🔧 Setup Instructions

### Step 1: Get API Keys

#### For Claude 3.5 Sonnet (Recommended):
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

#### For GPT-4:
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy the key (starts with `sk-`)

#### For Gemini Pro:
1. Go to [makersuite.google.com](https://makersuite.google.com)
2. Sign up or log in
3. Click "Get API Key"
4. Create a new API key
5. Copy the key

### Step 2: Configure Environment Variables

Create a `.env` file in your project root:

```bash
# AI API Keys
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-gemini-key-here

# Existing keys
DJANGO_SECRET_KEY=your-django-secret-key
DEBUG=True
```

### Step 3: Test Your Setup

Run the test script to verify all APIs work:

```bash
python test_ai_apis.py
```

## 🎯 AI Service Priority

The chatbot uses this smart priority order:

1. **Claude 3.5 Sonnet** - Best for natural conversation
2. **GPT-4 Turbo** - Best for complex reasoning
3. **Gemini Pro** - Good balance of quality and cost
4. **Dialogflow** - Good for specific intents
5. **Google Search + AI** - For current information and real-time data
6. **Enhanced Simple Responses** - Always works as fallback

### 🔍 **Smart Search Detection**

The chatbot automatically detects when you need current information and will:
- Search Google for real-time data
- Combine search results with AI analysis
- Provide comprehensive, up-to-date answers
- Fall back gracefully if search fails

## 💡 Recommendations

### For Best Quality:
- Set up **Claude 3.5 Sonnet** (highest quality responses)
- Add **GPT-4** as backup (excellent reasoning)

### For Cost-Effective:
- Use **Gemini Pro** (free tier available)
- Add **Claude 3.5 Sonnet** for premium quality

### For Development/Testing:
- Start with **Gemini Pro** (free tier)
- Add others as needed

## 🔍 Testing Your Setup

The chatbot will automatically:
- Try each API in priority order
- Fall back to the next service if one fails
- Use enhanced simple responses as final fallback
- Log which service was used in the console

## 📊 Expected Response Quality

With multiple APIs configured, you'll get:
- **More intelligent responses** - Complex reasoning and analysis
- **Better conversation flow** - Natural, engaging dialogue
- **Creative solutions** - Innovative problem-solving
- **Detailed explanations** - Comprehensive, helpful answers
- **Context awareness** - Better understanding of user intent

## 🚨 Troubleshooting

### Common Issues:

1. **"API key not found"** - Check your `.env` file
2. **"Rate limit exceeded"** - Wait a moment and try again
3. **"Insufficient credits"** - Add credits to your API account
4. **"Service unavailable"** - The service will automatically fall back to the next option

### Debug Mode:
Check the console output to see which AI service is being used:
- `✅ Using Claude 3.5 Sonnet response`
- `✅ Using GPT-4 response`
- `✅ Using Gemini Pro response`
- `✅ Using enhanced simple response system`

## 🎉 You're All Set!

Once configured, your chatbot will provide Google-level AI responses with intelligent fallback to ensure it always works perfectly!

