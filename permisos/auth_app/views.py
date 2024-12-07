from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm
from .models import Car

# Vista protegida que requiere que el usuario esté autenticado.
# Muestra un listado de autos disponibles en la base de datos.
@login_required
def dashboard(request):
    cars = Car.objects.all()  # Obtener todos los autos. Podrías filtrar según el usuario si fuera necesario.
    return render(request, 'auth_app/dashboard.html', {'user': request.user, 'cars': cars})

# Vista basada en clases para editar autos. 
# Protegida por permisos específicos (se necesita el permiso 'edit_car').
class EditCarView(PermissionRequiredMixin, TemplateView):
    permission_required = 'auth_app.edit_car'  # Permiso requerido para acceder a esta vista.
    template_name = 'auth_app/edit_car.html'  # Plantilla para editar autos.

# Vista para registrar usuarios.
# Incluye lógica para autenticar al usuario recién registrado y redirigir al dashboard.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # TODO: Asignar permisos al usuario según la selección en el formulario.
            # Se debe modificar UserRegistrationForm para incluir un campo de selección de permisos.

            login(request, user)  # Autenticar automáticamente al usuario registrado.
            return redirect('dashboard')  # Redirigir al dashboard.
    else:
        form = UserRegistrationForm()
    return render(request, 'auth_app/register.html', {'form': form})

# Vista de login personalizada.
# Permite utilizar una plantilla específica para la página de inicio de sesión.
class CustomLoginView(LoginView):
    template_name = 'auth_app/login.html'

# Vista para editar un auto específico.
# Obtiene el auto por ID y permite actualizar sus datos.
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # Obtener el objeto Car o retornar 404 si no existe.
    if request.method == 'POST':
        # Actualizar los campos del auto con los datos enviados en el formulario.
        car.model = request.POST['model']
        car.year = request.POST['year']
        car.save()  # Guardar los cambios en la base de datos.
        return redirect('dashboard')  # Redirigir al dashboard después de guardar.
    return render(request, 'auth_app/edit_car.html', {'car': car})  # Mostrar formulario de edición.

def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('/login/')  # Redirige manualmente a /login/