from django.contrib import admin

# Register your models here.
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'curso', 'matricula',
                    'is_avaliador', 'is_coordenador')
    fieldsets = (
        (None, {
            'fields': ('nome_completo', 'curso', 'matricula', 'password')
        }),
        ('Permissões', {
            'fields': (('is_staff', 'is_superuser'), 'groups'),
        }),
    )
    list_filter = ('curso', 'is_avaliador', 'is_coordenador')
    filter_horizontal = ('groups',)
    search_fields = ('nome_completo', 'matricula')

    def save_model(self, request, obj, form, change):
        # Permite alterar password do usuario direto no admin
        if obj.pk:
            if 'password' in form.changed_data:
                obj.set_password(obj.password)
        if 'groups' in form.changed_data:
            # atribui is_coordenador true se tiver no group
            if form.cleaned_data['groups'].filter(name='Coordenadores').exists():
                obj.is_coordenador = True
            else:
                obj.is_coordenador = False
            # atribui is_avaliador true se tiver no group
            if form.cleaned_data['groups'].filter(name='Avaliadores').exists():
                obj.is_avaliador = True
            else:
                obj.is_avaliador = False
        super().save_model(request, obj, form, change)