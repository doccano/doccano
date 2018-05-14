from django.db import models


class Label(models.Model):
    text = models.CharField(max_length=100)


class Annotation(models.Model):
    text = models.TextField()
    prob = models.FloatField()
    labels = models.ManyToManyField(Label)
    # users = models.ManyToManyField(User)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    # password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class Project(models.Model):
    name = models.CharField(max_length=100)
    # users = models.ManyToManyField(User)
