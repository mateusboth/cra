# Generated by Django 3.0.5 on 2020-05-19 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0005_auto_20200519_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disciplina',
            name='curso',
        ),
        migrations.AddField(
            model_name='curso',
            name='disciplina',
            field=models.ManyToManyField(to='curso.Disciplina'),
        ),
    ]
