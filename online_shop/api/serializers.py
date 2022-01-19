from rest_framework import serializers
from shop.models import Customer, Address, Category, ProductColor, Product, ProductImage


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
        fields = ['title', 'slug']
