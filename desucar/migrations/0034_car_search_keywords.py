# Generated by Django 2.0 on 2018-04-05 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desucar', '0033_officialdefect_n_targets_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='search_keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
