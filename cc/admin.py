from django.contrib import admin

# Register your models here.

from .models import Solicitacao, Resultado

admin.site.register(Solicitacao)
admin.site.register(Resultado)
