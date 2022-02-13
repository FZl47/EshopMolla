from django.db import models
from colorfield.fields import ColorField
from User.models import User
from Config.Tools import RandomString
from django.shortcuts import resolve_url
from django.utils import timezone
import datetime


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=40)

    @property
    def getTitle(self):
        return self.title.replace(' ', '-')

    def get_absolute_url(self):
        return f"{self.getTitle}-{self.id}"

    def __str__(self):
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=40)

    @property
    def getTitle(self):
        return self.title.replace(' ','-')

    def get_absolute_url(self):
        return f"{self.getTitle}-{self.id}"


    def __str__(self):
        return self.title


class ProductManagerCustomize(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status_show='active')


class Product(models.Model):
    STATUS_SHOW = (
        ('active', 'Active'),
        ('deactive', 'Deactive'),
    )
    STATUS_AVAILABLE = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )

    product_id = models.CharField(max_length=20, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    datecreate = models.DateTimeField(auto_now_add=True)
    dateupdate = models.DateTimeField(auto_now=True)
    status_show = models.CharField(max_length=10, choices=STATUS_SHOW, default='active')
    status_available = models.CharField(max_length=20, choices=STATUS_AVAILABLE, default='available')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    images = models.ManyToManyField(to='Product.Image', related_name='product')
    categories = models.ManyToManyField(Category, related_name='product')
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    colors = models.ManyToManyField('Product.Color', related_name='product')

    objects = models.Manager()
    getProducts = ProductManagerCustomize()

    class Meta:
        ordering = ('-id',)

    @property
    def gerPrice(self):
        return self.price

    @property
    def get_absolue_url(self):
        return f"{resolve_url('product:product')}/{self.title.replace(' ', '-')}-{self.product_id}"

    @property
    def getImageUrl(self):
        images = self.images
        if images.exists():
            return images.first().image.url
        # Image default for product
        return '/assets/images/default/product/Default.jpg'

    @property
    def isNew(self):
        # How long product is new
        _day = 4
        return True if (self.datecreate + datetime.timedelta(days=_day)) > timezone.now() else False

    def getRating(self):
        _rating = 2
        #  5 * 20 => 100%
        #  3 * 20 => 60%
        return _rating * 20   # برای گرفتن ریتینگ به صورت درصد

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.product_id = RandomString()
        super(Product, self).save(*args, **kwargs)


def upload_src_image(instance, path):
    _format = str(path).split('.')[-1]
    baseURL = 'products/images'
    return f'{baseURL}/{RandomString(20)}.{_format}'


class Image(models.Model):
    image = models.ImageField(upload_to=upload_src_image)

    def __str__(self):
        return 'image product'


class Color(models.Model):
    name = models.CharField(max_length=30)
    color = ColorField()

    def __str__(self):
        return self.name

    @property
    def getName(self):
        return self.name.replace(' ', '-')

    @property
    def get_absolute_url(self):
        return f"{self.getName}-{self.id}"
