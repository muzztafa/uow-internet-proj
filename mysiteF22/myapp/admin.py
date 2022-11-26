from django.contrib import admin
from .models import Product, Category, Client, Order
from django.db.models import F


"""
An F() object represents the value of a model field, transformed value of a model field, or 
annotated column. It makes it possible to refer to model field values and perform database operations
using them without actually having to pull them out of the database into Python memory.

Instead, Django uses the F() object to generate an SQL expression that describes 
the required operation at the database level.
"""


# Feature 3
def add_stock(modeladmin, request, queryset):
    queryset.update(stock=F('stock') + 50)


add_stock.short_description = "Add 50 items to Stock"


class ProductAdmin(admin.ModelAdmin):
    # Feature 1
    list_display = ('name', 'category', 'price', 'stock', 'available')
    # Feature 3
    actions = [add_stock]


# Feature 2
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'cat_list')

    @admin.display(description='Interested In (Categories)')
    def cat_list(self, obj):
        return ", \n".join([c.name for c in obj.interested_in.all()])


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)
