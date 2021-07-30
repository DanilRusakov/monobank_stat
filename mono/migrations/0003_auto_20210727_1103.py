# Generated by Django 3.1.5 on 2021-07-27 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mono', '0002_auto_20210727_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monouser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MonoPersonalStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mono_id', models.CharField(max_length=16, verbose_name='Transaction id')),
                ('time', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=255)),
                ('receipt_id', models.CharField(max_length=19)),
                ('mono_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mono.monouser')),
            ],
        ),
    ]
