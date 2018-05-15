from django.db import models


class Label(models.Model):
    text = models.CharField(max_length=100)

    def as_dict(self):
        return {'id': self.id, 'text': self.text}


class Annotation(models.Model):
    text = models.TextField()
    prob = models.FloatField(blank=True, null=True)
    labels = models.ManyToManyField(Label, blank=True, null=True)
    # users = models.ManyToManyField(User)

    def as_dict(self):
        return {'id': self.id, 'text': self.text, 'prob': self.prob}


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    # password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class Project(models.Model):
    name = models.CharField(max_length=100)
    # users = models.ManyToManyField(User)
