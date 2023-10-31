from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RegistroPacienteForm, RegistroHistoriaForm
from .models import Registro_Paciente, Registro_Historia
import os
from django.conf import settings
import mimetypes
import datetime
import platform



def descargar_archivo(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'db.sqlite3'
    filepath = os.path.join(settings.BASE_DIR, filename)

    with open(filepath, 'rb') as archivo:
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(archivo.read(), content_type=mime_type)
        #response['Content-Disposition'] = f"attachment; filename={filename}"
        print(datetime.datetime.now)
        response['Content-Disposition'] = f"attachment; filename=respaldo_{request.user.username}_{datetime.datetime.now()}.sqlite3"
        return response



# Create your views here.

@login_required(login_url='signin')
def index(request):
    search_query = request.GET.get('search')
    
    if search_query:
        pacientes = Registro_Paciente.objects.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query)
        )
    else:
        pacientes = Registro_Paciente.objects.all()
    
    print("Nombre del sistema operativo:", platform.system())
    print("Versión del sistema operativo:", platform.release())
    print("Arquitectura del sistema:", platform.architecture())
    return render(request, 'index.html', {'pacientes': reversed(pacientes)})

def detalles_paciente(request, pac_id):
    if request.method == 'POST':
        try:
            Pac = get_object_or_404(Registro_Paciente, id=pac_id)
            form = RegistroPacienteForm(request.POST, instance=Pac)
            if form.is_valid():
                form.save()
                return redirect('inicio')
            else:
                return render(request, 'detalles_pacientes.html', {'Registro_Paciente': Pac, 'form': form, 'error': 'no se pudo actualizar'})
        except:
            return render(request, 'detalles_pacientes.html', {'task': Pac, 'form': form, 'error': 'no se pudo actualizar'})
    else:
        Pac = get_object_or_404(Registro_Paciente, id=pac_id)
        form = RegistroPacienteForm(instance=Pac)
        return render(request, 'detalles_pacientes.html', {'Registro_Paciente': Pac, 'form': form})

def registrar_paciente(request):
    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Cambia esto a la ruta adecuada
    else:
        form = RegistroPacienteForm()
    return render(request, 'registrar_paciente.html', {'form': form})

def crear_registro_historia(request,paciente_id):
    paciente = Registro_Paciente.objects.get(pk=paciente_id)
    if request.method == 'POST':
        form = RegistroHistoriaForm(request.POST)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.paciente = paciente
            historia.save()
            return redirect('historias_por_paciente', paciente_id=paciente_id,historia_id=historia.id)
            # Realizar cualquier redireccionamiento o respuesta adecuada aquí
    else:
        form = RegistroHistoriaForm()
        
def editar_registro_historia(request,paciente_id , historia_id=None):
    historia = get_object_or_404(Registro_Historia, id=historia_id)

    if historia_id is not None:
        if request.method == 'POST':
            form = RegistroHistoriaForm(request.POST, instance=historia)
            if form.is_valid():
                form.save()
                return redirect('historias_por_paciente', paciente_id=paciente_id,historia_id=historia.id)
        else:
            form = RegistroHistoriaForm(instance=historia)

def historias_por_paciente(request, paciente_id,historia_id=None):
    paciente = Registro_Paciente.objects.get(pk=paciente_id)
    form = RegistroHistoriaForm()
    if historia_id is not None:
        historia = get_object_or_404(Registro_Historia, id=historia_id)
        form_his = RegistroHistoriaForm(instance=historia)
    else:
        historia = ''
        form_his = ''
    historias = Registro_Historia.objects.filter(paciente=paciente)
    return render(request, 'historias_por_paciente.html', {'paciente': paciente, 'historias': reversed(historias), 'form': form, 'form_his':form_his, 'historia_id':historia_id})

def eliminar_registro(request, paciente_id,historia_id = None):
    paciente = get_object_or_404(Registro_Historia, pk=historia_id)
    
    paciente.delete()
        
    return redirect('historias_por_paciente', paciente_id=paciente_id)
