# Generated by Django 2.0 on 2018-03-12 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desucar', '0017_auto_20180312_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialdefect',
            name='fix_end',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='officialdefect',
            name='fix_start',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
