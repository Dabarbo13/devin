from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from clinical_trials.models import Study, Participant
from donation_management.models import Donor


class Prospect(models.Model):
    """Prospective donors or study participants."""
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified'),
        ('converted', 'Converted'),
    )
    
    SOURCE_CHOICES = (
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('referral', 'Referral'),
        ('event', 'Event'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    )
    
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    source_details = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_donor_prospect = models.BooleanField(default=False)
    is_study_prospect = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class DemographicInfo(models.Model):
    """Demographic information for prospects."""
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    )
    
    ETHNICITY_CHOICES = (
        ('hispanic', 'Hispanic or Latino'),
        ('not_hispanic', 'Not Hispanic or Latino'),
        ('prefer_not_to_say', 'Prefer not to say'),
    )
    
    RACE_CHOICES = (
        ('american_indian', 'American Indian or Alaska Native'),
        ('asian', 'Asian'),
        ('black', 'Black or African American'),
        ('pacific_islander', 'Native Hawaiian or Other Pacific Islander'),
        ('white', 'White'),
        ('multiple', 'Two or More Races'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    )
    
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE, related_name='demographics')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, choices=ETHNICITY_CHOICES, blank=True, null=True)
    race = models.CharField(max_length=20, choices=RACE_CHOICES, blank=True, null=True)
    height_cm = models.PositiveIntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    hla_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Demographics for {self.prospect}"


class HealthInfo(models.Model):
    """Health information for prospects."""
    
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE, related_name='health_info')
    has_allergies = models.BooleanField(default=False)
    allergies_description = models.TextField(blank=True, null=True)
    has_chronic_diseases = models.BooleanField(default=False)
    chronic_diseases_description = models.TextField(blank=True, null=True)
    has_medications = models.BooleanField(default=False)
    medications_description = models.TextField(blank=True, null=True)
    has_surgeries = models.BooleanField(default=False)
    surgeries_description = models.TextField(blank=True, null=True)
    has_family_history = models.BooleanField(default=False)
    family_history_description = models.TextField(blank=True, null=True)
    has_infectious_diseases = models.BooleanField(default=False)
    infectious_diseases_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Health Info for {self.prospect}"


class StudyQualification(models.Model):
    """Study qualification for prospects."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified'),
    )
    
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='study_qualifications')
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='prospect_qualifications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='qualification_assessments')
    assessment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('prospect', 'study')
    
    def __str__(self):
        return f"{self.prospect} - {self.study.protocol_number} ({self.get_status_display()})"


class ContactLog(models.Model):
    """Contact logs for prospects."""
    
    CONTACT_TYPE_CHOICES = (
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('text', 'Text Message'),
        ('in_person', 'In Person'),
        ('other', 'Other'),
    )
    
    DIRECTION_CHOICES = (
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    )
    
    OUTCOME_CHOICES = (
        ('successful', 'Successful'),
        ('left_message', 'Left Message'),
        ('no_answer', 'No Answer'),
        ('wrong_number', 'Wrong Number'),
        ('not_interested', 'Not Interested'),
        ('follow_up', 'Follow Up Required'),
        ('other', 'Other'),
    )
    
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='contact_logs')
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    contact_date = models.DateTimeField()
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES)
    notes = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    contacted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contact_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-contact_date']
    
    def __str__(self):
        return f"{self.prospect} - {self.get_contact_type_display()} ({self.contact_date})"


class Message(models.Model):
    """Messages sent to or received from prospects."""
    
    MESSAGE_TYPE_CHOICES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('system', 'System Notification'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('queued', 'Queued'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('received', 'Received'),
    )
    
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    subject = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    recipient_email = models.EmailField(blank=True, null=True)
    recipient_phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    sent_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.prospect} - {self.get_message_type_display()} ({self.created_at})"


class MessageTemplate(models.Model):
    """Templates for messages."""
    
    MESSAGE_TYPE_CHOICES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
    )
    
    name = models.CharField(max_length=255)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    subject = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_message_type_display()})"


class Referral(models.Model):
    """Referrals from existing prospects, donors, or participants."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
        ('invalid', 'Invalid'),
    )
    
    REFERRER_TYPE_CHOICES = (
        ('prospect', 'Prospect'),
        ('donor', 'Donor'),
        ('participant', 'Participant'),
    )
    
    referrer_type = models.CharField(max_length=20, choices=REFERRER_TYPE_CHOICES)
    referrer_prospect = models.ForeignKey(Prospect, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_made')
    referrer_donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_made')
    referrer_participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_made')
    referred_prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='referral')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    referral_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    bonus_paid = models.BooleanField(default=False)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bonus_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        referrer = None
        if self.referrer_type == 'prospect' and self.referrer_prospect:
            referrer = self.referrer_prospect
        elif self.referrer_type == 'donor' and self.referrer_donor:
            referrer = self.referrer_donor
        elif self.referrer_type == 'participant' and self.referrer_participant:
            referrer = self.referrer_participant
        
        return f"Referral: {referrer} → {self.referred_prospect}"


class SocialMediaCampaign(models.Model):
    """Social media campaigns for recruiting."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    )
    
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    target_audience = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tracking_url = models.URLField(blank=True, null=True)
    tracking_code = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_display()})"


class CampaignMetrics(models.Model):
    """Metrics for social media campaigns."""
    
    campaign = models.ForeignKey(SocialMediaCampaign, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField()
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('campaign', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.campaign.name} - Metrics ({self.date})"
