

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User



def home(request):
    return render(request, 'cloudapp/home.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return redirect(f'/cloudapp/login/?email={email}')
        else:
            return redirect(f'/cloudapp/signup/details/?email={email}')
    return render(request, 'cloudapp/signup.html')

def signup_details(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        # 사용자 생성 로직 추가
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Authentication failed. Please try again.')
            return redirect('signup')

    return render(request, 'cloudapp/signup_details.html', {'email': email})


def login_view(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'cloudapp/login_details.html', {'email': email})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('file_list')
    else:
        form = DocumentForm()
    return render(request, 'cloudapp/upload.html', {'form': form})

@login_required
def file_list(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'cloudapp/file_list.html', {'documents': documents})

@login_required
def delete_file(request, id):
    document = get_object_or_404(Document, id=id, user=request.user)
    if request.method == 'POST':
        document.delete()
        return redirect('file_list')
    return render(request, 'cloudapp/delete_confirm.html', {'document': document})

def logout_view(request):
    logout(request)
    return redirect('home')
