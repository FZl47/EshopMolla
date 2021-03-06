from django.db import models
from django.db.models import Sum , F , Avg
from colorfield.fields import ColorField
from User.models import User
from Config.Tools import RandomString
from django.shortcuts import resolve_url
from django.utils import timezone
from django.core.validators import MinValueValidator
from Config.Tools import GetDifferenceTime
from ckeditor.fields import RichTextField
import datetime , random




# Create your models here.

class TypeProduct(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):return self.title


class Category(models.Model):
    title = models.CharField(max_length=40)

    @property
    def getTitle(self):
        return self.title.replace(' ', '-')

    def getSlug(self):
        return f"{self.getTitle}-{self.id}"

    def get_absolute_url_filter(self):
        return f"/p/products?filter=true&cats={self.getSlug()}"

    def get_absolute_url(self):
        return f"/p/category/{self.title}"


    def getProducts(self):
        return self.product.filter(productStock__count__gt=0).distinct()

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


def orderByPopulariy(products):
    products_sorted = sorted(sorted(products,key=lambda i: i.getRating()),key=lambda j: j.productIsStock)[::-1]
    return products_sorted

def orderByDate(products):
    return sorted(products.order_by('datecreate'),key=lambda i: i.productIsStock)[::-1]

def orderByPrice(products):
    return sorted(products.order_by('price'),key=lambda i: i.productIsStock)[::-1]

class ProductManagerCustomize(models.Manager):
    def get_queryset(self):
        products = super().get_queryset().filter(status_show='active')
        return products

    def getProductsStock(self):
        return self.get_queryset().filter(productStock__count__gt=0).distinct()



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
    type_product = models.ForeignKey('Product.TypeProduct',on_delete=models.CASCADE,related_name='product')
    title = models.CharField(max_length=300)
    description = RichTextField(null=True,blank=True)
    information = RichTextField(null=True,blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    datecreate = models.DateTimeField(auto_now_add=True)
    dateupdate = models.DateTimeField(auto_now=True)
    status_show = models.CharField(max_length=10, choices=STATUS_SHOW, default='active')
    status_available = models.CharField(max_length=20, choices=STATUS_AVAILABLE, default='available')
    images = models.ManyToManyField(to='Product.Image', related_name='product')
    categories = models.ManyToManyField(Category, related_name='product')
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)


    objects = models.Manager()
    getProducts = ProductManagerCustomize()

    class Meta:
        ordering = ('-id',)

    @property
    def gerPrice(self):
        return self.price

    def getSlug(self):
        slug = f"{self.title.replace(' ', '-')}-{self.product_id}"
        return slug

    @property
    def get_absolute_url(self):
        slug = self.getSlug()
        return resolve_url('product:product',slug=slug)

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
        _day = 2
        return True if (self.datecreate + datetime.timedelta(days=_day)) > timezone.now() else False

    @property
    def productIsStock(self):
        # Get all color seted for product if no color => out of stock
        stocks = self.productStock.all()
        for s in stocks:
            if s.productIsStock():
                return True
        return False

    def getRating(self):
        _rating = self.comments.aggregate(avgScores=Avg('score'))['avgScores'] or 0
        #  5 * 20 => 100%
        #  3 * 20 => 60%
        return _rating * 20 # for get rating by Percentage

    def getReviews(self):
        return 2

    def getColors(self):
        colors = Color.objects.filter(productStock__product__id=self.id,productStock__count__gt=0).distinct()
        return colors

    def getSizes(self):
        sizes = Size.objects.filter(productStock__product__id=self.id,productStock__count__gt=0).distinct()
        return sizes

    def getProductRelated(self):
        products = Product.getProducts.getProductsStock().filter(type_product=self.type_product).exclude(id=self.id).distinct()
        count_select_product = 7
        if products.count() < 5:
            count_select_product = products.count()
        products = random.sample(list(products),count_select_product)
        return products

    def getComments(self):
        return Comment.getComments.filter(product_id=self.id).distinct()


    def __str__(self):
        return self.title

    def __str_small__(self):
        return f"{self.title[:20]}..."

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


class Size(models.Model):
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product = models.ForeignKey('Product.Product',on_delete=models.CASCADE,related_name='productStock')
    count = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    color = models.ForeignKey('Product.Color',on_delete=models.CASCADE,related_name='productStock')
    size = models.ForeignKey('Product.Size',on_delete=models.CASCADE,related_name='productStock')

    def productIsStock(self):
        return self.count > 0

    def __str__(self):
        return f'{self.product.title}-{self.color.name}-{self.count}'



class Cart(models.Model):
    cart_id = models.CharField(max_length=50)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE,null=True)
    details = models.ManyToManyField('Product.CartDetail',related_name='cart')

    def save(self,*args,**kwargs):
        if self.pk is None:
            self.cart_id = RandomString(50)
        super(Cart,self).save(*args,**kwargs)


    def delete(self, *args, **kwargs):
        self.details.all().delete()
        super(Cart, self).delete(*args, **kwargs)

    @property
    def getPrice(self):
        return float(self.details.all().filter(product__status_show='active').aggregate(price=Sum(F('count') * F('product__price'),output_field=models.DecimalField(max_digits=12, decimal_places=2)))['price'] or 0)


    def getDetails(self):
        return self.details.all().filter(product__status_show='active')

    def getDetailsCount(self):
        return self.details.filter(product__status_show='active').count()


    def __str__(self):
        if self.user != None:
            return f'{self.user} - Cart'
        return f'{self.cart_id} - Cart'


