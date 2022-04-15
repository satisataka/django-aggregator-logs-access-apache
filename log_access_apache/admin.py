from django.contrib import admin
from .models import LogAccessApacheModel, FileLogModel
# Register your models here.

admin.site.register(FileLogModel)
admin.site.register(LogAccessApacheModel)
