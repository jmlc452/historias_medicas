from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from django.db.models import Q
from app_historias.models import Registro_Paciente, Registro_Historia
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import pdfkit



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
    template_path = 'informe copy.html'
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
    # return response

    # Eliminar el archivo PDF después de enviarlo por correo
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)
    
    #return redirect('historias_por_paciente', paciente_id=paciente_id)
    return response

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


# def render_pdf_open(request, paciente_id):
#     path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#     config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
#     paciente = get_object_or_404(Registro_Paciente, id=paciente_id)
#     historia = Registro_Historia.objects.filter(paciente=paciente).last()
#     template_path = 'informe copy.html'
#     context = {'p': paciente, 'h': historia}

#     # Generar un nombre de archivo único para el PDF
#     pdf_filename = f'report_{paciente_id}.pdf'
#     pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#     path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#     config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
#     css_path=r'C:\Users\Jorge Ribas\Desktop\historias_medicas\app_historias\static\style.css'
#     # create a pdf
#     pdf_options = {
#         'page-size': 'A4',
#         'encoding': 'UTF-8',
#     }
#     # pdfkit.from_string(html, pdf_path, options=pdf_options,configuration=config,css=css_path)
#     pdfkit.from_url('https://pypi.org/project/pdfkit/', 'out.pdf')

#     # Devolver el PDF como una descarga
#     with open(pdf_path, 'rb') as pdf_file:
#         response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#         response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
#         return response

def generar_informe(request,paciente_id):
    paciente = get_object_or_404(Registro_Paciente, id=paciente_id)
    historia = Registro_Historia.objects.filter(paciente=paciente).last()
    return render(request,'informe copy.html',{'p': paciente, 'h': historia})

def render_pdf_open(request, paciente_id):
    path_wkthmltopdf = r'C:\Users\viann\OneDrive\Escritorio\historias_medicas\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    # Generar un nombre de archivo único para el PDF
    pdf_filename = f'report_{paciente_id}.pdf'
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

    # create a pdf
    pdf_options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }
    # render(request,'informe copy.html',{'p': paciente, 'h': historia})
    # pdfkit.from_string(html, pdf_path, options=pdf_options,configuration=config,css=css_path)
    pdfkit.from_url(f'http://127.0.0.1:8000/informes/genpdf/{paciente_id}/', pdf_filename,configuration=config,options=pdf_options)

        # Devolver el PDF como una descarga
    with open(pdf_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
        return response

