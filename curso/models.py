"""
Modelos de cursos e disciplinas vinculadas a eles
Usa ForeignKey e não ManyToMany, se uma disciplina estiver em dois cursos ela terá que ser duplicada
"""
from django.db import models
from django.urls import reverse
from cra.snippets import unique_slugify

# Create your models here.


class Curso(models.Model):
    """Cursos existente e ativos com matriz"""
    nome = models.CharField(max_length=30)
    abreviacao = models.CharField(
        'Abreviação', max_length=3, help_text='Máximo 3 letras')
    matriz = models.CharField(
        max_length=4, help_text='Ano de aprovação de matriz do curso')
    is_active = models.BooleanField('Ativo', default=True)
    slug = models.SlugField(max_length=20)

    class Meta():
        ordering = ['-is_active', 'nome']

    def save(self, *args, **kwargs):
        slug_str = self.abreviacao + self.matriz
        unique_slugify(self, slug_str)
        self.abreviacao = self.abreviacao.upper()
        super(Curso, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.abreviacao}/{self.matriz}'

    def get_absolute_url(self):
        return reverse("curso:curso-detail", kwargs={"slug": self.slug})

class Disciplina(models.Model):
    """Modelo disciplina"""
    codigo = models.CharField(("Código"), max_length=12, primary_key=True, unique=True)
    nome = models.CharField(("Nome da disciplina"), max_length=50)
    curso = models.ManyToManyField('Curso')

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    def get_absolute_url(self):
        """Url para o template com detalhes de uma disciplinas especifica"""
        return reverse("curso:disciplina-detail", kwargs={"pk": self.codigo})