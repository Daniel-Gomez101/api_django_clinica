from rest_framework.permissions import BasePermission

# 1. El permiso que ya tenías (se queda igual)
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Lectura para cualquier usuario autenticado
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Crear, actualizar y eliminar solo para staff
        return request.user and request.user.is_staff


# 2. NUEVO: Permiso exclusivo para el rol de Médico
class IsMedicoUser(BasePermission):
    """Permite el acceso si el usuario pertenece al grupo 'Medico' o es Staff."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Pasa si es staff/admin O si pertenece al grupo Medico
        return request.user.is_staff or request.user.groups.filter(name='Medico').exists()


# 3. NUEVO: Permiso exclusivo para el rol de Paciente
class IsPacienteUser(BasePermission):
    """Permite el acceso si el usuario pertenece al grupo 'Paciente'."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        return request.user.groups.filter(name='Paciente').exists()