from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_dt').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='topics')
    last_updated = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='topics')
    created_dt = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.CASCADE)
    updated_dt = models.DateTimeField(null=True)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='posts')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    created_dt = models.DateTimeField(auto_now_add=True)
    # * for update data  after add button edit
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.CASCADE)
    updated_dt = models.DateTimeField(null=True)

    def __str__(self):
        trancated_message = Truncator(self.message)
        return trancated_message.chars(30)
