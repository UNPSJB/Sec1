# Generated by Django 4.1.1 on 2022-11-17 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0002_alter_alumno_dictado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alumnos', to='cursos.curso'),
        ),
    ]