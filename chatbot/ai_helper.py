import os
import json
from django.conf import settings

def get_ai_response(question):
    """
    Get AI response using multiple high-quality AI services with Google search integration:
    Priority: Claude 3.5 Sonnet > GPT-4 > Gemini Pro > Dialogflow > Google Search + Simple responses
    """
    print(f"🤖 Processing question: {question[:50]}...")
    
    # Check if this is a search-type question that needs real-time information
    search_keywords = [
        'prime minister', 'president', 'current', 'latest', 'news', 'today', 'recent',
        'weather', 'stock', 'price', 'rate', 'score', 'result', 'update',
        '2024', '2025', 'now', 'live', 'happening', 'breaking', 'india', 'usa', 'world'
    ]
    
    needs_search = any(keyword in question.lower() for keyword in search_keywords)
    
    # Try Claude 3.5 Sonnet first (best conversational AI)
    claude_response = try_claude_response(question)
    if claude_response:
        print("✅ Using Claude 3.5 Sonnet response")
        return claude_response
    
    # Try GPT-4 second
    gpt4_response = try_gpt4_response(question)
    if gpt4_response:
        print("✅ Using GPT-4 response")
        return gpt4_response
    
    # Try Gemini Pro third
    gemini_response = try_gemini_response(question)
    if gemini_response:
        print("✅ Using Gemini Pro response")
        return gemini_response
    
    # Try Dialogflow fourth
    dialogflow_response = try_dialogflow_response(question)
    if dialogflow_response:
        print("✅ Using Dialogflow response")
        return dialogflow_response
    
    # Try Google Search + AI enhancement for search-type questions
    if needs_search:
        print("🔍 Detected search-type question, trying Google search...")
        search_enhanced_response = try_google_search_enhanced(question)
        if search_enhanced_response:
            print("✅ Using Google Search + AI enhanced response")
            return search_enhanced_response
    
    # Final fallback to enhanced simple responses
    print("✅ Using enhanced simple response system")
    return get_enhanced_simple_response(question)

def try_google_search_enhanced(question):
    """Get Google search results and enhance with AI"""
    try:
        search_results = get_google_search_results(question)
        if not search_results:
            return None
            
        # Format search results for AI processing
        search_context = format_search_results(search_results)
        
        # Try to get AI response with search context
        enhanced_response = get_ai_response_with_context(question, search_context)
        if enhanced_response:
            return enhanced_response
            
        # Fallback to formatted search results
        return format_search_response(question, search_results)
        
    except Exception as e:
        print(f"Google Search enhanced error: {e}")
        return None

def get_google_search_results(query, num_results=5):
    """Get Google Custom Search results"""
    try:
        from googleapiclient.discovery import build
        
        api_key = os.getenv('GOOGLE_SEARCH_API_KEY') or getattr(settings, 'GOOGLE_SEARCH_API_KEY', None)
        search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID') or getattr(settings, 'GOOGLE_SEARCH_ENGINE_ID', None)
        
        if not api_key:
            print("Google Search API key not found")
            return None
            
        # Use default search engine if no custom one provided
        if not search_engine_id:
            search_engine_id = "017576662512468239146:omuauf_lfve"
        
        print(f"Using search engine ID: {search_engine_id}")
        
        service = build("customsearch", "v1", developerKey=api_key)
        
        result = service.cse().list(
            q=query,
            cx=search_engine_id,
            num=num_results,
            safe="medium"
        ).execute()
        
        items = result.get('items', [])
        print(f"Found {len(items)} search results")
        return items
        
    except Exception as e:
        print(f"Google Search API error: {e}")
        return None

def format_search_results(search_results):
    """Format search results for AI context"""
    if not search_results:
        return ""
    
    formatted = "Recent search results:\n"
    for i, item in enumerate(search_results[:3], 1):
        title = item.get('title', 'No title')
        snippet = item.get('snippet', 'No description')
        link = item.get('link', '')
        
        formatted += f"{i}. {title}\n"
        formatted += f"   {snippet}\n"
        formatted += f"   Source: {link}\n\n"
    
    return formatted

def get_ai_response_with_context(question, search_context):
    """Get AI response using search context"""
    try:
        # Try Claude first with search context
        claude_response = try_claude_with_context(question, search_context)
        if claude_response:
            return claude_response
            
        # Try GPT-4 with search context
        gpt4_response = try_gpt4_with_context(question, search_context)
        if gpt4_response:
            return gpt4_response
            
        # Try Gemini with search context
        gemini_response = try_gemini_with_context(question, search_context)
        if gemini_response:
            return gemini_response
            
    except Exception as e:
        print(f"AI with context error: {e}")
    
    return None

