from django.db import models
from User.models import User
from Config.Tools import RandomString
from django.shortcuts import resolve_url
# Create your models here.



class Category(models.Model):
    title = models.CharField(max_length=40)

    @property
    def getTitle(self):
        return self.title.replace(' ','-')

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS_SHOW = (
        ('active','Active'),
        ('deactive','Deactive'),
    )

    product_id = models.CharField(max_length=20,editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    datecreate = models.DateTimeField(auto_now_add=True)
    dateupdate = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_SHOW,default='deactive')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    images = models.ManyToManyField(to='Product.Image',related_name='product')
    categories = models.ManyToManyField(Category,related_name='product')

    class Meta:
        ordering = ('-id',)


    @property
    def get_absolue_url(self):
        return f"{resolve_url('product:product')}/{self.title.replace(' ','-')}-{self.product_id}"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.product_id = RandomString()
        super(Product, self).save(*args, **kwargs)



def upload_src_image(instance,path):
    _format = str(path).split('.')[-1]
    baseURL = 'products/images'
    return f'{baseURL}/{RandomString(20)}.{_format}'

class Image(models.Model):
    image = models.ImageField(upload_to=upload_src_image)

    def __str__(self):
        return 'image product'