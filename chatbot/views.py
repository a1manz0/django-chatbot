from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

from langchain import HuggingFaceHub
from dotenv import load_dotenv
import os


load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
llm=HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
                   huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
                   model_kwargs={"max_new_tokens":1200})
#print(llm("Tell me one joke about data scientist"))

def generate_response(message):
    return llm(message)


# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print(message)
        response = generate_response(message)
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
            auth.login(request, user)
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
