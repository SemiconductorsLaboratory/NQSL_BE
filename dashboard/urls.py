# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'meeting', views.MeetingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('meetings/', views.meeting_list, name='meeting_list'),
    path('meetings/create/', views.meeting_create, name='meeting_create'),
    path('meetings/update/<int:pk>/', views.meeting_update, name='meeting_update'),
]
