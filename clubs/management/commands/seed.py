from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User
import random

class Command(BaseCommand):
    """The database seeder."""
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')


    def handle(self, *args, **options):
        user_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                self._create_user()
            except (django.db.utils.IntegrityError):
                continue
            user_count += 1
        print('User seeding complete')

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        user_type=random.randint(0, 2)

        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = self.faker.text(max_nb_chars=20)
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,
            user_type=user_type,
        )

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
