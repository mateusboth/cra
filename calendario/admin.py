from django.contrib import admin
from .models import Calendario
# Register your models here.


@admin.register(Calendario) 
class CalendarioAdmin(admin.ModelAdmin):
    list_display = ('ano', 'semestre', 'is_active', 'inicio_solicitacoes', 'fim_solicitacoes','inicio_recursos','inicio_recursos')
    fields = [
        'is_active',
            'ano',
              'semestre',
            ('inicio_solicitacoes', 'fim_solicitacoes'),
              ('inicio_recursos', 'fim_recursos')
             ]
    list_filter = ('is_active',)
    # inlines = [BooksInline]
    # fieldsets = (
    #     (None, {
    #         'fields': ('abreviacao', 'matriz')
    #     }),
    #     ('Ativo ou algo assim', {
    #         'fields': ('is_active',)
    #     }),
    # )