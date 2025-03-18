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
        # Create the user first with the default process.
        user = super().save(request)
        # Now update the user based on our extra role field.
        role = self.validated_data.get("role", "")
        print("CustomRegisterSerializer save role:", role)
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True  # Enable only if you want full admin rights.
        else:
            user.is_staff = False
        user.save()
        return user