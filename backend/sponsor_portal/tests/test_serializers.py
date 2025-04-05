from django.test import TestCase
from django.utils import timezone
from sponsor_portal.models import (
    SponsorProfile, ResearcherProfile, ProtocolDraft, ProtocolReview,
    RecruitmentMetrics, CustomSampleRequest, SampleOrder, Dashboard
)
from sponsor_portal.serializers import (
    SponsorProfileSerializer, ResearcherProfileSerializer, ProtocolDraftSerializer,
    ProtocolReviewSerializer, RecruitmentMetricsSerializer, CustomSampleRequestSerializer,
    SampleOrderListSerializer, SampleOrderDetailSerializer, DashboardSerializer
)
from users.models import User
from clinical_trials.models import Study, StudySite
from donation_management.models import SampleType

class SponsorPortalSerializerTestCase(TestCase):
    def setUp(self):
        self.sponsor_user = User.objects.create_user(
            email='sponsor@example.com',
            password='password123',
            first_name='Test',
            last_name='Sponsor',
            is_sponsor=True
        )
        
        self.researcher_user = User.objects.create_user(
            email='researcher@example.com',
            password='password123',
            first_name='Test',
            last_name='Researcher',
            is_researcher=True
        )
        
        self.sponsor_profile = SponsorProfile.objects.create(
            user=self.sponsor_user,
            company_name='Test Pharma',
            company_address='123 Pharma St, City',
            company_website='https://testpharma.com',
            contact_phone='1234567890',
            department='Clinical Research',
            position='Director'
        )
        
        self.researcher_profile = ResearcherProfile.objects.create(
            user=self.researcher_user,
            institution_name='Test University',
            institution_address='456 University Ave, City',
            institution_website='https://testuniversity.edu',
            department='Biology',
            position='Professor',
            research_interests='Oncology, Immunology'
        )
        
        self.protocol_draft = ProtocolDraft.objects.create(
            title='Test Protocol',
            description='A test protocol for serializer testing',
            sponsor=self.sponsor_user,
            status='DRAFT',
            version='1.0',
            notes='Initial draft'
        )
        
        self.protocol_review = ProtocolReview.objects.create(
            protocol_draft=self.protocol_draft,
            reviewer=self.researcher_user,
            decision='APPROVED',
            comments='Looks good',
            review_date=timezone.now()
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
        
        self.site = StudySite.objects.create(
            study=self.study,
            name='Test Site',
            address='789 Site St, City',
            contact_name='Site Manager',
            contact_email='site@example.com',
            status='ACTIVE'
        )
        
        self.recruitment_metrics = RecruitmentMetrics.objects.create(
            study=self.study,
            site=self.site,
            date=timezone.now().date(),
            inquiries=50,
            screenings=30,
            screen_failures=10,
            enrollments=20,
            withdrawals=2,
            completions=15
        )
        
        self.sample_type = SampleType.objects.create(
            name='Blood',
            description='Whole blood sample',
            storage_temperature='4',
            shelf_life_days=30,
            is_active=True
        )
        
        self.sample_request = CustomSampleRequest.objects.create(
            researcher=self.researcher_user,
            title='Blood Samples Request',
            description='Need blood samples for research',
            sample_type=self.sample_type,
            quantity=10,
            donor_criteria='Healthy adults',
            target_date=timezone.now().date() + timezone.timedelta(days=30),
            status='PENDING'
        )
        
        self.sample_order = SampleOrder.objects.create(
            researcher=self.researcher_user,
            custom_request=self.sample_request,
            order_number='SO-001',
            status='PROCESSING',
            order_date=timezone.now().date(),
            target_date=timezone.now().date() + timezone.timedelta(days=14),
            shipping_address='456 University Ave, City',
            shipping_method='Express',
            total_amount=1000.00,
            payment_status='PENDING'
        )
        
        self.dashboard = Dashboard.objects.create(
            name='Research Dashboard',
            description='Dashboard for research data',
            dashboard_type='RESEARCHER',
            user=self.researcher_user,
            is_default=True,
            layout='{"layout": "grid"}'
        )
    
    def test_sponsor_profile_serializer(self):
        serializer = SponsorProfileSerializer(instance=self.sponsor_profile)
        data = serializer.data
        
        self.assertEqual(data['company_name'], self.sponsor_profile.company_name)
        self.assertEqual(data['company_address'], self.sponsor_profile.company_address)
        self.assertEqual(data['company_website'], self.sponsor_profile.company_website)
        self.assertEqual(data['contact_phone'], self.sponsor_profile.contact_phone)
        self.assertEqual(data['department'], self.sponsor_profile.department)
        self.assertEqual(data['position'], self.sponsor_profile.position)
        
        self.assertEqual(data['user']['email'], self.sponsor_user.email)
        self.assertEqual(data['user']['first_name'], self.sponsor_user.first_name)
        self.assertEqual(data['user']['last_name'], self.sponsor_user.last_name)
    
    def test_researcher_profile_serializer(self):
        serializer = ResearcherProfileSerializer(instance=self.researcher_profile)
        data = serializer.data
        
        self.assertEqual(data['institution_name'], self.researcher_profile.institution_name)
        self.assertEqual(data['institution_address'], self.researcher_profile.institution_address)
        self.assertEqual(data['institution_website'], self.researcher_profile.institution_website)
        self.assertEqual(data['department'], self.researcher_profile.department)
        self.assertEqual(data['position'], self.researcher_profile.position)
        self.assertEqual(data['research_interests'], self.researcher_profile.research_interests)
    
    def test_protocol_draft_serializer(self):
        serializer = ProtocolDraftSerializer(instance=self.protocol_draft)
        data = serializer.data
        
        self.assertEqual(data['title'], self.protocol_draft.title)
        self.assertEqual(data['description'], self.protocol_draft.description)
        self.assertEqual(data['status'], self.protocol_draft.status)
        self.assertEqual(data['version'], self.protocol_draft.version)
        self.assertEqual(data['notes'], self.protocol_draft.notes)
        
        self.assertEqual(data['sponsor']['email'], self.sponsor_user.email)
    
    def test_protocol_review_serializer(self):
        serializer = ProtocolReviewSerializer(instance=self.protocol_review)
        data = serializer.data
        
        self.assertEqual(data['decision'], self.protocol_review.decision)
        self.assertEqual(data['comments'], self.protocol_review.comments)
        
        self.assertEqual(data['reviewer']['email'], self.researcher_user.email)
        
        self.assertEqual(data['protocol_draft']['title'], self.protocol_draft.title)
    
    def test_recruitment_metrics_serializer(self):
        serializer = RecruitmentMetricsSerializer(instance=self.recruitment_metrics)
        data = serializer.data
        
        self.assertEqual(data['inquiries'], self.recruitment_metrics.inquiries)
        self.assertEqual(data['screenings'], self.recruitment_metrics.screenings)
        self.assertEqual(data['screen_failures'], self.recruitment_metrics.screen_failures)
        self.assertEqual(data['enrollments'], self.recruitment_metrics.enrollments)
        self.assertEqual(data['withdrawals'], self.recruitment_metrics.withdrawals)
        self.assertEqual(data['completions'], self.recruitment_metrics.completions)
        
        self.assertEqual(data['study']['title'], self.study.title)
        
        self.assertEqual(data['site']['name'], self.site.name)
    
    def test_custom_sample_request_serializer(self):
        serializer = CustomSampleRequestSerializer(instance=self.sample_request)
        data = serializer.data
        
        self.assertEqual(data['title'], self.sample_request.title)
        self.assertEqual(data['description'], self.sample_request.description)
        self.assertEqual(data['quantity'], self.sample_request.quantity)
        self.assertEqual(data['donor_criteria'], self.sample_request.donor_criteria)
        self.assertEqual(data['status'], self.sample_request.status)
        
        self.assertEqual(data['researcher']['email'], self.researcher_user.email)
        
        self.assertEqual(data['sample_type']['name'], self.sample_type.name)
    
    def test_sample_order_list_serializer(self):
        serializer = SampleOrderListSerializer(instance=self.sample_order)
        data = serializer.data
        
        self.assertEqual(data['order_number'], self.sample_order.order_number)
        self.assertEqual(data['status'], self.sample_order.status)
        self.assertEqual(data['payment_status'], self.sample_order.payment_status)
        self.assertEqual(data['total_amount'], str(self.sample_order.total_amount))
        
        self.assertEqual(data['researcher']['email'], self.researcher_user.email)
    
    def test_sample_order_detail_serializer(self):
        serializer = SampleOrderDetailSerializer(instance=self.sample_order)
        data = serializer.data
        
        self.assertEqual(data['order_number'], self.sample_order.order_number)
        self.assertEqual(data['status'], self.sample_order.status)
        self.assertEqual(data['shipping_address'], self.sample_order.shipping_address)
        self.assertEqual(data['shipping_method'], self.sample_order.shipping_method)
        self.assertEqual(data['payment_status'], self.sample_order.payment_status)
        self.assertEqual(data['total_amount'], str(self.sample_order.total_amount))
        
        self.assertEqual(data['researcher']['email'], self.researcher_user.email)
        
        self.assertEqual(data['custom_request']['title'], self.sample_request.title)
    
    def test_dashboard_serializer(self):
        serializer = DashboardSerializer(instance=self.dashboard)
        data = serializer.data
        
        self.assertEqual(data['name'], self.dashboard.name)
        self.assertEqual(data['description'], self.dashboard.description)
        self.assertEqual(data['dashboard_type'], self.dashboard.dashboard_type)
        self.assertEqual(data['is_default'], self.dashboard.is_default)
        self.assertEqual(data['layout'], self.dashboard.layout)
        
        self.assertEqual(data['user']['email'], self.researcher_user.email)