def try_claude_with_context(question, search_context):
    """Try Claude with search context"""
    try:
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY') or getattr(settings, 'ANTHROPIC_API_KEY', None)
        if not anthropic_api_key:
            return None
            
        import anthropic
        
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": f"""Based on the latest search results, please provide a comprehensive answer to: {question}

{search_context}

Please provide a detailed, accurate response using the search results. If the search results don't contain enough information, please mention that and provide what information is available."""
                }
            ]
        )
        
        return response.content[0].text.strip()
        
    except Exception as e:
        print(f"Claude with context error: {e}")
        return None

def try_gpt4_with_context(question, search_context):
    """Try GPT-4 with search context"""
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)
        if not openai_api_key:
            return None
            
        import openai
        
        client = openai.OpenAI(api_key=openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that provides accurate, up-to-date information based on search results. Always cite sources when possible."
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nSearch Results:\n{search_context}\n\nPlease provide a comprehensive answer based on the search results."
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"GPT-4 with context error: {e}")
        return None

def try_gemini_with_context(question, search_context):
    """Try Gemini with search context"""
    try:
        google_api_key = os.getenv('GOOGLE_API_KEY') or getattr(settings, 'GOOGLE_API_KEY', None)
        if not google_api_key:
            return None
            
        import google.generativeai as genai
        
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(
            f"Question: {question}\n\nSearch Results:\n{search_context}\n\nPlease provide a comprehensive answer based on the search results."
        )
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini with context error: {e}")
        return None

def format_search_response(question, search_results):
    """Format search results as a response"""
    if not search_results:
        return "I couldn't find recent information about that topic. Let me help you with what I know instead."
    
    response = f"🔍 **Search Results for: {question}**\n\n"
    
    for i, item in enumerate(search_results[:3], 1):
        title = item.get('title', 'No title')
        snippet = item.get('snippet', 'No description')
        link = item.get('link', '')
        
        response += f"**{i}. {title}**\n"
        response += f"{snippet}\n"
        response += f"🔗 [Read more]({link})\n\n"
    
    response += "💡 *These are the most recent and relevant results I found. For the most up-to-date information, please check the linked sources.*"
    
    return response

def try_claude_response(question):
    """Try to get response from Anthropic Claude 3.5 Sonnet"""
    try:
        anthropic_api_key = os.getenv('ANTHROPIC_API_KEY') or getattr(settings, 'ANTHROPIC_API_KEY', None)
        if not anthropic_api_key:
            return None
            
        import anthropic
        
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a helpful, friendly, and intelligent AI assistant. You excel at:
- Having natural, engaging conversations
- Providing detailed, accurate information
- Being empathetic and understanding
- Offering creative solutions
- Explaining complex topics simply

Please respond to this user question in a conversational, helpful way: {question}"""
                }
            ]
        )
        
        return response.content[0].text.strip()
        
    except Exception as e:
        print(f"Claude API error: {e}")
        return None

def try_gpt4_response(question):
    """Try to get response from OpenAI GPT-4"""
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)
        if not openai_api_key:
            return None
            
        import openai
        
        client = openai.OpenAI(api_key=openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": """You are a highly intelligent and helpful AI assistant. You excel at:
- Providing accurate, detailed information
- Having engaging conversations
- Solving complex problems
- Being creative and insightful
- Explaining things clearly

Be conversational, friendly, and helpful in your responses."""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"GPT-4 API error: {e}")
        return None

def try_gemini_response(question):
    """Try to get response from Google Gemini Pro"""
    try:
        google_api_key = os.getenv('GOOGLE_API_KEY') or getattr(settings, 'GOOGLE_API_KEY', None)
        if not google_api_key:
            return None
            
        import google.generativeai as genai
        
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(
            f"""You are a helpful, intelligent AI assistant. You excel at:
- Having natural conversations
- Providing accurate information
- Being creative and insightful
- Solving problems effectively

