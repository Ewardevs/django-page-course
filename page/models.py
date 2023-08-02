from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[(
        'admin', 'Admin'), ('docente', 'Docente'), ('alumno', 'Alumno')], default='alumno')
    # Otros campos adicionales que desees agregar para el rol

    def __str__(self):
        return self.user.username


class Curso(models.Model):
    img_curso = models.FileField(upload_to="imgs/", default=True)
    nombre_curso = models.CharField(max_length=50)
    descripcion_curso = models.CharField(max_length=250)
    fecha_inicio_curso = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    fecha_fin_curso = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_creacion_curso = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.nombre_curso


class Tarea(models.Model):
    titulo_tarea = models.CharField(max_length=50)
    descripcion_tarea = models.CharField(max_length=250)
    archivo_pdf = models.FileField(upload_to="pdfs/", blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    puntos = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(100)])

    def __str__(self):
        return self.titulo_tarea


class Inscripcion(models.Model):
    id_alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['id_alumno', 'id_curso']

    def __str__(self):
        return self.id_alumno.username + " esta inscripto en " + self.id_curso.nombre_curso


class Tarea_hecha(models.Model):
    ESTADOS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Entregado', 'Entregado'),
    ]
    id_alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    tarea = models.FileField("pdfs/alumno/", blank=True)
    puntos_hechos = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)])
    estado = models.CharField(
        max_length=100, null=True, choices=ESTADOS_CHOICES, default=ESTADOS_CHOICES[0])

    def __str__(self):
        return self.id_alumno.username + " tiene "+self.estado+" la tarea con nombre "+self.id_tarea.titulo_tarea+" del  curso "+self.id_tarea.curso.nombre_curso


@receiver(post_save, sender=Tarea)
def crear_tarea_hecha(sender, instance, created, **kwargs):
    if created:
        alumnos_inscritos = Inscripcion.objects.filter(id_curso=instance.curso)
        for alumno_inscrito in alumnos_inscritos:
            # Verificar si el usuario está inscrito antes de crear Tarea_hecha
            if alumno_inscrito.id_alumno:
                tarea_hecha = Tarea_hecha.objects.create(
                    id_alumno=alumno_inscrito.id_alumno,
                    id_tarea=instance,
                    estado='Pendiente',  # O puedes cambiar el estado predeterminado si lo deseas
                )
                tarea_hecha.save()


@receiver(post_save, sender=Inscripcion)
def crear_tareas_hechas_al_inscribirse(sender, instance, created, **kwargs):
    if created:
        tareas_del_curso = Tarea.objects.filter(curso=instance.id_curso)
        for tarea in tareas_del_curso:
            tarea_hecha = Tarea_hecha.objects.create(
                id_alumno=instance.id_alumno,
                id_tarea=tarea,
                estado='Pendiente',  # O puedes cambiar el estado predeterminado si lo deseas
            )
            tarea_hecha.save()


@receiver(post_delete, sender=Inscripcion)
def Eliminar_tareas_hechas(sender, instance, **kwargs):
    tareas_del_curso = Tarea_hecha.objects.filter(id_alumno=instance.id_alumno)
    for tarea in tareas_del_curso:
        tarea.delete()
