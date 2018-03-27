# Generated by Django 2.0.2 on 2018-03-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0009_auto_20180327_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviecrew',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='moviecrew',
            name='role',
        ),
        migrations.AddField(
            model_name='crewprofile',
            name='role',
            field=models.ManyToManyField(to='booking_system.CastType'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='crew',
            field=models.ManyToManyField(to='booking_system.CrewProfile'),
        ),
        migrations.DeleteModel(
            name='MovieCrew',
        ),
    ]