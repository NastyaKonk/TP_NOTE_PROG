# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from monapp.models import Product, ProductAttribute, ProductAttributeValue


class ProductListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())

    def test_product_list_view_status_code(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_template(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('product-list'))
        self.assertTemplateUsed(response, 'monapp/list_products.html')

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())

    def test_product_detail_view_status_code(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_template(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertTemplateUsed(response, 'monapp/detail_product.html')

class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')

    def test_product_create_view_status_code(self):
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_template(self):
        response = self.client.get(reverse('product-add'))
        self.assertTemplateUsed(response, 'monapp/new_product.html')

    def test_product_create_view_post(self):
        response = self.client.post(reverse('product-add'), {
            'name': 'New Product',
            'code': 'NP001',
            'price_ht': 15.00,
            'price_ttc': 18.00,
            'status': 1,
            'stock': 50,
            'date_creation': timezone.now()
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création

class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())

    def test_product_update_view_post(self):
        response = self.client.post(reverse('product-update', args=[self.product.id]), {
            'name': 'Updated Product',
            'code': 'TP001',
            'price_ht': 20.00,
            'price_ttc': 24.00,
            'status': 1,
            'stock': 150,
            'date_creation': timezone.now()
        })
        self.assertEqual(response.status_code, 302)  # Redirection après mise à jour
        self.product.refresh_from_db()
        self.assertEqual(self.product.price_ht, 20.00)

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())

    def test_product_delete_view_post(self):
        response = self.client.post(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())  # Vérifie que le produit a été supprimé
