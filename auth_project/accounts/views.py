from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('home')
        messages.error(request, 'Erreur lors de l’inscription.')
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
                login(request, user)
                messages.success(request, 'Connexion réussie !')
                return redirect('home')
            messages.error(request, 'Email ou mot de passe incorrect.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Déconnexion réussie.')
        return redirect('accounts:login')
