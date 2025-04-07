from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as the unique identifier."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    
    is_donor = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    is_investigator = models.BooleanField(default=False)
    is_coordinator = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_researcher = models.BooleanField(default=False)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    """Extended profile information for users."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"
        
    @property
    def is_active_study_participant(self):
        """Check if user is an active study participant."""
        from clinical_trials.models import Participant
        
        participant_records = Participant.objects.filter(user=self.user)
        
        active_statuses = ['screening', 'enrolled', 'active']
        return participant_records.filter(status__in=active_statuses).exists()
    
    @property
    def get_participant_studies(self):
        """Get all studies the user is participating in."""
        from clinical_trials.models import Participant
        
        participant_records = Participant.objects.filter(user=self.user)
        
        status_dict = dict(Participant.STATUS_CHOICES)
        
        return [
            {
                'study_id': p.study.protocol_number,
                'study_title': p.study.title,
                'status': status_dict.get(p.status) if p.status in status_dict else str(p.status),
                'enrollment_date': p.enrollment_date,
                'completion_date': p.completion_date
            }
            for p in participant_records
        ]
    
    @property
    def get_donation_history(self):
        """Get donation history if user is a donor."""
        try:
            from donation_management.models import Donation, Donor
            
            donor = Donor.objects.filter(user=self.user).first()
            if donor:
                donations = Donation.objects.filter(donor=donor)
                return [
                    {
                        'donation_id': d.donation_id,
                        'donation_type': d.donation_type.name,
                        'donation_date': d.donation_date,
                        'volume_ml': d.volume_ml
                    }
                    for d in donations
                ]
        except Exception:
            pass
        return []
