from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'name', 'email')
        success_url = reverse_lazy("index")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user = get_user_model().objects.create_user(
                phone_number=user.phone_number,
                password=self.cleaned_data.get('password1'),
                name=user.name,
                email=user.email
            )
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'name', 'email', 'is_active', 'is_staff')
