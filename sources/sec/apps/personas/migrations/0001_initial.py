# Generated by Django 4.1.1 on 2022-12-02 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('nacimiento', models.DateField()),
                ('domicilio', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('es_afiliado', models.BooleanField(default=False)),
                ('es_alumno', models.BooleanField(default=False)),
                ('es_profesor', models.BooleanField(default=False)),
                ('es_encargado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vinculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'Conyuge'), (1, 'Hijo'), (2, 'Tutor'), (3, 'Padre'), (4, 'Madre')])),
                ('vinculado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vinculantes', to='personas.persona')),
                ('vinculante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vinculados', to='personas.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveSmallIntegerField(choices=[(3, 'profesor'), (2, 'alumno'), (1, 'afiliado')])),
                ('desde', models.DateField(blank=True, null=True)),
                ('hasta', models.DateField(blank=True, null=True)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='personas.persona')),
            ],
        ),
        migrations.AddField(
            model_name='persona',
            name='familia',
            field=models.ManyToManyField(blank=True, through='personas.Vinculo', to='personas.persona'),
        ),
        migrations.AddField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
