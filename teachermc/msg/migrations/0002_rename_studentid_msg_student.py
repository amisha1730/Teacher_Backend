# Generated by Django 4.1.6 on 2023-02-13 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msg', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='msg',
            old_name='studentId',
            new_name='student',
        ),
    ]