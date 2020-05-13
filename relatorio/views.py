from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from cc.models import Solicitacao
from calendario.models import Calendario
from django_weasyprint import WeasyTemplateResponseMixin

# Relatorio de homologados
class RelatorioSolicitacaoSemestreView(ListView):
    model = Solicitacao

    def get_queryset(self):
        qs = super().get_queryset()
        semestre = get_object_or_404(Calendario, slug=self.kwargs.get('slug'))
        qs = qs.filter(semestre_solicitacao=semestre)
        return qs

class HomologadoPdfView(WeasyTemplateResponseMixin, RelatorioSolicitacaoSemestreView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    # show pdf in-line (default: True, show download dialog)
    template_name = 'relatorio/homologado.html'
    pdf_attachment = False
    # pdf_filename = 'homologação.pdf'
    pdf_stylesheets = [
        'static/css/pdf.css',
    ]

    # dynamically generate filename
    def get_pdf_filename(self):
        return f'homologados-{self.kwargs.get("slug")}.pdf'

# relatório de resultados
class ResultadoPdfView(WeasyTemplateResponseMixin, RelatorioSolicitacaoSemestreView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    # show pdf in-line (default: True, show download dialog)
    template_name = 'relatorio/resultado.html'
    pdf_attachment = False
    pdf_stylesheets = ['static/css/pdf.css', ]

    def get_pdf_filename(self):
        return f'resultado-{self.kwargs.get("slug")}.pdf'


class FichaIndividualPdfView(WeasyTemplateResponseMixin, RelatorioSolicitacaoSemestreView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    # show pdf in-line (default: True, show download dialog)
    template_name = 'relatorio/ficha-individual.html'
    pdf_attachment = False
    pdf_stylesheets = ['static/css/pdf.css', ]

    def get_pdf_filename(self):
        return f'fichas individuais-{self.kwargs.get("slug")}.pdf'


# from django.contrib.auth import get_user_model
# User = get_user_model()

class FolhaRostoPdfView(WeasyTemplateResponseMixin, RelatorioSolicitacaoSemestreView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    # show pdf in-line (default: True, show download dialog)
    template_name = 'relatorio/folha-rosto.html'
    pdf_attachment = False
    pdf_stylesheets = ['static/css/pdf.css', ]

    def get_pdf_filename(self):
        return f'folha de rosto-{self.kwargs.get("slug")}.pdf'