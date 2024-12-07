from django.contrib.auth.models import Permission, Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    # Campo para seleccionar un rol (opcional)
    role = forms.ChoiceField(
        choices=[
            ('admin', 'Admin'),
            ('editor', 'Editor'),
            ('viewer', 'Viewer'),
        ],
        required=False,
        help_text="Selecciona el rol del usuario.",
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Guardar el usuario
        if commit:
            user.save()

            # Asignar permisos o grupo basado en el rol seleccionado
            role = self.cleaned_data.get('role')
            if role == 'admin':
                user.is_staff = True  # Permitir acceso al panel de administración
                user.is_superuser = True  # Acceso total como superusuario
            elif role == 'editor':
                user.is_staff = True  # Acceso parcial al panel de administración
                # Asignar el permiso 'edit_car' al editor
                try:
                    permission = Permission.objects.get(codename='edit_car')
                    user.user_permissions.add(permission)
                except Permission.DoesNotExist:
                    print("Permission 'edit_car' does not exist. Ensure migrations are applied.")
            elif role == 'viewer':
                # Agregar al grupo 'Viewers' si no necesita permisos individuales
                viewer_group, created = Group.objects.get_or_create(name='Viewers')
                viewer_group.user_set.add(user)

            # Guardar cambios en el usuario
            user.save()

        return user