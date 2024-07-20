
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SampleModel, SEMModel
from rest_framework import generics, status
from .serializers import SampleModelSerializer
import json
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class SampleModelCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SampleModel.objects.all()
    serializer_class = SampleModelSerializer


class SampleModelDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SampleModel.objects.all()
    serializer_class = SampleModelSerializer


class SampleModelListView(APIView):
    def get(self, request):
        samples = SampleModel.objects.all()
        serializer = SampleModelSerializer(samples, many=True)
        names = [item['name'] for item in serializer.data]
        return Response(names, status=status.HTTP_200_OK)

@api_view(['GET'])
def sample_view(request):
    samples = SampleModel.objects.all().values('name')
    return Response(list(samples))


@api_view(['GET'])
def sem_model_list(request, sample_name):
    sem_models = SEMModel.objects.filter(sample__name=sample_name)
    return Response(sem_models)

@api_view(['GET'])
def Sample_detail(request, sample_name):

    sem_models = SEMModel.objects.filter(sample__name=sample_name).values('created_at', 'description')
    data = SampleModel.objects.filter(name=sample_name).values('name',
                                                               'user__name',
                                                               'description',
                                                               'date_created')
    return Response([data, sem_models])
