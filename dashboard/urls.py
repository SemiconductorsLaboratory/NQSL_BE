# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('meetings/', views.meeting_list, name='meeting_list'),
    path('meetings/create/', views.meeting_create, name='meeting_create'),
    path('meetings/update/<int:pk>/', views.meeting_update, name='meeting_update'),
]
