Django Custom Authentication
Projet Django avec authentification personnalisée par email pour deux types d'utilisateurs : Admin et Client.
Prérequis

Python 3.8+
Git

Installation

Clonez le dépôt :git clone https://github.com/wat650/authentication1.git
cd django-custom-auth


Créez et activez un environnement virtuel :python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate  # Windows


Installez les dépendances :pip install -r requirements.txt


Appliquez les migrations :python manage.py makemigrations
python manage.py migrate


Lancez le serveur :python manage.py runserver



Utilisation

Accédez à /accounts/register/ pour créer un compte.
Accédez à /accounts/login/ pour vous connecter.
Accédez à /accounts/logout/ pour vous déconnecter.

Structure du projet

accounts/: Application pour l'authentification.
custom_auth_project/: Configuration principale du projet.
templates/: Templates HTML.

Contribution

Forkez le projet.
Créez une branche (git checkout -b feature/amélioration).
Commitez vos changements (git commit -m 'Ajout de fonctionnalité').
Poussez la branche (git push origin feature/amélioration).
Créez une Pull Request.

