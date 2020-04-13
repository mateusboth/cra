from django.contrib import admin

# Register your models here.
from .models import Curso

@admin.register(Curso) 
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matriz', 'abreviacao', 'is_active')
    # fields = [('abreviacao', 'nome', 'matriz', 'is_active')]
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