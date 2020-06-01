from django.contrib import admin
from .models import Calendario


@admin.register(Calendario)
class CalendarioAdmin(admin.ModelAdmin):
    """Admin para app calendário, com os campos a serem exibidos"""
    list_display = ('__str__', 'is_active', 'inicio_solicitacoes',
                    'fim_solicitacoes', 'inicio_recursos', 'inicio_recursos')
    fields = [
        'is_active',
        'ano',
        'semestre',
        ('inicio_solicitacoes', 'fim_solicitacoes'),
        ('inicio_recursos', 'fim_recursos')
    ]
    list_filter = ('is_active',)
  