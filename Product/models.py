from django.db import models
from django.contrib.auth.models import User
from Config.Tools import RandomString
# Create your models here.



class ProductManager(models.Manager):
    def get_price_more_10(self):
        return self.filter(price__lt=10)

class ProductManagerCustomize(models.Manager):
    def get_queryset(self):
        return super(ProductManagerCustomize,self).get_queryset().filter(price__gt=3)

class Product(models.Model):
    STATUS_SHOW = (
        ('active','Active'),
        ('deactive','Deactive'),
    )
    product_id = models.CharField(max_length=20,default=RandomString)
    title = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    slug = models.SlugField()
    datecreate = models.DateTimeField(auto_now_add=True)
    dateupdate = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_SHOW,default='deactive')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='product')

    objects = ProductManager()
    getGreater_3 = ProductManagerCustomize()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title

