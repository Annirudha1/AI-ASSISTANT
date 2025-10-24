from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .serializers import UserSerializer, ChatSerializer
from .models import Chat
from .ai_helper import get_ai_response

# Template Views
def home_view(request):
    """Home page view"""
    return render(request, 'chatbot/home.html')

@login_required
def chat_view(request):
    """Chat interface view"""
    return render(request, 'chatbot/chat.html')

@login_required
def history_view(request):
    """Chat history view"""
    chats = Chat.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'chatbot/history.html', {'chats': chats})

def register_view_web(request):
    """Web registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AI Support Bot.')
            return redirect('chatbot:home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    
    return render(request, 'chatbot/register.html', {'form': form})

def login_view_web(request):
    """Web login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('chatbot:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'chatbot/login.html')

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('chatbot:home')

# API Views (existing)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class ChatAskView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        question = request.data.get('question')
        
        if not question:
            return Response(
                {'error': 'Please provide a question'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get AI response
            ai_answer = get_ai_response(question)
            
            # Save to database
            chat = Chat.objects.create(
                user=request.user,
                question=question,
                answer=ai_answer
            )
            
            serializer = ChatSerializer(chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChatHistoryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)
