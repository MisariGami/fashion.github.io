from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Size)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','color','size','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color','size')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
    list_display=('user','total_amt','paid_status','order_dt')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


admin.site.register(Wishlist)