from django.contrib import admin
from .models import SampleModel, Favorite, UserMachineModel


admin.site.register(SampleModel)
admin.site.register(Favorite)
admin.site.register(UserMachineModel)
