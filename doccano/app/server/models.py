from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Label(models.Model):
    text = models.CharField(max_length=100, unique=True)
    shortcut = models.CharField(max_length=10, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def as_dict(self):
        return {'id': self.id,
                'text': self.text,
                'shortcut': self.shortcut}

    def __str__(self):
        return self.text


class Document(models.Model):
    text = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def as_dict(self):
        return {'id': self.id,
                'text': self.text}

    def __str__(self):
        return self.text[:50]


class Annotation(models.Model):
    prob = models.FloatField(blank=True, null=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    data = models.ForeignKey(Document, related_name='annotations', on_delete=models.CASCADE)
    manual = models.BooleanField(default=False)

    def as_dict(self):
        return {'id': self.id,
                'doc': self.data.as_dict(),
                'label': self.label.as_dict(),
                'prob': self.prob,
                'manual': self.manual}
