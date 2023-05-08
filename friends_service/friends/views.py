from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship
from .forms import RegistrationForm, FriendRequestForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friends_service/friends/templates/friends/register.html', {'form': form})




@login_required
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        messages.error(request, 'You have already sent a friend request to this user')
        return redirect('user_detail', pk=receiver_id)
    elif Friendship.objects.filter(user1=request.user, user2=receiver).exists() or Friendship.objects.filter(user1=receiver, user2=request.user).exists():
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
            friendship = Friendship(user1=friend_request.sender, user2=friend_request.receiver)
            friendship.save()
            friend_request.accepted = True
            friend_request.save()
            messages.success(request, 'Friend request accepted')
        else:
            friend_request.delete()
            messages.success(request, 'Friend request rejected')
        return redirect('friend_requests')
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friends_service/friends/templates/friends/response_to_friend_request.html', {'friend_request': friend_request})


@login_required
def friend_requests(request):
    received_requests = FriendRequest.objects.filter(receiver=request.user)
    sent_requests = FriendRequest.objects.filter(sender=request.user)
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friends_service/friends/templates/friends/friend_requests.html', {'received_requests': received_requests, 'sent_requests': sent_requests})


@login_required
def friend_list(request):
    friendships1 = Friendship.objects.filter(user1=request.user)
    friendships2 = Friendship.objects.filter(user2=request.user)
    friends = []
    for friendship in friendships1:
        friends.append(friendship.user2)
    for friendship in friendships2:
        friends.append(friendship.user1)
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friends_service/friends/templates/friends/friend_list.html', {'friends': friends})


class UserListView(ListView):
    model = User
    template_name = '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friends_service/friends/templates/friends/friends/user_list.html'
    context_object_name = 'users'


class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friends_service/friends/templates/friends/user_update.html'
    success_url = reverse_lazy('friend_list')
