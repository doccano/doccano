from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # Print the entire cleaned_data for debugging
        print("CustomAccountAdapter form.cleaned_data:", form.cleaned_data)
        role = form.cleaned_data.get("role", "")
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True  # Remove if superuser should remain false
        else:
            user.is_staff = False
        user = super().save_user(request, user, form, commit=False)
        if commit:
            user.save()
        return user