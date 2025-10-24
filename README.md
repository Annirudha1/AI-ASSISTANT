# AI Customer Support Chatbot

A Django REST Framework project for an AI-powered customer support chatbot with JWT authentication.

## Features

- **User Authentication**: JWT-based registration and login
- **AI Chat**: Integration with OpenAI GPT-3.5-turbo or Hugging Face DialoGPT
- **Chat History**: Store and retrieve conversation history
- **RESTful API**: Clean API endpoints for frontend integration
- **Admin Panel**: Django admin interface for managing chats
- **CORS Support**: Ready for frontend integration

## Project Structure

```
chatbot_project/
├── chatbot_project/          # Main project settings
│   ├── settings.py          # Django settings with JWT and CORS config
│   └── urls.py              # Main URL configuration
├── chatbot/                  # Main app
│   ├── models.py            # Chat model
│   ├── serializers.py       # User and Chat serializers
│   ├── views.py             # API views
│   ├── urls.py              # App URL configuration
│   ├── admin.py             # Admin panel configuration
│   └── ai_helper.py         # AI integration logic
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `config.py` to `.env` (if needed)
   - Set your OpenAI API key (optional):
     ```bash
     export OPENAI_API_KEY="your_api_key_here"
     ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- **POST** `/api/register/` - User registration
  ```json
  {
    "username": "user123",
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

- **POST** `/api/login/` - User login
  ```json
  {
    "username": "user123",
    "password": "securepassword"
  }
  ```
  Returns JWT tokens for authentication.

### Chat

- **POST** `/api/chat/ask/` - Ask a question to the AI
  ```json
  {
    "question": "How can I reset my password?"
  }
  ```
  Requires JWT authentication header: `Authorization: Bearer <token>`

- **GET** `/api/chat/history/` - Get chat history
  Requires JWT authentication header: `Authorization: Bearer <token>`

## Testing with Postman

### 1. Register a User
- **Method**: POST
- **URL**: `http://localhost:8000/api/register/`
- **Body** (raw JSON):
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }
  ```

### 2. Login
- **Method**: POST
- **URL**: `http://localhost:8000/api/login/`
- **Body** (raw JSON):
  ```json
  {
    "username": "testuser",
    "password": "testpass123"
  }
  ```
- **Save the access token** from the response

### 3. Ask a Question
- **Method**: POST
- **URL**: `http://localhost:8000/api/chat/ask/`
- **Headers**: `Authorization: Bearer <your_access_token>`
- **Body** (raw JSON):
  ```json
  {
    "question": "What are your business hours?"
  }
  ```

### 4. Check Chat History
- **Method**: GET
- **URL**: `http://localhost:8000/api/chat/history/`
- **Headers**: `Authorization: Bearer <your_access_token>`

## AI Integration

The chatbot uses a fallback approach:

1. **Primary**: OpenAI GPT-3.5-turbo (if API key is provided)
2. **Fallback**: Hugging Face DialoGPT-medium (local model)

To use OpenAI:
1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Set the environment variable: `OPENAI_API_KEY=your_key_here`

## Admin Panel

Access the admin panel at `http://localhost:8000/admin/` to:
- View all chat conversations
- Filter chats by user and timestamp
- Search through questions and answers

## CORS Configuration

CORS is enabled for development. For production, update the settings in `chatbot_project/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Troubleshooting

### Common Issues

1. **NumPy compatibility warnings**: These are warnings and won't affect functionality
2. **JWT token expiration**: Tokens expire after 1 hour, refresh as needed
3. **AI model loading**: First request may take longer as models are downloaded

### Performance Tips

- For production, consider using Redis for token storage
- Implement rate limiting for chat endpoints
- Use environment variables for sensitive configuration

## Development

To add new features:

1. **New Models**: Add to `chatbot/models.py`
2. **New Endpoints**: Add to `chatbot/views.py` and `chatbot/urls.py`
3. **New Serializers**: Add to `chatbot/serializers.py`

## License

This project is open source and available under the MIT License.







