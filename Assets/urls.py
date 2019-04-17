from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.home, name='home'),
    path('icons/', views.icons, name='icons'),
    path('illustrations/', views.illustrations, name='illustrations'),
    path('uploadfiles/', views.uploadFile, name='uploadFile'),
    path('testing/', views.test, name='test'),
    path('getTags/<string>/', views.getTags, name='getTags'),
    path('getAssets/<taglist>', views.getAssets, name='getAssets'),
    path('getAssets/', views.getAssets, name='getAllAssets'),
    path('deleteAsset/', views.deleteAsset, name='deleteAsset'),
    path('bulkadd/', views.bulkadd)
]