from django.test import TestCase
from . import models
from User.models import User
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


    def test_create_obj_color(self):
        return models.Color.objects.create(name='TEST_COLOR_NAME',color='#FFF')


    def test_create_obj_type_product(self):
        return models.TypeProduct.objects.create(title='TEST_TITLE')


    def test_create_obj_brand(self):
        return models.Brand.objects.create(title='TEST_TITLE')


    def test_create_obj_product(self):
        type_product = self.test_create_obj_type_product()
        user = User.objects.create(username='TEST_USER',password='TEST_PASSWORD')
        brand = self.test_create_obj_brand()
        p = models.Product(type_product_id=type_product.id,title='TEST_VALUE',description='TEST_VALUE',information='TEST_VALUE',price=0,user_id=user.id,brand_id=brand.id)
        p.save()
        return p


    def test_add_comment_product(self):
        product = self.test_create_obj_product()
        user = User.objects.create(username='TEST_USER_2',password='TEST_PASSWORD')
        comment = models.Comment.objects.create(user_id=user.id,product_id=product.id,title='TEST_TITLE',message='TEST_VALUE',score=5)
        return comment
