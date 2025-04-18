from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from .models import EmailVerificationToken
from django.utils.translation import gettext_lazy as _


class HomePageView(View):
    def get(self, request) -> HttpResponse:
        user = request.user
        context = {
            'user': user
        }

        return render(request, "index.html", context)


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             _('Inscription réussie ! Veuillez vérifier votre email pour activer votre compte.'))
            return redirect('accounts:login')
        messages.error(request, _('Erreur lors de l’inscription.'))
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, _('Connexion réussie !'))
                    return redirect('home')
                else:
                    messages.error(request, _('Veuillez vérifier votre email pour activer votre compte.'))
            else:
                messages.error(request, _('Email ou mot de passe incorrect.'))
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, _('Déconnexion réussie.'))
        return redirect('accounts:login')


class VerifyEmailView(View):
    template_name = 'accounts/verify_email.html'

    def get(self, request, token):
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            if verification_token.is_valid():
                user = verification_token.user
                user.is_active = True
                user.save()
                verification_token.delete()  # Supprimer le token après utilisation
                messages.success(request,
                                 _('Votre email a été vérifié avec succès ! Vous pouvez maintenant vous connecter.'))
                return redirect('accounts:login')
            else:
                messages.error(request, _('Ce lien de vérification a expiré.'))
        except EmailVerificationToken.DoesNotExist:
            messages.error(request, _('Lien de vérification invalide.'))
        return render(request, self.template_name, {'token': token})
