from django.contrib import admin
from .models import LogAccessApacheModel, LastPositionInFileModel
# Register your models here.

admin.site.register(LastPositionInFileModel)
admin.site.register(LogAccessApacheModel)
