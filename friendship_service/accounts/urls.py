from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import SignUpView, MyLoginView, MyLogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='template/accounts/password_reset.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='template/accounts/password_reset_done.html'), name='password_change_done'),
]