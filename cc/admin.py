from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin
from .forms import HomologarForm
from django.db import IntegrityError
# Register your models here.

from .models import Solicitacao, Resultado

from django.http import HttpResponse
import csv


class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 0


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'disciplina',
                    'homologada', 'semestre_solicitacao', 'resultado')
    list_filter = ('semestre_solicitacao', 'homologada',)
    search_fields = ('solicitante', 'disciplina')
    actions = ['export_csv', 'homologar']
    inlines = [ResultadoInline]

    def homologar(self, request, queryset):
        # All requests here will actually be of type POST
        # so we will need to check for our special key 'apply'
        # rather than the actual request type
        if 'apply' in request.POST:
            # The user clicked submit on the intermediate form.
            # Perform our update action:
            form = HomologarForm(request.POST)
            if form.is_valid():
                h = form.cleaned_data['homologada']
                if h == 'SIM':
                    queryset.update(cursou_anteriormente=False,
                                    homologada='SIM')
                    for sol in queryset:
                        try:  # Se não existir um resultado cria um
                            r = Resultado(solicitacao=sol)
                            r.save()
                        except IntegrityError:  # erro se ja exitir um resultado
                            pass
                elif h == 'NAO':
                    queryset.update(cursou_anteriormente=True,
                                    homologada='NAO')
                    # deleta resultado se existir
                    for sol in queryset:
                        try:
                            sol.resultado.delete()
                        except sol._meta.model.resultado.RelatedObjectDoesNotExist:
                            pass
                else:
                    queryset.update(cursou_anteriormente=None,
                                    homologada='PEN')
                    # deleta resultado se existir
                    for sol in queryset:
                        try:
                            sol.resultado.delete()
                        except sol._meta.model.resultado.RelatedObjectDoesNotExist:
                            pass

            # Redirect to our admin view after our update has
            # completed with a nice little info message saying
            # our models have been updated:
            self.message_user(request,
                              "Alterado status de {} solicitações".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        form = HomologarForm()
        return render(request,
                      'admin/homologar.html',
                      context={'solicitacao_list': queryset, 'form': form, 'title': 'Homologar'})
    homologar.short_description = "Homologar solicitações"

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="solicitacoes.csv"'
        writer = csv.writer(response)
        writer.writerow(['curso', 'solicitante', 'disciplina',
                         'homologada', 'semestre_solicitacao',
                         'resultado', 'nota', 'avaliador', 'recurso'])
        for sol in queryset:
            row = [sol.solicitante.curso, sol.solicitante, sol.disciplina,
                    sol.get_homologada_display(), sol.semestre_solicitacao.__str__()]
            try:
                row += [sol.resultado.get_resultado_display(), sol.resultado.nota,
                        sol.resultado.avaliador, sol.resultado.solicitar_recurso]
            except sol._meta.model.resultado.RelatedObjectDoesNotExist:
                row.append('-')
            writer.writerow(row)
        return response
    export_csv.short_description = 'Exportar como csv'


admin.site.register(Resultado)
