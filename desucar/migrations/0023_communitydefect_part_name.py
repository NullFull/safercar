# Generated by Django 2.0 on 2018-03-19 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desucar', '0022_communitydefectpost_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitydefect',
            name='part_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
