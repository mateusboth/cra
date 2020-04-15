# <project>/<app>/management/commands/seed.py
from datetime import date
import logging
from django.core.management.base import BaseCommand
import random
from django.contrib.auth import get_user_model
from curso.models import Curso
from django.contrib.auth.models import Group, Permission

User = get_user_model()


logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates new """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete user instances")
    User.objects.all().exclude(is_superuser=True).delete()
    Group.objects.all().delete()


def create_group():
    """Cria group avaliador e coordenadores com permissão personalizadas"""
    avaliadores, created = Group.objects.get_or_create(name='avaliadores')
    proj_add_perm = Permission.objects.get(codename='can_add_resultado')
    avaliadores.permissions.add(proj_add_perm)
    coordenadores, created = Group.objects.get_or_create(name='coordenadores')
    proj_add_perm = Permission.objects.get(codename='can_add_avaliador')
    coordenadores.permissions.add(proj_add_perm)


def create_user():
    """Creates an user object combining different elements from the list"""
    logger.info("Creating user")
    cursos = Curso.objects.all()

    users = [
        {
            'matricula': '10',
            'email': 'emais@servidor.com',
            'nome_completo': 'Nome completo do aluno',
            'password': '12345678'
        }, {
            'matricula': '11',
            'email': 'emais@servidor.com',
            'nome_completo': 'Nome completo do avaliador',
            'is_avaliador': 'True',
            'password': '12345678'

        }, {
            'matricula': '12',
            'email': 'emais@servidor.com',
            'nome_completo': 'Nome completo do coordenador',
            'is_avaliador': 'True',
            'is_coordenador': 'True',
            'password': '12345678'
        },
    ]

    for u in users:
        curso = random.choice(cursos)
        user = User(curso=curso, **u)
        user.save()
        logger.info("%(user)s user created.")


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 15 calendari
    # for i in range(15):
    create_group()
    create_user()
