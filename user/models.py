'''Modela usuario para ser usado no app'''
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import reverse
from cra.snippets import unique_slugify
from .managers.UserManager import UserManager

from curso.models import Curso


class User(AbstractBaseUser, PermissionsMixin):
    """
    Login com número de matricula. Feito com base na explicação:
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
     """

    matricula = models.CharField(unique=True, max_length=15, primary_key=True)
    email = models.EmailField(('e-mail'))
    nome_completo = models.CharField(('Nome Completo'), max_length=70)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(('Data de criação'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    is_avaliador = models.BooleanField(default=False)
    is_coordenador = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['email', 'nome_completo']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        ordering = ['-matricula', 'nome_completo']
        permissions = [
            ('can_add_resultado', 'Pode adicionar resultado a solicitacao'),
            ('can_add_avaliador', 'Pode atribuir avaliador a solicitacao')
        ]

    def get_full_name(self):
        '''
        Returns the  name, with a space in between.
        '''
        return self.nome_completo

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        nome = str(self.nome_completo).split(' ')[0]
        return nome

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.nome_completo

    def get_absolute_url(self):
        return reverse("user-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """
        Criar slug e adiciona permissões se avaliador ou coordenador
        """
        slug_str = f'{self.nome_completo} {self.curso}'
        unique_slugify(self, slug_str)
        if self.is_avaliador:
            self.user_permissions.add('can_add_resultado')
        if self.is_coordenador:
            self.user_permissions.add('can_add_avaliador')
        super(User, self).save(*args, **kwargs)
