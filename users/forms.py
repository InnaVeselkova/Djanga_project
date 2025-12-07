from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
