# Generated by Django 4.2.4 on 2023-08-30 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_historias', '0002_registro_pasiente_cedula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro_pasiente',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
