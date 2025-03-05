from django.core.management.base import BaseCommand
from myapp.models import Visite
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update existing Visite entries to set a default user'

    def handle(self, *args, **kwargs):
        # Obtenez un utilisateur par défaut (remplacez 'admin' par l'utilisateur souhaité)
        default_user = User.objects.get(username='root')

        # Mettez à jour toutes les visites existantes
        updated_count = Visite.objects.filter(user__isnull=True).update(user=default_user)

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} visites'))