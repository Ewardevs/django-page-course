from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('cursos', views.cursos, name="cursos"),
    path('tarea/<str:id_curso>', views.mostrar_tarea, name="tarea"),
    path('enviar_tarea', views.enviar_tarea, name="enviar_tarea"),
    path('inscribirse/<int:id>', views.inscribirse, name="inscribirse"),
    path('desinscribirse/<int:id>', views.dar_de_baja, name="desinscribirse"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login")
]
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT})
]
