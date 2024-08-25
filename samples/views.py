from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from .models import SampleModel, SEMModel, Favorite, UserMachineModel, Substrate, AFMModel, Layer, LayerComposition, \
    Element, File
from rest_framework import generics, status, viewsets
from .serializers import SampleModelSerializer, FavoriteSerializer, SampleNameSerializer, UserModelSerializer, \
    AFMModelSerializer, SEMModelSerializer, ElementSerializer, UserMachineModelSerializer, LayerCompositionSerializer, \
    SubstrateModelSerializer, LayerSerializer, LayerThicknessSerializer, FileSerializer
from django.shortcuts import get_object_or_404

date_format = '%Y-%m-%d, %H:%M'


def addlayer(data):
    thickness = data['layer_thickness']
    layer_comp = data['layer_comp']
    datalayer = {
        'name': data['name'],
        'doped': data['doped'],
        'doped_percentage': data['doped_percentage']
    }
    layer_serializer = LayerSerializer(data=datalayer)
    if layer_serializer.is_valid():
        layer_serializer.save()
    else:
        return 'error', layer_serializer.errors
    thickness_data = {
        'thickness': float(thickness),
        'Layers': layer_serializer.data['id']
    }
    layerthickness_serializer = LayerThicknessSerializer(data=thickness_data)
    if layerthickness_serializer.is_valid():
        layerthickness_serializer.save()
    else:

        return 'error', layer_serializer.errors

    for layer in layer_comp:
        datacomp = {
            'layer': layer_serializer.data['id'],
            'element': int(layer['element']),
            'percentage': str(layer['percentage'])
        }
        layercomp_serializer = LayerCompositionSerializer(data=datacomp)
        if layercomp_serializer.is_valid():
            layercomp_serializer.save()
        else:
            return 'error', layerthickness_serializer.errors

    return 'validate', layerthickness_serializer.data['id']


class AddLayerSubstrateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        substrate_id = data['substrate_id']
        substrate = Substrate.objects.get(id=substrate_id)
        data.pop('substrate_id')
        status_layer, data_layer = addlayer(data)
        if status_layer == 'error':
            return Response(data_layer, status=status.HTTP_400_BAD_REQUEST)
        else:
            substrate.Layers.add(data_layer)
            substrate.save()
            return Response({'response': 'ok'}, status=status.HTTP_200_OK)


class SampleModelViewSet(viewsets.ModelViewSet):
    queryset = SampleModel.objects.all()
    serializer_class = SampleModelSerializer


class SampleInitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        sample_data = request.data.get("sample")
        if sample_data['prev_sample'] != "":
            sample_serializer = SampleModelSerializer(data=sample_data)
            if sample_serializer.is_valid():
                sample_serializer.save()
                return Response(sample_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        substrate_data = request.data.get("substrate")
        layer_id = []
        for layer in substrate_data['layers']:
            status_layer, data_layer = addlayer(layer)
            if status_layer == 'error':
                return Response(data_layer, status=status.HTTP_400_BAD_REQUEST)
            else:
                layer_id.append(data_layer)
        substrate_data.pop('layers')
        substrate_data['Layers'] = layer_id
        substrate_serializer = SubstrateModelSerializer(data=substrate_data)
        if not substrate_serializer.is_valid():
            return Response(substrate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sample_serializer = SampleModelSerializer(data=sample_data)
        if sample_serializer.is_valid():
            substrate_serializer.save()
        else:
            return Response(sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        sample_data['substrate'] = substrate_serializer.data['id']
        sample_serializer = SampleModelSerializer(data=sample_data)
        if sample_serializer.is_valid():
            sample_serializer.save()

        return Response([sample_serializer.data, substrate_serializer.data], status=status.HTTP_200_OK)


class SubstrateViewSet(viewsets.ModelViewSet):
    queryset = Substrate.objects.all()
    serializer_class = SubstrateModelSerializer


class UserMachineViewSet(viewsets.ModelViewSet):
    queryset = UserMachineModel.objects.all()
    serializer_class = UserMachineModelSerializer


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
            'user': sample.user_machine.name,
            'description': sample.description
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SampleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        sample = get_object_or_404(SampleModel, name=kwargs.get('name'))
        sample_id = sample.id
        Models = [SEMModel, AFMModel]

        sample_name_list = [sample.name]

        while sample.prev_sample is not None:
            sample_name_list.append(sample.prev_sample.name)
            sample = get_object_or_404(SampleModel, name=sample.prev_sample.name)

        sample_name_list.reverse()
        sample = get_object_or_404(SampleModel, name=sample_name_list[0])
        if sample.substrate is not None:
            substrate = {
                'sample_name': sample.name,
                'id': sample.substrate.id,
                'layer': Layer.objects.filter(layerthickness__substrate__samplemodel=sample).values_list('name',
                                                                                                         flat=True),
                'created_at': sample.date_created.strftime(date_format),
            }
        else:
            substrate = ''

        experiment_list = []
        for sample_name in sample_name_list:
            sample = get_object_or_404(SampleModel, name=sample_name)
            experiment_list0 = []
            for model in Models:
                all_experiments = model.objects.filter(sample=sample)
                for experiment in all_experiments:
                    dict_experiment = {
                        'id': experiment.id,
                        'model': experiment.name,
                        'methode': experiment.method,
                        'created_at': experiment.created_at.strftime(date_format)

                    }
                    experiment_list0.append(dict_experiment)
            experiment_list0 = sorted(experiment_list0, key=lambda x: x['created_at'])
            experiment_list.append(experiment_list0)

        samples = SampleModel.objects.filter(prev_sample__name=sample_name_list[-1])
        next_sample_list = list(samples.values_list('name', flat=True))

        response_data = {
            'sample_id': sample_id,
            'sample_list': sample_name_list,
            'substrate': substrate,
            'experiment_list': experiment_list,
            'next_sample_list': next_sample_list
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


class SubstrateView(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        sample = get_object_or_404(SampleModel, name=kwargs.get('name'))
        substrate = Substrate.objects.get(id=sample.substrate_id)
        data = {
            'id': substrate.id,
            'Company': substrate.Company,
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


class AFMModelViewSet(viewsets.ModelViewSet):
    queryset = AFMModel.objects.all()
    serializer_class = AFMModelSerializer


class SEMModelViewSet(viewsets.ModelViewSet):
    queryset = SEMModel.objects.all()
    serializer_class = SEMModelSerializer


class AFMModelCreateView(generics.CreateAPIView):
    queryset = AFMModel.objects.all()
    serializer_class = AFMModelSerializer


# Update an existing AFMModel instance
class AFMModelUpdateView(generics.RetrieveUpdateAPIView):
    queryset = AFMModel.objects.all()
    serializer_class = AFMModelSerializer
    lookup_field = 'id'


class SEMModelCreateView(generics.CreateAPIView):
    queryset = SEMModel.objects.all()
    serializer_class = SEMModelSerializer


# Update an existing AFMModel instance
class SEMModelUpdateView(generics.RetrieveUpdateAPIView):
    queryset = SEMModel.objects.all()
    serializer_class = SEMModelSerializer
    lookup_field = 'id'


class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


class LayerCompositionViewSet(viewsets.ModelViewSet):
    queryset = LayerComposition.objects.all()
    serializer_class = LayerCompositionSerializer


class UserMachineMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            user_machine = UserMachineModel.objects.get(user=user)
            serializer = UserMachineModelSerializer(user_machine)
            return Response(serializer.data)
        except UserMachineModel.DoesNotExist:
            return Response({"name": ""}, status=200)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class MethodList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        method_list = ['sem', 'afm']

        return Response(method_list, status=200)
