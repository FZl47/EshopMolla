from django.contrib import admin
from .models import Product , Category , Image , Color , Size , Brand , ProductStock
# Register your models here.

@admin.register(Product)
class ProductAdminCustomize(admin.ModelAdmin):
    list_display = ['title','price','datecreate','status_show','status_available']
    list_filter = ['user','datecreate','status_show','status_available']
    search_fields = ['title',]
    ordering = ['-dateupdate']
    list_editable = ['status_show','status_available']

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(ProductStock)