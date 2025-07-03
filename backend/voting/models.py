from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from django.core.validators import MinValueValidator, MaxValueValidator


class VotingConfiguration(models.Model):
    """Model to store voting configuration settings"""
    
    VOTING_METHOD_CHOICES = [
        ('approve_only', 'Apenas Aprovar'),
        ('disapprove_only', 'Apenas Reprovar'),
        ('approve_disapprove', 'Aprovar ou Reprovar'),
    ]
    
    STATUS_CHOICES = [
        ('configured', 'Configurada'),
        ('active', 'Ativa'),
        ('ended', 'Encerrada'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='voting_configurations')
    name = models.CharField(max_length=200, help_text="Nome da configuração de votação")
    description = models.TextField(help_text="Descrição da votação")
    voting_method = models.CharField(
        max_length=20, 
        choices=VOTING_METHOD_CHOICES, 
        default='approve_disapprove',
        help_text="Método de votação permitido"
    )
    start_date = models.DateField(help_text="Data de início da votação")
    end_date = models.DateField(help_text="Data de fim da votação")
    start_time = models.TimeField(help_text="Horário de início da votação")
    end_time = models.TimeField(help_text="Horário de fim da votação")
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='configured',
        help_text="Status atual da votação"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['project', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.project.name})"


class AnnotationRule(models.Model):
    """Model to store annotation rules for voting"""
    
    voting_configuration = models.ForeignKey(
        VotingConfiguration, 
        on_delete=models.CASCADE, 
        related_name='annotation_rules'
    )
    name = models.CharField(max_length=200, help_text="Nome da regra de anotação")
    description = models.TextField(help_text="Descrição detalhada da regra")
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Ordem de apresentação da regra"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['voting_configuration', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.voting_configuration.name})"


class Vote(models.Model):
    """Model to store individual votes on annotation rules"""
    
    VOTE_CHOICES = [
        ('approve', 'Aprovar'),
        ('disapprove', 'Reprovar'),
        ('neutral', 'Neutro'),
    ]
    
    annotation_rule = models.ForeignKey(
        AnnotationRule, 
        on_delete=models.CASCADE, 
        related_name='votes'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(
        max_length=15, 
        choices=VOTE_CHOICES,
        help_text="Voto do usuário na regra"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['annotation_rule', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.vote} - {self.annotation_rule.name}"
