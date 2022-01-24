from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BaseAuthentication


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        result = JWTAuthentication().authenticate(request)
        if result is not None:
            SessionAuthentication().enforce_csrf(request)
        return result
