# En views.py, agregar al inicio
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# En views.py, modificar o crear vista de login personalizada
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# En views.py - VERSIÓN SIMPLIFICADA Y FUNCIONAL
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@never_cache
def custom_logout(request):
    """Cierre de sesión seguro"""
    logout(request)
    response = redirect('login')
    
    # Headers para prevenir cache
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@never_cache
@csrf_protect
def custom_login(request):
    """Vista de login segura"""
    # Si ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Manejar error de login
            return render(request, 'registration/login.html', {
                'error': 'Credenciales inválidas'
            })
    
    return render(request, 'registration/login.html')

# Decorador seguro simplificado para todas tus vistas
def auth_required(view_func):
    """Decorador seguro simplificado"""
    return never_cache(login_required(view_func))

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from datetime import datetime, date, timedelta
import calendar
from django.db.models import Q
from .models import Paciente, Cita
from .models import Tratamiento, FotoTratamiento, InformacionAdicional, FotoInformacion
from django.utils import timezone 
import pytz
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@never_cache
@csrf_protect
def custom_login(request):
    """Vista de login segura y mejorada"""
    # Si ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # ✅ Forzar guardado de sesión
                request.session.save()
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {
                    'error': 'Credenciales inválidas',
                    'form': {'errors': True}
                })
        else:
            return render(request, 'registration/login.html', {
                'error': 'Por favor ingrese usuario y contraseña',
                'form': {'errors': True}
            })
    
    return render(request, 'registration/login.html')

@never_cache
def custom_logout(request):
    """Cierre de sesión seguro"""
    logout(request)
    response = redirect('login')
    
    # ✅ Headers para limpiar completamente la sesión
    response.delete_cookie('sessionid')
    response.delete_cookie('sessionid_sunrise')
    response.delete_cookie('csrftoken')
    
    # Headers para prevenir cache
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

# ✅ Decorador mejorado para todas las vistas que requieren autenticación
def auth_required(view_func):
    """Decorador seguro simplificado"""
    wrapped_view = login_required(view_func)
    wrapped_view = never_cache(wrapped_view)
    return wrapped_view

@auth_required
def home(request):
    return render(request, "HOME.html")

