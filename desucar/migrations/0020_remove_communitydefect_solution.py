# Generated by Django 2.0 on 2018-03-12 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('desucar', '0019_auto_20180312_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitydefect',
            name='solution',
        ),
    ]
