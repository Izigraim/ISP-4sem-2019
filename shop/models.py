from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from transliterate import translit
from decimal import Decimal
from django.conf import settings
from djongo import models as mdl


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


class Brand(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class ProductManager(models.Manager):

    def all(self):
        return super(ProductManager, self).get_queryset().filter(available=True, quantity__gt=0)


class Product(models.Model):

    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    processor = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0)
    ozu = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0)
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    predicted_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    objects = ProductManager()

    def __str__(self):
        return u'%s' % (self.title)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(str(instance.title))
        instance.slug = slug


pre_save.connect(pre_save_product_slug, sender=Product)


class CartItem(models.Model):

    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2,default=0.00)

    def __str__(self):
        return "Cart item for product {0}".format(self.product.title)


class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
)


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    items = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')), default='Самовывоз')
    data = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return "Заказ №{0}".format(self.id)


class Comment(mdl.Model):

    created_at = mdl.DateTimeField(auto_now_add=True, auto_now=False)

    name = mdl.CharField(max_length=20, null=True)
    comment = mdl.TextField(max_length=1000, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.name, self.created_at)
