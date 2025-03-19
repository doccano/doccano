from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):

        password = form.cleaned_data.get('password1')
        user = super().save_user(request, user, form, commit=False)
        user.plain_password = password
        
        print("CustomAccountAdapter form.cleaned_data:", form.cleaned_data)
        role = form.cleaned_data.get("role", "")
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
        
        if commit:
            user.save()
        return user