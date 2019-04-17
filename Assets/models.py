from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Tags(models.Model):
    tagName = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.tagName


class AssetType(models.Model):
    assetType = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.assetType


class Extension(models.Model):
    extName = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return self.extName


class Asset(models.Model):
    assetName = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    assetType = models.CharField(max_length=100)
    addedOn = models.DateTimeField(default=datetime.now())
    addedBy = models.CharField(max_length=100, default='User_0001')
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.assetName