@auth_required
def nuevo_paciente(request):
    print(f"🔐 USER AUTHENTICATED: {request.user.is_authenticated}")
    print(f"🔐 USER: {request.user}")
    print(f"🔐 SESSION KEY: {request.session.session_key}")
    print(f"🔐 SESSION DATA: {dict(request.session)}")
    
    if request.method == 'POST':
        # Datos personales - convertir a mayúsculas automáticamente
        nombre = request.POST['nombre'].strip().upper()  # ← Agregar .upper()
        apellido = request.POST['apellido'].strip().upper()  # ← Agregar .upper()
        ci = request.POST.get('ci', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero', 'masculino')
        ocupacion = request.POST.get('ocupacion', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        
        # Historial clínico
        motivo_consulta = request.POST.get('motivo_consulta', '').strip()
        enfermedad_actual = request.POST.get('enfermedad_actual', '').strip()
        antecedentes_familiares_patologicos = request.POST.get('antecedentes_familiares_patologicos', '').strip()
        
        # Antecedentes personales patológicos
        anemia = request.POST.get('anemia', 'pendiente')
        cardiopatias = request.POST.get('cardiopatias', 'pendiente')
        diabetes = request.POST.get('diabetes', 'pendiente')
        enf_gastricas = request.POST.get('enf_gastricas', 'pendiente')
        epilepsia = request.POST.get('epilepsia', 'pendiente')
        hipertencion = request.POST.get('hipertencion', 'pendiente')
        vih = request.POST.get('vih', 'pendiente')
        observaciones_patologicos = request.POST.get('observaciones_patologicos', '').strip()
        
        # Preguntas médicas
        tratamiento_medico_actual = request.POST.get('tratamiento_medico_actual', 'pendiente')
        tratamiento_medico_desc = request.POST.get('tratamiento_medico_desc', '').strip()
        toma_medicamentos = request.POST.get('toma_medicamentos', 'pendiente')
        medicamentos_desc = request.POST.get('medicamentos_desc', '').strip()
        alergias = request.POST.get('alergias', 'pendiente')
        alergias_desc = request.POST.get('alergias_desc', '').strip()
        intervencion_quirurgica = request.POST.get('intervencion_quirurgica', 'pendiente')
        intervencion_quirurgica_desc = request.POST.get('intervencion_quirurgica_desc', '').strip()
        reaccion_anestecia = request.POST.get('reaccion_anestecia', 'pendiente')
        reaccion_anestecia_desc = request.POST.get('reaccion_anestecia_desc', '').strip()
        hemorragia_exodoncia = request.POST.get('hemorragia_exodoncia', 'pendiente')
        hemorragia_exodoncia_desc = request.POST.get('hemorragia_exodoncia_desc', '').strip()
        alteraciones_cicatrizacion = request.POST.get('alteraciones_cicatrizacion', 'pendiente')
        alteraciones_cicatrizacion_desc = request.POST.get('alteraciones_cicatrizacion_desc', '').strip()
        embarazada = request.POST.get('embarazada', 'pendiente')
        embarazada_desc = request.POST.get('embarazada_desc', '').strip()
        
        # Antecedentes no patológicos
        fuma = request.POST.get('fuma', 'pendiente')
        bebe = request.POST.get('bebe', 'pendiente')
        respiracion_bucal = request.POST.get('respiracion_bucal', 'pendiente')
        queilofagia = request.POST.get('queilofagia', 'pendiente')
        onicofagia = request.POST.get('onicofagia', 'pendiente')
        bruxismo = request.POST.get('bruxismo', 'pendiente')
        mastica_coca = request.POST.get('mastica_coca', 'pendiente')
        mastica_chicle = request.POST.get('mastica_chicle', 'pendiente')
        mordisqueo_objetos = request.POST.get('mordisqueo_objetos', 'pendiente')
        
        # Menores de edad
        uso_biberon = request.POST.get('uso_biberon', 'pendiente')
        uso_chupon = request.POST.get('uso_chupon', 'pendiente')
        succion_dedo = request.POST.get('succion_dedo', 'pendiente')

        # VALORACIÓN DE HIGIENE DENTO-BUCAL
        higiene_bucal = request.POST.get('higiene_bucal', 'pendiente')
        frecuencia_cepillado = request.POST.get('frecuencia_cepillado', '').strip()
        cambio_cepillo = request.POST.get('cambio_cepillo', '').strip()
        suburra = request.POST.get('suburra', 'pendiente')
        materia_alba = request.POST.get('materia_alba', 'pendiente')
        placa_bacteriana = request.POST.get('placa_bacteriana', 'pendiente')
        tartaro = request.POST.get('tartaro', 'pendiente')
        halitosis = request.POST.get('halitosis', 'pendiente')
        
        # Convertir campos vacíos a None
        campos_texto = [ci, telefono, motivo_consulta, enfermedad_actual, antecedentes_familiares_patologicos, 
                       observaciones_patologicos, tratamiento_medico_desc, medicamentos_desc, alergias_desc,
                       intervencion_quirurgica_desc, reaccion_anestecia_desc, hemorragia_exodoncia_desc,
                       alteraciones_cicatrizacion_desc, embarazada_desc, frecuencia_cepillado, cambio_cepillo]
        
        for i, campo in enumerate(campos_texto):
            if not campo:
                campos_texto[i] = None
        
        Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            ci=campos_texto[0],
            fecha_nacimiento=fecha_nacimiento if fecha_nacimiento else None,
            genero=genero,
            ocupacion=ocupacion if ocupacion else None,
            telefono=campos_texto[1],
            motivo_consulta=campos_texto[2],
            enfermedad_actual=campos_texto[3],
            antecedentes_familiares_patologicos=campos_texto[4],
            anemia=anemia,
            cardiopatias=cardiopatias,
            diabetes=diabetes,
            enf_gastricas=enf_gastricas,
            epilepsia=epilepsia,
            hipertencion=hipertencion,
            vih=vih,
            observaciones_patologicos=campos_texto[5],
            tratamiento_medico_actual=tratamiento_medico_actual,
            tratamiento_medico_desc=campos_texto[6],
            toma_medicamentos=toma_medicamentos,
            medicamentos_desc=campos_texto[7],
            alergias=alergias,
            alergias_desc=campos_texto[8],
            intervencion_quirurgica=intervencion_quirurgica,
            intervencion_quirurgica_desc=campos_texto[9],
            reaccion_anestecia=reaccion_anestecia,
            reaccion_anestecia_desc=campos_texto[10],
            hemorragia_exodoncia=hemorragia_exodoncia,
            hemorragia_exodoncia_desc=campos_texto[11],
            alteraciones_cicatrizacion=alteraciones_cicatrizacion,
            alteraciones_cicatrizacion_desc=campos_texto[12],
            embarazada=embarazada,
            embarazada_desc=campos_texto[13],
            fuma=fuma,
            bebe=bebe,
            respiracion_bucal=respiracion_bucal,
            queilofagia=queilofagia,
            onicofagia=onicofagia,
            bruxismo=bruxismo,
            mastica_coca=mastica_coca,
            mastica_chicle=mastica_chicle,
            mordisqueo_objetos=mordisqueo_objetos,
            uso_biberon=uso_biberon,
            uso_chupon=uso_chupon,
            succion_dedo=succion_dedo,
            # VALORACIÓN DE HIGIENE DENTO-BUCAL
            higiene_bucal=higiene_bucal,
            frecuencia_cepillado=campos_texto[14],
            cambio_cepillo=campos_texto[15],
            suburra=suburra,
            materia_alba=materia_alba,
            placa_bacteriana=placa_bacteriana,
            tartaro=tartaro,
            halitosis=halitosis
        )
        return redirect('pacientes')
    return render(request, 'nuevo_paciente.html')

@auth_required
def pacientes(request):
    query = request.GET.get('q', '')
    pacientes = Paciente.objects.all()
    
    if query:
        # Buscar en múltiples campos
        pacientes = pacientes.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(ci__icontains=query) |
            Q(telefono__icontains=query)
        )
        
        # Si no hay resultados exactos, buscar con aproximación fonética
        if not pacientes.exists():
            pacientes = buscar_similares(query)
    
    return render(request, 'pacientes.html', {'pacientes': pacientes, 'query': query})

