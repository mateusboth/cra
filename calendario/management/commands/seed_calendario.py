# <project>/<app>/management/commands/seed.py
from datetime import date
import logging
from django.core.management.base import BaseCommand
import random
from calendario.models import Calendario


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
    logger.info("Delete Calendario instances")
    Calendario.objects.all().delete()

def create_calendario():
    """Creates an calendario object combining different elements from the list"""
    logger.info("Creating calendario")
    # street_flats = ["#221 B", "#101 A", "#550I", "#420G", "#A13"]
    # street_localities = ["Bakers Street", "Rajori Gardens", "Park Street", "MG Road", "Indiranagar"]
    # pincodes = ["101234", "101232", "101231", "101236", "101239"]
    calendarios = [
        {
            'ano': '2018',
            'semestre': '1',
            'is_active': False,
            'inicio_solicitacoes': date(2018, 3, 1),
            'fim_solicitacoes': date(2018, 3, 10),
            'inicio_recursos': date(2018, 3, 20),
            'fim_recursos': date(2018, 3, 25),
        }, {
            'ano': '2018',
            'semestre': '2',
            'is_active': False,
            'inicio_solicitacoes': date(2018, 8, 1),
            'fim_solicitacoes': date(2018, 8, 10),
            'inicio_recursos': date(2018, 8, 20),
            'fim_recursos': date(2018, 8, 25),
        }, {
            'ano': '2019',
            'semestre': '1',
            'is_active': False,
            'inicio_solicitacoes': date(2019, 3, 1),
            'fim_solicitacoes': date(2019, 3, 10),
            'inicio_recursos': date(2019, 3, 20),
            'fim_recursos': date(2019, 3, 25),
        }, {
            'ano': '2019',
            'semestre': '2',
            'is_active': False,
            'inicio_solicitacoes': date(2019, 8, 1),
            'fim_solicitacoes': date(2019, 8, 10),
            'inicio_recursos': date(2019, 8, 20),
            'fim_recursos': date(2019, 8, 25),
        }, {
            'ano': '2020',
            'semestre': '1',
            'is_active': True,
            'inicio_solicitacoes': date(2020, 3, 1),
            'fim_solicitacoes': date(2020, 3, 10),
            'inicio_recursos': date(2020, 3, 20),
            'fim_recursos': date(2020, 3, 25),
        }
    ]

    for cal in calendarios:
        calendario = Calendario(**cal)
        calendario.save()
        logger.info("%(calendario)s calendario created.")
    # return calendario


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
    create_calendario()

# TODO adicionar no usuario talvez?
# def create_django_contrib_auth_models_group(**kwargs):
#     defaults = {}
#     defaults["name"] = "group"
#     defaults.update(**kwargs)
#     return Group.objects.create(**defaults)
