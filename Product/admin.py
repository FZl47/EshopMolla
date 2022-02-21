from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Product)
class ProductAdminCustomize(admin.ModelAdmin):
    list_display = ['title','price','datecreate','status_show','status_available']
    list_filter = ['datecreate','status_show','status_available']
    search_fields = ['title',]
    ordering = ['-dateupdate']
    list_editable = ['status_show','status_available']

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(ProductStock)
admin.site.register(CartDetail)
admin.site.register(Cart)
admin.site.register(TypeProduct)
admin.site.register(WishList)
admin.site.register(WishDetail)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Coupon)