from django.urls import path, re_path
from .views import (
    SampleModelCreateAPIView,
    SampleDetailView,
    SampleDeleteView,
    SampleListView,
    FavoriteListView,
    FavoriteCreateView,
    FavoriteDeleteView,
    SampleDescriptionView,
    UserListView, SEMModelView, AFMModelView, UserMachineListView,
)

urlpatterns = [
    path('', SampleListView.as_view(), name='_detail'),
    path('user/', UserListView.as_view(), name='_detail'),
    path('add/', SampleModelCreateAPIView.as_view(), name='samplemodel-create'),
    path('remove/', SampleDeleteView.as_view(), name='samplemodel-create'),
    path('description/<str:name>/', SampleDescriptionView.as_view(), name='sample_description'),
    path('detail/<str:name>/', SampleDetailView.as_view(), name='sample_detail'),
    path('sem/<int:id>/', SEMModelView.as_view(), name='sem_detail'),
    path('afm/<int:id>/', AFMModelView.as_view(), name='afm_detail'),
    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/remove/', FavoriteDeleteView.as_view(), name='favorite-remove'),
    path('user-machines/', UserMachineListView.as_view(), name='user_machine_list'),
]
