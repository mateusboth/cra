# <project>/<app>/management/commands/seed.py
from datetime import date
import logging
from django.core.management.base import BaseCommand
import random
from cc.models import Solicitacao
from curso.models import Disciplina, Curso
from calendario.models import Calendario
from django.contrib.auth import get_user_model

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
    logger.info("Delete solicitacao instances")
    Solicitacao.objects.all().delete()

def create_solicitacao():
    """Creates an solicitacao object combining different elements from the list"""
    logger.info("Creating solicitacao")
    
    calendarios = Calendario.objects.all()
    disciplinas_all = list(Disciplina.objects.all())
    cursos = Curso.objects.all()

    for i in range(1, 11):
        # cria usuario
        curso = random.choice(cursos)
        user = User(curso=curso, matricula=f'203930{i}', 
                    nome_completo=f'João {i} da silva',
                    email='seed@seed.com')
        user.save()
        logger.info("%(user)s user created.")
        # seleciona disciplinas e faz solicitação
        disci = random.sample(disciplinas_all, i)
        for d in disci:
            cal = random.choice(calendarios)
            print(f'linha 53: {user}, {d}, {cal}')
            solicitacao = Solicitacao(
                                solicitante=user, 
                                semestre_solicitacao=cal,
                                disciplina=d)
            solicitacao.save()
            logger.info("%(solicitacao)s solicitacao created.")
# return solicitacao


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
    create_solicitacao()
