# Generated by Django 4.2.5 on 2023-10-05 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_historias', '0012_alter_registro_paciente_cedula_madre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro_historia',
            name='dx_ingreso',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro_historia',
            name='laboratorio_ingreso',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registro_historia',
            name='peso',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='registro_historia',
            name='plan',
            field=models.TextField(blank=True, null=True),
        ),
    ]