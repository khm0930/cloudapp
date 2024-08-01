

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages



def home(request):
    return render(request, 'cloudapp/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signup successful! You are now logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try again.')
    else:
        form = UserCreationForm()
    
    return render(request, 'cloudapp/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'cloudapp/login.html', {'form': form})




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
