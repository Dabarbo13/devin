from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from clinical_trials.models import Study, StudySite
from donation_management.models import Donor, SampleType, Sample


class SponsorProfile(models.Model):
    """Extended profile for sponsor users."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sponsor_profile')
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_website = models.URLField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20)
    department = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.user.full_name}"


class ResearcherProfile(models.Model):
    """Extended profile for researcher users."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='researcher_profile')
    institution_name = models.CharField(max_length=255)
    institution_address = models.TextField()
    institution_website = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    research_interests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.institution_name} - {self.user.full_name}"


class ProtocolDraft(models.Model):
    """Draft protocols for studies."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protocol_drafts',
                               limit_choices_to={'is_sponsor': True})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.CharField(max_length=50)
    document = models.FileField(upload_to='protocol_drafts/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} (v{self.version})"


class ProtocolReview(models.Model):
    """Reviews for protocol drafts."""
    
    DECISION_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revisions_needed', 'Revisions Needed'),
    )
    
    protocol_draft = models.ForeignKey(ProtocolDraft, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protocol_reviews')
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES, default='pending')
    comments = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.protocol_draft.title} - Review by {self.reviewer.full_name}"


class RecruitmentMetrics(models.Model):
    """Recruitment metrics for studies."""
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='recruitment_metrics')
    site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name='recruitment_metrics')
    date = models.DateField()
    inquiries = models.PositiveIntegerField(default=0)
    screenings = models.PositiveIntegerField(default=0)
    screen_failures = models.PositiveIntegerField(default=0)
    enrollments = models.PositiveIntegerField(default=0)
    withdrawals = models.PositiveIntegerField(default=0)
    completions = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('study', 'site', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.site.name} ({self.date})"


class CustomSampleRequest(models.Model):
    """Custom sample collection requests from researchers."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sample_requests',
                                  limit_choices_to={'is_researcher': True})
    title = models.CharField(max_length=255)
    description = models.TextField()
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    donor_criteria = models.TextField()
    processing_instructions = models.TextField(blank=True, null=True)
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.researcher.full_name}"


class SampleOrder(models.Model):
    """Orders for samples from researchers."""
    
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('collecting', 'Collecting'),
        ('shipping', 'Shipping'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )
    
    researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sample_orders',
                                  limit_choices_to={'is_researcher': True})
    custom_request = models.ForeignKey(CustomSampleRequest, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    order_date = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField()
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.researcher.full_name}"


class OrderItem(models.Model):
    """Items in a sample order."""
    
    order = models.ForeignKey(SampleOrder, on_delete=models.CASCADE, related_name='items')
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.sample_type.name} (x{self.quantity})"
    
    def save(self, *args, **kwargs):
        self.total_price = self.price_per_unit * self.quantity
        super().save(*args, **kwargs)


class OrderSample(models.Model):
    """Specific samples assigned to an order."""
    
    order = models.ForeignKey(SampleOrder, on_delete=models.CASCADE, related_name='samples')
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='orders')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='assigned_samples')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('order', 'sample')
    
    def __str__(self):
        return f"{self.order.order_number} - {self.sample.sample_id}"


class Dashboard(models.Model):
    """Custom dashboards for sponsors and researchers."""
    
    TYPE_CHOICES = (
        ('sponsor', 'Sponsor'),
        ('researcher', 'Researcher'),
        ('admin', 'Admin'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    dashboard_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    is_default = models.BooleanField(default=False)
    layout = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.full_name}"


class DashboardWidget(models.Model):
    """Widgets for dashboards."""
    
    TYPE_CHOICES = (
        ('chart', 'Chart'),
        ('table', 'Table'),
        ('metric', 'Metric'),
        ('list', 'List'),
        ('custom', 'Custom'),
    )
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    title = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    data_source = models.CharField(max_length=255)
    config = models.JSONField(default=dict)
    position = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.dashboard.name}"
