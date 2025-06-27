from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Discussion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.title} ({self.project.name})'


class ChatMessage(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:30]}"
