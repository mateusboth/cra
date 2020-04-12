from django.test import TestCase
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from calendario.models import Calendario

# Create your tests here.


class CalendarioListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 calendarios for pagination tests
        cal = {
            'semestre': '1',
            'is_active': True,
            'inicio_solicitacoes': date(2020, 3, 1),
            'fim_solicitacoes': date(2020, 3, 10),
            'inicio_recursos': date(2020, 3, 20),
            'fim_recursos': date(2020, 3, 25),
        }
        number_of_calendarios = 13

        for calendario_id in range(number_of_calendarios):
            Calendario.objects.create(
                ano=f'{2020+calendario_id}', **cal
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/calendario/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('calendario:calendarios'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('calendario:calendarios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendario/calendario_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('calendario:calendarios'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['calendario_list']) == 10)

    def test_lists_all_calendarios(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('calendario:calendarios')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['calendario_list']) == 3)


class CalendarioCreateViewTest(TestCase):
    """Test case for the CalendarioCreate view."""

    def setUp(self):
        # Create a calendario
        cal = {'ano': '2020',
               'semestre': '1',
               'is_active': True,
               'inicio_solicitacoes': date(2020, 3, 1),
               'fim_solicitacoes': date(2020, 3, 10),
               'inicio_recursos': date(2020, 3, 20),
               'fim_recursos': date(2020, 3, 25),
               }
        Calendario.objects.create(**cal)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('calendario:calendario-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendario/calendario_form.html')

    def test_redirects_to_list_view_on_success(self):
        response = self.client.post(reverse('calendario:calendario-create'),
                                    {'ano': '2021',
                                     'semestre': '1',
                                     'is_active': True,
                                     'inicio_solicitacoes': date(2020, 3, 1),
                                     'fim_solicitacoes': date(2020, 3, 10),
                                     'inicio_recursos': date(2020, 3, 20),
                                     'fim_recursos': date(2020, 3, 25),
                                     })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/calendario'))
