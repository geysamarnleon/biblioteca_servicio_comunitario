# Biblioteca de Servicio Comunitario

## Tabla de contenido

- [Acerca](#about)
- [Como empezar](#getting_started)

## Acerca <a name = "about"></a>

Este proyecto esta hecho para solucionar la problematica de la UNERG con respecto a no tener una biblioteca digital donde se pueda almacenar los proyectos de servicio comunitario para solucionar ese problema se va a estar ofreciendo la opcion de carga de proyectos y gestioanr usuarios del sistema, y facilitar la busqueda de los proyectos agregados en el sistema


## Como empezar <a name = "getting_started"></a>

En este apartado se va a ver el paso a paso que se debe seguir para poder hacer el despliegue de la aplicacion usando Docker y Docker Compose

### Prerequisitos

Las herramientas que debe tener instaladas en su sistema operativo para correr esta aplicacion son las siguientes.

```
Docker
Docker-Compose
```

### Pasos para el despliegue

Debe seguir los siguientes paso para poder hacer el despliegue de la aplicacion.

Nota: estos pasos son hechos usando el sistema operativo Ubuntu 22.04, Puede ser que en otras distribuciones o sistemas operativos cambien los comandos

#### Primero se debe hacer un build de la aplicacion y para eso se debe usar alguno el siguiente comando
```
sudo docker-compose build
```

#### Segundo Luego de hacer el build de la aplicacion debe de poner el siguiente comando ya hacer el despliegue de la aplicacion
```
sudo docker-compose up -d
```

Para acceder a la app http://localhost:8080/

Los usuarios que va a generar la aplicacion si nunca se ah hecho el despliegue es el siguiente

|Correo | Contraseña|
|-|-|
|admin@admin.com| admin_password|

Nota: Se recomienda cambiar los datos del administrador para brindar una mayor seguridad

## Configuraciones

si desea cambiar la carpeta debe acceder al codigo y cambiar la siguiente variable ubicada en el archivo
**app/core/setting**
debe buscar la siguiente variable **GOOGLE_DRIVE_STORAGE_MEDIA_ROOT="Nombre de la carpeta"**