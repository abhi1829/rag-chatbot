from django.shortcuts import render, redirect
from .forms import SignupForm , FileUploadForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from django.http import HttpResponseBadRequest

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            logger.info('User registered and logged in successfully.')
            return redirect('/')
        else:
            logger.error('Error during registration. Form errors: %s', form.errors)
            messages.error(request, 'Error during registration. Please check your input.')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})




@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        print('file uploading...')
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            # Access file name and size from the uploaded file
            uploaded_file.file_name = request.FILES['file'].name
            uploaded_file.file_size = request.FILES['file'].size
            uploaded_file.save()
            print('saving file...')
            # create_embeddings(uploaded_file)
            return redirect('accounts:dashboard')  # Redirect to the dashboard page
        else:
            print(form.errors)
            return HttpResponseBadRequest("Form validation failed")
    else:
        form = FileUploadForm()

    return render(request, 'accounts/upload_file.html', {'form': form})



@login_required
def dashboard(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    print(user_files)
    return render(request, 'accounts/dashboard.html', {'user_files': user_files})
