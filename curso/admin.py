from django.contrib import admin

# Register your models here.
from .models import Curso, Disciplina


class DisciplinaInline(admin.TabularInline):
    """Defines format of inline disciplina instance insertion (used in CursoAdmin)"""
    model = Disciplina.curso.through
    extra = 2

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'abreviacao', 'is_active',)
    fields = ['nome', 'abreviacao', 'matriz', 'is_active',]
    list_filter = ('is_active',)
    search_fields = ['nome',]
    # autocomplete_fields = ['disciplina',]
    # inlines = [DisciplinaInline]
    form = PersonForm



@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    # search_fields = ['nome', 'codigo']
    autocomplete_fields = ['curso',]
