from django.urls import path, re_path
from .views import (
    SampleModelCreateAPIView,
    Sample_detail,
    SampleDeleteView,
    SampleListView,
    FavoriteListView,
    FavoriteCreateView,
    FavoriteDeleteView,
)

urlpatterns = [
    path('', SampleListView.as_view(), name='_detail'),
    path('add/', SampleModelCreateAPIView.as_view(), name='samplemodel-create'),
    path('remove/', SampleDeleteView.as_view(), name='samplemodel-create'),
    path('<str:sample_name>/', Sample_detail, name='element_detail'),
    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/remove/', FavoriteDeleteView.as_view(), name='favorite-remove'),
]
