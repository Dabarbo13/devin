from rest_framework import serializers
from .models import (
    Prospect, DemographicInfo, HealthInfo, StudyQualification, ContactLog,
    Message, MessageTemplate, Referral, SocialMediaCampaign, CampaignMetrics
)
from users.serializers import UserSerializer
from clinical_trials.serializers import StudySerializer


class DemographicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicInfo
        fields = [
            'id', 'prospect', 'gender', 'ethnicity', 'race', 'height_cm',
            'weight_kg', 'blood_type', 'hla_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class HealthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInfo
        fields = [
            'id', 'prospect', 'has_allergies', 'allergies_description',
            'has_chronic_diseases', 'chronic_diseases_description',
            'has_medications', 'medications_description',
            'has_surgeries', 'surgeries_description',
            'has_family_history', 'family_history_description',
            'has_infectious_diseases', 'infectious_diseases_description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudyQualificationSerializer(serializers.ModelSerializer):
    assessed_by = UserSerializer(read_only=True)
    study = StudySerializer(read_only=True)
    
    class Meta:
        model = StudyQualification
        fields = [
            'id', 'prospect', 'study', 'status', 'notes',
            'assessed_by', 'assessment_date', 'updated_at'
        ]
        read_only_fields = ['assessment_date', 'updated_at']


class ContactLogSerializer(serializers.ModelSerializer):
    contacted_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ContactLog
        fields = [
            'id', 'prospect', 'contact_type', 'direction', 'contact_date',
            'outcome', 'notes', 'follow_up_date', 'contacted_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'prospect', 'message_type', 'subject', 'content',
            'sender', 'recipient_email', 'recipient_phone', 'status',
            'sent_at', 'delivered_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'sent_at', 'delivered_at']


class MessageTemplateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = MessageTemplate
        fields = [
            'id', 'name', 'message_type', 'subject', 'content',
            'is_active', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = [
            'id', 'referrer_type', 'referrer_prospect', 'referrer_donor',
            'referrer_participant', 'referred_prospect', 'status',
            'referral_date', 'notes', 'bonus_paid', 'bonus_amount',
            'bonus_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'referral_date']


class SocialMediaCampaignSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SocialMediaCampaign
        fields = [
            'id', 'name', 'description', 'platform', 'status',
            'start_date', 'end_date', 'target_audience', 'budget',
            'tracking_url', 'tracking_code', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CampaignMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignMetrics
        fields = [
            'id', 'campaign', 'date', 'impressions', 'clicks',
            'conversions', 'cost', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProspectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prospect
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'status', 'source', 'is_donor_prospect', 'is_study_prospect',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProspectDetailSerializer(serializers.ModelSerializer):
    demographics = DemographicInfoSerializer(read_only=True)
    health_info = HealthInfoSerializer(read_only=True)
    study_qualifications = StudyQualificationSerializer(many=True, read_only=True)
    contact_logs = ContactLogSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    referral = ReferralSerializer(read_only=True)
    
    class Meta:
        model = Prospect
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'address', 'status', 'source', 'source_details',
            'notes', 'is_donor_prospect', 'is_study_prospect', 'demographics',
            'health_info', 'study_qualifications', 'contact_logs', 'messages',
            'referral', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