Please respond to this user question in a helpful, conversational way: {question}"""
        )
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None

def try_dialogflow_response(question):
    """Try to get response from Google Dialogflow"""
    try:
        dialogflow_project_id = os.getenv('DIALOGFLOW_PROJECT_ID') or getattr(settings, 'DIALOGFLOW_PROJECT_ID', None)
        dialogflow_credentials_path = os.getenv('DIALOGFLOW_CREDENTIALS_PATH') or getattr(settings, 'DIALOGFLOW_CREDENTIALS_PATH', None)
        
        if not dialogflow_project_id or not dialogflow_credentials_path:
            return None
            
        if not os.path.exists(dialogflow_credentials_path):
            return None
            
        from google.cloud import dialogflow
        import uuid
        
        # Set up credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dialogflow_credentials_path
        
        # Create session client
        session_client = dialogflow.SessionsClient()
        
        # Use a consistent session ID for better conversation flow
        session_id = "chatbot-session-001"
        session = session_client.session_path(dialogflow_project_id, session_id)
        
        # Create text input
        text_input = dialogflow.TextInput(text=question, language_code="en-US")
        query_input = dialogflow.QueryInput(text=text_input)
        
        # Detect intent
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        # Get the response
        query_result = response.query_result
        
        # Return the fulfillment text if available
        if query_result.fulfillment_text:
            return query_result.fulfillment_text
        else:
            # If no fulfillment text, try to provide a helpful response
            if query_result.intent.display_name:
                return f"I understand you're asking about {query_result.intent.display_name}. How can I help you with that?"
            else:
                return "I'm here to help! Could you please tell me more about what you need assistance with?"
            
    except Exception as e:
        print(f"Dialogflow error: {e}")
        return None

def get_enhanced_simple_response(question):
    """
    Enhanced conversational responses with much better intelligence
    """
    question_lower = question.lower()
    
    # Common knowledge questions - provide accurate answers
    if 'capital' in question_lower and 'france' in question_lower:
        return """🇫🇷 **Capital of France**

The capital of France is **Paris**.

**Key Information:**
• **City**: Paris
• **Population**: ~2.1 million (city), ~12 million (metro area)
• **Language**: French
• **Famous For**: Eiffel Tower, Louvre Museum, Notre-Dame, Champs-Élysées
• **Nickname**: "City of Light" (La Ville Lumière)

Paris is not only the capital but also the largest city and cultural center of France. It's known worldwide for its art, fashion, cuisine, and architecture.

