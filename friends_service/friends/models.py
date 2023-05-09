from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def check_friendship(self):
        if Friendship.objects.filter(
                Q(user1=self.sender, user2=self.receiver) | Q(user1=self.receiver, user2=self.sender)).exists():
            return True
        else:
            return False


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')
    created_at = models.DateTimeField(auto_now_add=True)
