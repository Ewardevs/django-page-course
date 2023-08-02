from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import UserRole


class UserProfileInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# Register your models here
admin.site.register(Curso)
admin.site.register(Tarea)
admin.site.register(Tarea_hecha)
admin.site.register(Inscripcion)
admin.site.register(UserRole)
