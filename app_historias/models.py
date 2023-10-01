from django.db import models
from django import forms

# Create your models here.

class Registro_Paciente(models.Model):

    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField( max_length=50 , blank=True, null=True)
    fecha_nacimiento = models.CharField( max_length=50, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    direccion = models.CharField( max_length=100, blank=True, null=True)
    telefono=models.CharField(max_length=50, blank=True, null=True)
    REF_Dr = models.CharField( max_length=50, blank=True, null=True)
    nombre_madre=models.CharField(max_length=50, blank=True, null=True)
    cedula_madre=models.CharField(max_length=50)
    email = models.EmailField(max_length=254 , blank=True, null=True)
    antecedentes_personales = models.TextField(blank=True, null=True)
    pn=models.CharField(max_length=50, blank=True, null=True)
    tn=models.CharField(max_length=50, blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)
    enfermedad_actual = models.TextField(blank=True, null=True)
    
    

    fecha_registro = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)
    class Meta:
        verbose_name = "registro_pasiente"
        verbose_name_plural = "registro_pasientes"

    def __str__(self):
        return self.nombre

class Registro_Historia(models.Model):
    peso = models.FloatField( blank=True, null=True)
    talla = models.CharField( max_length=50, blank=True, null=True)
    ta = models.CharField( max_length=50, blank=True, null=True)
    examen_fisico = models.CharField( max_length=100, blank=True, null=True)
    laboratorio_ingreso=models.TextField(blank=True, null=True)
    dx_ingreso=models.TextField(blank=True, null=True)
    plan=models.TextField(blank=True, null=True)
    paciente = models.ForeignKey( Registro_Paciente, on_delete=models.CASCADE)

    creacion = models.DateField( auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = "Registro_Historia"
        verbose_name_plural = "Registro_Historias"
        

    def __str__(self):
        return f'historias de {self.paciente}'
