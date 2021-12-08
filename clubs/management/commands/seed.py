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
        self._create_member()
        print('Member: Jebediah Kerman has been created')
        self._create_officer()
        print('Officer: Valentina Kerman has been created')
        self._create_owner()
        print('Owner: Billie Kerman has been created')

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        user_type=random.randint(0, 2)
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = self._experience()
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def _experience(self):
        experience_list = ['Beginner', 'Intermediate', 'Advanced']
        expereince = random.choice(experience_list)
        return expereince

    def _create_member(self):
        first_name = 'Jebediah'
        last_name = 'Kerman'
        email = 'jeb@example.org'
        user_type = 1
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = 'Beginner'
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )
    def _create_officer(self):
        first_name = 'Valentina'
        last_name = 'Kerman'
        email = 'val@example.org'
        user_type = 2
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = 'Intermediate'
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )
    def _create_owner(self):
        first_name = 'Billie'
        last_name = 'Kerman'
        email = 'billie@example.org'
        user_type = 3
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = 'Advanced'
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )
