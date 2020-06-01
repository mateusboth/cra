from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin
from .forms import HomologarForm
from django.db import IntegrityError
from django.contrib import messages

# csv
from django.http import HttpResponse
import csv

from .models import Solicitacao, Resultado


class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 0


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'disciplina',
                    'homologada', 'semestre_solicitacao',)
    list_filter = ('semestre_solicitacao', 'homologada',)
    search_fields = ('solicitante', 'disciplina')
    actions = ['export_csv', 'homologar']
    inlines = [ResultadoInline]

    def homologar(self, request, queryset):
        """
        Ação para homologar/não homologar pedidos selecionados em bloco e
        criar/deletar resultados conforme necessidade
        """
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
                              f"Alterado status de {queryset.count()} solicitações para {h}")
            return HttpResponseRedirect(request.get_full_path())

        # exibi formulário
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


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('solicitante', 'disciplina',
                    'resultado', 'nota', 'avaliador', 'semestre',)
    list_editable = ('nota', 'avaliador')
    list_filter = ('solicitacao__semestre_solicitacao', 'resultado',
                   'solicitacao__solicitante__curso', 'solicitar_recurso')
    search_fields = ('solicitacao__solicitante__nome_completo',
                     'solicitacao__disciplina__nome',
                     'solicitacao__disciplina__codigo')
    fieldsets = (
        (None, {
            'fields': ('solicitante', 'disciplina', 'nota', 'avaliador', 'ausente')
        }),
        ('Recursos', {
            'fields': ('solicitar_recurso', 'resultado_recurso', 'nota_anterior'),
        })
    )
    readonly_fields = ('nota_anterior', 'solicitante', 'disciplina',)
    actions = ['recurso', 'ausente']

    def solicitante(self, resultado):
        return resultado.solicitacao.solicitante
    solicitante.short_description = 'solicitante'
    solicitante.admin_order_field = 'solicitacao__solicitante'

    def disciplina(self, resultado):
        return resultado.solicitacao.disciplina
    disciplina.short_description = 'disciplina'
    disciplina.admin_order_field = 'solicitacao__disciplina'

    def semestre(self, resultado):
        return resultado.solicitacao.semestre_solicitacao
    semestre.short_description = 'semestre'
    semestre.admin_order_field = 'solicitacao__semestre_solicitacao'
    ordering = ('solicitacao__semestre_solicitacao',
                'solicitacao__solicitante', 'solicitacao__disciplina')

    def recurso(self, request, queryset):
        """Altera solicitar_recurso para True, limpa campo nota, e salva nota_anterior"""
        for sol in queryset:
            sol.solicitar_recurso = True
            sol.nota_anterior = sol.nota
            sol.nota = None
            sol.save()
        self.message_user(request, 'Recursos solicitados')
    recurso.short_description = "Solicitar recurso"

    def ausente(self, request, queryset):
        """Altera ausent para True"""
        for sol in queryset:
            sol.ausente = True
            if sol.nota is not None:
                err = sol
                break
            sol.save()
        if err:
            self.message_user(request, f'{err.solicitacao.solicitante} não pode ter nota e estar ausente', 
                                messages.ERROR)
        else:
            self.message_user(request, 'Marcados como ausentes')
    ausente.short_description = "Marcar como ausente"