@auth_required
def buscar_similares(query):
    """
    Busca pacientes con nombres/apellidos similares fonéticamente
    """
    from django.db.models import Q
    from django.db.models.functions import Lower
    
    # Normalizar la query (minúsculas, sin espacios extras)
    query_normalizada = ' '.join(query.lower().split())
    
    # Obtener todos los pacientes
    todos_pacientes = Paciente.objects.all()
    resultados = []
    
    for paciente in todos_pacientes:
        # Crear strings combinados para comparar
        nombre_completo = f"{paciente.nombre.lower()} {paciente.apellido.lower()}"
        nombre_completo_invertido = f"{paciente.apellido.lower()} {paciente.nombre.lower()}"
        
        # Calcular similitud (método simple)
        similitud = calcular_similitud(query_normalizada, nombre_completo)
        similitud_invertida = calcular_similitud(query_normalizada, nombre_completo_invertido)
        
        # Si la similitud es mayor al 60%, incluir en resultados
        if similitud >= 0.6 or similitud_invertida >= 0.6:
            resultados.append(paciente)
    
    return resultados

@auth_required
def calcular_similitud(str1, str2):
    """
    Calcula similitud entre dos strings usando método simple
    """
    # Método simple de similitud por caracteres comunes
    if not str1 or not str2:
        return 0
    
    # Convertir a conjuntos de palabras
    palabras1 = set(str1.split())
    palabras2 = set(str2.split())
    
    if not palabras1 or not palabras2:
        return 0
    
    # Calcular similitud de Jaccard simple
    interseccion = palabras1.intersection(palabras2)
    union = palabras1.union(palabras2)
    
    return len(interseccion) / len(union) if union else 0

