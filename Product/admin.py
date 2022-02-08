from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdminCustomize(admin.ModelAdmin):
    list_display = ['title','price','datecreate','status']
    list_filter = ['user','datecreate','status']
    search_fields = ['title',]
    prepopulated_fields = {'slug':['product_id',]}
    raw_id_fields = ['user',]
    ordering = ['-dateupdate']
    list_editable = ['status',]