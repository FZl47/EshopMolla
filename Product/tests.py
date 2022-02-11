from django.test import TestCase
from . import models

class TestProductApp(TestCase):

    def test_get_product_active(self):
        products = models.Product.objects.exists()
        if products:
            prd = products.first()
            self.assertEqual(prd.status_available == 'available')