class CartDetail(models.Model):
    productStock = models.ForeignKey('Product.ProductStock',on_delete=models.CASCADE)
    product = models.ForeignKey('Product.Product',on_delete=models.CASCADE)
    count = models.IntegerField()
    dateTimeCreated = models.DateTimeField(auto_now_add=True)


    def getPrice(self):
        if self.product.status_show == 'active':
            return self.count * self.product.price
        return 0

    def __str__(self):
        try:
            if self.cart.first().user != None:
                return f'{self.cart.first().user} - Cart Detail'
            return f'{self.cart.first().cart_id} - Cart Detail'
        except:
            return 'deleted'


class WishList(models.Model):
    wishlist_id = models.CharField(max_length=50)
    user = models.ForeignKey('User.User',on_delete=models.CASCADE,null=True)
    details = models.ManyToManyField('Product.WishDetail',related_name='wishlist')

    def getDetails(self):
        return self.details.all().filter(product__status_show='active')


    def __str__(self):
        if self.user != None:
            return f'{self.user} - WishList'
        return f'{self.wishlist_id} - WishList'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.wishlist_id = RandomString(50)
        super(WishList, self).save(*args, **kwargs)

        def delete(self, *args, **kwargs):
            self.details.all().delete()
            super(WishList, self).delete(*args, **kwargs)

class WishDetail(models.Model):
    product = models.ForeignKey('Product.Product',on_delete=models.CASCADE)
    dateTimeCreate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.wishlist.first() != None:
            if self.wishlist.first().user != None:
                return f'{self.wishlist.first().user} - Wish Detail'
            return f'{self.wishlist.first().wishlist_id} - Wish Detail'
        return 'deleted'


class Order(models.Model):
    user = models.ForeignKey('User.User',on_delete=models.CASCADE)
    dateTimeCreate = models.DateTimeField(auto_now_add=True)
    dateTimePay = models.DateTimeField(null=True)
    shipping = models.ForeignKey('Transportation.Shipping',on_delete=models.SET_NULL,null=True)
    shippingText = models.CharField(max_length=50,null=True)
    is_pay = models.BooleanField(default=False)
    withCoupon = models.BooleanField(default=False)
    couponPrice = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    coupon = models.ForeignKey('Product.Coupon',on_delete=models.SET_NULL,null=True,blank=True)
    priceProducts = models.DecimalField(max_digits=50,decimal_places=2,null=True)
    priceShipping = models.DecimalField(max_digits=12,decimal_places=2,null=True)
    total = models.DecimalField(max_digits=50,decimal_places=2,null=True)
    note = models.TextField(null=True)
    address = models.ForeignKey('Transportation.Address',on_delete=models.SET_NULL,null=True)
    addressText = models.TextField(null=True)

    def get_absolute_url(self):
        return resolve_url('user:getOrder',id=self.id)

    def getPrice(self):
        totalPriceProduct = self.getPriceProducts()
        return float(totalPriceProduct + self.shipping.price - self.couponPrice)

    def getPriceProducts(self):
        return self.orderdetail_set.all().aggregate(totalPriceProduct=Sum(F('product__price') * F('count')))['totalPriceProduct']

    def getTimePastPayment(self):
        return GetDifferenceTime(self.dateTimePay)

    def getDetails(self):
        return self.orderdetail_set.all()

    def __str__(self):
        return f'Order - {self.user}'


class OrderDetail(models.Model):
    order = models.ForeignKey('Product.Order',on_delete=models.CASCADE)
    product = models.ForeignKey('Product.Product',on_delete=models.SET_NULL,null=True)
    productStock = models.ForeignKey('Product.ProductStock',on_delete=models.SET_NULL,null=True)
    sizeText = models.CharField(max_length=50,null=True)
    colorText = models.CharField(max_length=50,null=True)
    count = models.IntegerField()

    def __str__(self):
        return f"Order detail - {self.order.user}"


class CommentManagerCustomize(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(checked=True).distinct()

class Comment(models.Model):
        user = models.ForeignKey('User.User',on_delete=models.CASCADE)
        product = models.ForeignKey('Product.Product',on_delete=models.CASCADE,related_name='comments')
        dateTimeCreate = models.DateTimeField(auto_now_add=True)
        title = models.CharField(max_length=70)
        message = models.TextField()
        score = models.IntegerField()
        checked = models.BooleanField(default=False)

        class Meta:
            ordering = ['-id']

        objects = models.Manager()
        getComments = CommentManagerCustomize()

        def getDateTimeCreate(self):
            return GetDifferenceTime(self.dateTimeCreate)


        def __str__(self):
            return f"{self.user.first_name or 'unknown'} - {self.product.title}"



class Coupon(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    dateTimeCreate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def getPrice(self,price):
        return int(price) - self.price














