from django.test import TestCase
from django.utils import timezone
from clinical_trials.models import Study, StudyPhase, StudyArm, Participant
from clinical_trials.serializers import StudySerializer, StudyDetailSerializer, ParticipantSerializer
from users.models import User

class ClinicalTrialsSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='investigator@example.com',
            password='password123',
            first_name='Principal',
            last_name='Investigator',
            is_investigator=True
        )
        
        self.study = Study.objects.create(
            title='Test Study',
            protocol_number='TS-001',
            description='A test study for serializer testing',
            status='ACTIVE',
            phase='PHASE_1',
            therapeutic_area='Oncology',
            indication='Cancer',
            principal_investigator=self.user,
            sponsor_name='Test Sponsor',
            start_date=timezone.now().date(),
            target_enrollment=100
        )
        
        self.phase1 = StudyPhase.objects.create(
            study=self.study,
            name='Screening',
            description='Screening phase',
            order=1
        )
        
        self.phase2 = StudyPhase.objects.create(
            study=self.study,
            name='Treatment',
            description='Treatment phase',
            order=2
        )
        
        self.arm1 = StudyArm.objects.create(
            study=self.study,
            name='Control',
            description='Control arm'
        )
        
        self.arm2 = StudyArm.objects.create(
            study=self.study,
            name='Treatment',
            description='Treatment arm'
        )
        
        self.participant = Participant.objects.create(
            study=self.study,
            arm=self.arm2,
            participant_id='P001',
            first_name='Test',
            last_name='Participant',
            date_of_birth=timezone.now().date() - timezone.timedelta(days=365*30),
            gender='MALE',
            contact_email='participant@example.com',
            status='ENROLLED',
            enrollment_date=timezone.now().date()
        )
    
    def test_study_list_serializer(self):
        serializer = StudySerializer(instance=self.study)
        data = serializer.data
        
        self.assertEqual(data['title'], self.study.title)
        self.assertEqual(data['protocol_number'], self.study.protocol_number)
        self.assertEqual(data['status'], self.study.status)
        self.assertEqual(data['phase'], self.study.phase)
    
    def test_study_detail_serializer(self):
        serializer = StudyDetailSerializer(instance=self.study)
        data = serializer.data
        
        self.assertEqual(data['title'], self.study.title)
        self.assertEqual(data['protocol_number'], self.study.protocol_number)
        self.assertEqual(data['description'], self.study.description)
        self.assertEqual(data['status'], self.study.status)
        self.assertEqual(data['phase'], self.study.phase)
        self.assertEqual(data['therapeutic_area'], self.study.therapeutic_area)
        self.assertEqual(data['indication'], self.study.indication)
        self.assertEqual(data['sponsor_name'], self.study.sponsor_name)
        
        self.assertEqual(len(data['phases']), 2)
        self.assertEqual(data['phases'][0]['name'], self.phase1.name)
        self.assertEqual(data['phases'][1]['name'], self.phase2.name)
        
        self.assertEqual(len(data['arms']), 2)
        self.assertEqual(data['arms'][0]['name'], self.arm1.name)
        self.assertEqual(data['arms'][1]['name'], self.arm2.name)
        
        self.assertEqual(data['principal_investigator']['email'], self.user.email)
        self.assertEqual(data['principal_investigator']['first_name'], self.user.first_name)
        self.assertEqual(data['principal_investigator']['last_name'], self.user.last_name)
    
    def test_participant_serializer(self):
        serializer = ParticipantSerializer(instance=self.participant)
        data = serializer.data
        
        self.assertEqual(data['participant_id'], self.participant.participant_id)
        self.assertEqual(data['first_name'], self.participant.first_name)
        self.assertEqual(data['last_name'], self.participant.last_name)
        self.assertEqual(data['gender'], self.participant.gender)
        self.assertEqual(data['status'], self.participant.status)
