from django.urls import path, re_path
from .views import (
    sample_view,
    SampleModelCreateAPIView,
    Sample_detail,
    SampleModelDestroyAPIView
)

urlpatterns = [
    path('', sample_view),
    path('add/', SampleModelCreateAPIView.as_view(), name='samplemodel-create'),
    path('remove/', SampleModelDestroyAPIView.as_view(), name='samplemodel-create'),
    path('<str:sample_name>/', Sample_detail, name='element_detail'),
]
