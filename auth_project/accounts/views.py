from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserCreationForm, UserLoginForm, ResendVerificationForm
from django.contrib.auth import authenticate, login, logout
from .models import EmailVerificationToken, User
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


class ResendVerificationView(View):
    template_name = 'accounts/resend_verification.html'

    def get(self, request):
        form = ResendVerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ResendVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            # Supprimer tout token existant
            EmailVerificationToken.objects.filter(user=user).delete()
            # Créer un nouveau token
            token = EmailVerificationToken.objects.create(user=user)
            verification_url = f"{settings.BASE_URL}/accounts/verify-email/{token.token}/"
            subject = _('Renvoyer la vérification de votre adresse email')
            message = _(
                f'Bonjour {user.get_full_name() or user.email},\n\n'
                f'Vous avez demandé un nouveau lien de vérification. Veuillez cliquer sur le lien suivant pour '
                f'vérifier votre adresse email :\n'
                f'{verification_url}\n\n'
                f'Ce lien expire dans 24 heures.\n\n'
                f'Merci,\nL\'équipe MonApp'
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, _('Un nouvel email de vérification a été envoyé.'))
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})