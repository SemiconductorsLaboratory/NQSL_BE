
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SampleModel, SEMModel, Favorite
from rest_framework import generics, status
from .serializers import SampleModelSerializer, FavoriteSerializer, SampleNameSerializer
import json
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class SampleModelCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SampleModel.objects.all()
    serializer_class = SampleModelSerializer


class SampleDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sample_name = request.data.get('name')
        if not sample_name:
            return Response({"error": "Sample name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sample = SampleModel.objects.get(name=sample_name)
            sample.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SampleModel.DoesNotExist:
            return Response({"error": "Sample not found."}, status=status.HTTP_404_NOT_FOUND)


class SampleListView(generics.ListAPIView):
    queryset = SampleModel.objects.all()
    serializer_class = SampleNameSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def Sample_detail(request, sample_name):
    print('sample_name')

    sem_models = SEMModel.objects.filter(sample__name=sample_name).values('created_at', 'description')
    data = SampleModel.objects.filter(name=sample_name).values('name',
                                                               'user__name',
                                                               'description',
                                                               'date_created')
    return Response([data, sem_models])


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('sample')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        sample_names = [entry['sample_name'] for entry in serializer.data]
        return Response(sample_names)


class FavoriteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('ok1')
        sample_name = request.data.get('sample_name')
        try:
            sample = SampleModel.objects.get(name=sample_name)
            favorite, created = Favorite.objects.get_or_create(user=request.user, sample=sample)
            if created:
                return Response({'status': 'added', 'sample_name': sample_name}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'exists', 'sample_name': sample_name}, status=status.HTTP_200_OK)
        except SampleModel.DoesNotExist:
            return Response({'status': 'not_found', 'sample_name': sample_name}, status=status.HTTP_404_NOT_FOUND)

class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sample_name = request.data.get('sample_name')
        try:
            sample = SampleModel.objects.get(name=sample_name)
            favorite = Favorite.objects.filter(user=request.user, sample=sample).first()
            if favorite:
                favorite.delete()
                return Response({'status': 'removed', 'sample_name': sample_name}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'not_found', 'sample_name': sample_name}, status=status.HTTP_404_NOT_FOUND)
        except SampleModel.DoesNotExist:
            return Response({'status': 'not_found', 'sample_name': sample_name}, status=status.HTTP_404_NOT_FOUND)
