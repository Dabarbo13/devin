from rest_framework import serializers
from .models import (
    Donor, DonorMedicalHistory, PhysicalExam, LabTest, DonorEligibilityRule,
    DonorEligibilityAssessment, DonationType, DonationAppointment, Donation,
    SampleType, StorageUnit, StorageLocation, Sample, ChainOfCustodyLog
)
from users.serializers import UserSerializer


class DonorMedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorMedicalHistory
        fields = [
            'id', 'donor', 'has_allergies', 'allergies_description',
            'has_chronic_diseases', 'chronic_diseases_description',
            'has_medications', 'medications_description',
            'has_surgeries', 'surgeries_description',
            'has_family_history', 'family_history_description',
            'has_infectious_diseases', 'infectious_diseases_description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PhysicalExamSerializer(serializers.ModelSerializer):
    examiner = UserSerializer(read_only=True)
    
    class Meta:
        model = PhysicalExam
        fields = [
            'id', 'donor', 'exam_date', 'examiner', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'heart_rate', 'temperature', 'respiratory_rate',
            'height_cm', 'weight_kg', 'general_appearance', 'heent', 'cardiovascular',
            'respiratory', 'gastrointestinal', 'musculoskeletal', 'neurological',
            'skin', 'notes', 'is_eligible', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LabTestSerializer(serializers.ModelSerializer):
    ordered_by = UserSerializer(read_only=True)
    
    class Meta:
        model = LabTest
        fields = [
            'id', 'donor', 'test_name', 'test_code', 'ordered_by', 'order_date',
            'collection_date', 'result_date', 'status', 'result_value',
            'reference_range', 'is_abnormal', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DonorEligibilityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorEligibilityRule
        fields = [
            'id', 'name', 'description', 'rule_type', 'parameter',
            'condition', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DonorEligibilityAssessmentSerializer(serializers.ModelSerializer):
    assessed_by = UserSerializer(read_only=True)
    rule = DonorEligibilityRuleSerializer(read_only=True)
    
    class Meta:
        model = DonorEligibilityAssessment
        fields = [
            'id', 'donor', 'rule', 'is_met', 'assessed_by',
            'assessment_date', 'notes'
        ]


class DonationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationType
        fields = [
            'id', 'name', 'description', 'preparation_instructions',
            'recovery_time_days', 'minimum_interval_days', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DonationAppointmentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    donation_type = DonationTypeSerializer(read_only=True)
    
    class Meta:
        model = DonationAppointment
        fields = [
            'id', 'donor', 'donation_type', 'scheduled_date', 'scheduled_time',
            'end_time', 'status', 'notes', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SampleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleType
        fields = [
            'id', 'name', 'description', 'storage_temperature',
            'shelf_life_days', 'processing_instructions', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = [
            'id', 'name', 'unit_type', 'location', 'temperature_range',
            'capacity', 'is_active', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StorageLocationSerializer(serializers.ModelSerializer):
    storage_unit = StorageUnitSerializer(read_only=True)
    
    class Meta:
        model = StorageLocation
        fields = [
            'id', 'storage_unit', 'name', 'position', 'is_available',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DonationSerializer(serializers.ModelSerializer):
    donation_type = DonationTypeSerializer(read_only=True)
    collected_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Donation
        fields = [
            'id', 'donor', 'appointment', 'donation_type', 'donation_date',
            'donation_id', 'volume_ml', 'collected_by', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SampleSerializer(serializers.ModelSerializer):
    sample_type = SampleTypeSerializer(read_only=True)
    storage_location = StorageLocationSerializer(read_only=True)
    processed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Sample
        fields = [
            'id', 'donation', 'sample_type', 'sample_id', 'barcode',
            'volume_ml', 'status', 'collection_date', 'expiration_date',
            'storage_location', 'processed_by', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ChainOfCustodyLogSerializer(serializers.ModelSerializer):
    performed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ChainOfCustodyLog
        fields = [
            'id', 'sample', 'action', 'timestamp', 'performed_by',
            'from_location', 'to_location', 'notes'
        ]


class DonorListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Donor
        fields = [
            'id', 'user', 'donor_id', 'blood_type', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DonorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    medical_history = DonorMedicalHistorySerializer(read_only=True)
    physical_exams = PhysicalExamSerializer(many=True, read_only=True)
    lab_tests = LabTestSerializer(many=True, read_only=True)
    eligibility_assessments = DonorEligibilityAssessmentSerializer(many=True, read_only=True)
    donation_appointments = DonationAppointmentSerializer(many=True, read_only=True)
    donations = DonationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Donor
        fields = [
            'id', 'user', 'donor_id', 'blood_type', 'height_cm', 'weight_kg',
            'bmi', 'status', 'hla_type', 'notes', 'medical_history',
            'physical_exams', 'lab_tests', 'eligibility_assessments',
            'donation_appointments', 'donations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'bmi']
