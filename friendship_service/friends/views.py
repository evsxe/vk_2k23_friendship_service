from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import Http404

from accounts.models import User
from .models import FriendRequest


@login_required
def friendship_requests(request):
    incoming_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    outgoing_requests = FriendRequest.objects.filter(from_user=request.user, accepted=False)
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friendship_service/accounts/templates/friends/templates/friends/friendship_requests.html',
                  {'incoming_requests': incoming_requests, 'outgoing_requests': outgoing_requests})


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, pk=request_id, to_user=request.user)
    friend_request.accepted = True
    friend_request.save()
    messages.success(request, f'You are now friends with {friend_request.from_user.username}.')
    return redirect('friendship_requests')


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, pk=request_id, to_user=request.user)
    friend_request.delete()
    messages.success(request, 'Friend request rejected.')
    return redirect('friendship_requests')


@login_required
def friends_list(request):
    friends = request.user.friends.all()
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friendship_service/accounts/templates/friends/templates/friends/friends_list.html', {'friends': friends})


@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(User, pk=friend_id)
    request.user.friends.remove(friend)
    messages.success(request, f'{friend.username} removed from friends.')
    return redirect('friends_list')


@login_required
def send_friend_request(request, to_user_id):
    to_user = get_object_or_404(User, pk=to_user_id)
    if request.user == to_user:
        raise Http404
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    messages.success(request, f'Friend request sent to {to_user.username}.')
    return redirect('user_profile', username=to_user.username)


@login_required
@require_POST
def cancel_friend_request(request, to_user_id):
    to_user = get_object_or_404(User, pk=to_user_id)
    FriendRequest.objects.filter(from_user=request.user, to_user=to_user).delete()
    messages.success(request, f'Friend request to {to_user.username} cancelled.')
    return redirect('user_profile', username=to_user.username)


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect('edit_profile')
    is_friend = request.user.is_friend_with(user)
    friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=user).first()
    return render(request, '/Users/evgeniysaluev/PycharmProjects/vk_2k23_friendship_service/friendship_service/accounts/templates/friends/templates/friends/user_profile.html',
                  {'user': user, 'is_friend': is_friend, 'friend_request': friend_request})
