from django.urls import path
from .views import friendship_requests, accept_friend_request, reject_friend_request, friends_list, remove_friend, send_friend_request, cancel_friend_request, user_profile

urlpatterns = [
    path('', friendship_requests, name='friendship_requests'),
    path('accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friends/', friends_list, name='friends_list'),
    path('remove/<int:friend_id>/', remove_friend, name='remove_friend'),
    path('send_request/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('cancel_request/<int:to_user_id>/', cancel_friend_request, name='cancel_friend_request'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
]