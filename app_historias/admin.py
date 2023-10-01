from django.contrib import admin
from .models import Registro_Historia,Registro_Paciente

# Register your models here.

admin.site.register(Registro_Paciente)
admin.site.register(Registro_Historia)