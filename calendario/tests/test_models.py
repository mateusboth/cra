from datetime import date
from django.test import TestCase
from django.db import IntegrityError
# Create your tests here.

from calendario.models import Calendario

cal = { 'ano': '2020',
        'semestre': '1',
        'is_active': True,
        'inicio_solicitacoes': date(2020, 3, 1),
        'fim_solicitacoes': date(2020, 3, 10),
        'inicio_recursos': date(2020, 3, 20),
        'fim_recursos': date(2020, 3, 25),
        }
class CalendarioModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Calendario.objects.create(**cal)

    def test_object_name_ano_semestre(self):
        calendario = Calendario.objects.get(id=1)
        expected_object_name = '{0}/{1}'.format(
            calendario.ano, calendario.semestre)
        self.assertEqual(expected_object_name, str(calendario))

    def test_get_absolute_url(self):
        calendario = Calendario.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(calendario.get_absolute_url(), '/calendario/2020-1/')
    
    def test_get_delete_url(self):
        calendario = Calendario.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(calendario.get_delete_url(), '/calendario/2020-1/delete')

    def test_uniqueConstraint(self):
        # top level exception as we want to figure out its exact type
        with self.assertRaises(Exception) as raised:
            Calendario.objects.create(**cal)
        # if it fails, we'll get the correct type to import
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_save_one_active(self):
        cal_2 = cal.copy()
        cal_2['ano'] = '2021'
        novo = Calendario.objects.create(**cal_2)
        ativo = Calendario.objects.get(is_active=True)
        self.assertEqual(ativo, novo)


