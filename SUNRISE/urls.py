from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    
    path('paciente/<int:paciente_id>/pdf/', views.generar_pdf_paciente, name='pdf_paciente'),

    # Login y logout seguros
    path('instalar/', views.instalar_sistema, name='instalar'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('jeec/', admin.site.urls),

    path('', views.home, name="home"),
    path('nuevo_paciente/', views.nuevo_paciente, name='nuevo_paciente'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('paciente/<int:paciente_id>/', views.paciente_detalle, name='paciente_detalle'),
    path('editar_paciente/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('eliminar_paciente/<int:paciente_id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('citas/', views.calendario_citas, name='citas'),
    path('citas/<int:year>/<int:month>/', views.calendario_citas, name='citas_mes'),
    path('citas/dia/<int:year>/<int:month>/<int:day>/', views.citas_dia, name='citas_dia'),
    path('citas/nueva/<int:year>/<int:month>/<int:day>/', views.nueva_cita, name='nueva_cita'),
    path('citas/editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('buscar-pacientes/', views.buscar_pacientes, name='buscar_pacientes'),
    path('tratamientos/', views.lista_tratamientos, name='tratamientos'),
    path('tratamientos/nuevo/', views.nuevo_tratamiento, name='nuevo_tratamiento'),
    path('tratamientos/<int:tratamiento_id>/', views.ver_tratamiento, name='ver_tratamiento'),
    path('tratamientos/<int:tratamiento_id>/editar/', views.editar_tratamiento, name='editar_tratamiento'),
    path('tratamientos/<int:tratamiento_id>/mostrar/', views.mostrar_tratamiento, name='mostrar_tratamiento'),
    path('tratamientos/<int:tratamiento_id>/eliminar/', views.eliminar_tratamiento, name='eliminar_tratamiento'),
    path('tratamientos/foto/<int:foto_id>/eliminar/', views.eliminar_foto_tratamiento, name='eliminar_foto_tratamiento'),
    path('paciente/<int:paciente_id>/añadir-informacion/', views.añadir_informacion, name='añadir_informacion'),
path('informacion/<int:informacion_id>/editar/', views.editar_informacion, name='editar_informacion'),
path('informacion/<int:informacion_id>/eliminar/', views.eliminar_informacion, name='eliminar_informacion'),
path('informacion/foto/<int:foto_id>/eliminar/', views.eliminar_foto_informacion, name='eliminar_foto_informacion'),
path('paciente/<int:paciente_id>/odontograma/', views.odontograma, name='odontograma'),
path('paciente/<int:paciente_id>/odontograma/guardar/', views.guardar_odontograma, name='guardar_odontograma'),
path('paciente/<int:paciente_id>/diente/<int:diente_numero>/nueva-accion/', 
     views.nueva_accion_dental, name='nueva_accion_dental'),
    path('paciente/<int:paciente_id>/diente/<int:diente_numero>/acciones/', 
         views.lista_acciones_dental, name='lista_acciones_dental'),
    path('accion-dental/<int:accion_id>/editar/', 
         views.editar_accion_dental, name='editar_accion_dental'),
    path('accion-dental/<int:accion_id>/galeria/', 
         views.galeria_accion_dental, name='galeria_accion_dental'),
    path('accion-dental/foto-antes/<int:foto_id>/eliminar/', 
         views.eliminar_foto_antes, name='eliminar_foto_antes'),
    path('accion-dental/foto-despues/<int:foto_id>/eliminar/', 
         views.eliminar_foto_despues, name='eliminar_foto_despues'),
    path('accion-dental/<int:accion_id>/mostrar-galeria/', 
         views.mostrar_galeria_completa, name='mostrar_galeria_completa'),
         path('accion-dental/<int:accion_id>/eliminar/', 
     views.eliminar_accion_dental, name='eliminar_accion_dental'),  
]

# Redirección raíz al login si no está autenticado
def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)