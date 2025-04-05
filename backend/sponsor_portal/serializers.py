from rest_framework import serializers
from .models import (
    SponsorProfile, ResearcherProfile, ProtocolDraft, ProtocolReview,
    RecruitmentMetrics, CustomSampleRequest, SampleOrder, OrderItem,
    OrderSample, Dashboard, DashboardWidget
)
from users.serializers import UserSerializer
from clinical_trials.serializers import StudySerializer, StudySiteSerializer
from donation_management.serializers import SampleTypeSerializer, SampleSerializer


class SponsorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SponsorProfile
        fields = [
            'id', 'user', 'company_name', 'company_address', 'company_website',
            'contact_phone', 'department', 'position', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ResearcherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ResearcherProfile
        fields = [
            'id', 'user', 'institution_name', 'institution_address',
            'institution_website', 'department', 'position',
            'research_interests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProtocolDraftSerializer(serializers.ModelSerializer):
    sponsor = UserSerializer(read_only=True)
    
    class Meta:
        model = ProtocolDraft
        fields = [
            'id', 'title', 'description', 'sponsor', 'status',
            'version', 'document', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProtocolReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    protocol_draft = ProtocolDraftSerializer(read_only=True)
    
    class Meta:
        model = ProtocolReview
        fields = [
            'id', 'protocol_draft', 'reviewer', 'decision',
            'comments', 'review_date', 'updated_at'
        ]
        read_only_fields = ['review_date', 'updated_at']


class RecruitmentMetricsSerializer(serializers.ModelSerializer):
    study = StudySerializer(read_only=True)
    site = StudySiteSerializer(read_only=True)
    
    class Meta:
        model = RecruitmentMetrics
        fields = [
            'id', 'study', 'site', 'date', 'inquiries', 'screenings',
            'screen_failures', 'enrollments', 'withdrawals', 'completions',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CustomSampleRequestSerializer(serializers.ModelSerializer):
    researcher = UserSerializer(read_only=True)
    sample_type = SampleTypeSerializer(read_only=True)
    
    class Meta:
        model = CustomSampleRequest
        fields = [
            'id', 'researcher', 'title', 'description', 'sample_type',
            'quantity', 'donor_criteria', 'processing_instructions',
            'target_date', 'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    sample_type = SampleTypeSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'sample_type', 'quantity', 'price_per_unit',
            'total_price', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_price']


class OrderSampleSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)
    
    class Meta:
        model = OrderSample
        fields = ['id', 'order', 'sample', 'order_item', 'created_at']
        read_only_fields = ['created_at']


class SampleOrderListSerializer(serializers.ModelSerializer):
    researcher = UserSerializer(read_only=True)
    
    class Meta:
        model = SampleOrder
        fields = [
            'id', 'researcher', 'order_number', 'status', 'order_date',
            'target_date', 'payment_status', 'total_amount', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'order_date']


class SampleOrderDetailSerializer(serializers.ModelSerializer):
    researcher = UserSerializer(read_only=True)
    custom_request = CustomSampleRequestSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    samples = OrderSampleSerializer(many=True, read_only=True)
    
    class Meta:
        model = SampleOrder
        fields = [
            'id', 'researcher', 'custom_request', 'order_number', 'status',
            'order_date', 'target_date', 'shipping_address', 'shipping_method',
            'tracking_number', 'shipped_date', 'received_date', 'total_amount',
            'payment_status', 'payment_date', 'notes', 'items', 'samples',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'order_date']


class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'dashboard', 'title', 'widget_type', 'data_source',
            'config', 'position', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DashboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    widgets = DashboardWidgetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dashboard
        fields = [
            'id', 'name', 'description', 'dashboard_type', 'user',
            'is_default', 'layout', 'widgets', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
