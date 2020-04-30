"""Modelos referente a certificações de conhecimentos, inclui:
 solicitações, homologação, resultado
 
 Depende do app curso, com Modelos Curso e Disciplina"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models
from curso.models import Curso, Disciplina
from calendario.models import Calendario
from cra.snippets import unique_slugify
User = get_user_model()


class Solicitacao(models.Model):
    """Solicitações, depende de User e curso"""
    HOMOLOGACAO = (
        ('PEN', 'Pendente'),
        ('SIM', 'Homologado'),
        ('NAO', 'Não Homologado'),
    )

    #TODO trocar homologada de boolean para choice homologada e não homologada, e ajustar forms
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    justificativa = models.TextField(("Justificativa para o pedido"),
                                     help_text="O candidato pode explicar os motivos para solicitar a prova, por exemplo: experiência profissional, cursos não regulares, aproveitamentos indeferidos, entre outros.", blank=True, null=True)
    documentos = models.FileField(("Documentos comprobatorios de conhecimentos"),
                                  upload_to=None, max_length=100, blank=True, null=True,
                                  validators=[FileExtensionValidator(['.pdf'])])
    data_solicitacao = models.DateTimeField(
        ("Data da solicitação"), auto_now_add=True)
    cursou_anteriormente = models.BooleanField(
        ("Cursou anteriormente a disciplina solicitada"), blank=True, null=True)
    homologada = models.CharField(
        max_length=3,
        choices=HOMOLOGACAO,
        default='PEN'
    )
    semestre_solicitacao = models.ForeignKey(Calendario, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['semestre_solicitacao', 'solicitante', 'disciplina']
        constraints = [
            models.UniqueConstraint(
                fields=['solicitante', 'disciplina'], name='unique_solicitação')
        ]

    def __str__(self):
        return f'{self.disciplina} {self.solicitante} '

    def get_absolute_url(self):
        """Busca url de uma solicitação especifica"""
        return reverse("cc:solicitacao-detail", kwargs={"pk": self.pk})
    
def validate_nota(nota):
    if 0 > nota or 10 < nota:
        raise ValidationError(
            ('%(nota)s não esta entre 0-10.'),
            params={'nota': nota},
        )


class Resultado(models.Model):
    RESULTADO = (
        ('APR', 'Aprovado'),
        ('REP', 'Reprovado'),
        ('AUS', 'Ausente'),
        ('PEN', 'Pendente')
    )

    solicitacao = models.OneToOneField(
        "Solicitacao", on_delete=models.CASCADE)
    nota = models.DecimalField(decimal_places=1, max_digits=3,
                               validators=[validate_nota], blank=True, null=True)
    avaliador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ausente = models.BooleanField(default=False)
    resultado = models.CharField(
        max_length=3,
        choices=RESULTADO,
        blank=True,
        default='PEN'
    )
    data_resultado = models.DateTimeField(
        ("Data do resultado"), auto_now_add=True)

    def __str__(self):
        return self.resultado

    def get_absolute_url(self):
        """Busca url de uma solicitação especifica"""
        return reverse("cc:solicitacao-detail", kwargs={"pk": self.solicitacao.pk})

    def get_update_url(self):
        return reverse('cc:resultado-update', kwargs={'pk_sol': self.solicitacao.pk, 'pk': self.pk})

    def save(self, *args, **kwargs):
        """Altera o resultado conferme nota/ausente"""
        if self.ausente:
            self.resultado = 'AUS'
        elif self.nota is None:
            self.resultado = 'PEN'
        else:
            if self.nota >= 7:
                self.resultado = 'APR'
            else:
                self.resultado = 'REP'
        super(Resultado, self).save(*args, **kwargs)
    
    def clean(self, *args, **kwargs):
        if self.ausente and self.nota is not None:
            raise ValidationError(
                'Aluno não pode estar ausente e ter nota. Contate o setor responavel se o aluno tive comparecido')
        super(Resultado, self).clean(*args, **kwargs)


class Recurso(models.Model):
    resultado = models.OneToOneField("Resultado", on_delete=models.CASCADE)
    justificativa = models.TextField((""))
    documentos = models.FileField(("Documentos comprobatorios da justificativa"),
                                  upload_to=None, max_length=100, blank=True, null=True)
    data_solicitacao_recurso = models.DateTimeField(
        ("Data da solicitação do recurso"), auto_now_add=True)


# PENDENTE RECURSOS
