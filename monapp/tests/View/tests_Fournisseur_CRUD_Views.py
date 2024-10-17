# tests/test_fournisseurs_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Fournisseur
from monapp.forms import FournisseurForm

class FournisseurListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(name='Fournisseur Test')

    def test_fournisseur_list_view_status_code(self):
        response = self.client.get(reverse('fournisseur-list'))
        self.assertEqual(response.status_code, 200)

    def test_fournisseur_list_view_template(self):
        response = self.client.get(reverse('fournisseur-list'))
        self.assertTemplateUsed(response, 'monapp/list_fournisseurs.html')

    # def test_fournisseur_list_view_queryset(self):
    #     response = self.client.get(reverse('fournisseur-list'))
    #     self.assertQuerySetEqual(response.context['fournisseurs'], [repr(self.fournisseur)])

class FournisseurDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(name='Fournisseur Test')

    def test_fournisseur_detail_view_status_code(self):
        response = self.client.get(reverse('fournisseur-detail', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 200)

    def test_fournisseur_detail_view_template(self):
        response = self.client.get(reverse('fournisseur-detail', args=[self.fournisseur.id]))
        self.assertTemplateUsed(response, 'monapp/detail_fournisseur.html')

class FournisseurCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_fournisseur_create_view_status_code(self):
        response = self.client.get(reverse('fournisseur-add'))
        self.assertEqual(response.status_code, 200)

    def test_fournisseur_create_view_template(self):
        response = self.client.get(reverse('fournisseur-add'))
        self.assertTemplateUsed(response, 'monapp/new_fournisseur.html')

    def test_fournisseur_create_view_post(self):
        response = self.client.post(reverse('fournisseur-add'), {
            'name': 'Nouveau Fournisseur',
            'mail': 'mail',
            'adresse': 'adresse'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(Fournisseur.objects.filter(name='Nouveau Fournisseur').exists())  # Vérifie que le fournisseur a été créé

class FournisseurUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(name='Fournisseur Test')

    def test_fournisseur_update_view_post(self):
        response = self.client.post(reverse('fournisseur-update', args=[self.fournisseur.id]), {
            'name': 'Fournisseur Mis à Jour',
            'mail': 'mail',
            'adresse': 'adresse'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après mise à jour
        self.fournisseur.refresh_from_db()
        self.assertEqual(self.fournisseur.name, 'Fournisseur Mis à Jour')  # Vérifie que le nom a été mis à jour

class FournisseurDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.fournisseur = Fournisseur.objects.create(name='Fournisseur Test')

    def test_fournisseur_delete_view_post(self):
        response = self.client.post(reverse('fournisseur-delete', args=[self.fournisseur.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertFalse(Fournisseur.objects.filter(id=self.fournisseur.id).exists())  # Vérifie que le fournisseur a été supprimé
