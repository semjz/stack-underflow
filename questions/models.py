from django.db import models
from users.models import User
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Question(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    vote = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    vote = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
