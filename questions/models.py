from django.db import models
from users.models import User
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name="question_upvoters")
    downvoters = models.ManyToManyField(User, related_name="question_downvoters")
    tags = models.ManyToManyField(Tag)

    @property
    def votes(self):
        return self.upvoters.count() - self.downvoters.count()


class Answer(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvoters = models.ManyToManyField(User, related_name="answer_upvoters")
    downvoters = models.ManyToManyField(User, related_name="answer_downvoters")

    @property
    def votes(self):
        return self.upvoters.count() - self.downvoters.count()

