# Generated by Django 3.1.5 on 2021-07-27 09:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mono', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MonoUserInfo',
            new_name='MonoUser',
        ),
    ]
