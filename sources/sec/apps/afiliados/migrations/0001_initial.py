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
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuit', models.CharField(max_length=13)),
                ('razonSocial', models.CharField(max_length=50)),
                ('rama', models.CharField(max_length=50)),
                ('domicilio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Afiliado',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='personas.rol')),
                ('cuil', models.CharField(max_length=13)),
                ('nacionalidad', models.CharField(max_length=50)),
                ('estadoCivil', models.CharField(max_length=50)),
                ('domicilio', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('ingresoTrabajo', models.DateField()),
                ('sueldo', models.FloatField(max_length=50)),
                ('jornadaLaboral', models.CharField(max_length=50)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afiliados.empresa')),
            ],
            bases=('personas.rol',),
        ),
    ]
