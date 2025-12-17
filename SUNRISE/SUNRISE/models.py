from django.db import models
from django.core.exceptions import ValidationError
from datetime import time
from django.db.models import Q 

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')], default='masculino')
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # HISTORIAL CLÍNICO - Campos existentes
    motivo_consulta = models.TextField(blank=True, null=True)
    enfermedad_actual = models.TextField(blank=True, null=True)
    antecedentes_familiares_patologicos = models.TextField(blank=True, null=True)
    
    # ANTECEDENTES PERSONALES PATOLÓGICOS (Checkboxes)
    anemia = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    cardiopatias = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    diabetes = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    enf_gastricas = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    epilepsia = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    hipertencion = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    vih = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    observaciones_patologicos = models.TextField(blank=True, null=True)
    
    # PREGUNTAS MÉDICAS (con campos de texto condicionales)
    tratamiento_medico_actual = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    tratamiento_medico_desc = models.TextField(blank=True, null=True)
    
    toma_medicamentos = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    medicamentos_desc = models.TextField(blank=True, null=True)
    
    alergias = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    alergias_desc = models.TextField(blank=True, null=True)
    
    intervencion_quirurgica = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    intervencion_quirurgica_desc = models.TextField(blank=True, null=True)
    
    reaccion_anestecia = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    reaccion_anestecia_desc = models.TextField(blank=True, null=True)
    
    hemorragia_exodoncia = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    hemorragia_exodoncia_desc = models.TextField(blank=True, null=True)
    
    alteraciones_cicatrizacion = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    alteraciones_cicatrizacion_desc = models.TextField(blank=True, null=True)
    
    embarazada = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    embarazada_desc = models.TextField(blank=True, null=True)
    
    # ANTECEDENTES PERSONALES NO PATOLÓGICOS
    fuma = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    bebe = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    respiracion_bucal = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    queilofagia = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    onicofagia = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    bruxismo = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    mastica_coca = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    mastica_chicle = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    mordisqueo_objetos = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    
    # SI ES MENOR DE EDAD
    uso_biberon = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    uso_chupon = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    succion_dedo = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')

    # VALORACIÓN DE HIGIENE DENTO-BUCAL
    higiene_bucal = models.CharField(max_length=10, choices=[('mala', 'Mala'), ('regular', 'Regular'), ('buena', 'Buena'), ('pendiente', 'Pendiente')], default='pendiente')
    frecuencia_cepillado = models.CharField(max_length=100, blank=True, null=True)
    cambio_cepillo = models.CharField(max_length=100, blank=True, null=True)
    suburra = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    materia_alba = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    placa_bacteriana = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    tartaro = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')
    halitosis = models.CharField(max_length=10, choices=[('si', 'Sí'), ('no', 'No'), ('pendiente', 'Pendiente')], default='pendiente')

    # CAMPO ODONTOGRAMA - SOLO UNA VEZ
    odontograma_data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
      
class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dentista = models.CharField(max_length=100, default='Dr. Principal')
    motivo = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('programada', 'Programada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ], default='programada')
    
    def clean(self):
        # Validar que no haya citas que se solapen
        citas_solapadas = Cita.objects.filter(
            fecha=self.fecha
        ).exclude(id=self.id).filter(
            Q(hora_inicio__lt=self.hora_fin, hora_fin__gt=self.hora_inicio)
        )
        
        if citas_solapadas.exists():
            raise ValidationError('Ya existe una cita programada que se solapa con este horario')
        
        # Validar que hora_fin sea mayor que hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError('La hora de fin debe ser posterior a la hora de inicio')
    
    def __str__(self):
        return f"{self.paciente.nombre} - {self.fecha} {self.hora_inicio}"

class Tratamiento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    materiales = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class FotoTratamiento(models.Model):
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='tratamientos/')
    descripcion = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Foto de {self.tratamiento.titulo}"

class InformacionAdicional(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='informacion_adicional')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.paciente.nombre}"

class FotoInformacion(models.Model):
    informacion = models.ForeignKey(InformacionAdicional, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='informacion_pacientes/')
    descripcion = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Foto de {self.informacion.titulo}"
    
class AccionDiente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='acciones_dientes')
    numero_diente = models.IntegerField()
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diente {self.numero_diente} - {self.titulo}"

class FotoAccionDiente(models.Model):
    TIPO_FOTO = [
        ('antes', 'Antes'),
        ('despues', 'Después'),
    ]
    
    accion_diente = models.ForeignKey(AccionDiente, on_delete=models.CASCADE, related_name='fotos')
    tipo_foto = models.CharField(max_length=10, choices=TIPO_FOTO)
    imagen = models.ImageField(upload_to='acciones_dientes/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_foto_display()} - {self.accion_diente.titulo}"
    
class AccionDental(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='acciones_dentales')
    diente_numero = models.IntegerField()
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diente {self.diente_numero} - {self.titulo}"

class FotoAntes(models.Model):
    accion = models.ForeignKey(AccionDental, on_delete=models.CASCADE, related_name='fotos_antes')
    imagen = models.ImageField(upload_to='acciones_dentales/antes/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Antes - {self.accion.titulo}"

class FotoDespues(models.Model):
    accion = models.ForeignKey(AccionDental, on_delete=models.CASCADE, related_name='fotos_despues')
    imagen = models.ImageField(upload_to='acciones_dentales/despues/')
    descripcion = models.CharField(max_length=200, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Después - {self.accion.titulo}"