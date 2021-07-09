from django.db import models
from django.core.validators import MinValueValidator as minv, MaxValueValidator as maxv
from django.contrib.auth import get_user_model
from django.db.models import indexes
from django.db.models.fields import proxy

# getting user model
User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=110, verbose_name="اسم محصول", help_text="در اینجا اسم محصول را وارد نمایید")
    slug = models.SlugField(unique=True, verbose_name="آدرس محصول", allow_unicode=True)
    description = models.TextField(verbose_name="توضیحات محصول", help_text="در اینجا توضیحات کامل و دقیقی راجب محصول میتوانید ارائه کنید")
    category = models.ForeignKey("ProductCategory", on_delete=models.CASCADE, verbose_name="دسته بندی محصول", related_name="cproduct")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت محصول", help_text="در اینجا قیمت محصول را وارد نمایید") 
    quantity = models.IntegerField(validators=[minv(0)], verbose_name="موجودی", default=0)
    discountable = models.BooleanField(blank=True, default=False, verbose_name="تخفیف دارد؟")
    discount_amount = models.IntegerField(null=True, blank=True, validators=[minv(1), maxv(100)], verbose_name="میزان تخفیف", help_text="عددی مابین 1 تا 100 را وارد نمایید")
    properties = models.ManyToManyField("ProductProperty", verbose_name="ویژگی های کالا", related_name="pproduct") 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["title", "-price"]
        indexes = [
            models.Index(name="title_index", fields=["title"])
        ] 

class ProductCategory(models.Model):
    title = models.CharField(max_length=60, verbose_name="نام دسته بندی")
    slug = models.SlugField(unique=True, verbose_name="آدرس محصول", allow_unicode=True)
    description = models.TextField(verbose_name="توضیحات دسته بندی")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["title"]

class ProductProperty(models.Model):
    title = models.CharField(max_length=200, verbose_name="ویژگی", help_text="ویژگی را بصورت کامل وارد نمایید")
    value = models.CharField(max_length=255, verbose_name="مقدار ویژگی", help_text="مقدار را متناسب با ویژگی کامل کنید")
    place = models.IntegerField(validators=[minv(1)], verbose_name="جایگاه ویژگی")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"
        ordering = ["place"]  

class ProductImage(models.Model):
    title = models.CharField(max_length=120, verbose_name="عنوان عکس", help_text="عنوان عکس را وارد نمایید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pimage")
    image = models.ImageField(upload_to="ProductImages/%Y/%m/%d", verbose_name="عکس", help_text="عکس محصول را آپلود نمایید")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "عکس محصول"
        verbose_name_plural = "عکس های محصول"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="خریدار", related_name="ucart")   
    items = models.ManyToManyField("Item", verbose_name="اجناس", related_name="icart")
    is_ordered = models.BooleanField(default=False, verbose_name="آیا سفارش داده شده؟")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"سبد خرید | {self.user}"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید ها"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="خریدار", related_name="uorder")
    items = models.ManyToManyField("Item", verbose_name="اجناس", related_name="iorder")    
    is_purchased = models.BooleanField(default=False, verbose_name="آیا پرداخت شده؟")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by:{self.user} | {self.items} | {self.is_purchased}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ["created"]    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="خریدار", related_name="upayment")
    items = models.ManyToManyField("Item", verbose_name="اجناس", related_name="ipayment")
    total = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت کل")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.items}"

    class Meta:
        verbose_name = "خرید"
        verbose_name_plural = "خرید ها"    

class Item(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="اجناس", related_name="ipayment")
    quantity = models.IntegerField(validators=[minv(0)], verbose_name="موجودی", default=0)