from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from monapp.views import ProductAttributeValueCreateView, ProductAttributeValueListView
from monapp.models import ProductAttribute, ProductAttributeValue
from django.contrib.auth.models import User 

class ProductAttributeValueTestUrls(SimpleTestCase):
    def test_create_view_url_is_resolved(self):
        """
        Tester que l'URL de la création de ProductAttributeValue renvoie la bonne vue
        """
        url = reverse('attributeValue-add')
        self.assertEqual(resolve(url).func.view_class, ProductAttributeValueCreateView)
    def test_list_view_url_is_resolved(self):
        """
        Tester que l'URL de la liste de ProductAttributeValue renvoie la bonne vue
        """
        url = reverse('attributeValue-list')
        self.assertEqual(resolve(url).func.view_class, ProductAttributeValueListView)


class ProductAttributeValueTestUrlResponses(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
    def test_create_view_status_code(self):
        """
        Tester que l'URL de créationProductAttribute renvoie un statut 200 (OK)
        """
        response = self.client.get(reverse('attributeValue-add'))
        self.assertEqual(response.status_code, 200)
    def test_list_view_status_code(self):
        """
        Tester que l'URL de la liste renvoie un statut 200 (OK)
        """
        response = self.client.get(reverse('attributeValue-list'))
        self.assertEqual(response.status_code, 200)


class ProductAttributeValueTestUrlResponsesWithParameters(TestCase):
    def setUp(self):
        self.attribute = ProductAttribute.objects.create(name="Couleur")
        self.value = ProductAttributeValue.objects.create( value="Rouge",
        product_attribute=self.attribute)
    def test_detail_view_status_code(self):
        """
        Tester que l'URL des détails renvoie un statut 200 pour un ID valide
        """
        url = reverse('attributeValue-detail', args=[self.value.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_detail_view_status_code_invalid_id(self):
        """
        Tester que l'URL des détails renvoie un statut 404 pour un ID invalide
        """
        url = reverse('attributeValue-detail', args=[9999]) # ID non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class ProductAttributeValueTestUrlResponsesWithParameters(TestCase):
    def setUp(self):
        self.attribute = ProductAttribute.objects.create(name="Couleur")
        self.value = ProductAttributeValue.objects.create( value="Rouge",
        product_attribute=self.attribute)
    def test_detail_view_status_code(self):
        """
        Tester que l'URL des détails renvoie un statut 200 pour un ID valide
        """
        url = reverse('attributeValue-detail', args=[self.value.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_detail_view_status_code_invalid_id(self):
        """
        Tester que l'URL des détails renvoie un statut 404 pour un ID invalide
        """
        url = reverse('attributeValue-detail', args=[9999]) # ID non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class ProductAttributeValueTestUrlRedirect(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        # Créer un attribut produit de test pour l'utiliser dans le formulaire
        self.product_attribute = ProductAttribute.objects.create(name="Couleur")
    def test_redirect_after_creation(self):
        """
        Tester qu'après la création d'un ProductAttributeValue, l'utilisateur est redirigé correctement
        """
        response = self.client.post(reverse('attributeValue-add'), {
        'value': 'Bleu',
        'product_attribute': self.product_attribute.id,
        'position': 2 } )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monapp/attribute/value/1')