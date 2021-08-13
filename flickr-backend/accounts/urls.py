from django.urls import path
from .api.views import *
from .api import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'accounts'

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="signup"),
     path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('password-reset-email', RequestPasswordResetEmail.as_view(),
         name="reset=pass"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheck.as_view(),
         name="password-reset-confirm"),
    path('password-reset-complete/', SetNewPassword.as_view(),
         name="password-reset-complete"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete-account/', views.DeleteAccount, name='delete-account'),

]
