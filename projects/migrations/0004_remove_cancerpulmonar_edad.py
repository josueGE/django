# Generated by Django 4.2.1 on 2023-06-13 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_cancerpulmonar_edad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cancerpulmonar',
            name='edad',
        ),
    ]