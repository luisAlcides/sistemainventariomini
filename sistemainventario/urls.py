"""
URL configuration for sistemainventario project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard principal
    path('', core_views.dashboard, name='dashboard'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Apps
    path('facturacion/', include('facturacion.urls')),
    path('inventario/', include('inventario.urls')),
    path('catalogos/', include('catalogos.urls')),
    path('reportes/', include('reportes.urls')),
    path('configuracion/', include('configuracion.urls')),
]

