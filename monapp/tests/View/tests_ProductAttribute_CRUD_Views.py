# tests/test_product_attributes_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import ProductAttribute
from monapp.forms import ProductAttributeForm

class ProductAttributeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name='Color')

    def test_product_attribute_list_view_status_code(self):
        response = self.client.get(reverse('attribute-list'))
        self.assertEqual(response.status_code, 200)

    def test_product_attribute_list_view_template(self):
        response = self.client.get(reverse('attribute-list'))
        self.assertTemplateUsed(response, 'monapp/list_attributes.html')

    # def test_product_attribute_list_view_queryset(self):
    #     response = self.client.get(reverse('attribute-list'))
    #     self.assertQuerySetEqual(response.context['productattributes'], [repr(self.product_attribute)])

class ProductAttributeDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name='Color')

    def test_product_attribute_detail_view_status_code(self):
        response = self.client.get(reverse('attribute-detail', args=[self.product_attribute.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_attribute_detail_view_template(self):
        response = self.client.get(reverse('attribute-detail', args=[self.product_attribute.id]))
        self.assertTemplateUsed(response, 'monapp/detail_attribute.html')

class ProductAttributeCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_product_attribute_create_view_status_code(self):
        response = self.client.get(reverse('attribute-add'))
        self.assertEqual(response.status_code, 200)

    def test_product_attribute_create_view_template(self):
        response = self.client.get(reverse('attribute-add'))
        self.assertTemplateUsed(response, 'monapp/new_productAttribute.html')

    def test_product_attribute_create_view_post(self):
        response = self.client.post(reverse('attribute-add'), {
            'name': 'Size'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(ProductAttribute.objects.filter(name='Size').exists())  # Vérifie que l'attribut a été créé

class ProductAttributeUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name='Color')

    def test_product_attribute_update_view_post(self):
        response = self.client.post(reverse('attribute-update', args=[self.product_attribute.id]), {
            'name': 'New Color'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après mise à jour
        self.product_attribute.refresh_from_db()
        self.assertEqual(self.product_attribute.name, 'New Color')  # Vérifie que le nom a été mis à jour

class ProductAttributeDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name='Color')

    def test_product_attribute_delete_view_post(self):
        response = self.client.post(reverse('attribute-delete', args=[self.product_attribute.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertFalse(ProductAttribute.objects.filter(id=self.product_attribute.id).exists())  # Vérifie que l'attribut a été supprimé
