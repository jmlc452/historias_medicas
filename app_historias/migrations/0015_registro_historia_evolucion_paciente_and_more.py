# Generated by Django 4.2.5 on 2023-10-05 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_historias', '0014_alter_registro_historia_examen_fisico'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro_historia',
            name='evolucion_paciente',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro_historia',
            name='examen_fisico',
            field=models.TextField(blank=True, null=True),
        ),
    ]