from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Tweet(models.Model):
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='tweets')


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_comments')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,
                              related_name='tweet_comments')
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    content = models.TextField()
    user_from = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='message_send')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='message_received')
    read = models.BooleanField()


