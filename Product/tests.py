from django.test import TestCase
from . import models

class TestProductApp(TestCase):

    def test_get_product_active(self):
        products = models.Product.objects.exists()
        if products:
            prd = products.first()
            self.assertEqual(prd.status_available == 'available')


    def test_page_products(self):
        x = self.client.get('http://127.0.0.1:8000/p/products?filter=true&cats=[%22Shoes-1%22,%22T-shirt-3%22]&brands=[%22Nike-1%22,%22Addidass-2%22,%22Poma-3%22]&colors=[%22Blue-sky-1%22,%22red-2%22,%22orange-3%22,%22Black-4%22,%22Gray-5%22,%22Gold-6%22,%22White-7%22,%22Green-8%22,%22Green-Light-9%22,%22Blue-10%22,%22Blue-Light-11%22]&range=0-20000')
        if x.status_code != 200:
            raise Exception('Error in test page products')