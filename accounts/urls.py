from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='registration'),
    path('auth/active/user/', VerifyCodeView.as_view(), name='verify_code'),
    path('auth/resend/code/', ResendCodeView.as_view(), name='resend_code'),
    path('auth/login/', TokenObtainPairView.as_view(), name='access_tocken)'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh_toocken'),
    path('auth/forgot-password/', RequestPasswordResetCodeView.as_view(), name='forgot_password_code'),
    path('auth/set_new_password/', SetNewPasswordView.as_view(), name='set_new_password'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),  
    path('auth/profile/', UserProfileView.as_view(), name='profile'),  
]
