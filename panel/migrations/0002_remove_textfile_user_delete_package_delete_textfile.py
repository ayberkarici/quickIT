# Generated by Django 5.0.3 on 2024-03-14 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textfile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Package',
        ),
        migrations.DeleteModel(
            name='TextFile',
        ),
    ]
