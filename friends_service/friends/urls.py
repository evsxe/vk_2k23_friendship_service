from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    # path('login/', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    # path('users/<int:pk>/detail/', views.user_detail, name='user_detail'),
    path('users/<int:receiver_id>/send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('friend_requests/<int:friend_request_id>/response/', views.response_to_friend_request, name='response_to_friend_request'),
    path('friend_list/', views.friend_list, name='friend_list'),
]
