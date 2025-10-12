from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),  
]
