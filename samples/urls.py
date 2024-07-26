from django.urls import path, re_path
from .views import (
    SampleModelCreateAPIView,
    SampleDetailView,
    SampleDeleteView,
    SampleListView,
    FavoriteListView,
    FavoriteCreateView,
    FavoriteDeleteView,
    SampleModelRetrieveByNameAPIView,
    UserListView
)

urlpatterns = [
    path('', SampleListView.as_view(), name='_detail'),
    path('user/', UserListView.as_view(), name='_detail'),
    path('add/', SampleModelCreateAPIView.as_view(), name='samplemodel-create'),
    path('remove/', SampleDeleteView.as_view(), name='samplemodel-create'),
    path('description/<str:name>/', SampleModelRetrieveByNameAPIView.as_view(), name='sample_description'),
    path('detail/<str:name>/', SampleDetailView.as_view(), name='sample_detail'),
    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/remove/', FavoriteDeleteView.as_view(), name='favorite-remove'),
]
