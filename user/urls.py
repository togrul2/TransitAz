from django.urls import path
from . import views

urlpatterns = [
    path('add_phone/', views.add_phone, name='add_phone'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('', views.my_profile, name='my_profile'),
]