@auth_required
def paciente_detalle(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # CALCULAR EDAD (tu código existente)
    edad = None
    fecha_nacimiento_espanol = "No especificada"
    
    if paciente.fecha_nacimiento:
        hoy = date.today()
        edad = hoy.year - paciente.fecha_nacimiento.year
        
        # Ajustar si aún no ha cumplido años este año
        if hoy.month < paciente.fecha_nacimiento.month or (hoy.month == paciente.fecha_nacimiento.month and hoy.day < paciente.fecha_nacimiento.day):
            edad -= 1
        
        # Nombres de meses en español
        meses_espanol = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        # Formatear fecha en español
        fecha_nacimiento_espanol = f"{paciente.fecha_nacimiento.day} de {meses_espanol[paciente.fecha_nacimiento.month]} de {paciente.fecha_nacimiento.year}"

    # ↓↓↓ NUEVO CÓDIGO: CONVERTIR FECHA DE CREACIÓN A ZONA HORARIA LOCAL ↓↓↓
    fecha_creacion_local = None
    if paciente.fecha_creacion:
        # Cambia 'America/La_Paz' por tu zona horaria
        local_tz = pytz.timezone('America/La_Paz')  # ← CAMBIA ESTO
        fecha_creacion_local = paciente.fecha_creacion.astimezone(local_tz)
    # ↑↑↑ FIN DEL NUEVO CÓDIGO ↑↑↑
    
    context = {
        'paciente': paciente,
        'fecha_nacimiento_espanol': fecha_nacimiento_espanol,
        'edad': edad,
        'fecha_creacion_local': fecha_creacion_local,  # ← AGREGAR AL CONTEXTO
    }
    return render(request, 'paciente_detalle.html', context)

@auth_required
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        # Actualizar datos personales
        paciente.nombre = request.POST['nombre']
        paciente.apellido = request.POST['apellido']
        
        # Manejar campos opcionales de datos personales
        ci = request.POST.get('ci', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        ocupacion = request.POST.get('ocupacion', '').strip()
        
        # Convertir campos vacíos a None
        paciente.ci = ci if ci else None
        paciente.telefono = telefono if telefono else None
        paciente.ocupacion = ocupacion if ocupacion else None
        
        # Género
        paciente.genero = request.POST.get('genero', 'masculino')
        
        # Manejar fecha de nacimiento
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        paciente.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento else None
        
        # Historial clínico - campos de texto
        motivo_consulta = request.POST.get('motivo_consulta', '').strip()
        enfermedad_actual = request.POST.get('enfermedad_actual', '').strip()
        antecedentes_familiares_patologicos = request.POST.get('antecedentes_familiares_patologicos', '').strip()
        observaciones_patologicos = request.POST.get('observaciones_patologicos', '').strip()
        
        paciente.motivo_consulta = motivo_consulta if motivo_consulta else None
        paciente.enfermedad_actual = enfermedad_actual if enfermedad_actual else None
        paciente.antecedentes_familiares_patologicos = antecedentes_familiares_patologicos if antecedentes_familiares_patologicos else None
        paciente.observaciones_patologicos = observaciones_patologicos if observaciones_patologicos else None
        
        # Antecedentes personales patológicos (checkboxes)
        paciente.anemia = request.POST.get('anemia', 'pendiente')
        paciente.cardiopatias = request.POST.get('cardiopatias', 'pendiente')
        paciente.diabetes = request.POST.get('diabetes', 'pendiente')
        paciente.enf_gastricas = request.POST.get('enf_gastricas', 'pendiente')
        paciente.epilepsia = request.POST.get('epilepsia', 'pendiente')
        paciente.hipertencion = request.POST.get('hipertencion', 'pendiente')
        paciente.vih = request.POST.get('vih', 'pendiente')
        
        # Preguntas médicas con descripciones
        paciente.tratamiento_medico_actual = request.POST.get('tratamiento_medico_actual', 'pendiente')
        paciente.tratamiento_medico_desc = request.POST.get('tratamiento_medico_desc', '').strip() or None
        paciente.toma_medicamentos = request.POST.get('toma_medicamentos', 'pendiente')
        paciente.medicamentos_desc = request.POST.get('medicamentos_desc', '').strip() or None
        paciente.alergias = request.POST.get('alergias', 'pendiente')
        paciente.alergias_desc = request.POST.get('alergias_desc', '').strip() or None
        paciente.intervencion_quirurgica = request.POST.get('intervencion_quirurgica', 'pendiente')
        paciente.intervencion_quirurgica_desc = request.POST.get('intervencion_quirurgica_desc', '').strip() or None
        paciente.reaccion_anestecia = request.POST.get('reaccion_anestecia', 'pendiente')
        paciente.reaccion_anestecia_desc = request.POST.get('reaccion_anestecia_desc', '').strip() or None
        paciente.hemorragia_exodoncia = request.POST.get('hemorragia_exodoncia', 'pendiente')
        paciente.hemorragia_exodoncia_desc = request.POST.get('hemorragia_exodoncia_desc', '').strip() or None
        paciente.alteraciones_cicatrizacion = request.POST.get('alteraciones_cicatrizacion', 'pendiente')
        paciente.alteraciones_cicatrizacion_desc = request.POST.get('alteraciones_cicatrizacion_desc', '').strip() or None
        paciente.embarazada = request.POST.get('embarazada', 'pendiente')
        paciente.embarazada_desc = request.POST.get('embarazada_desc', '').strip() or None
        
        # Antecedentes no patológicos
        paciente.fuma = request.POST.get('fuma', 'pendiente')
        paciente.bebe = request.POST.get('bebe', 'pendiente')
        paciente.respiracion_bucal = request.POST.get('respiracion_bucal', 'pendiente')
        paciente.queilofagia = request.POST.get('queilofagia', 'pendiente')
        paciente.onicofagia = request.POST.get('onicofagia', 'pendiente')
        paciente.bruxismo = request.POST.get('bruxismo', 'pendiente')
        paciente.mastica_coca = request.POST.get('mastica_coca', 'pendiente')
        paciente.mastica_chicle = request.POST.get('mastica_chicle', 'pendiente')
        paciente.mordisqueo_objetos = request.POST.get('mordisqueo_objetos', 'pendiente')
        
        # Menores de edad
        paciente.uso_biberon = request.POST.get('uso_biberon', 'pendiente')
        paciente.uso_chupon = request.POST.get('uso_chupon', 'pendiente')
        paciente.succion_dedo = request.POST.get('succion_dedo', 'pendiente')
        
        paciente.save()
        
        return redirect('paciente_detalle', paciente_id=paciente.id)
    
    return render(request, 'editar_paciente.html', {'paciente': paciente})

@auth_required
def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes')
    return redirect('pacientes')

@auth_required
def calendario_citas(request, year=None, month=None):
    # Obtener el año y mes actual si no se especifican
    hoy = datetime.now()
    if year is None:
        year = hoy.year
    if month is None:
        month = hoy.month
    
    # Crear calendario
    cal = calendar.Calendar(firstweekday=0)  # Lunes como primer día
    mes_calendario = cal.monthdatescalendar(year, month)
    
    # Preparar datos para el template
    calendario_data = []
    for semana in mes_calendario:
        semana_data = []
        for dia in semana:
            # Verificar si hay citas en este día
            citas_dia = Cita.objects.filter(fecha=dia)
            con_citas = citas_dia.exists()
            num_citas = citas_dia.count()
            
            semana_data.append({
                'date': dia,
                'day': dia.day,
                'month': dia.month,
                'year': dia.year,
                'es_mes_actual': dia.month == month,
                'con_citas': con_citas,
                'num_citas': num_citas,
                'es_hoy': dia == hoy.date()
            })
        calendario_data.append(semana_data)
    
    # Nombres de meses en español
    meses_espanol = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    # Calcular meses anterior y siguiente
    mes_anterior = month - 1 if month > 1 else 12
    año_anterior = year if month > 1 else year - 1
    mes_siguiente = month + 1 if month < 12 else 1
    año_siguiente = year if month < 12 else year + 1
    
    context = {
        'calendario': calendario_data,
        'año_actual': year,
        'mes_actual': meses_espanol[month],
        'mes_numero': month,
        'mes_anterior': meses_espanol[mes_anterior],
        'mes_siguiente': meses_espanol[mes_siguiente],
        'url_mes_anterior': f'/citas/{año_anterior}/{mes_anterior}/',
        'url_mes_siguiente': f'/citas/{año_siguiente}/{mes_siguiente}/',
    }
    
    return render(request, 'calendario_citas.html', context)  

@auth_required
def citas_dia(request, year, month, day):
    fecha = date(year, month, day)
    citas = Cita.objects.filter(fecha=fecha).order_by('hora_inicio')  # Cambiar 'hora' por 'hora_inicio'
    
    context = {
        'fecha': fecha,
        'citas': citas,
    }
    return render(request, 'citas_dia.html', context)

@auth_required
def nueva_cita(request, year, month, day):
    fecha = date(year, month, day)
    
    if request.method == 'POST':
        try:
            paciente_id = request.POST.get('paciente_id')
            paciente_busqueda = request.POST.get('paciente_busqueda', '').strip()
            hora_inicio = request.POST.get('hora_inicio')  # Usar get() en lugar de acceso directo
            hora_fin = request.POST.get('hora_fin')        # Usar get() en lugar de acceso directo
            dentista = request.POST.get('dentista')
            motivo = request.POST.get('motivo', '')
            
            # Validar campos requeridos
            if not hora_inicio or not hora_fin or not dentista:
                context = {
                    'fecha': fecha,
                    'error': 'Todos los campos son requeridos: Hora inicio, Hora fin y Dentista'
                }
                return render(request, 'nueva_cita.html', context)
            
            # Manejar paciente existente o nuevo
            if paciente_id:
                paciente = Paciente.objects.get(id=paciente_id)
            elif paciente_busqueda:
                partes = paciente_busqueda.split()
                if len(partes) >= 2:
                    nombre = partes[0].strip().upper()
                    apellido = ' '.join(partes[1:]).strip().upper()
                else:
                    nombre = paciente_busqueda.strip().upper()
                    apellido = ''
                
                paciente = Paciente.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    ci='',
                    fecha_nacimiento=None,
                    telefono='',
                    motivo_consulta=motivo or 'Consulta programada desde cita'
                )
            else:
                context = {
                    'fecha': fecha,
                    'error': 'Debe seleccionar o ingresar un paciente'
                }
                return render(request, 'nueva_cita.html', context)
            
            # Convertir strings a objetos time
            from datetime import datetime
            inicio_dt = datetime.strptime(hora_inicio, '%H:%M').time()
            fin_dt = datetime.strptime(hora_fin, '%H:%M').time()
            
            # Verificar si hay citas que se solapen
            citas_solapadas = Cita.objects.filter(
                fecha=fecha
            ).filter(
                Q(hora_inicio__lt=fin_dt, hora_fin__gt=inicio_dt)
            )
            
            if citas_solapadas.exists():
                context = {
                    'fecha': fecha, 
                    'error': 'Ya existe una cita programada que se solapa con este horario'
                }
                return render(request, 'nueva_cita.html', context)
            
            # Validar que hora_fin sea mayor que hora_inicio
            if fin_dt <= inicio_dt:
                context = {
                    'fecha': fecha,
                    'error': 'La hora de fin debe ser posterior a la hora de inicio'
                }
                return render(request, 'nueva_cita.html', context)
            
            # Crear la cita
            Cita.objects.create(
                paciente=paciente,
                fecha=fecha,
                hora_inicio=inicio_dt,
                hora_fin=fin_dt,
                dentista=dentista,
                motivo=motivo
            )
            return redirect('citas_dia', year=year, month=month, day=day)
            
        except Paciente.DoesNotExist:
            context = {
                'fecha': fecha,
                'error': 'El paciente seleccionado no existe'
            }
            return render(request, 'nueva_cita.html', context)
        except Exception as e:
            context = {
                'fecha': fecha,
                'error': f'Error al crear la cita: {str(e)}'
            }
            return render(request, 'nueva_cita.html', context)
    
    return render(request, 'nueva_cita.html', {'fecha': fecha})

@auth_required
def buscar_pacientes(request):
    query = request.GET.get('q', '')
    pacientes = Paciente.objects.all()
    
    if query:
        # Buscar en nombre, apellido o CI
        pacientes = pacientes.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(ci__icontains=query)
        )[:10]  # Limitar a 10 resultados
        
        resultados = []
        for paciente in pacientes:
            resultados.append({
                'id': paciente.id,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
                'ci': paciente.ci
            })
        
        return JsonResponse({'pacientes': resultados})
    
    return JsonResponse({'pacientes': []})

