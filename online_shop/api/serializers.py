from rest_framework import serializers
from shop.models import Customer

class UserAdminSerializer(serializers.ModelSerializer):
    password = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = "__all__"