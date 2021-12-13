from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User, Club, ClubContract
import random

class Command(BaseCommand):
    """The database seeder."""
    PASSWORD = "Password123"
    USER_COUNT = 100
    CLUB_COUNT = 3
    CONTRACT_COUNT = 200

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')


    def handle(self, *args, **options):
        club_count = 0
        while club_count < Command.CLUB_COUNT:
            print(f'Seeding club {club_count}',  end='\r')
            try:
                self._create_club()
            except (django.db.utils.IntegrityError):
                continue
            club_count += 1
        print('Club seeding is complete')
        self._create_kerbal_club()
        print('Kerbal Chess Club has been created')

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

        self.users = User.objects.all()
        self.allClubs = Club.objects.all()
        contract_count = 0
        while contract_count < Command.CONTRACT_COUNT:
            print(f'Seeding contract {contract_count}',  end='\r')
            try:
                self._create_contract()
            except (django.db.utils.IntegrityError):
                continue
            contract_count += 1
        self.assign_billie_to_kerbal()
        print('Billie is the owner of Kerbal Chess Club')
        print('Contract seeding is complete')

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        # user_type=random.randint(0, 2)
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = self._experience()
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            # user_type=user_type,
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
        # user_type = 1
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = 'Beginner'
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            # user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )
    def _create_officer(self):
        first_name = 'Valentina'
        last_name = 'Kerman'
        email = 'val@example.org'
        # user_type = 2
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = 'Intermediate'
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            # user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )
    def _create_owner(self):
        first_name = 'Billie'
        last_name = 'Kerman'
        email = 'billie@example.org'
        # user_type = 3
        bio = self.faker.text(max_nb_chars=520)
        statement = self.faker.text(max_nb_chars=520)
        experience = 'Advanced'
        User.objects.create_user(

            first_name=first_name,
            last_name=last_name,
            email=email,
            # user_type=user_type,
            password=Command.PASSWORD,
            bio=bio,
            statement=statement,
            experience=experience,

        )

    def _create_club(self):
        club_name = self.faker.word()
        club_location = self.faker.location_on_land()
        club_description = self.faker.text(max_nb_chars=200)
        Club.objects.create(

        club_name = club_name,
        club_location = club_location,
        club_description = club_description,

        )

    def _create_kerbal_club(self):
        club_name = 'Kerbal Chess Club'
        club_location = self.faker.location_on_land()
        club_description = 'Welcome to Kerbal Chess Club'
        Club.objects.create(

            club_name = club_name,
            club_location = club_location,
            club_description = club_description,

        )

    def _create_contract(self):
        contract = ClubContract()
        contract.user = self.get_random_user()
        contract.club = self.get_random_club()
        contract.role = self.get_random_role()
        contract.save()

    def get_random_user(self):
        self.users = User.objects.all()
        index = random.randint(0,self.users.count()-1)
        return self.users[index]

    def get_random_club(self):
        self.allClubs = Club.objects.all()
        index = random.randint(0,self.allClubs.count()-1)
        return self.allClubs[index]

    def get_random_role(self):
        random_number = random.randint(0,3)
        return random_number

    def assign_billie_to_kerbal(self):
        contract = ClubContract()
        contract.user = User.objects.get(first_name = 'Billie')
        contract.club = Club.objects.get(club_name='Kerbal Chess Club')
        contract.role = 3
        contract.save()
