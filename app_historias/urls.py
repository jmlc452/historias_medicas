from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='inicio'),
    path('registerpas/', views.registrar_paciente,name='registerpas'),
    path('regishis/<int:paciente_id>/',views.crear_registro_historia,name='registro_his'),
    path('historias_por_paciente/<int:paciente_id>/<int:historia_id>/', views.historias_por_paciente, name='historias_por_paciente'),
    path('historias_por_paciente/<int:paciente_id>/', views.historias_por_paciente, name='historias_por_paciente'),
    path('detalles/<int:pac_id>/', views.detalles_paciente, name='detalles_paciente'),
    path('editar_registro_historia/<int:paciente_id>/<int:historia_id>/',views.editar_registro_historia,name='editar_registro_historia'),
    path('editar_registro_historia/<int:paciente_id>/',views.editar_registro_historia,name='editar_registro_historia'),
    path('descargar_archivo/', views.descargar_archivo, name='descargar_archivo'),
    
]
