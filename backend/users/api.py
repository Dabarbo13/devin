from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user profiles that provides a comprehensive view
    of user data including participant and donor information.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def comprehensive_profile(self, request, pk=None):
        """
        Returns a comprehensive profile view that includes:
        - Basic demographic information
        - Study participation history (past and current)
        - Donation history
        - Medical history (if available)
        """
        profile = self.get_object()
        user = profile.user
        
        data = {
            'user_id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'phone_number': user.phone_number,
            'date_of_birth': user.date_of_birth,
            'address': user.address,
            'organization': user.organization,
            'is_donor': user.is_donor,
            'profile': {
                'bio': profile.bio,
                'profile_picture': request.build_absolute_uri(profile.profile_picture.url) if profile.profile_picture else None,
            }
        }
        
        data['study_participation'] = profile.get_participant_studies
        data['is_active_participant'] = profile.is_active_study_participant
        
        data['donation_history'] = profile.get_donation_history
        
        if user.is_donor and hasattr(user, 'donor_profile'):
            try:
                donor = user.donor_profile
                data['donor_info'] = {
                    'donor_id': donor.donor_id,
                    'blood_type': donor.blood_type,
                    'height_cm': donor.height_cm,
                    'weight_kg': donor.weight_kg,
                    'bmi': donor.bmi,
                    'status': donor.status,
                    'hla_type': donor.hla_type,
                }
                
                if hasattr(donor, 'medical_history'):
                    medical_history = donor.medical_history
                    data['medical_history'] = {
                        'has_allergies': medical_history.has_allergies,
                        'allergies_description': medical_history.allergies_description,
                        'has_chronic_diseases': medical_history.has_chronic_diseases,
                        'chronic_diseases_description': medical_history.chronic_diseases_description,
                        'has_medications': medical_history.has_medications,
                        'medications_description': medical_history.medications_description,
                        'has_surgeries': medical_history.has_surgeries,
                        'surgeries_description': medical_history.surgeries_description,
                        'has_family_history': medical_history.has_family_history,
                        'family_history_description': medical_history.family_history_description,
                        'has_infectious_diseases': medical_history.has_infectious_diseases,
                        'infectious_diseases_description': medical_history.infectious_diseases_description,
                    }
            except Exception as e:
                data['donor_info_error'] = str(e)
        
        return Response(data)
