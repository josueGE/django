# Generated by Django 4.2.1 on 2023-06-13 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_pacientepaciente_diabetes_paciente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancerpulmonar',
            name='edad',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
