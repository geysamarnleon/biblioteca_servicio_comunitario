import uuid
from django.db import models
from django.core.validators import FileExtensionValidator


from authentication.models import AuthUser, Area, Programa, Tutores
from gdstorage.storage import GoogleDriveStorage

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .utils.driver_connection import get_id_from_url, get_drive_service, change_file_settings, delete_file

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

periodo = []

for i in range(2000, 2051):
    periodo.extend([(f"{i}-1", f"{i}-1")])
    periodo.extend([(f"{i}-2", f"{i}-2")])


class Project_SC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    tematica = models.CharField(max_length=200)

    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True)
    programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, blank=True, null=True)
    tutor = models.ForeignKey(Tutores, on_delete=models.SET_NULL, blank=True, null=True)
    periodo = models.CharField("Periodos del area", choices=periodo, null=False, blank=False, max_length=6)

    tipo_proyecto = models.CharField(
        max_length=4, choices=[("SC", "Servicio Comunitario"), ("PreG", "Pre-Grado"), ("PosG", "Post-Grado")], default="SC"
    )

    coordinador = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, blank=True, null=True)

    resumen = models.TextField(blank=True, null=True)
    ubicacion_servicio = models.CharField(max_length=200)

    file = models.FileField(
        upload_to="./proyectos",
        storage=gd_storage,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "png", "jpg"])],
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Proyecto de servicio comunitario"
        verbose_name_plural = "Proyectos de servicio comunitario"


@receiver(pre_save, sender=Project_SC)
def delete_file_before(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(id=instance.id)

        if obj.file.url:
            file_id = get_id_from_url(obj.file.url)
            service = get_drive_service()
            delete_file(service, file_id)

    except:
        pass


@receiver(post_save, sender=Project_SC)
def change_config_file_drive(sender, instance, **kwargs):
    if instance.file.url:
        file_id = get_id_from_url(instance.file.url)
        service = get_drive_service()
        change_file_settings(service, file_id)


@receiver(post_delete, sender=Project_SC)
def delete_file_drive(sender, instance, **kwargs):
    file_id = get_id_from_url(instance.file.url)
    service = get_drive_service()
    delete_file(service, file_id)
