from django.test import TestCase
from django.utils import timezone
from recruiting.models import (
    Prospect, DemographicInfo, HealthInfo, StudyQualification,
    ContactLog, Message, Referral, SocialMediaCampaign, CampaignMetrics
)
from recruiting.serializers import (
    ProspectListSerializer, ProspectDetailSerializer, DemographicInfoSerializer,
    HealthInfoSerializer, StudyQualificationSerializer, ContactLogSerializer,
    MessageSerializer, ReferralSerializer, SocialMediaCampaignSerializer,
    CampaignMetricsSerializer
)
from users.models import User
from clinical_trials.models import Study

class RecruitingSerializerTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            email='recruiter@example.com',
            password='password123',
            first_name='Test',
            last_name='Recruiter',
            is_recruiter=True
        )
        
        self.study = Study.objects.create(
            title='Test Study',
            protocol_number='TS-001',
            status='ACTIVE',
            phase='PHASE_1',
            therapeutic_area='Oncology',
            indication='Cancer',
            sponsor_name='Test Sponsor',
            start_date=timezone.now().date(),
            target_enrollment=100
        )
        
        self.prospect = Prospect.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            status='NEW',
            source='WEBSITE',
            assigned_to=self.recruiter
        )
        
        self.demographic_info = DemographicInfo.objects.create(
            prospect=self.prospect,
            date_of_birth=timezone.now().date() - timezone.timedelta(days=365*30),
            gender='MALE',
            ethnicity='CAUCASIAN',
            address='123 Main St',
            city='Anytown',
            state='CA',
            zip_code='12345',
            education_level='BACHELORS'
        )
        
        self.health_info = HealthInfo.objects.create(
            prospect=self.prospect,
            height_cm=180,
            weight_kg=75,
            bmi=23.1,
            blood_type='A_POSITIVE',
            has_allergies=True,
            allergies_description='Pollen, dust',
            has_medical_conditions=False,
            medications='Antihistamines'
        )
        
        self.qualification = StudyQualification.objects.create(
            prospect=self.prospect,
            study=self.study,
            is_qualified=True,
            qualification_date=timezone.now().date(),
            notes='Meets all criteria'
        )
        
        self.contact_log = ContactLog.objects.create(
            prospect=self.prospect,
            contact_type='PHONE',
            contacted_by=self.recruiter,
            contact_date=timezone.now(),
            outcome='INTERESTED',
            notes='Discussed study details'
        )
        
        self.message = Message.objects.create(
            prospect=self.prospect,
            message_type='EMAIL',
            sent_by=self.recruiter,
            sent_date=timezone.now(),
            subject='Study Information',
            content='Here is information about the study',
            status='SENT'
        )
        
        self.referral = Referral.objects.create(
            prospect=self.prospect,
            referrer_name='Jane Smith',
            referrer_email='jane.smith@example.com',
            referrer_phone='0987654321',
            relationship='FRIEND',
            status='PENDING',
            bonus_amount=50.00
        )
        
        self.campaign = SocialMediaCampaign.objects.create(
            name='Facebook Campaign',
            platform='FACEBOOK',
            target_audience='Adults 25-45',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30),
            budget=1000.00,
            status='ACTIVE'
        )
        
        self.metrics = CampaignMetrics.objects.create(
            campaign=self.campaign,
            date=timezone.now().date(),
            impressions=5000,
            clicks=200,
            conversions=20,
            cost=50.00
        )
    
    def test_prospect_list_serializer(self):
        serializer = ProspectListSerializer(instance=self.prospect)
        data = serializer.data
        
        self.assertEqual(data['first_name'], self.prospect.first_name)
        self.assertEqual(data['last_name'], self.prospect.last_name)
        self.assertEqual(data['email'], self.prospect.email)
        self.assertEqual(data['phone'], self.prospect.phone)
        self.assertEqual(data['status'], self.prospect.status)
        self.assertEqual(data['source'], self.prospect.source)
    
    def test_prospect_detail_serializer(self):
        serializer = ProspectDetailSerializer(instance=self.prospect)
        data = serializer.data
        
        self.assertEqual(data['first_name'], self.prospect.first_name)
        self.assertEqual(data['last_name'], self.prospect.last_name)
        self.assertEqual(data['email'], self.prospect.email)
        self.assertEqual(data['phone'], self.prospect.phone)
        self.assertEqual(data['status'], self.prospect.status)
        self.assertEqual(data['source'], self.prospect.source)
        
        self.assertEqual(data['demographic_info']['gender'], self.demographic_info.gender)
        self.assertEqual(data['demographic_info']['ethnicity'], self.demographic_info.ethnicity)
        
        self.assertEqual(data['health_info']['height_cm'], self.health_info.height_cm)
        self.assertEqual(data['health_info']['weight_kg'], self.health_info.weight_kg)
        self.assertEqual(data['health_info']['blood_type'], self.health_info.blood_type)
        
        self.assertEqual(len(data['contact_logs']), 1)
        self.assertEqual(data['contact_logs'][0]['contact_type'], self.contact_log.contact_type)
        self.assertEqual(data['contact_logs'][0]['outcome'], self.contact_log.outcome)
    
    def test_demographic_info_serializer(self):
        serializer = DemographicInfoSerializer(instance=self.demographic_info)
        data = serializer.data
        
        self.assertEqual(data['gender'], self.demographic_info.gender)
        self.assertEqual(data['ethnicity'], self.demographic_info.ethnicity)
        self.assertEqual(data['address'], self.demographic_info.address)
        self.assertEqual(data['city'], self.demographic_info.city)
        self.assertEqual(data['state'], self.demographic_info.state)
        self.assertEqual(data['zip_code'], self.demographic_info.zip_code)
        self.assertEqual(data['education_level'], self.demographic_info.education_level)
    
    def test_health_info_serializer(self):
        serializer = HealthInfoSerializer(instance=self.health_info)
        data = serializer.data
        
        self.assertEqual(data['height_cm'], self.health_info.height_cm)
        self.assertEqual(data['weight_kg'], self.health_info.weight_kg)
        self.assertEqual(data['bmi'], self.health_info.bmi)
        self.assertEqual(data['blood_type'], self.health_info.blood_type)
        self.assertTrue(data['has_allergies'])
        self.assertEqual(data['allergies_description'], self.health_info.allergies_description)
        self.assertFalse(data['has_medical_conditions'])
        self.assertEqual(data['medications'], self.health_info.medications)
    
    def test_social_media_campaign_serializer(self):
        serializer = SocialMediaCampaignSerializer(instance=self.campaign)
        data = serializer.data
        
        self.assertEqual(data['name'], self.campaign.name)
        self.assertEqual(data['platform'], self.campaign.platform)
        self.assertEqual(data['target_audience'], self.campaign.target_audience)
        self.assertEqual(data['budget'], str(self.campaign.budget))
        self.assertEqual(data['status'], self.campaign.status)
    
    def test_campaign_metrics_serializer(self):
        serializer = CampaignMetricsSerializer(instance=self.metrics)
        data = serializer.data
        
        self.assertEqual(data['impressions'], self.metrics.impressions)
        self.assertEqual(data['clicks'], self.metrics.clicks)
        self.assertEqual(data['conversions'], self.metrics.conversions)
        self.assertEqual(data['cost'], str(self.metrics.cost))
