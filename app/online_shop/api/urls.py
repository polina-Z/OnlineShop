from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup),
    path('login/', views.login),
    path("user_list/", views.UserListView.as_view(), name="user_list"),
]
