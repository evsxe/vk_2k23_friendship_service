from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from . import views
from .models import FriendRequest, Friendship


class TestModels(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='user1', password='password1')
        cls.user2 = User.objects.create_user(username='user2', password='password2')
        cls.user3 = User.objects.create_user(username='user3', password='password3')

    def test_create_friend_request(self):
        friend_request = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)
        self.assertEqual(friend_request.sender, self.user1)
        self.assertEqual(friend_request.receiver, self.user2)
        self.assertFalse(friend_request.accepted)

    def test_check_friendship_false(self):
        friend_request = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)
        self.assertFalse(friend_request.check_friendship())

    def test_check_friendship_true(self):
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        friend_request = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)
        self.assertTrue(friend_request.check_friendship())

    def test_create_friendship(self):
        friendship = Friendship.objects.create(user1=self.user1, user2=self.user2)
        self.assertEqual(friendship.user1, self.user1)
        self.assertEqual(friendship.user2, self.user2)


class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_user_list_url_resolves(self):
        url = reverse('user_list')
        self.assertEqual(resolve(url).func.view_class, views.UserListView)

    def test_user_update_url_resolves(self):
        url = reverse('user_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.UserUpdateView)

    def test_login_view_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_home_view_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home_view)

    def test_user_detail_url_resolves(self):
        url = reverse('user_detail', args=[1])
        self.assertEqual(resolve(url).func, views.user_detail)

    def test_send_friend_request_url_resolves(self):
        url = reverse('send_friend_request', args=[1])
        self.assertEqual(resolve(url).func, views.send_friend_request)

    def test_friend_requests_url_resolves(self):
        url = reverse('friend_requests')
        self.assertEqual(resolve(url).func, views.friend_requests)

    def test_response_to_friend_request_url_resolves(self):
        url = reverse('response_to_friend_request', args=[1])
        self.assertEqual(resolve(url).func, views.response_to_friend_request)

    def test_friend_list_url_resolves(self):
        url = reverse('friend_list')
        self.assertEqual(resolve(url).func, views.friend_list)