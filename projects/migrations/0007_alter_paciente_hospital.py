# Generated by Django 4.2.1 on 2023-06-15 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_paciente_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.hospital'),
        ),
    ]
