# Generated by Django 4.2.3 on 2023-07-31 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_rename_fecha_creacion_cursso_cursos_fecha_creacion_curso_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cursos',
            new_name='Curso',
        ),
        migrations.RenameModel(
            old_name='tareas',
            new_name='tarea',
        ),
        migrations.RenameField(
            model_name='tarea',
            old_name='archivo',
            new_name='archivo_pdf',
        ),
    ]