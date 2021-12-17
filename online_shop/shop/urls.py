from django.urls import path
from .views import RegistrationView

urlpatterns = [
    # Auth
    path('signup/', RegistrationView.as_view(), name='signup')
]
