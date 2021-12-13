from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club, ClubContract

class Command(BaseCommand):
        """The database unseeder."""
        def handle(self, *args, **options):
            User.objects.filter(is_staff=False, is_superuser=False).delete()
            Club.objects.all().delete()
            ClubContract.objects.all().delete()
