from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import *

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
        return HttpResponse("hola")
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
    tareas = Tarea_hecha.objects.filter(
        id_alumno=request.user, id_tarea__curso__nombre_curso=id_curso)
    if tareas:
        return render(request, "tareas.html", {
            "tareas": tareas
        })
    else:
        return redirect("home")


@login_required
def enviar_tarea(request):
    cargar_tarea = Tarea_hecha.objects.filter(
        id=request.POST["id"]).update(tarea=request.POST["pdf_file"], estado="Entregado")
    return redirect("home")


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
