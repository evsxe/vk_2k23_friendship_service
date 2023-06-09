from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from pathlib import Path

from .models import FriendRequest, Friendship
from .forms import RegistrationForm, LoginForm

PATH_TO_TEMPLATES = Path(Path.cwd(), 'friends', 'templates', 'friends')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(
        request,
        Path(PATH_TO_TEMPLATES, 'register.html'),
        {'form': form}
    )


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, Path(PATH_TO_TEMPLATES, 'user_detail.html'), {'user': user})


def home_view(request):
    return render(
        request,
        Path(PATH_TO_TEMPLATES, 'home.html')
    )


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # handle invalid login
            return render(
                request,
                Path(PATH_TO_TEMPLATES, 'login.html'),
                {'form': LoginForm(), 'error': 'Invalid login credentials'}
            )
    else:
        return render(
            request,
            Path(PATH_TO_TEMPLATES, 'login.html'),
            {'form': LoginForm()})


@login_required
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        messages.error(request, 'You have already sent a friend request to this user')
        return redirect('user_detail', pk=receiver_id)
    elif Friendship.objects.filter(user1=request.user, user2=receiver).exists() or \
            Friendship.objects.filter(user1=receiver, user2=request.user).exists():
        messages.error(request, 'You are already friends with this user')
        return redirect('user_detail', pk=receiver_id)
    else:
        friend_request = FriendRequest(sender=request.user, receiver=receiver)
        friend_request.save()
        messages.success(request, 'Friend request sent')
        return redirect('user_detail', pk=receiver_id)


@login_required
def response_to_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
    if friend_request.receiver != request.user:
        messages.error(request, 'You are not authorized to respond to this friend request')
        return redirect('friend_requests')
    if request.method == 'POST':
        accepted = request.POST.get('accepted')
        if accepted == 'true':
            if Friendship.objects.filter(
                    Q(user1=friend_request.sender, user2=friend_request.receiver) | Q(user1=friend_request.receiver,
                                                                                      user2=friend_request.sender)).exists():
                messages.warning(request, 'You have already accepted this friend request')
            else:
                friendship = Friendship(user1=friend_request.sender, user2=friend_request.receiver)
                friendship.save()
                friend_request.accepted = True
                friend_request.save()
                messages.success(request, 'Friend request accepted')
        else:
            friend_request.delete()
            messages.success(request, 'Friend request rejected')
        return redirect('friend_requests')
    return render(
        request,
        Path(PATH_TO_TEMPLATES, 'response_to_friend_request.html'),
        {'friend_request': friend_request}
    )


@login_required
def friend_requests(request):
    received_requests = FriendRequest.objects.filter(receiver=request.user)
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    return render(
        request,
        Path(PATH_TO_TEMPLATES, 'friend_requests.html'),
        {'received_requests': received_requests, 'sent_requests': sent_requests}
    )


@login_required
def friend_list(request):
    friendships1 = Friendship.objects.filter(user1=request.user)
    friendships2 = Friendship.objects.filter(user2=request.user)
    friends = []
    for friendship in friendships1:
        friends.append(friendship.user2)
    for friendship in friendships2:
        friends.append(friendship.user1)
    return render(
        request,
        Path(PATH_TO_TEMPLATES, 'friend_list.html'),
        {'friends': friends}
    )


class UserListView(ListView):
    model = User
    template_name = Path(PATH_TO_TEMPLATES, 'user_list.html')
    context_object_name = 'users'


class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = Path(PATH_TO_TEMPLATES, 'user_update.html')
    success_url = reverse_lazy('friend_list')
