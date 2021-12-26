from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup),
    path('user/', views.UserApiView.as_view(), name='user'),
    path("user_list/", views.UserListView.as_view(), name="user_list"),
]