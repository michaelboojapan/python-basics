from django.db import models
from django.urls import reverse
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('tweets:tweet-detail', kwargs={'tweet_id': self.id})  # f"/pages/{self.id}/"

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'likes': random.randint(0, 200)
        }

    class Meta:
        ordering = ['-id']
