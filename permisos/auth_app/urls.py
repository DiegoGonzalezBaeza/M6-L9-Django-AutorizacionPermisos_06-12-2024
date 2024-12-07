from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Ruta para la vista de login personalizada.
    # Utiliza la clase CustomLoginView que define una plantilla específica para el inicio de sesión.
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # Ruta para la vista de registro.
    # Permite registrar nuevos usuarios y asignarles permisos específicos.
    path('register/', views.register, name='register'),

    # Ruta para la vista del dashboard.
    # Protegida por el decorador @login_required para que solo usuarios autenticados accedan.
    path('dashboard/', views.dashboard, name='dashboard'),

    # Ruta para la edición de autos.
    # Permite editar un auto específico por ID; considera el manejo de permisos en la lógica de la vista.
    path('edit-car/<int:car_id>/', views.edit_car, name='edit_car'),

    # Ruta para el cierre de sesión (logout).
    # Usa la vista genérica LogoutView incluida en Django.
    path('logout/', views.custom_logout, name='logout'),
]