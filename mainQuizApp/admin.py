from django.contrib import admin
from .models import UploadedFile, Tests

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(Tests)
