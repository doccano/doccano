from django.db import models


class Label(models.Model):
    text = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10)

    def as_dict(self):
        return {'id': self.id,
                'text': self.text,
                'shortcut': self.shortcut}


class RawData(models.Model):
    text = models.TextField()

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


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    # password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class Project(models.Model):
    name = models.CharField(max_length=100)
    # users = models.ManyToManyField(User)
