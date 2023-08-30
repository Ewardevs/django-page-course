from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail

from Cursos.settings import EMAIL_HOST_USER


# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    elif request.method == "GET":
        return render(request, 'login.html')
    else:
        user = authenticate(request,
                            username=request.POST["username"],
                            password=request.POST["password"])
        if user is None:
            return render(request, 'login.html', {
                "error": 'Usuario o Contraseña no existen'
            })
        else:
            auth_login(request, user)
            return redirect("home")


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "GET":
            return render(request, "register.html")
        else:
            if request.POST["password1"] == request.POST["password2"]:
                try:
                    user = User.objects.create_user(
                        username=request.POST["username"],
                        password=request.POST["password1"]
                    )
                    user.save()
                    auth_login(request, user)
                    return redirect("home")
                except IntegrityError:
                    return render(request, "register.html", {
                        "error": 'Usuario actualmente existe'
                    })
            else:
                return render(request, "register.html", {
                    "error": 'Contraseñas no coinciden'
                })


@login_required
def home(request):
    is_user = get_object_or_404(UserRole, user=request.user)
    if is_user.role == "docente":
        cursos = Curso.objects.filter(docente=request.user)
        return render(request, "vista_docente/home.html", {
            "cursos": cursos
        })

    elif is_user.role == "alumno":
        cursos_inscriptos = Inscripcion.objects.filter(id_alumno=request.user)
        print(request.user.id)
        return render(request, "home.html", {
            "cursos": cursos_inscriptos,
        })


@login_required
def cursos(request):
    cursos_inscriptos = Inscripcion.objects.filter(id_alumno=request.user)
    cursos = Curso.objects.exclude(
        id__in=cursos_inscriptos.values_list("id_curso", flat=True))
    return render(request, "cursos.html", {
        "cursos": cursos,

    })


@login_required
def inscribirse(request, id):
    is_user = UserRole.objects.filter(user=request.user, role="alumno")
    if is_user:
        curso = get_object_or_404(Curso, id=id)
        incripcion = Inscripcion.objects.create(
            id_alumno=request.user, id_curso=curso)
        incripcion.save()
        send_mail(
            f'aviso de suscripcion',
            f'gracias {request.user} por la suscripcion a {curso.nombre_curso}',
            EMAIL_HOST_USER,
            ['alexanderovelarela@gmail.com'],
            fail_silently=False,
        )

        return redirect("home")
    else:
        return render(request, "cursos.html", {
            "error": 'No es alumno'
        })


@login_required
def dar_de_baja(request, id):
    inscripto = get_object_or_404(Inscripcion, id=id)
    inscripto.delete()
    return redirect("home")


@login_required
def mostrar_tarea(request, id_curso):
    is_user = get_object_or_404(UserRole, user=request.user)
    if is_user.role == "docente":
        tareas = Tarea.objects.filter(
            curso__docente=request.user,
            curso__nombre_curso=id_curso)

        curso = get_object_or_404(Curso, nombre_curso=id_curso)
        if len(tareas) > 0:
            return render(request, "vista_docente/tareas.html", {
                "curso": curso,
                "tareas": tareas
            })
        else:
            curso = get_object_or_404(Curso, nombre_curso=id_curso)
            return render(request, "vista_docente/tareas.html", {
                "curso": curso,
                "error": "no hay tareas"
            })

    elif is_user.role == "alumno":
        tareas = Tarea_hecha.objects.filter(
            id_alumno=request.user, id_tarea__curso__nombre_curso=id_curso)
        if len(tareas) > 0:
            return render(request, "tareas.html", {
                "tareas": tareas
            })
        else:
            return render(request, "tareas.html", {
                "tareas": tareas,
                "error": "no hay tareas"
            })


@login_required
def enviar_tarea(request, nombre):
    cargar_tarea = Tarea_hecha.objects.filter(
        id=request.POST["id"]).update(tarea=request.POST["pdf_file"], estado="Entregado")
    return redirect("tarea", nombre)


