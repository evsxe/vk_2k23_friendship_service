from django.test import TestCase
from django.contrib.auth.models import User
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
