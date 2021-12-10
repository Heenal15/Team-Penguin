from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Club

class Command(BaseCommand):
        """The database unseeder."""
        def handle(self, *args, **options):
            User.objects.filter(is_staff=False, is_superuser=False).delete()
            # Club.objects.filter(club_name!='Kerbal Chess Club').delete()
