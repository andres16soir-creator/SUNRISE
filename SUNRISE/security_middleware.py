# security_middleware.py - VERSIÓN CORREGIDA
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import sys
import os

# Agregar ruta para importar
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from .codigo_instalacion import codigo_manager
except ImportError:
    print("⚠️ No se pudo importar codigo_manager")
    codigo_manager = None

class CodigoInstalacionMiddleware(MiddlewareMixin):
    """Middleware que verifica si se ingresó el código de instalación"""
    
    def process_request(self, request):
        # Si no tenemos el manager, permitir acceso
        if not codigo_manager:
            return None
        
        # URLs que NO requieren verificación
        urls_permitidas = [
            '/instalar/',
            '/static/',
            '/media/',
            '/login/',      # Para que pueda acceder al login
            '/paciente/',   # Para permitir acceso al odontograma y detalle de pacientes
            '/odontograma/',# Por si acaso
        ]
        
        # Verificar si la URL actual está permitida
        for url in urls_permitidas:
            if request.path.startswith(url):
                return None
        
        # Si YA está instalado, permitir acceso normal
        if codigo_manager.ya_esta_instalado():
            return None
        
        # Si NO está instalado, redirigir a página de instalación
        return HttpResponseRedirect('/instalar/')

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware para cabeceras de seguridad"""
    
    def process_response(self, request, response):
        # Cabeceras de seguridad básicas
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Control de caché para páginas sensibles
        if request.path in ['/login/', '/logout/', '/instalar/']:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        else:
            response['Cache-Control'] = 'private, must-revalidate'
        
        return response