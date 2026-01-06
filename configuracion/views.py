"""
Vistas para el módulo de configuración.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from usuarios.models import Usuario, Rol


@login_required
def index(request):
    """
    Página de configuración.
    """
    total_usuarios = Usuario.objects.count()
    total_roles = Rol.objects.filter(activo=True).count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_roles': total_roles,
    }
    
    return render(request, 'configuracion/index.html', context)

