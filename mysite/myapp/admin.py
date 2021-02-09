from django.contrib import admin

# Register your models here.
from myapp.models import MyUser, Product, Order, Cancel

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cancel)