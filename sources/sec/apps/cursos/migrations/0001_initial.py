# Generated by Django 4.1.1 on 2022-11-14 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
            ],
            bases=('personas.rol',),
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(max_length=2)),
                ('capacidad', models.PositiveIntegerField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('desde', models.DateField()),
                ('hasta', models.DateField()),
                ('cupo', models.PositiveIntegerField(max_length=20)),
                ('cantModulos', models.PositiveIntegerField(max_length=20)),
                ('descuento', models.PositiveIntegerField(max_length=2)),
                ('precio', models.PositiveIntegerField(max_length=4)),
                ('formaPago', models.PositiveSmallIntegerField(choices=[(0, 'Clase'), (1, 'Mensual')])),
            ],
        ),
        migrations.CreateModel(
            name='Dictado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo', models.FloatField(max_length=10)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('aula', models.ManyToManyField(to='cursos.aula')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('area', models.PositiveSmallIntegerField(choices=[(0, 'Capacitacion'), (1, 'Cultura'), (2, 'Gimnasio')])),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
                ('domicilio', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=13)),
                ('aniosExperiencia', models.PositiveIntegerField(max_length=2)),
                ('cbu', models.PositiveIntegerField(max_length=22)),
                ('especializacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.especialidad')),
            ],
            bases=('personas.rol',),
        ),
        migrations.CreateModel(
            name='Titularidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.DateField()),
                ('hasta', models.DateField(blank=True, null=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.profesor')),
            ],
        ),
        migrations.CreateModel(
            name='PagoDictado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pago', models.DateField()),
                ('monto', models.FloatField(max_length=10)),
                ('tipoPago', models.PositiveSmallIntegerField(choices=[(0, 'Debito'), (1, 'Credito'), (2, 'Efectivo')])),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.alumno')),
                ('dictado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.dictado')),
            ],
        ),
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liquidacion', models.DateField()),
                ('monto', models.FloatField(max_length=4)),
                ('titular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.titularidad')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='especialidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.especialidad'),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesor',
            field=models.ManyToManyField(through='cursos.Titularidad', to='cursos.profesor'),
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.TimeField()),
                ('fin', models.TimeField()),
                ('dia', models.PositiveSmallIntegerField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes')])),
                ('dictado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.dictado')),
            ],
        ),
        migrations.CreateModel(
            name='AsistenciaProfesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asistencia', models.DateField()),
                ('titular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.titularidad')),
            ],
        ),
        migrations.AddField(
            model_name='alumno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='dictado',
            field=models.ManyToManyField(through='cursos.PagoDictado', to='cursos.dictado'),
        ),
    ]
