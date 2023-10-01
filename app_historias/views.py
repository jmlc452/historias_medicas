from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RegistroPacienteForm, RegistroHistoriaForm
from .models import Registro_Paciente, Registro_Historia
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import mimetypes

# Create your views here.

def descargar_archivo(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'db.sqlite3'
    filepath = os.path.join(settings.BASE_DIR, filename)

    with open(filepath, 'rb') as archivo:
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(archivo.read(), content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={filename}"
        return response

@login_required(login_url='signin')
def index(request):
    search_query = request.GET.get('search')
    
    if search_query:
        pacientes = Registro_Paciente.objects.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(cedula__icontains=search_query)
        )
    else:
        pacientes = Registro_Paciente.objects.all()
      
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
    # import pywhatkit as kit

    # # Número de teléfono al que deseas enviar el mensaje (con el código de país, sin espacios ni caracteres especiales)
    # numero_telefono = "+584243391569"

    # # Mensaje que deseas enviar
    # mensaje = "¡Hola desde Python!"

    # Envía el mensaje de WhatsApp inmediatamente
    # kit.sendwhatmsg_instantly(numero_telefono, mensaje,1)
    historias = Registro_Historia.objects.filter(paciente=paciente)
    return render(request, 'historias_por_paciente.html', {'paciente': paciente, 'historias': reversed(historias), 'form': form, 'form_his':form_his, 'historia_id':historia_id})



def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def render_pdf_view(request,paciente_id):

    paciente=get_object_or_404(Registro_Paciente, id=paciente_id)
    historia = Registro_Historia.objects.filter(paciente=paciente).last
    template_path = 'informe.html'
    context = {'p': paciente,'h': historia}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    print(response.content)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
   
     # Definir la ruta donde se guardará el archivo PDF en la raíz del proyecto
    pdf_filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'report.pdf')

    # Guardar el archivo PDF en la ruta especificada
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(response.content)

    # Llamar a la función para enviar el correo electrónico
    enviar_correo(paciente.email, pdf_filename)
    
    # Eliminar el archivo PDF después de enviarlo por correo
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)
    
    return redirect('historias_por_paciente', paciente_id=paciente_id)

def enviar_correo(email_to,pdf,):
    email_address = settings.GMAIL_ORIGIN
    email_password = settings.GMAIL_PASSWORD
    
    # Crea el objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email_to
    msg['Subject'] = 'Informe'

    # Adjunta el archivo PDF
    pdf_file = pdf  # Cambia esto al nombre de tu archivo PDF
    with open(pdf_file, 'rb') as attachment:
        pdf_attach = MIMEApplication(attachment.read(), _subtype="pdf")
        pdf_attach.add_header('Content-Disposition', f'attachment; filename={pdf_file}')
        msg.attach(pdf_attach)
        
    # Conecta al servidor SMTP de Gmail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
    except Exception as e:
        print(f"No se pudo conectar al servidor SMTP: {e}")
        
    # Envía el correo electrónico
    try:
        server.sendmail(email_address, email_to, msg.as_string())
        print('Correo enviado con éxito')
    except Exception as e:
        print(f"No se pudo enviar el correo electrónico: {e}")

    # Cierra la conexión con el servidor SMTP
    server.quit()





