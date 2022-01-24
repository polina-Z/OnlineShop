from django.urls import path
from . import views
import uuid
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Auth
    path('signup/', views.signup),
    path('login/', views.LoginView.as_view()),
    path('refresh_token/', views.RefreshTokenView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view()),

    # User
    path('customer/list/', views.UserListView.as_view()),
    path('customer/address/', views.AddressList.as_view()),
    path('customer/<uuid:pk>/', views.UserDetails.as_view()),
    path('profile/', views.ProfileView.as_view()),

    # Category
    path('category/list/', views.CategoryListView.as_view()),

    # Product
    path('products/list/', views.ProductListView.as_view()),
    path('products/create/', views.ProductCreateView.as_view()),

    # Shop
    path('shop/myshop/', views.MyShopsListView.as_view()),
    path('shop/myshop/create/', views.ShopCreateView.as_view()),

]


