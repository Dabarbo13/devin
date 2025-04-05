from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserProfile
from users.serializers import UserSerializer, UserProfileSerializer, UserCreateSerializer, UserUpdateSerializer

User = get_user_model()

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'is_donor': True
        }
        self.user = User.objects.create_user(**self.user_data)
        self.profile = UserProfile.objects.create(user=self.user, bio='Test bio')
    
    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(data['email'], self.user_data['email'])
        self.assertEqual(data['first_name'], self.user_data['first_name'])
        self.assertEqual(data['last_name'], self.user_data['last_name'])
        self.assertEqual(data['phone_number'], self.user_data['phone_number'])
        self.assertEqual(data['is_donor'], self.user_data['is_donor'])
        self.assertIn('profile', data)
        self.assertEqual(data['profile']['bio'], 'Test bio')
        self.assertNotIn('password', data)
    
    def test_user_create_serializer(self):
        new_user_data = {
            'email': 'new@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User',
            'is_recruiter': True
        }
        
        serializer = UserCreateSerializer(data=new_user_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, new_user_data['email'])
        self.assertEqual(user.first_name, new_user_data['first_name'])
        self.assertEqual(user.last_name, new_user_data['last_name'])
        self.assertEqual(user.is_recruiter, new_user_data['is_recruiter'])
        self.assertTrue(user.check_password(new_user_data['password']))
        self.assertTrue(hasattr(user, 'profile'))
    
    def test_user_update_serializer(self):
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'is_sponsor': True
        }
        
        serializer = UserUpdateSerializer(instance=self.user, data=update_data)
        self.assertTrue(serializer.is_valid())
        
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, update_data['first_name'])
        self.assertEqual(updated_user.last_name, update_data['last_name'])
        self.assertEqual(updated_user.is_sponsor, update_data['is_sponsor'])
        self.assertEqual(updated_user.email, self.user_data['email'])  # Email shouldn't change
    
    def test_user_profile_serializer(self):
        profile_data = {
            'bio': 'Updated bio'
        }
        
        serializer = UserProfileSerializer(instance=self.profile, data=profile_data)
        self.assertTrue(serializer.is_valid())
        
        updated_profile = serializer.save()
        self.assertEqual(updated_profile.bio, profile_data['bio'])
