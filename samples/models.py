from django.contrib.auth.models import User
from django.db import models
from users.models import UserAccount


class UserMachineModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    firstName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.firstName or ''} {self.lastName or ''}".strip()


class Element(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    Symbol = models.CharField(max_length=255, blank=True, null=True)
    atomic_number = models.IntegerField()

    def __str__(self):
        return self.Symbol


class Layer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    doped = models.ForeignKey(Element, on_delete=models.CASCADE, blank=True, null=True)
    doped_percentage = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class LayerComposition(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.layer.name} - {self.element.name}: {self.percentage}%"


class LayerThickness(models.Model):
    id = models.AutoField(primary_key=True)
    # TODO mask
    Layers = models.ForeignKey(Layer, on_delete=models.CASCADE)
    thickness = models.FloatField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.Layers.name+' - '+str(self.thickness)


class Substrate(models.Model):
    id = models.AutoField(primary_key=True)
    Company = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Layers = models.ManyToManyField(LayerThickness, blank=True, null=True)


class SampleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    user_machine = models.ForeignKey(UserMachineModel, on_delete=models.CASCADE)
    date_created = models.DateTimeField(blank=True, null=True)
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


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='file/')
    created_at = models.DateTimeField(auto_now_add=True)


class SEMModel(models.Model):
    STATUS_CHOICES = [
        ('SEM', 'SEM'),
        ('HRSEM', 'HRSEM'),
    ]

    id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=255, choices=STATUS_CHOICES, default='SEM')
    sample = models.ForeignKey('SampleModel', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    image = models.ImageField(upload_to='SEM_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    magnification = models.BigIntegerField(blank=True, null=True)
    voltage = models.FloatField(blank=True, null=True)
    current = models.FloatField(blank=True, null=True)
    file = models.ManyToManyField(File, blank=True)

    @property
    def name(self):
        return 'sem'

    class Meta:
        verbose_name = 'SEM'
        verbose_name_plural = 'SEMs'

    def __str__(self):
        return f'SEMModel {self.id}'


class AFMModel(models.Model):
    STATUS_CHOICES = [
        ('AFM', 'AFM'),
        ('KPAFM', 'KPAFM'),
    ]
    id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=255, choices=STATUS_CHOICES, default='AFM')
    sample = models.ForeignKey('SampleModel', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    image = models.ImageField(upload_to='AFM_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.ManyToManyField(File, blank=True)

    @property
    def name(self):
        return 'afm'

    class Meta:
        verbose_name = 'afm'
        verbose_name_plural = 'afms'

    def __str__(self):
        return f'AFMModel {self.id}'

