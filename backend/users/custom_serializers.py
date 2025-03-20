from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('annotator', 'Annotator'),
    )
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['role'] = self.validated_data.get("role", "")
        print("CustomRegisterSerializer cleaned data:", data)
        return data

    def save(self, request):
        user = super().save(request)
        role = self.validated_data.get("role", "")
        print("CustomRegisterSerializer save role:", role)
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
        user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("CustomRegisterSerializer initialized")
