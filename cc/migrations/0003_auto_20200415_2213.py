# Generated by Django 3.0.4 on 2020-04-16 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0002_auto_20200412_1455'),
        ('cc', '0002_auto_20200415_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacao',
            name='semestre_solicitacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calendario.Calendario'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='justificativa',
            field=models.TextField(blank=True, help_text='O candidato pode explicar os motivos para solicitar a prova, por exemplo: experiência profissional, cursos não regulares, aproveitamentos indeferidos, entre outros.', null=True, verbose_name='Justificativa para o pedido'),
        ),
    ]