# tests/test_product_items_views.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from monapp.models import Product, ProductItem
from monapp.forms import ProductItemForm

class ProductItemListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())
        self.product_item = ProductItem.objects.create(color='Red', code='RI001', product=self.product)

    def test_product_item_list_view_status_code(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)

    def test_product_item_list_view_template(self):
        response = self.client.get(reverse('item-list'))
        self.assertTemplateUsed(response, 'monapp/list_items.html')

    # def test_product_item_list_view_queryset(self):
    #     response = self.client.get(reverse('item-list'))
    #     self.assertQuerySetEqual(response.context['productitems'], [repr(self.product_item)])

class ProductItemDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())
        self.product_item = ProductItem.objects.create(color='Red', code='RI001', product=self.product)

    def test_product_item_detail_view_status_code(self):
        response = self.client.get(reverse('item-detail', args=[self.product_item.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_item_detail_view_template(self):
        response = self.client.get(reverse('item-detail', args=[self.product_item.id]))
        self.assertTemplateUsed(response, 'monapp/detail_item.html')

class ProductItemCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())

    def test_product_item_create_view_status_code(self):
        response = self.client.get(reverse('item-add'))
        self.assertEqual(response.status_code, 200)

    def test_product_item_create_view_template(self):
        response = self.client.get(reverse('item-add'))
        self.assertTemplateUsed(response, 'monapp/new_productItem.html')

    def test_product_item_create_view_post(self):
        response = self.client.post(reverse('item-add'), {
            'color': 'Blue',
            'code': 'BI001',
            'product': self.product.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(ProductItem.objects.filter(code='BI001').exists())  # Vérifie que le produit a été créé

class ProductItemUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())
        self.product_item = ProductItem.objects.create(color='Red', code='RI001', product=self.product)

    def test_product_item_update_view_post(self):
        response = self.client.post(reverse('item-update', args=[self.product_item.id]), {
            'color': 'Green',
            'code': 'RI001',
            'product': self.product.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirection après mise à jour
        self.product_item.refresh_from_db()
        self.assertEqual(self.product_item.color, 'Green')  # Vérifie que la couleur a été mise à jour

class ProductItemDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product = Product.objects.create(name='Test Product', code='TP001', price_ht=10.00, price_ttc=12.00, status=1, stock=100, date_creation=timezone.now())
        self.product_item = ProductItem.objects.create(color='Red', code='RI001', product=self.product)

    def test_product_item_delete_view_post(self):
        response = self.client.post(reverse('item-delete', args=[self.product_item.id]))
        self.assertEqual(response.status_code, 302)  # Redirection après suppression
        self.assertFalse(ProductItem.objects.filter(id=self.product_item.id).exists())  # Vérifie que l'élément a été supprimé
