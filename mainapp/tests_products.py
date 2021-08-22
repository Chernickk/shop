from django.test import TestCase
from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="стулья")
        self.product_1 = Product.objects.create(name="стул 1",
                                                category=category,
                                                price=1999.5,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="стул 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_deleted=True)

        self.product_3 = Product.objects.create(name="стул 3",
                                                category=category,
                                                price=998.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertIn('стул 1', str(product_1))
        self.assertIn('стул 2', str(product_2))

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="стул 1")
        product_3 = Product.objects.get(name="стул 3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
