from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Customer, Address, Category, Product, Shop
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .permissions import IsOwnerOrReadOnly, IsShopOwner, IsProductOwner
from .serializers import UserAdminSerializer, AddressSerializer, CustomerSerializer, CategorySerializer
from .serializers import ProductSerializer, ProductCreateSerializer, ShopAddSerializer, ShopSerializer
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.utils import timezone


# User
class UserListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetails(generics.RetrieveAPIView):
    serializer_class = UserAdminSerializer
    queryset = Customer.objects.all()


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
            login(request)
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except KeyError:
            return JsonResponse({"error": "All necessary fields not provided"}, status=400)
        except IntegrityError as ex:
            return JsonResponse({"error": str(ex)}, status=400)
#
#
# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         user = authenticate(request, username=data['username'], password=data['password'])
#         if user is None:
#             return JsonResponse({'error': 'Could not login. Please check username and password'}, status=400)
#         else:
#             try:
#                 token = Token.objects.get(user=user)
#             except:
#                 token = Token.objects.create(user=user)
#             return JsonResponse({'token': str(token)}, status=200)


class LoginView(APIView):

    def post(self, request):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                response.set_cookie(
                    key=settings.COOKIE_APP['REFRESH_NAME'],
                    value=str(refresh),
                    expires=timezone.localtime() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.COOKIE_APP['SECURE'],
                    httponly=settings.COOKIE_APP['HTTP_ONLY'],
                    samesite=settings.COOKIE_APP['SAMESITE']
                )
                csrf.get_token(request)
                response.data = {'access': str(refresh.access_token)}
                return response
            else:
                return Response({"detail": "This account is not active"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie(
            key=settings.COOKIE_APP['REFRESH_NAME'],
            path=settings.COOKIE_APP['PATH'],
            domain=settings.COOKIE_APP['DOMAIN'],
            samesite=settings.COOKIE_APP['SAMESITE'],
        )
        return response


class RefreshTokenView(APIView):

    def post(self, request):
        try:
            refresh = RefreshToken(request.COOKIES['refresh_token'])
        except KeyError:
            return Response({"detail": "Refresh token is missing"}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            return Response({'detail': e.args[0]}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'access': str(refresh.access_token)})


class AddressList(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        return customer.address.all()


class ProfileView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)


# Product type
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()[:5]
    serializer_class = CategorySerializer


class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsShopOwner]


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsShopOwner]


# Products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsShopOwner]


class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsProductOwner]


class ShopCreateView(generics.CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopAddSerializer
    permission_classes = [IsShopOwner]


class MyShopsListView(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsShopOwner]

    def get_queryset(self):
        print(self.request.user)
        customer = Customer.objects.get(user=self.request.user)
        return Shop.objects.filter(owner=customer)
