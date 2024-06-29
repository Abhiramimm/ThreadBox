from django.contrib import admin

from store.models import Size,Brand,Category,Tag,Product

# Register your models here.

admin.site.register(Size)

admin.site.register(Brand)

admin.site.register(Category)

admin.site.register(Tag)

admin.site.register(Product)