@auth_required
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    pacientes = Paciente.objects.all()
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            paciente_id = request.POST.get('paciente')
            hora_inicio = request.POST.get('hora_inicio')
            hora_fin = request.POST.get('hora_fin')
            dentista = request.POST.get('dentista')
            motivo = request.POST.get('motivo', '')
            
            # Validar campos requeridos
            if not paciente_id or not hora_inicio or not hora_fin or not dentista:
                context = {
                    'cita': cita,
                    'pacientes': pacientes,
                    'error': 'Todos los campos son requeridos'
                }
                return render(request, 'editar_cita.html', context)
            
            # Actualizar paciente
            cita.paciente_id = paciente_id
            
            # Convertir strings a objetos time
            from datetime import datetime
            inicio_dt = datetime.strptime(hora_inicio, '%H:%M').time()
            fin_dt = datetime.strptime(hora_fin, '%H:%M').time()
            
            # Verificar si hay conflicto con otras citas (excluyendo la actual)
            citas_solapadas = Cita.objects.filter(
                fecha=cita.fecha
            ).exclude(id=cita.id).filter(
                Q(hora_inicio__lt=fin_dt, hora_fin__gt=inicio_dt)
            )
            
            if citas_solapadas.exists():
                context = {
                    'cita': cita,
                    'pacientes': pacientes,
                    'error': 'Ya existe otra cita programada que se solapa con este horario'
                }
                return render(request, 'editar_cita.html', context)
            
            # Validar que hora_fin sea mayor que hora_inicio
            if fin_dt <= inicio_dt:
                context = {
                    'cita': cita,
                    'pacientes': pacientes,
                    'error': 'La hora de fin debe ser posterior a la hora de inicio'
                }
                return render(request, 'editar_cita.html', context)
            
            # Actualizar los campos
            cita.hora_inicio = inicio_dt
            cita.hora_fin = fin_dt
            cita.dentista = dentista
            cita.motivo = motivo
            
            cita.save()
            return redirect('citas_dia', year=cita.fecha.year, month=cita.fecha.month, day=cita.fecha.day)
            
        except Exception as e:
            context = {
                'cita': cita,
                'pacientes': pacientes,
                'error': f'Error al actualizar la cita: {str(e)}'
            }
            return render(request, 'editar_cita.html', context)
    
    context = {
        'cita': cita,
        'pacientes': pacientes,
    }
    return render(request, 'editar_cita.html', context)

