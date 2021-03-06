# Generated by Django 2.0 on 2018-05-14 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('desucar', '0035_auto_20180514_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='NHTSADefect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_detail', models.TextField()),
                ('n_targets', models.IntegerField(blank=True, null=True)),
                ('make_start', models.DateField(null=True)),
                ('make_end', models.DateField(null=True)),
                ('make_date_comment', models.CharField(blank=True, max_length=30, null=True)),
                ('recall_code', models.CharField(max_length=20)),
                ('fix_start', models.CharField(blank=True, max_length=40, null=True)),
                ('part_name', models.CharField(max_length=20)),
                ('original_part_name', models.CharField(max_length=20)),
                ('original_defect', models.TextField()),
                ('original_summary', models.TextField()),
                ('original_solution', models.TextField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nhtsa_defects', to='desucar.Car')),
            ],
        ),
    ]
