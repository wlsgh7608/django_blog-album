# Generated by Django 3.2.7 on 2021-09-30 06:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='CONTENT'),
            preserve_default=False,
        ),
    ]