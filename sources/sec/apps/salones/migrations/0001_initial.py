# Generated by Django 4.1.1 on 2022-10-31 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('afiliados', '0001_initial'),
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seña', models.FloatField(max_length=8)),
                ('fechaReserva', models.DateField()),
                ('fechaInicio', models.DateField()),
                ('afiliado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='afiliados.afiliado')),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=30)),
                ('capacidad', models.PositiveIntegerField(max_length=3)),
                ('montoSalon', models.FloatField(max_length=5)),
                ('afiliados', models.ManyToManyField(through='salones.Alquiler', to='afiliados.afiliado')),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=120)),
                ('obligatorio', models.BooleanField()),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salones.salon')),
            ],
        ),
        migrations.CreateModel(
            name='PagoAlquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPago', models.DateField()),
                ('monto', models.FloatField(max_length=6)),
                ('tipoPago', models.CharField(max_length=5)),
                ('alquiler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salones.alquiler')),
            ],
        ),
        migrations.AddField(
            model_name='alquiler',
            name='salon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salones.salon'),
        ),
    ]
