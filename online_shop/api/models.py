from django.utils.timezone import now
from django.db import models
import uuid
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.contrib.postgres import fields
import PIL


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    country = models.CharField(max_length=60, null=False, verbose_name='Country')
    region = models.CharField(max_length=100, null=True, verbose_name='Region')
    town = models.CharField(max_length=100, verbose_name='Town')
    street = models.CharField(max_length=100, null=False, verbose_name='Street')
    house = models.CharField(max_length=10, null=False, verbose_name='House')
    flat = models.PositiveIntegerField(null=True, verbose_name='Flat')

    class Meta:
        unique_together = [['country', 'region', 'town', 'street', 'house', 'flat']]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        flat = self.flat

        if self.flat is None:
            flat = "-"

        return """Address:
                        country: {};
                        region: {};
                        town: {};
                        street: {};
                        house: {};
                        flat: {}""".format(self.country, self.region, self.town, self.street, self.house, flat)


class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ManyToManyField(Address, verbose_name="Address", related_name="customer_addresses", null=True)
    birthdate = models.DateField(verbose_name="Birth Date")
    image = models.ImageField(verbose_name="User Image", null=True, upload_to='customers/')
    phone = models.CharField(max_length=13, verbose_name="Phone Number")
    store_owner = models.BooleanField(default=False, verbose_name="Shop Owner")
    date_joined = models.DateField(default=now(), verbose_name="Date Joined")

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return "Customer username: {}".format(self.user.username)


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Category Name")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Category Image", upload_to='categories/')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return "Category: {}".format(self.title)


class Shop(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Shop Name")
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Shop Owner")
    image = models.ImageField(verbose_name="Shop Image", upload_to='shops/')
    info = models.TextField(verbose_name="Shop Info")
    created_date = models.DateField(verbose_name="Created Date")

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return "Shop: {}".format(self.title)


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Product Name")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Related Shop")
    description = models.TextField(verbose_name="Product Description")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField(default=0, verbose_name="Price")
    total_count = models.PositiveIntegerField(default=1, verbose_name="Number of products")
    created_at = models.DateField(default=now(), verbose_name="Created Date")
    size = fields.ArrayField(models.CharField(max_length=5), null=False, blank=False, default="M")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return "Product: {}".format(self.title)


class ProductColor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    COLOR_CHOICES = [
        ("#FFFFFF", "white"),
        ("#000000", "black"),
        ("#06bf06", "green"),
        ("#0625bf", "blue"),
        ("#ed0909", "red")
    ]
    color = ColorField(samples=COLOR_CHOICES)
    product = models.ForeignKey(Product, verbose_name="Related product", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', default="product_one.png", null=False, blank=False)

    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'

    def __str__(self):
        return "Product Image: {}".format(self.image.name)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=13, verbose_name="Phone Number")
    created_at = models.DateField(default=now(), verbose_name="Created Date")
    comment = models.TextField(verbose_name="Order comment")

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return "User order (username): {}".format(self.customer.user.username)
