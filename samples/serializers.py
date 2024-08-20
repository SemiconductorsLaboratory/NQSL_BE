from rest_framework import serializers
from .models import (SampleModel,
                     Favorite,
                     UserMachineModel,
                     AFMModel,
                     SEMModel,
                     Element, LayerComposition, Substrate, Layer, LayerThickness, File
                     )


class SampleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['name']


class SampleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleModel
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMachineModel
        fields = ['id', 'name', 'firstName', 'lastName']
        read_only_fields = ['id']


class FavoriteSerializer(serializers.ModelSerializer):
    sample_name = serializers.CharField(source='sample.name', read_only=True)

    class Meta:
        model = Favorite
        fields = ['sample_name']


class AFMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AFMModel
        fields = '__all__'


class SEMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEMModel
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class UserMachineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMachineModel
        fields = '__all__'


class LayerCompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerComposition
        fields = '__all__'


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'


class LayerThicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerThickness
        fields = '__all__'


class SubstrateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substrate
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'