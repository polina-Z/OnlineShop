from rest_framework import serializers
from .models import Customer, Address, Category, ProductColor, Product, ProductImage, Shop


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'country', 'region', 'town', 'street', 'house', 'flat']


class UserAdminSerializer(serializers.ModelSerializer):
    password = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image']


class ProductSerializer(serializers.ModelSerializer):
    # shop = ShopSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['title', 'shop', 'category', 'description', 'price', 'total_count', 'size']


class ProductColorSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductColor
        fields = ['color']


class ProductCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    size = serializers.ListField()

    class Meta:
        model = Product
        fields = "__all__"


class ShopAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['title', 'image', 'info']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
