from django.contrib import admin

from .models import Reference
from .models import Bar
from .models import Stock
from .models import Order
from .models import OrderItem

admin.site.register(Reference)
admin.site.register(Bar)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(OrderItem)
