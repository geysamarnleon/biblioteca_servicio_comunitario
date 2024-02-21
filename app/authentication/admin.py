from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from .models import Area, Programa, Rol, AuthUser, Tutores
from django.contrib.auth.models import Group
from admin_interface.models import Theme

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(Theme)
admin.site.register(Tutores)
admin.site.register(Programa)


@register(AuthUser)
class AuthUserAdmin(ModelAdmin):
    list_display = (
        "nombre_1",
        "nombre_2",
        "apellido_1",
        "apellido_2",
        "tipo_documentacion",
        "cedula",
        "area",
        "rol",
    )


@register(Rol)
class RolAdmin(ModelAdmin):
    list_display = ("nombre",)


@register(Area)
class AreaAdmin(ModelAdmin):
    list_display = ("nombre",)
