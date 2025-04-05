from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Donor(models.Model):
    """Biological material donor model."""
    
    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('unknown', 'Unknown'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    donor_id = models.CharField(max_length=50, unique=True)
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPE_CHOICES, default='unknown')
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    hla_type = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor_id} - {self.user.full_name}"
    
    def save(self, *args, **kwargs):
        if self.height_cm and self.weight_kg:
            height_m = float(self.height_cm) / 100
            self.bmi = float(self.weight_kg) / (height_m * height_m)
        super().save(*args, **kwargs)


class DonorMedicalHistory(models.Model):
    """Medical history for donors."""
    
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE, related_name='medical_history')
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
        return f"Medical History for {self.donor.donor_id}"


class PhysicalExam(models.Model):
    """Physical examination records for donors."""
    
    RESULT_CHOICES = (
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal'),
        ('not_examined', 'Not Examined'),
    )
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='physical_exams')
    exam_date = models.DateField()
    examiner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='conducted_exams')
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    general_appearance = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    heent = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    cardiovascular = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    respiratory = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    gastrointestinal = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    musculoskeletal = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    neurological = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    skin = models.CharField(max_length=20, choices=RESULT_CHOICES, default='not_examined')
    notes = models.TextField(blank=True, null=True)
    is_eligible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor.donor_id} - Exam ({self.exam_date})"


class LabTest(models.Model):
    """Laboratory test records for donors."""
    
    STATUS_CHOICES = (
        ('ordered', 'Ordered'),
        ('collected', 'Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='lab_tests')
    test_name = models.CharField(max_length=255)
    test_code = models.CharField(max_length=50)
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordered_tests')
    order_date = models.DateTimeField()
    collection_date = models.DateTimeField(null=True, blank=True)
    result_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    result_value = models.CharField(max_length=255, blank=True, null=True)
    reference_range = models.CharField(max_length=255, blank=True, null=True)
    is_abnormal = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor.donor_id} - {self.test_name} ({self.order_date})"


class DonorEligibilityRule(models.Model):
    """Eligibility rules for donors."""
    
    RULE_TYPE_CHOICES = (
        ('inclusion', 'Inclusion'),
        ('exclusion', 'Exclusion'),
    )
    
    PARAMETER_TYPE_CHOICES = (
        ('age', 'Age'),
        ('bmi', 'BMI'),
        ('blood_type', 'Blood Type'),
        ('hla_type', 'HLA Type'),
        ('medical_history', 'Medical History'),
        ('lab_result', 'Lab Result'),
        ('physical_exam', 'Physical Exam'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    parameter = models.CharField(max_length=20, choices=PARAMETER_TYPE_CHOICES)
    condition = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_rule_type_display()} - {self.name}"  # type: ignore


class DonorEligibilityAssessment(models.Model):
    """Eligibility assessment for donors."""
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='eligibility_assessments')
    rule = models.ForeignKey(DonorEligibilityRule, on_delete=models.CASCADE)
    is_met = models.BooleanField()
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='donor_assessments')
    assessment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('donor', 'rule')
    
    def __str__(self):
        return f"{self.donor.donor_id} - {self.rule.name}"


class DonationType(models.Model):
    """Types of biological donations."""
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    preparation_instructions = models.TextField()
    recovery_time_days = models.PositiveIntegerField(default=0)
    minimum_interval_days = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class DonationAppointment(models.Model):
    """Scheduled donation appointments."""
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('checked_in', 'Checked In'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_appointments')
    donation_type = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor.donor_id} - {self.donation_type.name} ({self.scheduled_date})"


class Donation(models.Model):
    """Completed biological donations."""
    
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    appointment = models.OneToOneField(DonationAppointment, on_delete=models.SET_NULL, null=True, related_name='donation')
    donation_type = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    donation_date = models.DateTimeField()
    donation_id = models.CharField(max_length=50, unique=True)
    volume_ml = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collected_donations')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donation_id} - {self.donor.donor_id} ({self.donation_date})"


class SampleType(models.Model):
    """Types of biological samples."""
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    storage_temperature = models.CharField(max_length=50)
    shelf_life_days = models.PositiveIntegerField()
    processing_instructions = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class StorageUnit(models.Model):
    """Storage units for biological samples."""
    
    UNIT_TYPE_CHOICES = (
        ('freezer', 'Freezer'),
        ('refrigerator', 'Refrigerator'),
        ('room_temp', 'Room Temperature'),
        ('incubator', 'Incubator'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    temperature_range = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_unit_type_display()})"  # type: ignore


class StorageLocation(models.Model):
    """Specific locations within storage units."""
    
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('storage_unit', 'position')
    
    def __str__(self):
        return f"{self.storage_unit.name} - {self.position}"


class Sample(models.Model):
    """Biological samples from donations."""
    
    STATUS_CHOICES = (
        ('collected', 'Collected'),
        ('processing', 'Processing'),
        ('stored', 'Stored'),
        ('reserved', 'Reserved'),
        ('shipped', 'Shipped'),
        ('used', 'Used'),
        ('disposed', 'Disposed'),
    )
    
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='samples')
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE)
    sample_id = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=100, unique=True)
    volume_ml = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='collected')
    collection_date = models.DateTimeField()
    expiration_date = models.DateField()
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True, related_name='samples')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_samples')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sample_id} - {self.sample_type.name}"


class ChainOfCustodyLog(models.Model):
    """Chain of custody logs for samples."""
    
    ACTION_CHOICES = (
        ('collected', 'Collected'),
        ('processed', 'Processed'),
        ('stored', 'Stored'),
        ('retrieved', 'Retrieved from Storage'),
        ('transferred', 'Transferred'),
        ('shipped', 'Shipped'),
        ('received', 'Received'),
        ('used', 'Used'),
        ('disposed', 'Disposed'),
    )
    
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='custody_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField()
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='custody_actions')
    from_location = models.CharField(max_length=255, blank=True, null=True)
    to_location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.sample.sample_id} - {self.get_action_display()} ({self.timestamp})"  # type: ignore
