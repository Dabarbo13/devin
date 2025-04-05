from django.test import TestCase
from django.utils import timezone
from donation_management.models import (
    Donor, DonorMedicalHistory, DonationType, SampleType, StorageUnit, StorageLocation
)
from donation_management.serializers import (
    DonorListSerializer, DonorDetailSerializer, DonorMedicalHistorySerializer,
    DonationTypeSerializer, SampleTypeSerializer, StorageUnitSerializer, StorageLocationSerializer
)
from users.models import User

class DonationManagementSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='donor@example.com',
            password='password123',
            first_name='Test',
            last_name='Donor',
            is_donor=True
        )
        
        self.donor = Donor.objects.create(
            user=self.user,
            donor_id='D001',
            blood_type='A_POSITIVE',
            height_cm=180,
            weight_kg=75,
            status='ACTIVE',
            hla_type='A*01:01,B*08:01'
        )
        
        self.medical_history = DonorMedicalHistory.objects.create(
            donor=self.donor,
            has_allergies=True,
            allergies_description='Pollen, dust',
            has_chronic_diseases=False,
            has_medications=True,
            medications_description='Antihistamines'
        )
        
        self.donation_type = DonationType.objects.create(
            name='Whole Blood',
            description='Standard whole blood donation',
            preparation_instructions='Eat well and stay hydrated',
            recovery_time_days=1,
            minimum_interval_days=56,
            is_active=True
        )
        
        self.sample_type = SampleType.objects.create(
            name='Plasma',
            description='Blood plasma',
            storage_temperature='-20',
            shelf_life_days=365,
            processing_instructions='Centrifuge at 3000 rpm for 15 minutes',
            is_active=True
        )
        
        self.storage_unit = StorageUnit.objects.create(
            name='Freezer 1',
            unit_type='FREEZER',
            location='Lab Room 101',
            temperature_range='-30 to -20',
            capacity=100,
            is_active=True
        )
        
        self.storage_location = StorageLocation.objects.create(
            storage_unit=self.storage_unit,
            name='Shelf A',
            position='1-1',
            is_available=True
        )
    
    def test_donor_list_serializer(self):
        serializer = DonorListSerializer(instance=self.donor)
        data = serializer.data
        
        self.assertEqual(data['donor_id'], self.donor.donor_id)
        self.assertEqual(data['blood_type'], self.donor.blood_type)
        self.assertEqual(data['status'], self.donor.status)
        
        self.assertEqual(data['user']['email'], self.user.email)
        self.assertEqual(data['user']['first_name'], self.user.first_name)
        self.assertEqual(data['user']['last_name'], self.user.last_name)
    
    def test_donor_detail_serializer(self):
        serializer = DonorDetailSerializer(instance=self.donor)
        data = serializer.data
        
        self.assertEqual(data['donor_id'], self.donor.donor_id)
        self.assertEqual(data['blood_type'], self.donor.blood_type)
        self.assertEqual(data['height_cm'], self.donor.height_cm)
        self.assertEqual(data['weight_kg'], self.donor.weight_kg)
        self.assertEqual(data['status'], self.donor.status)
        self.assertEqual(data['hla_type'], self.donor.hla_type)
        
        self.assertTrue(data['medical_history']['has_allergies'])
        self.assertEqual(data['medical_history']['allergies_description'], 'Pollen, dust')
        self.assertFalse(data['medical_history']['has_chronic_diseases'])
        self.assertTrue(data['medical_history']['has_medications'])
        self.assertEqual(data['medical_history']['medications_description'], 'Antihistamines')
    
    def test_donor_medical_history_serializer(self):
        serializer = DonorMedicalHistorySerializer(instance=self.medical_history)
        data = serializer.data
        
        self.assertTrue(data['has_allergies'])
        self.assertEqual(data['allergies_description'], 'Pollen, dust')
        self.assertFalse(data['has_chronic_diseases'])
        self.assertTrue(data['has_medications'])
        self.assertEqual(data['medications_description'], 'Antihistamines')
    
    def test_donation_type_serializer(self):
        serializer = DonationTypeSerializer(instance=self.donation_type)
        data = serializer.data
        
        self.assertEqual(data['name'], self.donation_type.name)
        self.assertEqual(data['description'], self.donation_type.description)
        self.assertEqual(data['preparation_instructions'], self.donation_type.preparation_instructions)
        self.assertEqual(data['recovery_time_days'], self.donation_type.recovery_time_days)
        self.assertEqual(data['minimum_interval_days'], self.donation_type.minimum_interval_days)
        self.assertTrue(data['is_active'])
    
    def test_sample_type_serializer(self):
        serializer = SampleTypeSerializer(instance=self.sample_type)
        data = serializer.data
        
        self.assertEqual(data['name'], self.sample_type.name)
        self.assertEqual(data['description'], self.sample_type.description)
        self.assertEqual(data['storage_temperature'], self.sample_type.storage_temperature)
        self.assertEqual(data['shelf_life_days'], self.sample_type.shelf_life_days)
        self.assertEqual(data['processing_instructions'], self.sample_type.processing_instructions)
        self.assertTrue(data['is_active'])
    
    def test_storage_unit_serializer(self):
        serializer = StorageUnitSerializer(instance=self.storage_unit)
        data = serializer.data
        
        self.assertEqual(data['name'], self.storage_unit.name)
        self.assertEqual(data['unit_type'], self.storage_unit.unit_type)
        self.assertEqual(data['location'], self.storage_unit.location)
        self.assertEqual(data['temperature_range'], self.storage_unit.temperature_range)
        self.assertEqual(data['capacity'], self.storage_unit.capacity)
        self.assertTrue(data['is_active'])
    
    def test_storage_location_serializer(self):
        serializer = StorageLocationSerializer(instance=self.storage_location)
        data = serializer.data
        
        self.assertEqual(data['name'], self.storage_location.name)
        self.assertEqual(data['position'], self.storage_location.position)
        self.assertTrue(data['is_available'])
        
        self.assertEqual(data['storage_unit']['name'], self.storage_unit.name)
        self.assertEqual(data['storage_unit']['unit_type'], self.storage_unit.unit_type)