*This is basic geographical knowledge that doesn't change frequently.*"""
    
    elif 'capital' in question_lower and 'india' in question_lower:
        return """🇮🇳 **Capital of India**

The capital of India is **New Delhi**.

**Key Information:**
• **City**: New Delhi
• **State**: Delhi (National Capital Territory)
• **Population**: ~32 million (metro area)
• **Language**: Hindi, English
• **Famous For**: Red Fort, India Gate, Qutub Minar, Lotus Temple
• **Government**: Houses Parliament, Supreme Court, and major ministries

New Delhi serves as the political and administrative center of India, while Mumbai is the financial capital.

*This is basic geographical knowledge that doesn't change frequently.*"""
    
    elif 'capital' in question_lower and 'usa' in question_lower:
        return """🇺🇸 **Capital of USA**

The capital of the United States is **Washington, D.C.**

**Key Information:**
• **City**: Washington, D.C. (District of Columbia)
• **Population**: ~700,000 (city), ~6.3 million (metro area)
• **Language**: English
• **Famous For**: White House, Capitol Building, Lincoln Memorial, Washington Monument
• **Government**: Houses all three branches of federal government

Washington, D.C. is the political center of the United States, while New York is the financial capital.

*This is basic geographical knowledge that doesn't change frequently.*"""
    
    elif 'capital' in question_lower and 'china' in question_lower:
        return """🇨🇳 **Capital of China**

The capital of China is **Beijing**.

**Key Information:**
• **City**: Beijing
• **Population**: ~21.5 million (metro area)
• **Language**: Mandarin Chinese
• **Famous For**: Forbidden City, Great Wall, Tiananmen Square, Temple of Heaven
• **Government**: Houses the central government and Communist Party headquarters

Beijing is the political, cultural, and educational center of China, while Shanghai is the financial capital.

*This is basic geographical knowledge that doesn't change frequently.*"""
    
    # More common knowledge questions
    elif 'largest' in question_lower and ('country' in question_lower or 'nation' in question_lower):
        return """🌍 **Largest Country in the World**

**Russia** is the largest country in the world by land area.

**Key Information:**
• **Country**: Russia (Russian Federation)
• **Area**: ~17.1 million km² (6.6 million sq mi)
• **Population**: ~146 million
• **Capital**: Moscow
• **Spans**: 11 time zones across Europe and Asia
• **Borders**: 14 countries

Russia covers more than 1/8th of the Earth's inhabited land area and spans two continents.

*This is basic geographical knowledge that doesn't change frequently.*"""
    
    elif 'population' in question_lower and ('india' in question_lower or 'china' in question_lower):
        if 'india' in question_lower:
            return """🇮🇳 **Population of India**

India has approximately **1.4 billion people** (as of 2024).

**Key Information:**
• **Population**: ~1.4 billion (1,400,000,000)
• **Rank**: 2nd most populous country in the world
• **Growth Rate**: ~0.7% annually
• **Density**: ~464 people per km²
• **Largest Cities**: Mumbai, Delhi, Bangalore, Kolkata, Chennai

India is expected to become the world's most populous country by 2027, surpassing China.

*Population figures are estimates and change over time.*"""
        else:
            return """🇨🇳 **Population of China**

China has approximately **1.4 billion people** (as of 2024).

**Key Information:**
• **Population**: ~1.4 billion (1,400,000,000)
• **Rank**: 1st most populous country in the world
• **Growth Rate**: ~0.1% annually (slowing)
• **Density**: ~153 people per km²
• **Largest Cities**: Shanghai, Beijing, Chongqing, Tianjin, Guangzhou

China has the world's largest population, though India is expected to surpass it soon.

*Population figures are estimates and change over time.*"""
    
    elif 'ocean' in question_lower and 'largest' in question_lower:
        return """🌊 **Largest Ocean in the World**

The **Pacific Ocean** is the largest ocean in the world.

**Key Information:**
• **Ocean**: Pacific Ocean
• **Area**: ~165.2 million km² (63.8 million sq mi)
• **Covers**: ~46% of Earth's water surface
• **Depth**: Average 4,280 meters (14,040 feet)
• **Deepest Point**: Mariana Trench (11,034 meters)

The Pacific Ocean is larger than all land masses combined and contains more than half of Earth's free water.

*This is basic geographical knowledge that doesn't change frequently.*"""
    
    # Current information questions - provide specific answers
    elif 'prime minister' in question_lower and 'india' in question_lower:
        return """🇮🇳 **Prime Minister of India**

As of 2024, **Narendra Modi** is the Prime Minister of India. He has been serving as the 14th Prime Minister since May 26, 2014, and was re-elected for a second term in 2019.

**Key Information:**
• **Name**: Narendra Damodardas Modi
• **Party**: Bharatiya Janata Party (BJP)
• **Term**: 2014-present (2nd term)
• **Previous Role**: Chief Minister of Gujarat (2001-2014)

For the most current and detailed information, I recommend checking official government websites or recent news sources. 📰

*Note: Political information can change, so always verify with current sources.*"""
    
    elif 'president' in question_lower and ('usa' in question_lower or 'america' in question_lower):
        return """🇺🇸 **President of the United States**

As of 2024, **Joe Biden** is the President of the United States. He has been serving as the 46th President since January 20, 2021.

**Key Information:**
• **Name**: Joseph Robinette Biden Jr.
• **Party**: Democratic Party
• **Term**: 2021-present
• **Previous Role**: Vice President (2009-2017), U.S. Senator (1973-2009)

For the most current and detailed information, I recommend checking official government websites or recent news sources. 📰

*Note: Political information can change, so always verify with current sources.*"""
    
    elif any(word in question_lower for word in ['current', 'latest', 'now', 'today']):
        return """🔍 **Current Information Search**

I can help you find the most current information! For real-time data like:
- Current Prime Minister of India
- Latest news and updates
- Today's weather
- Stock prices
- Recent events

I'll search the web for the most up-to-date information. Let me know what specific current information you need! 📰"""
    
    # Greetings and introductions
    elif any(word in question_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        responses = [
            "Hello there! 👋 I'm your AI assistant with Google search capabilities, and I'm excited to help you today! What can I do for you?",
            "Hi! Great to meet you! I can help with any questions, search for current information, or just chat. What's on your mind?",
            "Hey! I'm ready and eager to assist you with both AI responses and real-time search. How can I make your day better?",
            "Good to see you! I'm your intelligent assistant with web search, ready to help with anything you need. What would you like to know?"
        ]
        import random
        return random.choice(responses)
    
    # How are you / feeling questions
    elif any(word in question_lower for word in ['how are you', 'how do you feel', 'are you okay', 'how\'s it going', 'how are you doing']):
        responses = [
            "I'm doing absolutely fantastic, thank you for asking! I'm energized and ready to help you with both AI responses and real-time search. How are you doing today?",
            "I'm wonderful! I love helping people like you and I'm always excited to learn, assist, and search for current information. What can I help you with?",
            "I'm excellent! I'm here 24/7 and always ready to chat, help, provide information, and search the web. How can I make your day better?",
            "I'm doing great! I'm constantly learning and improving, and I'm thrilled to be able to help you with both AI and search capabilities. What do you need assistance with?"
        ]
        import random
        return random.choice(responses)
    
    # Help and capabilities
    elif any(word in question_lower for word in ['what can you do', 'help', 'capabilities', 'what do you do', 'how can you help', 'what are your skills']):
        return """I'm your advanced AI assistant with Google-level intelligence! Here's what I excel at:

🧠 **Intelligent Assistance:**
• Answer complex questions with detailed explanations
• Help with problem-solving and critical thinking
• Provide creative solutions and ideas
• Explain difficult concepts in simple terms
• Offer insights and analysis

🔍 **Real-Time Information:**
• Current news and events
• Political leaders and government updates
• Latest weather, stocks, and prices
• Recent discoveries and breakthroughs
• Up-to-date facts and data

💬 **Natural Conversation:**
• Engaging, intelligent dialogue
• Context-aware responses
• Adapt to your communication style
• Friendly and helpful personality
• Remember our conversation flow

🎯 **Knowledge Areas:**
• Science and technology
• History and culture
• Business and economics
• Creative writing and arts
• Learning and education
• Current events and news
• General knowledge and facts

🚀 **Advanced Capabilities:**
• Complex reasoning and analysis
• Creative problem-solving
• Multi-step task planning
• Research and fact-checking
• Code review and programming help
• Real-time information gathering
• Creative writing and storytelling

What would you like to explore or discuss? I'm here to help you discover and learn! 😊"""
    
    # Business and professional questions
    elif any(word in question_lower for word in ['business', 'work', 'career', 'professional', 'job', 'interview']):
        return """💼 **Professional & Business Help:**

I can assist you with various business and career topics:

**Career Development:**
• Resume and cover letter writing
• Interview preparation and tips
• Career planning and goal setting
• Professional networking strategies
• Skill development recommendations

**Business Operations:**
• Business planning and strategy
• Marketing and branding advice
• Financial planning and budgeting
• Team management and leadership
• Process optimization

**Professional Skills:**
• Communication and presentation
• Project management
• Problem-solving techniques
• Time management and productivity
• Industry-specific knowledge

**Current Business Information:**
• Latest industry news and trends
• Market updates and analysis
• Company information and updates
• Economic indicators and reports

What specific aspect of your professional life would you like help with? I'm here to provide detailed, actionable advice! 🚀"""
    
    # Technical questions
    elif any(word in question_lower for word in ['code', 'programming', 'technical', 'software', 'development', 'bug', 'error']):
        return """💻 **Technical Assistance:**

I can help you with a wide range of technical topics:

**Programming & Development:**
• Code review and optimization
• Debugging and troubleshooting
• Best practices and design patterns
• Framework and library recommendations
• Architecture and system design

**Software & Tools:**
• Software recommendations
• Configuration and setup help
• Performance optimization
• Security best practices
• Integration and automation

**Learning & Skills:**
• Programming language guidance
• Technology stack advice
• Learning path recommendations
• Project planning and management
• Industry trends and updates

**Current Tech Information:**
• Latest technology news
• Software updates and releases
• Security alerts and patches
• Industry developments

What technical challenge are you facing? I'd love to help you solve it! 🔧"""
    
    # Creative and writing
    elif any(word in question_lower for word in ['write', 'creative', 'story', 'content', 'blog', 'article', 'poem']):
        return """✍️ **Creative & Writing Help:**

I love helping with creative projects! Here's what I can do:

**Writing Assistance:**
• Creative writing and storytelling
• Blog posts and articles
• Marketing copy and content
• Technical documentation
• Poetry and creative expression

**Content Strategy:**
• Content planning and ideation
• Audience targeting and engagement
• SEO and optimization tips
• Social media content
• Brand voice development

**Creative Projects:**
• Brainstorming and ideation
• Character and plot development
• Creative problem-solving
• Design thinking
• Innovation and inspiration

**Current Creative Information:**
• Latest trends in writing and content
• Popular topics and themes
• Creative industry updates
• Inspiration and ideas

What kind of creative project are you working on? I'm excited to help bring your ideas to life! 🎨"""
    
    # Learning and education
    elif any(word in question_lower for word in ['learn', 'study', 'education', 'teach', 'explain', 'understand']):
        return """📚 **Learning & Education Support:**

I'm passionate about helping you learn and grow! Here's how I can assist:

**Learning Support:**
• Explain complex topics simply
• Create study guides and summaries
• Provide practice questions and examples
• Break down difficult concepts
• Offer multiple learning approaches

**Subject Areas:**
• Science and mathematics
• History and social studies
• Languages and literature
• Technology and programming
• Business and economics
• Arts and humanities

**Study Strategies:**
• Effective study techniques
• Memory and retention tips
• Time management for learning
• Note-taking strategies
• Test preparation methods

**Current Educational Information:**
• Latest educational resources
• Recent research and studies
• Educational technology updates
• Learning trends and methods

What would you like to learn about? I'll make it engaging and easy to understand! 🎓"""
    
    # Problem-solving
    elif any(word in question_lower for word in ['problem', 'issue', 'trouble', 'stuck', 'difficult', 'challenge']):
        return """🔧 **Problem-Solving Support:**

I love tackling challenges! Here's how I can help:

**Problem Analysis:**
• Break down complex problems
• Identify root causes and patterns
• Analyze different perspectives
• Consider multiple solutions
• Evaluate pros and cons

**Solution Strategies:**
• Creative problem-solving techniques
• Step-by-step action plans
• Resource identification
• Risk assessment and mitigation
• Implementation guidance

**Support Areas:**
• Technical troubleshooting
• Personal and professional challenges
• Decision-making processes
• Conflict resolution
• Process improvement

**Current Problem-Solving Resources:**
• Latest tools and techniques
• Industry best practices
• Case studies and examples
• Expert insights and advice

What problem are you facing? Let's work through it together and find the best solution! 💡"""
    
    # Thank you
    elif any(word in question_lower for word in ['thank you', 'thanks', 'appreciate', 'grateful', 'awesome']):
        responses = [
            "You're very welcome! I'm thrilled I could help you. Is there anything else you'd like to explore or discuss? 😊",
            "My absolute pleasure! I love helping people like you. What else can I assist you with today? 🌟",
            "You're so welcome! That's exactly what I'm here for. Feel free to ask me anything else! ✨",
            "Anytime! I'm always excited to help. What other questions or topics would you like to dive into? 🤗"
        ]
        import random
        return random.choice(responses)
    
    # Goodbye
    elif any(word in question_lower for word in ['bye', 'goodbye', 'see you later', 'farewell', 'have a good day']):
        responses = [
            "Goodbye! It was wonderful chatting with you. Feel free to come back anytime - I'm always here to help! 👋",
            "See you later! I'm always here when you need assistance. Take care and have an amazing day! 😊",
            "Farewell! Thanks for the great conversation. Come back soon - I love helping you! 🌟",
            "Have a fantastic day! I'll be here whenever you need help or just want to chat! ✨"
        ]
        import random
        return random.choice(responses)
    
    # Default intelligent response
    else:
        responses = [
            "That's a fascinating question! I'd love to help you explore this topic in detail. Could you tell me more about what specific aspect you're most interested in?",
            "I'm excited to help with that! This sounds like something I can definitely assist you with. What additional context would help me give you the best possible answer?",
            "Great question! I'm always thrilled to help people like you. Can you provide more details about what you'd like to know or achieve?",
            "I'm listening and ready to help! That's exactly the kind of interesting challenge I enjoy tackling. What specific information would be most valuable for you?",
            "Absolutely! I love helping with questions like this. What additional details would help me provide you with the most comprehensive and useful response?",
            "Perfect! I'm here to help with exactly this kind of inquiry. What specific aspects would you like me to focus on or explain in detail?",
            "I'm all ears and excited to help! That's the kind of question I really enjoy working through. What additional context would help me give you the best answer?",
            "Excellent question! I'm here to help you get exactly what you need. What specific information or outcome are you looking for?"
        ]
        import random
        return random.choice(responses)