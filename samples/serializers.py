from rest_framework import serializers
from .models import SampleModel, Favorite


class SampleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['name']


class SampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['id', 'name', 'description', 'user', 'date_created']
        read_only_fields = ['id']

class FavoriteSerializer(serializers.ModelSerializer):
    sample_name = serializers.CharField(source='sample.name', read_only=True)

    class Meta:
        model = Favorite
        fields = ['sample_name']