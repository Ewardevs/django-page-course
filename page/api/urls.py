from django.urls import path
from .api import UserApiView

urlpatterns = [
    path("", UserApiView, name="users")
]
