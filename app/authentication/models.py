from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class Area(models.Model):
    nombre = models.CharField("Nombre del area", unique=True)

    def __str__(self):
        return self.nombre


class Programa(models.Model):
    nombre = models.CharField("Nombre del programa", unique=True)
    area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


class Tutores(models.Model):
    nombre_1 = models.CharField("Primer Nombre", max_length=50, blank=True, null=True)
    nombre_2 = models.CharField("Segundo Nombre", max_length=50, blank=True, null=True)
    apellido_1 = models.CharField("Primer Apellido", max_length=50, blank=True, null=True)
    apellido_2 = models.CharField("Segundo Apellido", max_length=50, blank=True, null=True)

    tipo_documentacion = models.CharField(max_length=1, choices=[("V", "Venezolano")], default="V")
    cedula = models.CharField("Cedula", max_length=8, unique=True, blank=True, null=True)

    area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre_1 + " " + self.apellido_1

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"


class Rol(models.Model):
    nombre = models.CharField("Nombre del rol administrativo", unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class AuthUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=250, unique=True)

    nombre_1 = models.CharField("Primer Nombre", max_length=50)
    nombre_2 = models.CharField("Segundo Nombre", max_length=50)
    apellido_1 = models.CharField("Primer Apellido", max_length=50)
    apellido_2 = models.CharField("Segundo Apellido", max_length=50)

    tipo_documentacion = models.CharField(max_length=1, choices=[("V", "Venezolano")], default="V")
    cedula = models.CharField("Cedula", max_length=8, unique=True)

    email = models.EmailField("Correo Electronico", unique=True, max_length=255)

    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["tipo_documentacion", "cedula", "username"]

    objects = UserManager()

    def __str__(self):
        return "{} {}, C.I{}, Area: {}, Rol: {}".format(self.nombre_1, self.apellido_1, self.cedula, self.area, self.rol)


@receiver(pre_save, sender=AuthUser)
def pre_save_auth(sender, instance, **kwargs):
    # Verifica si el usuario es un superusuario y evita hashear su contraseña automáticamente
    if instance.is_superuser:
        return

    if instance.pk is None:
        # Es un nuevo usuario, por lo que se debe hashear la contraseña
        instance.password = make_password(instance.password)
    else:
        # Es un usuario existente, por lo que se debe verificar si la contraseña ha sido actualizada
        try:
            user = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass  # El usuario no existe todavía
        else:
            if user.password != instance.password:
                # La contraseña ha sido actualizada, por lo que se debe hashear la nueva contraseña
                instance.password = make_password(instance.password)
