from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

#Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="brand_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'
    
# Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")
    
    class Meta:
        verbose_name_plural='2. Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='3. Brands'

    def __str__(self):
        return self.title

# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural='4. Colors'
    
    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color: %s"></div>' % (self))


    def __str__(self):
        return self.title

# Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='5. Sizes'

    def __str__(self):
        return self.title

# Product
class Product(models.Model):
    title=models.CharField(max_length=200)
    
    slug=models.CharField(max_length=400)
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='6. Products'

    def __str__(self):
        return self.title

# Product attribute
class ProductAttribute(models.Model):     
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to="product_imgs/", null=True)

    class Meta:
        verbose_name_plural='7. ProductAttributes'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" />' % (self.image.url))

    def __str__(self):
        return self.product.title

# Order
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='8. Orders'

# OrderItems 
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='9. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" />' % (self.image))
    

#wishlist
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    # class Meta:
    #     verbose_name_plural='Wishlist'