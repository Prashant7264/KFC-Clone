from django.contrib import admin
from kfcstoreapp.models import product

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','is_active']
    list_filter=['price','is_active']


admin.site.register(product,productAdmin)