from django.test import TestCase
from django.test import Client
from django.core.management import call_command
from mainapp.models import Product


class TestMainappSmoke(TestCase):
    def setUp(self) -> None:
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mainapp/index.html')

        response = self.client.get('/products/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mainapp/contact.html')

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mainapp/products.html')

        for product in Product.objects.all():
            self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('mainapp/product.html')
