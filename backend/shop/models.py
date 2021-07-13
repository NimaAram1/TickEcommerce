from django.db import models
from django.core.validators import MinValueValidator as minv, MaxValueValidator as maxv
from django.contrib.auth import get_user_model
from django.utils.text import gettext_lazy as _

# getting user model
User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=110, verbose_name=_("Product's name"), help_text=_("Enter your product's name"))
    slug = models.SlugField(unique=True, verbose_name=_("Product's link'"), allow_unicode=True)
    description = models.TextField(verbose_name=_("Product's description"), help_text=_("Enter your product's description"))
    category = models.ForeignKey("ProductCategory", on_delete=models.CASCADE, verbose_name=_("Category"), related_name="cproduct")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=_("Price"), help_text=_("Enter your product's price")) 
    quantity = models.IntegerField(validators=[minv(0)], verbose_name=_("Quantity of products"), default=0)
    discountable = models.BooleanField(blank=True, default=False, verbose_name=_("Has a discount?"))
    discount_amount = models.IntegerField(null=True, blank=True, validators=[minv(1), maxv(100)], verbose_name=_("Amount of discount"), help_text=_("You must enter an integer from 0 to 100"))
    properties = models.ManyToManyField("ProductProperty", verbose_name=_("Product's properties"), related_name="pproduct") 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["title", "-price"]
        indexes = [
            models.Index(name="title_index", fields=["title"])
        ] 

class ProductCategory(models.Model):
    title = models.CharField(max_length=60, verbose_name=_("Category's name"))
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name=_("Category's link"))
    description = models.TextField(verbose_name=_("Category's description'"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["title"]

class ProductProperty(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Property's title"), help_text=_("Enter your property's title acording to it value"))
    value = models.CharField(max_length=255, verbose_name=_("Property's value"), help_text=_("Enter your property's value acording to it "))
    place = models.IntegerField(validators=[minv(1)], verbose_name=_("Property's place"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        ordering = ["place"]  

class ProductImage(models.Model):
    title = models.CharField(max_length=120, verbose_name=_("Pciture's title"), help_text=_("Enter your picture's title"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pimage")
    image = models.ImageField(upload_to="ProductImages/%Y/%m/%d", verbose_name=_("Image"), help_text=_("Upload your product's image"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _("Product's image")
        verbose_name_plural = _("Product's images")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Purchaser"), related_name="ucart")   
    items = models.ManyToManyField("Item", verbose_name=_("Items"), related_name="icart")
    is_ordered = models.BooleanField(default=False, verbose_name=_("Was the cart ordered?"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{_('Cart')} | {self.user}"

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Purchaser"), related_name="uorder")
    items = models.ManyToManyField("Item", verbose_name=_("Items"), related_name="iorder")    
    is_purchased = models.BooleanField(default=False, verbose_name=_("Was the items purchased?"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{_('Order by')}:{self.user} | {self.items} | {self.is_purchased}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["created"]    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Purchaser"), related_name="upayment")
    items = models.ManyToManyField("Item", verbose_name=_("Items"), related_name="ipayment")
    total = models.DecimalField(max_digits=12, decimal_places=0, verbose_name=_("Total price"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.items}"

    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")    

class Item(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Item"), related_name="ipayment")
    quantity = models.IntegerField(validators=[minv(0)], verbose_name=_("Quantity of item"), default=0)