#!/usr/bin/env python3
"""
Simple test script for the chatbot API
Run this after starting the Django server
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register/", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Django server is running.")
        return False

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    
    data = {
        "username": "testuser2",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login/", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            return token_data.get('access')
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Django server is running.")
        return None

def test_chat_ask(token):
    """Test asking a question to the chatbot"""
    print("\nTesting chat ask...")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": "What are your business hours?"}
    
    try:
        response = requests.post(f"{BASE_URL}/chat/ask/", json=data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Chat ask successful!")
            chat_data = response.json()
            print(f"Question: {chat_data['question']}")
            print(f"Answer: {chat_data['answer'][:100]}...")
            return True
        else:
            print(f"❌ Chat ask failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Django server is running.")
        return False

def test_chat_history(token):
    """Test getting chat history"""
    print("\nTesting chat history...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/chat/history/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Chat history successful!")
            history = response.json()
            print(f"Found {len(history)} chat entries")
            return True
        else:
            print(f"❌ Chat history failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Django server is running.")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print("Make sure the Django server is running on http://localhost:8000")
    print("=" * 50)
    
    # Test registration
    if not test_register():
        return
    
    # Test login
    token = test_login()
    if not token:
        return
    
    # Test chat ask
    if not test_chat_ask(token):
        return
    
    # Test chat history
    if not test_chat_history(token):
        return
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! The API is working correctly.")
    print("\nYou can now test with Postman using these endpoints:")
    print(f"- Register: POST {BASE_URL}/register/")
    print(f"- Login: POST {BASE_URL}/login/")
    print(f"- Chat Ask: POST {BASE_URL}/chat/ask/")
    print(f"- Chat History: GET {BASE_URL}/chat/history/")

if __name__ == "__main__":
    main()
