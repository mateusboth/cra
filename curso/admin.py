from django.contrib import admin

# Register your models here.
from .models import Curso, Disciplina

class DisciplinaInline(admin.TabularInline):
    """Defines format of inline disciplina instance insertion (used in CursoAdmin)"""
    model = Disciplina.curso.through
    extra = 4

class CursoInline(admin.TabularInline):
    """Defines format of inline disciplina instance insertion (used in CursoAdmin)"""
    model = Curso
    extra = 1
    
@admin.register(Curso) 
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matriz', 'abreviacao', 'is_active',)
    # fields = [('abreviacao', 'nome', 'matriz', 'is_active')]
    list_filter = ('is_active',)
    inlines = [DisciplinaInline]

    # fieldsets = (
    #     (None, {
    #         'fields': ('abreviacao', 'matriz')
    #     }),
    #     ('Ativo ou algo assim', {
    #         'fields': ('is_active',)
    #     }),
    # )
    
@admin.register(Disciplina) 
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    # fields = [('abreviacao', 'nome', 'matriz', 'is_active')]
    
    