"""Model Calendario com datas de inicio e fim para solicitação e recursos"""
from django.db import models
from django.urls import reverse
from django.db import transaction
from cra.snippets import unique_slugify


class Calendario(models.Model):
    """Calendario referente as datas do semestre"""
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

    def get_absolute_url(self):
        return reverse("calendario:calendario-detail", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("calendario:calendario-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Garante que exista apenas um is_active=True e define a slug"""    
        slug_str = f'{self.ano}-{self.semestre}'
        unique_slugify(self, slug_str)
        if self.is_active:
            with transaction.atomic():
                Calendario.objects.filter(
                    is_active=True).update(is_active=False)
                return super(Calendario, self).save(*args, **kwargs)
        else:
            return super(Calendario, self).save(*args, **kwargs)

    def get_fields(self):
        """ Permite usar for no template para exibir todos os atributos do objeto"""
        return [(field.verbose_name, field.value_to_string(self)) for field in Calendario._meta.fields]
