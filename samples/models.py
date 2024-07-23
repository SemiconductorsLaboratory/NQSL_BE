from django.contrib.auth.models import User
from django.db import models
from users.models import UserAccount


class UserMachineModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Substrate(models.Model):
    id = models.AutoField(primary_key=True)
    Company = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class SampleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(UserMachineModel, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    substrate = models.ForeignKey(Substrate, on_delete=models.CASCADE, blank=True, null=True)
    prev_sample = models.ForeignKey('SampleModel', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sample = models.ForeignKey(SampleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.sample.name}"

class SEMModel(models.Model):
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('SampleModel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='SEM_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    magnification = models.BigIntegerField(blank=True, null=True)
    voltage = models.FloatField(blank=True, null=True)
    current = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'SEM'
        verbose_name_plural = 'SEMs'

    def __str__(self):
        return f'SEMModel {self.id}'


class SEMModelFile(models.Model):
    my_model = models.ForeignKey(SEMModel, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='SEM_File/')


class Element(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    atomic_number = models.IntegerField()


class Layer(models.Model):
    name = models.CharField(max_length=100)
    thickness = models.FloatField()
    substrate = models.ForeignKey(Substrate, on_delete=models.CASCADE, blank=True, null=True)
    doped = models.ForeignKey(Element, on_delete=models.CASCADE, blank=True, null=True)
    doped_percentage = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class LayerComposition(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.layer.name} - {self.element.name}: {self.percentage}%"