from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User


class MyLoginView(LoginView):
    template_name = '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friendship_service/accounts/templates/accounts/login.html'


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friendship_service/accounts/templates/accounts/logout.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friendship_service/accounts/templates/accounts/signup.html'
    success_url = reverse_lazy('home')
