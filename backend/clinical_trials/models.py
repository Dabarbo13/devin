from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Study(models.Model):
    """Clinical trial study model."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    )
    
    PHASE_CHOICES = (
        ('PHASE_0', 'Phase 0'),
        ('PHASE_1', 'Phase 1'),
        ('PHASE_2', 'Phase 2'),
        ('PHASE_3', 'Phase 3'),
        ('PHASE_4', 'Phase 4'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    protocol_number = models.CharField(max_length=100, unique=True)
    sponsor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sponsored_studies', 
                               limit_choices_to={'is_sponsor': True}, null=True, blank=True)
    sponsor_name = models.CharField(max_length=255, null=True, blank=True)
    principal_investigator = models.ForeignKey(User, on_delete=models.PROTECT, 
                                              related_name='pi_studies',
                                              limit_choices_to={'is_investigator': True})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES, null=True, blank=True)
    therapeutic_area = models.CharField(max_length=255, null=True, blank=True)
    indication = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    target_participants = models.PositiveIntegerField(default=0)
    target_enrollment = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.protocol_number}: {self.title}"


class StudyPhase(models.Model):
    """Clinical trial study phase model."""
    
    PHASE_CHOICES = (
        ('phase_0', 'Phase 0'),
        ('phase_1', 'Phase 1'),
        ('phase_2', 'Phase 2'),
        ('phase_3', 'Phase 3'),
        ('phase_4', 'Phase 4'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='phases')
    phase_type = models.CharField(max_length=20, choices=PHASE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('study', 'phase_type')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.get_phase_type_display()}"  # type: ignore


class StudyArm(models.Model):
    """Clinical trial study arm model."""
    
    ARM_TYPE_CHOICES = (
        ('experimental', 'Experimental'),
        ('control', 'Control'),
        ('placebo', 'Placebo'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='arms')
    name = models.CharField(max_length=255)
    description = models.TextField()
    arm_type = models.CharField(max_length=20, choices=ARM_TYPE_CHOICES)
    target_participants = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.name}"


class VisitTemplate(models.Model):
    """Template for study visits."""
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='visit_templates')
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=60)
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.name}"


class StudyDocument(models.Model):
    """Documents associated with a study."""
    
    DOCUMENT_TYPE_CHOICES = (
        ('protocol', 'Protocol'),
        ('consent', 'Informed Consent'),
        ('brochure', 'Investigator Brochure'),
        ('sop', 'Standard Operating Procedure'),
        ('other', 'Other'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    version = models.CharField(max_length=50)
    file = models.FileField(upload_to='study_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.title} (v{self.version})"


class ProtocolVersion(models.Model):
    """Protocol versions for a study."""
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='protocol_versions')
    version_number = models.CharField(max_length=50)
    effective_date = models.DateField()
    document = models.ForeignKey(StudyDocument, on_delete=models.SET_NULL, null=True, 
                                related_name='protocol_versions',
                                limit_choices_to={'document_type': 'protocol'})
    is_current = models.BooleanField(default=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_protocols')
    approval_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('study', 'version_number')
    
    def __str__(self):
        return f"{self.study.protocol_number} - v{self.version_number}"


class StudySite(models.Model):
    """Clinical trial study sites."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=255)
    address = models.TextField()
    principal_investigator = models.ForeignKey(User, on_delete=models.PROTECT, 
                                              related_name='site_pi',
                                              limit_choices_to={'is_investigator': True})
    coordinator = models.ForeignKey(User, on_delete=models.PROTECT, 
                                   related_name='site_coordinator',
                                   limit_choices_to={'is_coordinator': True})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    activation_date = models.DateField(null=True, blank=True)
    target_enrollment = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.name}"


