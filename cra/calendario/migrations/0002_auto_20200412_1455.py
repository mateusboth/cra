# Generated by Django 3.0.4 on 2020-04-12 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendario',
            name='fim_recursos',
            field=models.DateField(verbose_name='Fim dos Recursos'),
        ),
        migrations.AlterField(
            model_name='calendario',
            name='fim_solicitacoes',
            field=models.DateField(verbose_name='Fim das Solicitações'),
        ),
        migrations.AlterField(
            model_name='calendario',
            name='inicio_recursos',
            field=models.DateField(verbose_name='Inicío dos Recursos'),
        ),
        migrations.AlterField(
            model_name='calendario',
            name='inicio_solicitacoes',
            field=models.DateField(verbose_name='Inicío das Solicitações'),
        ),
        migrations.AlterField(
            model_name='calendario',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Calendário em vigor'),
        ),
    ]
