# Generated by Django 3.0.7 on 2020-06-11 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0002_auto_20200610_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=50)),
                ('sta_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='persinfo',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.Unit'),
        ),
    ]
