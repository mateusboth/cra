# <project>/<app>/management/commands/seed.py
import logging
from django.core.management.base import BaseCommand
import random
import csv
from curso.models import Curso, Disciplina
from django.core.exceptions import ObjectDoesNotExist

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
    logger.info("Delete curso instances")
    Curso.objects.all().delete()
    Disciplina.objects.all().delete()


def create_curso():
    """Creates an curso object combining different elements from the list"""
    logger.info("Creating curso")
    cursos = [
        {
            'nome': 'ENGENHARIA METALÚRGICA',
            'abreviacao': 'EM',
            'matriz': '2016',
            'is_active': False,
        }, {
            'nome': 'ENGENHARIA METALÚRGICA',
            'abreviacao': 'EM',
            'matriz': '2019',
            'is_active': True,
        }, {
            'nome': 'ENGENHARIA DE PRODUÇÃO',
            'abreviacao': 'EP',
            'matriz': '2016',
        }, {
            'nome': 'LICENCIATURA EM MATEMÁTICA',
            'abreviacao': 'LM',
            'matriz': '2017',
            'is_active': False,
        }, {
            'nome': 'LICENCIATURA EM MATEMÁTICA',
            'abreviacao': 'LM',
            'matriz': '2019',
        }, {
            'nome': 'TECNOLOGIA EM PROCESSOS GERENCIAIS',
            'abreviacao': 'TPG',
            'matriz': '2019',
        }, {
            'nome': 'TECNOLOGIA EM PROCESSOS METALÚRGICOS',
            'abreviacao': 'TPM',
            'matriz': '2017',
        },
    ]

    for cal in cursos:
        curso = Curso(**cal)
        curso.save()
        logger.info("%(curso)s created.")
    # return curso


def create_disciplina():
    # cursos = Curso.objects.all()
    # disciplinas = [
    #     {
    #         'codigo': 'CAX-MTM001',
    #         'nome': 'Matemática Elementar',
    #         # 'curso': cursos[0].pk
    #     }
    # ]
    # for disc in disciplinas:
    #     disciplina = Disciplina(**disc)
    #     disciplina.save()
    #     disciplina.curso.add(cursos[0])

    #     logger.info("%(disciplina)s created.")

    with open('curso/management/commands/disciplinas.csv', encoding="ISO-8859-1") as csvfile:
        disciplinas = csv.reader(csvfile, quotechar='|')
        for row in disciplinas:            
            if row[0] == 'curso':
                curso = Curso(nome=row[1], abreviacao=row[2], matriz=row[3], is_active=row[4])
                curso.save()
            else:
                try:
                    disciplina= Disciplina.objects.get(codigo=row[0])
                    disciplina.curso.add(curso)
                except ObjectDoesNotExist:
                    disciplina = Disciplina(codigo=row[0], nome=row[1])
                    disciplina.save()
                    disciplina.curso.add(curso)
                   
        
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
    # create_curso()
    create_disciplina()

# TODO adicionar no usuario talvez?
# def create_django_contrib_auth_models_group(**kwargs):
#     defaults = {}
#     defaults["name"] = "group"
#     defaults.update(**kwargs)
#     return Group.objects.create(**defaults)