@login_required
def mostrar_puntaje(request):
    cursos_inscriptos = Inscripcion.objects.filter(id_alumno=request.user)
    puntajes = Tarea_hecha.objects.filter(id_alumno=request.user)
    lista = []
    dato = {}
    for curso in cursos_inscriptos:
        dato = {"id_curso": curso.id_curso.id,
                "curso": curso.id_curso.nombre_curso, "puntaje": 0, "tareas_pendientes": 0, "tareas_entregadas": 0, "tareas_corregidas": 0}
        for puntaje in puntajes:
            if puntaje.id_tarea.curso.id == curso.id_curso.id:
                if puntaje.estado == "Pendiente":
                    dato["tareas_pendientes"] += 1
                elif puntaje.estado == "Entregado":
                    dato["tareas_entregadas"] += 1
                elif puntaje.estado == "Corregido":
                    dato["tareas_corregidas"] += 1
                if puntaje.puntos_hechos is not None:
                    dato["puntaje"] += puntaje.puntos_hechos
        lista.append(dato)
    return render(request, "puntajes.html", {
        "puntajes": lista,
        "tareas": puntajes

    })


@login_required
def tabla(request, id_curso):
    cursos_inscriptos = Inscripcion.objects.filter(
        id_curso__docente=request.user, id_curso_id=id_curso)
    puntajes = Tarea_hecha.objects.filter(
        id_tarea__curso__docente=request.user, id_tarea__curso__id=id_curso)
    lista = []
    dato = {}
    for curso in cursos_inscriptos:
        dato = {"id_curso": curso.id_curso.id, "alumno": curso.id_alumno.username,
                "curso": curso.id_curso.nombre_curso, "puntaje": 0, "tareas_pendientes": 0, "tareas_entregadas": 0, "tareas_corregidas": 0}
        for puntaje in puntajes:
            if curso.id_alumno.id == puntaje.id_alumno.id:
                if puntaje.id_tarea.curso.id == curso.id_curso.id:
                    if puntaje.estado == "Pendiente":
                        dato["tareas_pendientes"] += 1
                    elif puntaje.estado == "Entregado":
                        dato["tareas_entregadas"] += 1
                    elif puntaje.estado == "Corregido":
                        dato["tareas_corregidas"] += 1
                    if puntaje.puntos_hechos is not None:
                        dato["puntaje"] += puntaje.puntos_hechos
        lista.append(dato)
    return render(request, "vista_docente/puntaje_alumnos.html", {
        "alumnos": lista,
    })


@login_required
def crear_tarea(request):
    curso = get_object_or_404(Curso, nombre_curso=request.POST["id_curso"])
    tarea_nueva = Tarea.objects.create(
        titulo_tarea=request.POST["titulo_tarea"],
        descripcion_tarea=request.POST["descripcion_tarea"],
        archivo_pdf=request.POST["archivo_pdf"],
        puntos=request.POST["puntos"],
        curso_id=curso.id
    )
    tarea_nueva.save()
    return redirect("tarea", request.POST["id_curso"])


@login_required
def eliminar_tarea(request):
    tarea_eliminada = get_object_or_404(Tarea, pk=request.POST["id"])
    tarea_eliminada.delete()

    return redirect("home")


@login_required
def lista_completados(request, id_tarea):
    alumnos = Tarea_hecha.objects.filter(
        id_tarea=id_tarea
    )

    return render(request, "vista_docente/lista_completado.html", {
        "lista": alumnos
    })


@login_required
def corregir_tarea(request, id_tarea):
    tarea = get_object_or_404(Tarea_hecha, id=id_tarea)

    if request.method == "GET":
        return render(request, "vista_docente/alumno.html", {
            "tarea": tarea
        })
    else:
        tarea.puntos_hechos = int(request.POST["puntos"])
        tarea.save()
        return redirect("home")
