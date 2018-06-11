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
    text = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def as_dict(self):
        return {'id': self.id,
                'text': self.text,
                'shortcut': self.shortcut}


class RawData(models.Model):
    text = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def as_dict(self):
        return {'id': self.id,
                'text': self.text}


class Annotation(models.Model):
    prob = models.FloatField(blank=True, null=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    data = models.ForeignKey(RawData, on_delete=models.CASCADE)
    manual = models.BooleanField(default=False)

    def as_dict(self):
        return {'id': self.id,
                'data_id': self.data.id,
                'label_id': self.label.id,
                'prob': self.prob,
                'manual': self.manual}
