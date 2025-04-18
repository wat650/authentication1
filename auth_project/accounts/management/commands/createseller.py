from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from accounts.models import Seller
from django.utils.translation import gettext_lazy as _
import getpass
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a new seller user interactively'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Création d’un nouveau vendeur'))

        # Collecter les champs requis pour User
        email = None
        while not email:
            email = input('Email: ')
            if not email:
                self.stdout.write(self.style.ERROR('L’email est requis.'))
            elif User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR('Cet email existe déjà.'))
                email = None

        first_name = input('Prénom: ') or ''
        password = None
        while not password:
            password = getpass.getpass('Mot de passe: ')
            password2 = getpass.getpass('Confirmer le mot de passe: ')
            if password != password2:
                self.stdout.write(self.style.ERROR('Les mots de passe ne correspondent pas.'))
                password = None
            elif not password:
                self.stdout.write(self.style.ERROR('Le mot de passe est requis.'))

        # Collecter les champs pour Seller
        store_name = input('Nom du magasin (optionnel): ') or None

        try:
            # Créer l’utilisateur
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                password=password,
                is_staff=False,  # Pas un admin
                is_superuser=False,  # Pas un superutilisateur
            )

            # Créer le profil Seller
            Seller.objects.create(
                user=user,
                store_name=store_name,
            )

            self.stdout.write(self.style.SUCCESS(f'Vendeur {email} créé avec succès !'))
        except Exception as e:
            raise CommandError(f'Erreur lors de la création du vendeur : {str(e)}')