class Participant(models.Model):
    """Clinical trial participant model."""
    
    STATUS_CHOICES = (
        ('screening', 'Screening'),
        ('enrolled', 'Enrolled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn'),
        ('screen_failed', 'Screen Failed'),
    )
    
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
        ('PREFER_NOT_TO_SAY', 'Prefer not to say'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='participants')
    study_arm = models.ForeignKey(StudyArm, on_delete=models.SET_NULL, null=True, related_name='participants')
    arm = models.ForeignKey(StudyArm, on_delete=models.SET_NULL, null=True, related_name='arm_participants')
    site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name='participants', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='trial_participations')
    participant_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='screening')
    enrollment_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    withdrawal_date = models.DateField(null=True, blank=True)
    withdrawal_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.participant_id} - {self.study.protocol_number}"


class EligibilityCriteria(models.Model):
    """Eligibility criteria for study participants."""
    
    CRITERIA_TYPE_CHOICES = (
        ('inclusion', 'Inclusion'),
        ('exclusion', 'Exclusion'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='eligibility_criteria')
    criteria_type = models.CharField(max_length=20, choices=CRITERIA_TYPE_CHOICES)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['criteria_type', 'order']
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.get_criteria_type_display()} #{self.order}"  # type: ignore


class ParticipantEligibility(models.Model):
    """Participant eligibility assessment."""
    
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='eligibility_assessments')
    criteria = models.ForeignKey(EligibilityCriteria, on_delete=models.CASCADE)
    is_met = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assessed_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('participant', 'criteria')
    
    def __str__(self):
        return f"{self.participant.participant_id} - {self.criteria}"


class Visit(models.Model):
    """Scheduled visits for participants."""
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
    )
    
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='visits')
    template = models.ForeignKey(VisitTemplate, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name='visits')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    actual_date = models.DateField(null=True, blank=True)
    actual_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.participant.participant_id} - {self.template.name if self.template else 'Visit'} ({self.scheduled_date})"


class AdverseEvent(models.Model):
    """Adverse events during clinical trials."""
    
    SEVERITY_CHOICES = (
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('life_threatening', 'Life-threatening'),
        ('death', 'Death'),
    )
    
    RELATEDNESS_CHOICES = (
        ('unrelated', 'Unrelated'),
        ('unlikely', 'Unlikely'),
        ('possible', 'Possible'),
        ('probable', 'Probable'),
        ('definite', 'Definite'),
    )
    
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='adverse_events')
    description = models.TextField()
    onset_date = models.DateField()
    resolution_date = models.DateField(null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    is_serious = models.BooleanField(default=False)
    relatedness = models.CharField(max_length=20, choices=RELATEDNESS_CHOICES)
    action_taken = models.TextField()
    outcome = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_events')
    report_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.participant.participant_id} - AE ({self.onset_date})"


class ProtocolDeviation(models.Model):
    """Protocol deviations during clinical trials."""
    
    CATEGORY_CHOICES = (
        ('inclusion_exclusion', 'Inclusion/Exclusion Criteria'),
        ('informed_consent', 'Informed Consent'),
        ('study_procedures', 'Study Procedures'),
        ('medication', 'Study Medication'),
        ('visit_schedule', 'Visit Schedule'),
        ('other', 'Other'),
    )
    
    SEVERITY_CHOICES = (
        ('minor', 'Minor'),
        ('major', 'Major'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='deviations')
    site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name='deviations')
    participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, related_name='deviations')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    deviation_date = models.DateField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    corrective_action = models.TextField()
    preventive_action = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_deviations')
    report_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.study.protocol_number} - {self.get_category_display()} ({self.deviation_date})"  # type: ignore


class SiteActivityLog(models.Model):
    """Activity logs for study sites."""
    
    ACTIVITY_TYPE_CHOICES = (
        ('enrollment', 'Participant Enrollment'),
        ('visit', 'Participant Visit'),
        ('adverse_event', 'Adverse Event'),
        ('deviation', 'Protocol Deviation'),
        ('document', 'Document Upload'),
        ('other', 'Other'),
    )
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='activity_logs')
    site = models.ForeignKey(StudySite, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='site_activities')
    activity_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-activity_date']
    
    def __str__(self):
        return f"{self.site.name} - {self.get_activity_type_display()} ({self.activity_date})"  # type: ignore
