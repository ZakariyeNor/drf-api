from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model):
    """
    Model to represent a follower/following relationship between users.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'  # Users this user is following
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed'  # Users who follow this user
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'followed')  # prevent duplicates
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner.username} follows {self.followed.username}"
