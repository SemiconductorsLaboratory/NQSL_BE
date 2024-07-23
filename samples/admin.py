from django.contrib import admin
from .models import SampleModel, Favorite


admin.site.register(SampleModel)
admin.site.register(Favorite)