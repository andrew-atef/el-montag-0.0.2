from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
# Create your models here.

class Features(models.Model):
    image = models.ImageField(upload_to='media/img/%y/%m/%d', null=True, blank=True)

class Home_grid_slider(models.Model):
    image = models.ImageField(upload_to='media/img/%y/%m/%d', null=True, blank=True)


class Category(models.Model):
    choices = (
        ('category1','category1'),
        ('category2','category2'),
        ('category3','category3'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    home_slider = models.CharField(max_length=100, null=True, blank=True, choices=choices)
    def __str__(self):
        return self.name

class Governorates(models.Model):
    name = models.CharField(max_length=100)
    region = models.TextField(max_length=2800)
    shipping = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.name

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class All_image(models.Model):
    image = models.ImageField(upload_to='media/img/%y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.image.url


class Product(models.Model):
    title = models.CharField(max_length=250)
    desc = HTMLField()
    price = models.DecimalField(max_digits=6, decimal_places=1, default=0.0, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=6, decimal_places=1, default=0.0, null=True, blank=True)
    discount_percentage = models.CharField(max_length=5, null=True, blank=True)
    affiliate_earn = models.DecimalField(max_digits=6, decimal_places=1, default=0.0, null=True, blank=True)
    coupon_discount = models.DecimalField(max_digits=6, decimal_places=1, default=0.0, null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    main_image = models.ImageField(upload_to='media/main_image/%y/%m/%d')
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    all_image = models.ManyToManyField(All_image, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # has many Cart

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if self.discount_percentage:
    #         self.sale_price = ((100 - float(self.discount_percentage)) / 100) * float(self.price)
    #     super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    affiliate_code = models.CharField(max_length=10, null=True, blank=True)
    # has many Item

    def __str__(self):
        return f'{self.user.username} Cart'


class Address_details(models.Model):
    governorates = (
        ('القاهرة', 'القاهرة'),
        ('الجيزة', 'الجيزة'),
        ('الإسكندرية', 'الإسكندرية'),
        ('الإسماعيلية', 'الإسماعيلية'),
        ('بور سعيد', 'بور سعيد'),
        ('السويس', 'السويس'),
        ('أسوان', 'أسوان'),
        ('أسيوط', 'أسيوط'),
        ('الأقصر', 'الأقصر'),
        ('البحر الأحمر', 'البحر الأحمر'),
        ('البحيرة', 'البحيرة'),
        ('بنى سويف', 'بنى سويف'),
        ('جنوب سيناء', 'جنوب سيناء'),
        ('الدقهلية', 'الدقهلية'),
        ('دمياط', 'دمياط'),
        ('سوهاج', 'سوهاج'),
        ('الشرقية', 'الشرقية'),
        ('سينا', 'سينا'),
        ('الغربية', 'الغربية'),
        ('الفيوم', 'الفيوم'),
        ('القليوبية', 'القليوبية'),
        ('قنا', 'قنا'),
        ('كفر الشيخ', 'كفر الشيخ'),
        ('مطروح', 'مطروح'),
        ('المنوفية', 'المنوفية'),
        ('المنيا', 'المنيا'),
        ('الوادى الجديد', 'الوادى الجديد'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    number1 = models.CharField(max_length=20)
    number2 = models.CharField(max_length=20, null=True, blank=True)
    governorate = models.CharField(max_length=50, choices=governorates)
    region = models.CharField(max_length=50)
    address = models.TextField(max_length=1000, blank=False)
    active = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    shipping = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # has one cart

    def __str__(self):
        return f'{self.user.username} Address details - id: {self.id}'


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} -  {self.id}"


class Order(models.Model):
    all_status = (
        ('جاري تاكيد الطلب','جاري تاكيد الطلب'),
        ('جاري تجهيز الطلب','جاري تجهيز الطلب'),
        ('قيد التوصيل','قيد التوصيل'),
        ('تم التوصيل','تم التوصيل'),
        ('تعليق التوصيل','تعليق التوصيل'),
        ('تم إلغاء أو رفض الطلب','تم إلغاء أو رفض الطلب'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    number1 = models.CharField(max_length=11)
    number2 = models.CharField(max_length=11, null=True, blank=True)
    governorate = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    address = models.TextField(max_length=1000)
    notes = models.TextField(max_length=1000, null=True, blank=True)
    coupon = models.CharField(max_length=100, null=True, blank=True)
    coupon_discount = models.CharField(max_length=5, null=True, blank=True)
    total = models.CharField(max_length=10)
    earn = models.CharField(max_length=10)
    affiliate_code = models.CharField(max_length=10, null=True, blank=True)
    shipping = models.CharField(max_length=10)
    payable = models.CharField(max_length=20)
    items = models.TextField(max_length=2000)
    status = models.CharField(max_length=50, choices=all_status)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
