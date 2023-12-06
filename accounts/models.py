from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class User(AbstractUser):
    email = models.EmailField(unique=True)


def get_upload_path(instance, filename):
    # Get the file type, username, and construct the upload path
    file_type = instance.file_type
    username = instance.user.username
    return os.path.join('uploaded_files', username, file_type, filename)

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type_choices = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('txt', 'Text'),
    ]
    file_type = models.CharField(max_length=3, choices=file_type_choices)
    file_name = models.CharField(max_length=255, default='')
    file_size = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to=get_upload_path)