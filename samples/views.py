from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SampleModel, SEMModel, Favorite, UserMachineModel, Substrate, AFMModel, Layer, LayerComposition
from rest_framework import generics, status
from .serializers import SampleModelSerializer, FavoriteSerializer, SampleNameSerializer, UserModelSerializer
import json
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

date_format = '%Y-%m-%d, %H:%M'


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


class UserListView(generics.ListAPIView):
    queryset = UserMachineModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]


class SampleDescriptionView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        sample = get_object_or_404(SampleModel, name=kwargs.get('name'))

        layer_names = Layer.objects.filter(layerthickness__substrate__samplemodel=sample).values_list('name', flat=True)
        prev_sample = ''
        if sample.prev_sample is not None:
            prev_sample = sample.prev_sample.name
        response_data = {
            'substrate': layer_names,
            'date': sample.date_created.strftime(date_format),
            'user': sample.user.name,
            'prev_sample': prev_sample,
            'description': sample.description
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SampleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        sample = get_object_or_404(SampleModel, name=kwargs.get('name'))

        layer_names = Layer.objects.filter(layerthickness__substrate__samplemodel=sample).values_list('name', flat=True)
        sem_models = SEMModel.objects.filter(sample=sample).values('created_at', 'description', 'method', 'id')
        afm_models = AFMModel.objects.filter(sample=sample).values('created_at', 'description', 'method', 'id')
        for sem in sem_models:
            created_at = sem['created_at']
            sem['created_at'] = created_at.strftime(date_format)
        for afm in afm_models:
            created_at = afm['created_at']
            afm['created_at'] = created_at.strftime(date_format)

        response_data = {
            'substrate': {
                'layer': layer_names,
                'created_at': sample.date_created.strftime(date_format)
            },
            'sem': list(sem_models),
            'afm': list(afm_models)
        }

        return Response(response_data, status=status.HTTP_200_OK)


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


class SEMModelView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        sem_model = get_object_or_404(SEMModel, id=kwargs.get('id'))
        files = [file.file.url for file in sem_model.file.all()]
        sem_data = {
            'id': sem_model.id,
            'method': sem_model.method,
            'sample': sem_model.sample.id,
            'created_at': sem_model.created_at.strftime(date_format),
            'image': sem_model.image.url if sem_model.image else None,
            'description': sem_model.description,
            'magnification': sem_model.magnification,
            'voltage': sem_model.voltage,
            'current': sem_model.current,
            'files': files
        }
        return Response(sem_data)


class AFMModelView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        afm_model = get_object_or_404(AFMModel, id=kwargs.get('id'))
        files = [file.file.url for file in afm_model.file.all()]
        afm_data = {
            'id': afm_model.id,
            'method': afm_model.method,
            'sample': afm_model.sample.id,
            'created_at': afm_model.created_at.strftime(date_format),
            'image': afm_model.image.url if afm_model.image else None,
            'description': afm_model.description,
            'files': files
        }
        return Response(afm_data)


class UserMachineListView(APIView):

    def get(self, request, *args, **kwargs):
        user_machines = UserMachineModel.objects.all().values('id', 'name', 'firstName', 'lastName', 'user_id')
        user_machines_list = list(user_machines)
        return Response(user_machines_list)


class SubstrateView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        sample = get_object_or_404(SampleModel, name=kwargs.get('name'))
        substrate = Substrate.objects.get(id=sample.substrate_id)
        data = {
        'id': substrate.id,
        'Company' : substrate.Company,
        'date': substrate.date_created,
        }
        layers = []
        for layer in substrate.Layers.all():
            layer_data = {
                'id_layer_thickness': layer.id,
                'layer_thickness': layer.thickness,
                'order': layer.order,
                'id_layer': layer.Layers.id,
                'name': layer.Layers.name,
                'doped': layer.Layers.doped,
                'doped_percentage': layer.Layers.doped_percentage
            }
            layer_comp = []
            for comp in LayerComposition.objects.filter(layer=layer.Layers):
                dict_comp = {
                    'id': comp.layer_id,
                    'element': comp.element.Symbol,
                    'percentage': comp.percentage
                }
                layer_comp.append(dict_comp)
            layer_data['layer_comp'] = layer_comp
            layers.append(layer_data)
        data['layers'] = layers
        return Response(data)
