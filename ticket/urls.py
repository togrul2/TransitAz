from django.urls import path
from . import views

urlpatterns = [
    path('bus/<int:pk>', views.getBus, name='bus'),
]
