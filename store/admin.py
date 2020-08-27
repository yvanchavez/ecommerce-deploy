from django.contrib import admin

from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
class ShippingAddressInline(admin.TabularInline):
    model = ShippingAddress
    fields = ['direccion','distrito','provincia']

class OrderAdmin(admin.ModelAdmin):
    list_display=('transaction_id','customer','get_cart_total','complete')
    inlines = [
        OrderItemInline,ShippingAddressInline
    ]
    def get_cart_total(self, object):
        return object.get_cart_total

    get_cart_total.short_description = "Total"




admin.site.register(User)
admin.site.register(PasswordReset)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)