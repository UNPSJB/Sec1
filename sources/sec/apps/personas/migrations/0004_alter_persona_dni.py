# Generated by Django 4.1.1 on 2022-11-18 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0003_alter_rol_desde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='dni',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
