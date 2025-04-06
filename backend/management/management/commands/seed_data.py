import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from users.models import User
from clinical_trials.models import *
from donation_management.models import *
from recruiting.models import *
from sponsor_portal.models import *
from web_store.models import *

class Command(BaseCommand):
    help = 'Seed the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            default=20,
            type=int,
            help='Number of users to create'
        )
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Flush the database before seeding'
        )

    def handle(self, *args, **options):
        self.faker = Faker()
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        try:
            with transaction.atomic():
                if options['flush']:
                    self.stdout.write(self.style.WARNING('Flushing database...'))
                    self.flush_database()
                    
                self.create_users(options['users'])
                self.create_clinical_trials_data()
                self.create_donation_management_data()
                self.create_recruiting_data()
                self.create_sponsor_portal_data()
                self.create_web_store_data()
                
                self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding database: {str(e)}'))
            raise

    def flush_database(self):
        User.objects.filter(is_superuser=False).delete()

    def create_users(self, count):
        self.stdout.write(self.style.SUCCESS('Creating users...'))
        
        admin_email = 'admin@biobank.com'
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))
            
        roles = [
            {'is_donor': True},
            {'is_investigator': True},
            {'is_coordinator': True},
            {'is_sponsor': True},
            {'is_researcher': True},
            {'is_recruiter': True},
        ]
        
        created_users = []
        for i in range(count):
            role = random.choice(roles)
            email = self.faker.email()
            
            if User.objects.filter(email=email).exists():
                continue
                
            user = User.objects.create_user(
                email=email,
                password='password123',
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                phone_number=self.faker.phone_number(),
                date_of_birth=self.faker.date_of_birth(minimum_age=18, maximum_age=80),
                address=self.faker.address(),
                organization=self.faker.company(),
                **role
            )
            created_users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_users)} users'))
        self.users = User.objects.all()
        self.donors = User.objects.filter(is_donor=True)
        self.investigators = User.objects.filter(is_investigator=True)
        self.coordinators = User.objects.filter(is_coordinator=True)
        self.sponsors = User.objects.filter(is_sponsor=True)
        self.researchers = User.objects.filter(is_researcher=True)
        self.recruiters = User.objects.filter(is_recruiter=True)

    def create_clinical_trials_data(self):
        self.stdout.write(self.style.SUCCESS('Creating clinical trials data...'))

    def create_donation_management_data(self):
        self.stdout.write(self.style.SUCCESS('Creating donation management data...'))

    def create_recruiting_data(self):
        self.stdout.write(self.style.SUCCESS('Creating recruiting data...'))

    def create_sponsor_portal_data(self):
        self.stdout.write(self.style.SUCCESS('Creating sponsor portal data...'))

    def create_web_store_data(self):
        self.stdout.write(self.style.SUCCESS('Creating web store data...'))
