from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('pdf/<int:paciente_id>/',views.render_pdf_view,name='pdf'),
    path('openpdf/<int:paciente_id>/',views.render_pdf_open,name='openpdf'),
]
