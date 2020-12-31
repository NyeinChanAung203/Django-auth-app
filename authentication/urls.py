from django.urls import path
from .views import RegistrationView,LoginView,ActivateAccountView,HomeView,LogoutView,RequestResetEmailView,SetNewPasswordView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(HomeView.as_view()),name="home"),
    path('register',RegistrationView.as_view(),name="register"),
    path('login',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(),name="logout"),
    path('activate/<uidb64>/<token>/',ActivateAccountView.as_view(),name="activate"),
    path('request-reset-email/',RequestResetEmailView.as_view(),name="reset"),
    path('set-new-password/<uidb64>/<token>/',SetNewPasswordView.as_view(),name="set-new-password"),
]