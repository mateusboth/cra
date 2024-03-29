# Generated by Django 3.0.4 on 2020-04-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'ordering': ['-is_active', 'nome']},
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('codigo', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='Código')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome da disciplina')),
                ('curso', models.ManyToManyField(to='curso.Curso')),
            ],
        ),
    ]
