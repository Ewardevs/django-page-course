# Generated by Django 4.2.3 on 2023-08-01 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_alter_tarea_archivo_pdf_tarea_hecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea_hecha',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Entregado', 'Entregado')], default=('Pendiente', 'Pendiente'), max_length=100, null=True),
        ),
    ]