# security_middleware.py
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Headers de seguridad básicos
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # SOLO prevenir cache para rutas de autenticación
        # Esto evita que interfiera con la sesión de usuarios logueados
        if request.path in ['/login/', '/logout/']:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        else:
            #  Para otras rutas, permitir cache pero mantener sesión
            response['Cache-Control'] = 'private, must-revalidate'
        
        return response