from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SampleModelCreateAPIView,
    SampleDetailView,
    SampleDeleteView,
    SampleListView,
    FavoriteListView,
    FavoriteCreateView,
    FavoriteDeleteView,
    SampleDescriptionView,
    UserListView,
    SEMModelView,
    AFMModelView,
    UserMachineListView,
    SubstrateView,
    AFMModelCreateView,
    AFMModelUpdateView,
    SEMModelCreateView,
    SEMModelUpdateView,
    ElementViewSet,
)

router = DefaultRouter()
router.register(r'elements', ElementViewSet)

urlpatterns = [
    path('', SampleListView.as_view(), name='_detail'),
    path('user/', UserListView.as_view(), name='_detail'),
    path('add/', SampleModelCreateAPIView.as_view(), name='samplemodel-create'),
    path('remove/', SampleDeleteView.as_view(), name='samplemodel-create'),

    path('description/<str:name>/', SampleDescriptionView.as_view(), name='sample_description'),
    path('detail/<str:name>/', SampleDetailView.as_view(), name='sample_detail'),

    path('sem/<int:id>/', SEMModelView.as_view(), name='sem_detail'),
    path('sem/add/', SEMModelCreateView.as_view(), name='semmodel-add'),
    path('sem/<int:id>/edit/', SEMModelUpdateView.as_view(), name='semmodel-edit'),

    path('afm/<int:id>/', AFMModelView.as_view(), name='afm_detail'),
    path('afm/add/', AFMModelCreateView.as_view(), name='afmmodel-add'),
    path('afm/<int:id>/edit/', AFMModelUpdateView.as_view(), name='afmmodel-edit'),

    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/remove/', FavoriteDeleteView.as_view(), name='favorite-remove'),

    path('user-machines/', UserMachineListView.as_view(), name='user_machine_list'),


    path('substrate/<str:name>/', SubstrateView.as_view(), name='substrate'),
    path('', include(router.urls)),
]
