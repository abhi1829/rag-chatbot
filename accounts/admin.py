from django.contrib import admin
from accounts.models import User, UploadedFile

admin.site.register(User)
admin.site.register(UploadedFile)
# Register your models here.
