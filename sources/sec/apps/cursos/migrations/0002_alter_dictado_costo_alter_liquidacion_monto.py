# Generated by Django 4.1.1 on 2024-10-12 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictado',
            name='costo',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='liquidacion',
            name='monto',
            field=models.FloatField(),
        ),
    ]
