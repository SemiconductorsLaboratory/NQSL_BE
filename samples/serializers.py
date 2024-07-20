from rest_framework import serializers
from .models import SampleModel


class SampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['id', 'name', 'description', 'user', 'date_created']
        read_only_fields = ['id', 'date_created']
