"""
Modelos de cursos e disciplinas vinculadas a eles
"""
from django.db import models
from django.urls import reverse
from cra.snippets import unique_slugify


class Curso(models.Model):
    """Cursos existente e ativos com matriz"""
    nome = models.CharField(max_length=30)
    abreviacao = models.CharField(
        'Abreviação', max_length=3, help_text='Máximo 3 letras')
    matriz = models.CharField(
        max_length=4, help_text='Ano de aprovação de matriz do curso')
    is_active = models.BooleanField('Ativo', default=True)
    slug = models.SlugField(max_length=40, unique=True)

    class Meta():
        ordering = ['-is_active', 'nome']

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        slug_str = self.abreviacao + self.matriz
        unique_slugify(self, slug_str)
        # Garante que abreviação esteja em maiúsculas
        self.abreviacao = self.abreviacao.upper()
        super(Curso, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome}/{self.matriz}'


class Disciplina(models.Model):
    """Modelo disciplina"""
    codigo = models.CharField(
        ("Código"), max_length=12, primary_key=True, unique=True)
    nome = models.CharField(("Nome da disciplina"), max_length=100)
    curso = models.ManyToManyField('Curso')

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # Garante que codigo esteja em maiúsculas
        self.codigo = self.codigo.upper()
        super(Disciplina, self).save(*args, **kwargs)
