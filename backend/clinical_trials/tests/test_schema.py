from django.test import TestCase
from django.contrib.auth import get_user_model
from graphene.test import Client
from biobank_project.schema import schema
from clinical_trials.models import Study, StudyPhase, StudyArm, VisitTemplate

User = get_user_model()

class GraphQLSchemaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            is_staff=True
        )
        
        self.study = Study.objects.create(
            title='Test Study',
            description='Test study description',
            protocol_number='TEST-001',
            sponsor=self.user,
            principal_investigator=self.user,
            status='active'
        )
        
        self.phase = StudyPhase.objects.create(
            study=self.study,
            phase_type='phase_1',
            name='Phase 1',
            description='Test phase description'
        )
        
        self.arm = StudyArm.objects.create(
            study=self.study,
            name='Test Arm',
            description='Test arm description',
            arm_type='experimental'
        )
        
        self.visit_template = VisitTemplate.objects.create(
            study=self.study,
            name='Test Visit',
            description='Test visit description',
            duration_minutes=60,
            order=1
        )
        
        self.client = Client(schema)
    
    def test_query_studies(self):
        query = '''
        query {
            studies {
                id
                title
                protocolNumber
                status
            }
        }
        '''
        
        context = {'request': type('MockRequest', (), {'user': self.user})}
        result = self.client.execute(query, context=context)
        
        self.assertNotIn('errors', result)
        
        studies = result['data']['studies']
        self.assertEqual(len(studies), 1)
        self.assertEqual(studies[0]['title'], 'Test Study')
        self.assertEqual(studies[0]['protocolNumber'], 'TEST-001')
        self.assertEqual(studies[0]['status'], 'active')
    
    def test_query_study_by_id(self):
        query = '''
        query($id: ID!) {
            study(id: $id) {
                id
                title
                protocolNumber
                status
            }
        }
        '''
        
        context = {'request': type('MockRequest', (), {'user': self.user})}
        result = self.client.execute(query, context=context, variables={'id': str(self.study.id)})
        
        self.assertNotIn('errors', result)
        
        study = result['data']['study']
        self.assertEqual(study['title'], 'Test Study')
        self.assertEqual(study['protocolNumber'], 'TEST-001')
        self.assertEqual(study['status'], 'active')
    
    def test_query_study_phases(self):
        query = '''
        query($studyId: ID!) {
            studyPhases(studyId: $studyId) {
                id
                phaseType
                name
                description
            }
        }
        '''
        
        context = {'request': type('MockRequest', (), {'user': self.user})}
        result = self.client.execute(query, context=context, variables={'studyId': str(self.study.id)})
        
        self.assertNotIn('errors', result)
        
        phases = result['data']['studyPhases']
        self.assertEqual(len(phases), 1)
        self.assertEqual(phases[0]['phaseType'], 'phase_1')
        self.assertEqual(phases[0]['name'], 'Phase 1')
        self.assertEqual(phases[0]['description'], 'Test phase description')
    
    def test_query_study_arms(self):
        query = '''
        query($studyId: ID!) {
            studyArms(studyId: $studyId) {
                id
                name
                description
                armType
            }
        }
        '''
        
        context = {'request': type('MockRequest', (), {'user': self.user})}
        result = self.client.execute(query, context=context, variables={'studyId': str(self.study.id)})
        
        self.assertNotIn('errors', result)
        
        arms = result['data']['studyArms']
        self.assertEqual(len(arms), 1)
        self.assertEqual(arms[0]['name'], 'Test Arm')
        self.assertEqual(arms[0]['description'], 'Test arm description')
        self.assertEqual(arms[0]['armType'], 'experimental')
    
    def test_query_visit_templates(self):
        query = '''
        query($studyId: ID!) {
            visitTemplates(studyId: $studyId) {
                id
                name
                description
                durationMinutes
                order
            }
        }
        '''
        
        context = {'request': type('MockRequest', (), {'user': self.user})}
        result = self.client.execute(query, context=context, variables={'studyId': str(self.study.id)})
        
        self.assertNotIn('errors', result)
        
        templates = result['data']['visitTemplates']
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0]['name'], 'Test Visit')
        self.assertEqual(templates[0]['description'], 'Test visit description')
        self.assertEqual(templates[0]['durationMinutes'], 60)
        self.assertEqual(templates[0]['order'], 1)
    
    def test_create_study_mutation(self):
        mutation = '''
        mutation($input: StudyInput!) {
            createStudy(input: $input) {
                study {
                    id
                    title
                    protocolNumber
                    status
                }
            }
        }
        '''
        
        variables = {
            'input': {
                'title': 'New Test Study',
                'protocolNumber': 'TEST-002',
                'status': 'draft',
                'description': 'New test study description'
            }
        }
        
        context = {'request': type('MockRequest', (), {'user': self.user})}
        result = self.client.execute(mutation, context=context, variables=variables)
        
        self.assertNotIn('errors', result)
        
        study = result['data']['createStudy']['study']
        self.assertEqual(study['title'], 'New Test Study')
        self.assertEqual(study['protocolNumber'], 'TEST-002')
        self.assertEqual(study['status'], 'draft')
        
        self.assertTrue(Study.objects.filter(protocol_number='TEST-002').exists())
