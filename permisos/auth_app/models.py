from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Modelo de usuario personalizado
class CustomUser(AbstractUser):
    # Agregar un campo opcional para asignar un rol o tipo de permiso
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Admin'),
            ('editor', 'Editor'),
            ('viewer', 'Viewer'),
        ],
        blank=True,  # Opcional
        null=True,
        help_text="Rol del usuario para determinar sus permisos.",
    )

# Modelo para representar autos con permisos específicos
class Car(models.Model):
    model = models.CharField(max_length=100, help_text="Modelo del auto.")
    year = models.IntegerField(help_text="Año de fabricación del auto.")

    class Meta:
        permissions = [
            ('edit_car', 'Can edit car'),
            ('view_car_details', 'Can view car details'),
        ]