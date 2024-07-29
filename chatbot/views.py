from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

#from langchain import PromptTemplate,HuggingFaceHub,LLMChain
import os


# Create your views here.

def chatbot(request):
    print('heeeeereee')
    if request.method == 'POST':
        message = request.POST.get('message')
        response = 'hi'#generate_response(message, llm_chain)
        print(response)
        
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message,
        'response': response})
    return render(request, 'chatbot.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, login)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
