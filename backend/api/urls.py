from django.urls import path
from .views import health, upload_image

urlpatterns = [
    path('health/', health),
    path('upload-image/', upload_image),
]