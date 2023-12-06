from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms as django_forms  # Use an alias to avoid naming conflicts
from .models import User, UploadedFile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include password1 and password2

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class FileUploadForm(django_forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file_type', 'file']
        exclude = ['user','file_name','file_size']
