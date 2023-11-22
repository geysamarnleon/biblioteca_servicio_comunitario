#!/bin/bash
# Ejecuta las migraciones de la base de datos
python manage.py migrate --noinput

# Recopila los archivos estáticos
python manage.py collectstatic --noinput

# Carga los datos iniciales de la aplicación
python manage.py loaddata admin_interface_theme_biblioteca.json

# Verifica si el usuario administrador ya existe
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    # Crea el usuario administrador
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin_password',
        nombre_1='Nombre',
        apellido_1='Apellido',
        cedula='12345678',
        area=None,
        rol=None
    )

    # Agrega el usuario administrador al grupo de administradores
    # admin_group = Group.objects.get(name='Administradores')
    # admin_group.user_set.add(admin_user)

    # Guarda los cambios en la base de datos
    admin_user.save()
else:
    # El usuario administrador ya existe, no es necesario crearlo
    print("El usuario administrador ya existe.")
    
EOF

# Ejecuta el servidor de desarrollo
python manage.py runserver 0.0.0.0:8000