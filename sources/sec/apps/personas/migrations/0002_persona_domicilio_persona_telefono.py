# Generated by Django 4.1.1 on 2022-11-25 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='domicilio',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
