from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from shop.models import Customer, Address, Category, Product
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.models import Token
from .permissions import IsShopOwner
from .serializers import UserAdminSerializer, AddressSerializer, CustomerSerializer, CategorySerializer


# User
class UserListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            extra_fields = dict()
            extra_fields_2 = dict()
            for i in ["birthdate", "image", "phone", "store_owner"]:
                extra_fields[i] = data[i]
            for i in ["country", "region", "town", "street", "house", "flat"]:
                extra_fields_2[i] = data[i]

            address, is_created = Address.objects.get_or_create(**extra_fields_2)
            user = User.objects.create_user(
                data['username'],
                password=data['password'],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            user.save()
            customer = Customer.objects.create(
                user=user, **extra_fields
            )
            customer.address.add(address)
            user_login = authenticate(username=data['username'], password=data['password'])
            login(request, user_login)
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except KeyError:
            return JsonResponse({"error": "All necessary fields not provided"}, status=400)
        except IntegrityError as ex:
            return JsonResponse({"error": str(ex)}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error': 'Could not login. Please check username and password'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)


class AddressList(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        return customer.address.all()


# Product type
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser, IsShopOwner]
