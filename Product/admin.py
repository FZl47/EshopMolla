from django.contrib import admin
from .models import Product , Category , Image
# Register your models here.

@admin.register(Product)
class ProductAdminCustomize(admin.ModelAdmin):
    list_display = ['title','price','datecreate','status']
    list_filter = ['user','datecreate','status']
    search_fields = ['title',]
    ordering = ['-dateupdate']
    list_editable = ['status',]

admin.site.register(Category)
admin.site.register(Image)