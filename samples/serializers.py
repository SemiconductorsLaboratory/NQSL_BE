from rest_framework import serializers
from .models import SampleModel, Favorite, UserMachineModel, AFMModel, SEMModel


class SampleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['name']


class SampleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SampleModel
        fields = ['id', 'name', 'description', 'user', 'date_created', 'substrate', 'prev_sample']
        read_only_fields = ['id']


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