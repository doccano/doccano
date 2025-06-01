from django.db import models

class Group(models.Model):
    # Define fields exactly as they exist in auth_group
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'auth_group'  # Explicitly map to existing table
        managed = False  # Prevent Django from modifying the table

class GroupPermissions(models.Model):
    # Define fields exactly as they exist in auth_group_permissions
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_group_permissions'  # Explicitly map to existing table
        managed = False  # Prevent Django from modifying the table

class Permission(models.Model):
    # Define fields exactly as they exist in auth_permission
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('ContentType', on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = 'auth_permission'  # Explicitly map to existing table
        managed = False  # Prevent Django from modifying the table

class ContentType(models.Model):
    # Define fields exactly as they exist in django_content_type
    id = models.AutoField(primary_key=True)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        db_table = 'django_content_type'  # Explicitly map to existing table
        managed = False  # Prevent Django from modifying the table