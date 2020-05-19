"""Model Calendario com datas de inicio e fim para solicitação e recursos"""
from django.db import models, transaction
from django.core.exceptions import ValidationError
from cra.snippets import unique_slugify


class Calendario(models.Model):
    """Calendario com ano/semetre com datas de ínicio e fim das solicitações e recursos"""
    ano = models.CharField(
        ("Ano"), max_length=4,
        help_text='Ano dos pedidos, ex: 2020')
    semestre = models.CharField(
        ("Semestre"), max_length=1,
        help_text='Semestre dos pedidos')
    is_active = models.BooleanField('Calendário em vigor', default=True)
    inicio_solicitacoes = models.DateField(
        "Inicío das Solicitações", auto_now=False, auto_now_add=False)
    fim_solicitacoes = models.DateField(
        "Fim das Solicitações", auto_now=False, auto_now_add=False)
    inicio_recursos = models.DateField(
        "Inicío dos Recursos", auto_now=False, auto_now_add=False)
    fim_recursos = models.DateField(
        "Fim dos Recursos", auto_now=False, auto_now_add=False)
    slug = models.SlugField(unique=True)

    class Meta():
        ordering = ['-ano', '-semestre']
        constraints = [
            models.UniqueConstraint(
                fields=['ano', 'semestre'], name='unique_ano_semestre')
        ]

    def __str__(self):
        return f'{self.ano}/{self.semestre}'

    def save(self, *args, **kwargs): # pylint: disable=arguments-differ
        """Garante que exista apenas um is_active=True e define a slug"""
        slug_str = f'{self.ano}-{self.semestre}'
        unique_slugify(self, slug_str)
        if self.is_active:
            # Garante que intereção seja atomica com o DB e so um esteja ativo
            with transaction.atomic(): 
                Calendario.objects.filter(
                    is_active=True).update(is_active=False)
                return super(Calendario, self).save(*args, **kwargs)
        else:
            return super(Calendario, self).save(*args, **kwargs)

    def clean(self):
        """Raise ValidationError se a data de inicio é depois da data fim"""
        super(Calendario, self).clean()
        if self.inicio_solicitacoes > self.fim_solicitacoes:
            raise ValidationError(
                'Data de fim das solicitações deve ser posterior a de inicio',
                code='Datas inválidas')
        if self.inicio_recursos > self.fim_recursos:
            raise ValidationError(
                'Data de fim dos recursos deve ser posterior a de inicio',
                code='Datas inválidas')
