from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup),
    path('login/', views.login),

    # User
    path('customer/list/', views.UserListView.as_view()),
    path('customer/address/', views.AddressList.as_view()),
]

