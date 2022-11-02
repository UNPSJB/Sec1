# Generated by Django 4.1.1 on 2022-10-31 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroAula', models.PositiveIntegerField(max_length=30)),
                ('capacidad', models.PositiveIntegerField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
                ('fechaDesde', models.DateField()),
                ('fechaHasta', models.DateField()),
                ('cupo', models.IntegerField(max_length=2)),
                ('modulos', models.IntegerField(max_length=2)),
                ('descuento', models.IntegerField(max_length=2)),
                ('precio', models.IntegerField(max_length=4)),
                ('pagos', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
                ('dni', models.CharField(max_length=8)),
                ('nombre', models.CharField(max_length=20)),
                ('apellido', models.CharField(max_length=20)),
                ('domicilio', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=20)),
                ('añosExperiencia', models.IntegerField(max_length=2)),
                ('especializacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.especialidad')),
            ],
            bases=('personas.rol',),
        ),
        migrations.CreateModel(
            name='Titularidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaDesde', models.DateField()),
                ('fechaHasta', models.DateField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.profesor')),
            ],
        ),
        migrations.CreateModel(
            name='Dictado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo', models.FloatField(max_length=10)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('aula', models.ManyToManyField(to='cursos.aula')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='especialidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.especialidad'),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesores',
            field=models.ManyToManyField(through='cursos.Titularidad', to='cursos.profesor'),
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
            ],
            bases=('personas.rol',),
        ),
    ]
