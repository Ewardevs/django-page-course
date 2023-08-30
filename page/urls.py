from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # Vista Login, Logout , Register
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout_user, name="logout"),
    # Vista Alumno
    path('cursos', views.cursos, name="cursos"),
    path('enviar_tarea/<str:nombre>', views.enviar_tarea, name="enviar_tarea"),
    path('puntajes', views.mostrar_puntaje, name="puntajes"),
    path('desinscribirse/<int:id>', views.dar_de_baja, name="desinscribirse"),
    path('inscribirse/<int:id>', views.inscribirse, name="inscribirse"),
    # Vista Docente
    path('tabla/<int:id_curso>', views.tabla, name="tabla"),
    path('crear_tarea/', views.crear_tarea, name="crear_tarea"),
    path('eliminar_tarea', views.eliminar_tarea, name="eliminar_tarea"),
    path('lista_completado/<int:id_tarea>',
         views.lista_completados, name="lista_completado"),
    path('lista_completado/alumno/<int:id_tarea>',
         views.corregir_tarea, name="corregir"),
    # Vista Compartida
    path('', views.home, name="home"),
    path('tarea/<str:id_curso>', views.mostrar_tarea, name="tarea"),


]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT})
]