@auth_required
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    fecha = cita.fecha  # Guardar la fecha antes de eliminar para redireccionar
    
    if request.method == 'POST':
        cita.delete()
        return redirect('citas_dia', year=fecha.year, month=fecha.month, day=fecha.day)
    
    return redirect('citas_dia', year=fecha.year, month=fecha.month, day=fecha.day)

@auth_required
def lista_tratamientos(request):
    tratamientos = Tratamiento.objects.all().order_by('titulo')
    return render(request, 'lista_tratamientos.html', {'tratamientos': tratamientos})

@auth_required
def nuevo_tratamiento(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        materiales = request.POST['materiales']
        costo = request.POST['costo']
        
        tratamiento = Tratamiento.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            materiales=materiales,
            costo=costo
        )
        
        # Manejar múltiples imágenes
        fotos = request.FILES.getlist('fotos')
        for foto in fotos:
            FotoTratamiento.objects.create(
                tratamiento=tratamiento,
                imagen=foto
            )
        
        return redirect('tratamientos')
    
    return render(request, 'nuevo_tratamiento.html')

@auth_required
def ver_tratamiento(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    return render(request, 'ver_tratamiento.html', {'tratamiento': tratamiento})

@auth_required
def editar_tratamiento(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    
    if request.method == 'POST':
        tratamiento.titulo = request.POST['titulo']
        tratamiento.descripcion = request.POST['descripcion']
        tratamiento.materiales = request.POST['materiales']
        tratamiento.costo = request.POST['costo']
        tratamiento.save()
        
        # Manejar nuevas imágenes
        nuevas_fotos = request.FILES.getlist('nuevas_fotos')
        for foto in nuevas_fotos:
            FotoTratamiento.objects.create(
                tratamiento=tratamiento,
                imagen=foto
            )
        
        return redirect('ver_tratamiento', tratamiento_id=tratamiento.id)
    
    return render(request, 'editar_tratamiento.html', {'tratamiento': tratamiento})

@auth_required
def mostrar_tratamiento(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    return render(request, 'mostrar_tratamiento.html', {'tratamiento': tratamiento})

@auth_required
def eliminar_tratamiento(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)
    if request.method == 'POST':
        tratamiento.delete()
        return redirect('tratamientos')
    return redirect('tratamientos')

@auth_required
def eliminar_foto_tratamiento(request, foto_id):
    foto = get_object_or_404(FotoTratamiento, id=foto_id)
    tratamiento_id = foto.tratamiento.id
    
    if request.method == 'POST':
        foto.delete()
        return redirect('editar_tratamiento', tratamiento_id=tratamiento_id)
    
    return redirect('editar_tratamiento', tratamiento_id=tratamiento_id)

@auth_required
def añadir_informacion(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        
        informacion = InformacionAdicional.objects.create(
            paciente=paciente,
            titulo=titulo,
            descripcion=descripcion
        )
        
        # Manejar imágenes
        fotos = request.FILES.getlist('fotos')
        for foto in fotos:
            FotoInformacion.objects.create(
                informacion=informacion,
                imagen=foto
            )
        
        return redirect('paciente_detalle', paciente_id=paciente.id)
    
    return render(request, 'añadir_informacion.html', {'paciente': paciente})

@auth_required
def editar_informacion(request, informacion_id):
    informacion = get_object_or_404(InformacionAdicional, id=informacion_id)
    
    if request.method == 'POST':
        informacion.titulo = request.POST['titulo']
        informacion.descripcion = request.POST['descripcion']
        informacion.save()
        
        # Manejar nuevas imágenes
        nuevas_fotos = request.FILES.getlist('nuevas_fotos')
        for foto in nuevas_fotos:
            FotoInformacion.objects.create(
                informacion=informacion,
                imagen=foto
            )
        
        return redirect('paciente_detalle', paciente_id=informacion.paciente.id)
    
    return render(request, 'editar_informacion.html', {'informacion': informacion})

@auth_required
def eliminar_informacion(request, informacion_id):
    informacion = get_object_or_404(InformacionAdicional, id=informacion_id)
    paciente_id = informacion.paciente.id
    
    if request.method == 'POST':
        informacion.delete()
        return redirect('paciente_detalle', paciente_id=paciente_id)
    
    return redirect('paciente_detalle', paciente_id=paciente_id)

@auth_required
def eliminar_foto_informacion(request, foto_id):
    foto = get_object_or_404(FotoInformacion, id=foto_id)
    informacion_id = foto.informacion.id
    paciente_id = foto.informacion.paciente.id
    
    if request.method == 'POST':
        foto.delete()
        return redirect('editar_informacion', informacion_id=informacion_id)
    
    return redirect('editar_informacion', informacion_id=informacion_id)
    foto = get_object_or_404(FotoInformacion, id=foto_id)
    informacion_id = foto.informacion.id
    paciente_id = foto.informacion.paciente.id
    
    if request.method == 'POST':
        foto.delete()
        return redirect('editar_informacion', informacion_id=informacion_id)
    
    return redirect('editar_informacion', informacion_id=informacion_id)

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Paciente

@auth_required
def odontograma(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Obtener datos del odontograma si existen
    datos_odontograma = paciente.odontograma_data if paciente.odontograma_data else {}
    
    # OBTENER LAS ACCIONES DE LOS DIENTES - CORREGIDO
    from .models import AccionDental  # Cambiado a AccionDental
    
    acciones_por_diente = {}
    try:
        # Obtener todas las acciones para este paciente
        acciones = AccionDental.objects.filter(paciente=paciente)  # Cambiado a AccionDental
        print(f"🔍 DEBUG odontograma view:")
        print(f"   Paciente: {paciente.nombre} {paciente.apellido}")
        print(f"   ID Paciente: {paciente.id}")
        print(f"   Acciones encontradas: {acciones.count()}")
        
        for accion in acciones:
            diente_numero = str(accion.diente_numero)  # CORRECTO: diente_numero
            if diente_numero not in acciones_por_diente:
                acciones_por_diente[diente_numero] = []
            acciones_por_diente[diente_numero].append(accion.titulo)
            print(f"   - Diente {diente_numero}: '{accion.titulo}' (ID: {accion.id})")
            
    except Exception as e:
        print(f"❌ ERROR en vista odontograma: {e}")
        import traceback
        traceback.print_exc()
        acciones_por_diente = {}

    print(f"🔍 acciones_por_diente final: {acciones_por_diente}")

    context = {
        'paciente': paciente,
        'datos_odontograma_json': json.dumps(datos_odontograma),
        'acciones_por_diente_json': json.dumps(acciones_por_diente)
    }
    
    return render(request, 'odontograma.html', context)

@auth_required
def guardar_odontograma(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        try:
            datos_odontograma = request.POST.get('datos_odontograma')
            print(f"📥 Datos recibidos: {datos_odontograma}")
            
            if datos_odontograma:
                datos_dict = json.loads(datos_odontograma)
                paciente.odontograma_data = datos_dict
                paciente.save()
                print("✅ Odontograma guardado en base de datos")
                
                # Si es una petición AJAX, responder con JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Odontograma guardado correctamente'})
                else:
                    messages.success(request, 'Odontograma guardado correctamente.')
                    return redirect('odontograma', paciente_id=paciente.id)
            else:
                error_msg = 'No hay datos para guardar'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': error_msg})
                else:
                    messages.warning(request, error_msg)
                
        except Exception as e:
            error_msg = f'Error al guardar: {str(e)}'
            print(f"❌ Error: {error_msg}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})
            else:
                messages.error(request, error_msg)
    
    return redirect('odontograma', paciente_id=paciente.id)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import AccionDental, FotoAntes, FotoDespues

@auth_required
def nueva_accion_dental(request, paciente_id, diente_numero):
    print(f"🔍 DEBUG - Entrando a nueva_accion_dental")
    print(f"   paciente_id: {paciente_id}")
    print(f"   diente_numero: {diente_numero}")
    print(f"   method: {request.method}")
    
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        print(f"🔍 DATOS DEL FORMULARIO:")
        print(f"   título: {titulo}")
        print(f"   descripción: {descripcion}")
        
        if titulo and descripcion:
            try:
                # Crear la nueva acción
                accion = AccionDental.objects.create(
                    paciente=paciente,
                    diente_numero=diente_numero,
                    titulo=titulo,
                    descripcion=descripcion
                )
                
                print(f"✅ ACCIÓN CREADA EXITOSAMENTE:")
                print(f"   ID: {accion.id}")
                print(f"   Título: {accion.titulo}")
                print(f"   Diente: {accion.diente_numero}")
                
                # Redirección después de guardar
                return redirect('lista_acciones_dental', 
                               paciente_id=paciente.id, 
                               diente_numero=diente_numero)
                               
            except Exception as e:
                print(f"❌ ERROR al crear acción: {e}")
                # Aquí podrías mostrar un mensaje de error al usuario
        else:
            print("❌ FORMULARIO INCOMPLETO")
    
    context = {
        'paciente': paciente,
        'diente_numero': diente_numero,
    }
    return render(request, 'nueva_accion_dental.html', context)

@auth_required
def lista_acciones_dental(request, paciente_id, diente_numero):
    # DEBUG
    print(f"🔍 DEBUG lista_acciones_dental:")
    print(f"   paciente_id: {paciente_id}")
    print(f"   diente_numero: {diente_numero}")
    
    paciente = get_object_or_404(Paciente, id=paciente_id)
    acciones = AccionDental.objects.filter(
        paciente=paciente, 
        diente_numero=diente_numero
    ).order_by('-fecha_creacion')
    
    context = {
        'paciente': paciente,
        'diente_numero': diente_numero,
        'acciones': acciones,
    }
    return render(request, 'lista_acciones_dental.html', context)

@auth_required
def editar_accion_dental(request, accion_id):
    print(f"🔍 EDITANDO ACCIÓN ID: {accion_id}")
    
    accion = get_object_or_404(AccionDental, id=accion_id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        print(f"🔍 ACTUALIZANDO ACCIÓN:")
        print(f"   Nuevo título: {titulo}")
        print(f"   Nueva descripción: {descripcion}")
        
        accion.titulo = titulo
        accion.descripcion = descripcion
        accion.save()
        
        print(f"✅ ACCIÓN ACTUALIZADA")
        
        return redirect('lista_acciones_dental', 
                       paciente_id=accion.paciente.id, 
                       diente_numero=accion.diente_numero)
    
    context = {
        'accion': accion,
    }
    return render(request, 'editar_accion_dental.html', context)

@auth_required
def galeria_accion_dental(request, accion_id):
    print(f"🔍 GALERÍA ACCIÓN ID: {accion_id}")
    
    try:
        accion = get_object_or_404(AccionDental, id=accion_id)
        print(f"✅ Acción para galería: {accion.titulo}")
        
        if request.method == 'POST':
            print("🔍 📥 RECIBIENDO FORMULARIO POST...")
            print(f"🔍 Método: {request.method}")
            print(f"🔍 Content-Type: {request.content_type}")
            print(f"🔍 FILES keys: {list(request.FILES.keys())}")
            print(f"🔍 POST keys: {list(request.POST.keys())}")
            
            # Determinar qué tipo de fotos se están subiendo
            tipo_foto = request.POST.get('tipo_foto', '')
            print(f"🔍 Tipo de foto: {tipo_foto}")
            
            fotos_antes = request.FILES.getlist('fotos_antes')
            fotos_despues = request.FILES.getlist('fotos_despues')
            
            print(f"📸 Fotos ANTES: {len(fotos_antes)} archivos")
            print(f"📸 Fotos DESPUÉS: {len(fotos_despues)} archivos")
            
            subidas_realizadas = False
            tipo_subido = 'ambos'
            
            # Manejar subida de fotos ANTES
            if fotos_antes:
                for foto in fotos_antes:
                    try:
                        FotoAntes.objects.create(
                            accion=accion,
                            imagen=foto
                        )
                        print(f"✅ Foto ANTES subida: {foto.name}")
                        subidas_realizadas = True
                        tipo_subido = 'antes'
                    except Exception as e:
                        print(f"❌ Error subiendo foto ANTES {foto.name}: {e}")
            
            # Manejar subida de fotos DESPUÉS
            if fotos_despues:
                for foto in fotos_despues:
                    try:
                        FotoDespues.objects.create(
                            accion=accion,
                            imagen=foto
                        )
                        print(f"✅ Foto DESPUÉS subida: {foto.name}")
                        subidas_realizadas = True
                        tipo_subido = 'despues'
                    except Exception as e:
                        print(f"❌ Error subiendo foto DESPUÉS {foto.name}: {e}")
            
            # Redirigir solo si se subieron fotos
            if subidas_realizadas:
                from django.urls import reverse
                redirect_url = reverse('galeria_accion_dental', kwargs={'accion_id': accion.id}) + f'?subida=exito&tipo={tipo_subido}'
                print(f"🔄 Redirigiendo a: {redirect_url}")
                return redirect(redirect_url)
            else:
                print("ℹ️ No se subieron fotos, recargando página")
                return redirect('galeria_accion_dental', accion_id=accion.id)
        
        # Para GET requests, mostrar la página normal
        context = {
            'accion': accion,
        }
        return render(request, 'galeria_accion_dental.html', context)
        
    except Exception as e:
        print(f"❌ ERROR en galeria_accion_dental: {e}")
        import traceback
        print(traceback.format_exc())
        return redirect('lista_acciones_dental', paciente_id=1, diente_numero=1)
    
@auth_required
def eliminar_foto_antes(request, foto_id):
    foto = get_object_or_404(FotoAntes, id=foto_id)
    accion_id = foto.accion.id
    
    if request.method == 'POST':
        foto.delete()
        return redirect('galeria_accion_dental', accion_id=accion_id)
    
    return redirect('galeria_accion_dental', accion_id=accion_id)

@auth_required
def eliminar_foto_despues(request, foto_id):
    foto = get_object_or_404(FotoDespues, id=foto_id)
    accion_id = foto.accion.id
    
    if request.method == 'POST':
        foto.delete()
        return redirect('galeria_accion_dental', accion_id=accion_id)
    
    return redirect('galeria_accion_dental', accion_id=accion_id)

@auth_required
def mostrar_galeria_completa(request, accion_id):
    accion = get_object_or_404(AccionDental, id=accion_id)
    
    context = {
        'accion': accion,
    }
    return render(request, 'mostrar_galeria_completa.html', context)

@auth_required
def eliminar_accion_dental(request, accion_id):
    accion = get_object_or_404(AccionDental, id=accion_id)
    paciente_id = accion.paciente.id
    diente_numero = accion.diente_numero
    
    if request.method == 'POST':
        # Eliminar todas las fotos asociadas primero
        accion.fotos_antes.all().delete()
        accion.fotos_despues.all().delete()
        
        # Eliminar la acción
        accion.delete()
        
        print(f"✅ Acción dental eliminada: {accion.titulo}")
        
        # Redirigir a la lista de acciones del mismo diente
        return redirect('lista_acciones_dental', paciente_id=paciente_id, diente_numero=diente_numero)
    
    # Si no es POST, redirigir a la lista
    return redirect('lista_acciones_dental', paciente_id=paciente_id, diente_numero=diente_numero)