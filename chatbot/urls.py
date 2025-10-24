from django.urls import path
from .views import (
    RegisterView, LoginView, ChatAskView, ChatHistoryView,
    home_view, chat_view, history_view, register_view_web, 
    login_view_web, logout_view
)

app_name = 'chatbot'

urlpatterns = [
    # Template Views
    path('', home_view, name='home'),
    path('chat/', chat_view, name='chat'),
    path('history/', history_view, name='history'),
    path('register/', register_view_web, name='register'),
    path('login/', login_view_web, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # API Endpoints
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/chat/ask/', ChatAskView.as_view(), name='api_chat_ask'),
    path('api/chat/history/', ChatHistoryView.as_view(), name='api_chat_history'),
]
