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

class Semestre(models.Model):
    SEMESTRES = (
        ('PEN', 'Pendente'),
        ('OPT', 'Optativa'),
        ('1', '1º Semestre'),
        ('2', '2º Semestre'),
        ('3', '3º Semestre'),
        ('4', '4º Semestre'),
        ('5', '5º Semestre'),
        ('6', '6º Semestre'),
        ('7', '7º Semestre'),
        ('8', '8º Semestre'),
        ('9', '9º Semestre'),
        ('10', '10º Semestre'),
    )

    curso = models.ForeignKey("Curso", on_delete=models.CASCADE)
    disciplina = models.ForeignKey("Disciplina", on_delete=models.CASCADE)
    Semestre = models.CharField(
        max_length=3,
        choices=SEMESTRES,
        default='PEN',
    )


class Disciplina(models.Model):
    """Modelo disciplina"""
    codigo = models.CharField(("Código"), max_length=12, primary_key=True)
    nome = models.CharField(("Nome da disciplina"), max_length=50)
    curso = models.ManyToManyField('Curso', verbose_name=(
        "Curso"), through='Semestre')

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    # def get_absolute_url(self):
    #     """Url para o template com detalhes de uma disciplinas especifica"""
    #     return reverse("cc:disciplina-detail", kwargs={"slug": self.slug})