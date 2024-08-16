from rest_framework import serializers
from .models import SampleModel, Favorite, UserMachineModel, AFMModel, SEMModel


class SampleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ['name']


class SampleModelSerializer(serializers.ModelSerializer):
    prev_sample_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = SampleModel
        fields = '__all__'
        extra_kwargs = {
            'prev_sample': {'read_only': True},
        }

    def create(self, validated_data):
        # Get the previous sample name from the validated data
        prev_sample_name = validated_data.pop('prev_sample_name', None)

        if prev_sample_name:
            # Try to retrieve the SampleModel instance based on the name
            try:
                prev_sample = SampleModel.objects.get(name=prev_sample_name)
                validated_data['prev_sample'] = prev_sample
            except SampleModel.DoesNotExist:
                raise serializers.ValidationError(f"Previous sample with name '{prev_sample_name}' does not exist.")

        # Create and return the SampleModel instance
        return super().create(validated_data)

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