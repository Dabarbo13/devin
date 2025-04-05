from rest_framework import serializers
from .models import (
    Study, StudyPhase, StudyArm, Participant, VisitTemplate, StudyDocument,
    ProtocolVersion, StudySite, EligibilityCriteria, ParticipantEligibility,
    Visit, AdverseEvent, ProtocolDeviation, SiteActivityLog
)
from users.serializers import UserSerializer


class StudyPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPhase
        fields = ['id', 'study', 'name', 'description', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class StudyArmSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyArm
        fields = ['id', 'study', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class VisitTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitTemplate
        fields = [
            'id', 'study', 'phase', 'name', 'description', 'order', 
            'days_from_enrollment', 'window_before', 'window_after',
            'is_required', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyDocument
        fields = [
            'id', 'study', 'title', 'document_type', 'version', 'file',
            'uploaded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProtocolVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolVersion
        fields = [
            'id', 'study', 'version_number', 'effective_date', 'document',
            'approved_by', 'approval_date', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudySiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySite
        fields = [
            'id', 'study', 'name', 'address', 'contact_name', 'contact_email',
            'contact_phone', 'status', 'activation_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EligibilityCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityCriteria
        fields = [
            'id', 'study', 'criteria_type', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = [
            'id', 'title', 'protocol_number', 'status', 'phase',
            'start_date', 'end_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudyDetailSerializer(serializers.ModelSerializer):
    phases = StudyPhaseSerializer(many=True, read_only=True)
    arms = StudyArmSerializer(many=True, read_only=True)
    visit_templates = VisitTemplateSerializer(many=True, read_only=True)
    documents = StudyDocumentSerializer(many=True, read_only=True)
    protocol_versions = ProtocolVersionSerializer(many=True, read_only=True)
    sites = StudySiteSerializer(many=True, read_only=True)
    eligibility_criteria = EligibilityCriteriaSerializer(many=True, read_only=True)
    principal_investigator = UserSerializer(read_only=True)
    
    class Meta:
        model = Study
        fields = [
            'id', 'title', 'protocol_number', 'description', 'status', 'phase',
            'therapeutic_area', 'indication', 'principal_investigator',
            'sponsor_name', 'start_date', 'end_date', 'target_enrollment',
            'phases', 'arms', 'visit_templates', 'documents', 'protocol_versions',
            'sites', 'eligibility_criteria', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ParticipantEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantEligibility
        fields = [
            'id', 'participant', 'criteria', 'is_met', 'notes',
            'assessed_by', 'assessment_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            'id', 'participant', 'visit_template', 'scheduled_date', 'actual_date',
            'status', 'conducted_by', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AdverseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdverseEvent
        fields = [
            'id', 'participant', 'event_date', 'description', 'severity',
            'relatedness', 'outcome', 'is_serious', 'is_expected',
            'reported_by', 'report_date', 'resolution_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProtocolDeviationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolDeviation
        fields = [
            'id', 'study', 'site', 'participant', 'deviation_date',
            'description', 'deviation_type', 'severity', 'impact_on_subject',
            'corrective_action', 'preventative_action', 'reported_by',
            'report_date', 'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SiteActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteActivityLog
        fields = [
            'id', 'study', 'site', 'activity_type', 'description',
            'performed_by', 'activity_date', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']


class ParticipantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            'id', 'study', 'site', 'participant_id', 'status',
            'enrollment_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ParticipantDetailSerializer(serializers.ModelSerializer):
    eligibility_assessments = ParticipantEligibilitySerializer(many=True, read_only=True)
    visits = VisitSerializer(many=True, read_only=True)
    adverse_events = AdverseEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = Participant
        fields = [
            'id', 'study', 'site', 'arm', 'participant_id', 'first_name',
            'last_name', 'date_of_birth', 'gender', 'contact_email',
            'contact_phone', 'address', 'status', 'enrollment_date',
            'completion_date', 'withdrawal_date', 'withdrawal_reason',
            'eligibility_assessments', 'visits', 'adverse_events',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
