from django.contrib import admin
from .models import Tags, AssetType, Asset, Extension

# Register your models here.
admin.site.register(Tags)
admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(Extension)