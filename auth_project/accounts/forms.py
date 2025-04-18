from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from accounts.models import Client
from utils.enums import GenderChoices

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'})
    )
    city = forms.CharField(
        label=_('City'),
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre ville'})
    )
    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    gender = forms.ChoiceField(
        label=_('Gender'),
        choices=[('', 'Sélectionnez votre genre')] + GenderChoices.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords don’t match'))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                city=self.cleaned_data.get('city'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender')
            )
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'})
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )
