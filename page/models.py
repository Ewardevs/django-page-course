from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[(
        'admin', 'Admin'), ('docente', 'Docente'), ('alumno', 'Alumno')], default='alumno')
    # Otros campos adicionales que desees agregar para el rol

    def __str__(self):
        return self.user.username


class Curso(models.Model):
    img_curso = models.FileField(upload_to="imgs/")
    docente = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_curso = models.CharField(max_length=50)
    descripcion_curso = models.TextField()
    fecha_inicio_curso = models.DateTimeField(
        auto_now=False, auto_now_add=False)
    fecha_fin_curso = models.DateTimeField(auto_now=False, auto_now_add=False)
    fecha_creacion_curso = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    def clean(self):
        # Validación para asegurarse de que solo los docentes puedan ser asignados al curso
        if self.docente.userrole.role != 'docente':
            raise ValidationError(
                "El docente asignado debe tener el rol de 'Docente'")

    def __str__(self):
        return self.nombre_curso


class Tarea(models.Model):
    titulo_tarea = models.CharField(max_length=50)
    descripcion_tarea = models.TextField(max_length=250)
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
        ('Corregido', 'Corregido'),
    ]
    id_alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    tarea = models.FileField("pdfs/alumno/", blank=True)
    puntos_hechos = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)])
    estado = models.CharField(
        max_length=100, null=True, choices=ESTADOS_CHOICES, default=ESTADOS_CHOICES[0])

    def __str__(self) -> str:
        return self.id_alumno.username + " "+self.id_tarea.titulo_tarea


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
    tareas_del_curso = Tarea_hecha.objects.filter(
        id_alumno=instance.id_alumno, id_tarea__curso=instance.id_curso)
    for tarea in tareas_del_curso:
        tarea.delete()


@receiver(post_save, sender=User)
def crear_rol(sender, instance, created, **kwargs):
    if created:
        rol = UserRole.objects.create(
            user=instance, role="alumno")
        rol.save()


@receiver(post_save, sender=Tarea_hecha)
def completar_tarea_al_recibir_puntaje(sender, instance, **kwargs):
    if instance.puntos_hechos != None:
        instance.estado = "Entregado"


@receiver(pre_save, sender=Tarea_hecha)
def cambiar_estado_si_puntaje(sender, instance, **kwargs):
    if instance.puntos_hechos is not None and instance.puntos_hechos >= 0:
        instance.estado = 'Corregido'


# Registrar la señal
pre_save.connect(cambiar_estado_si_puntaje, sender=Tarea_hecha)
