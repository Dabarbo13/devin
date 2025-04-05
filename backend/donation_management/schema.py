import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import (
    Donor, DonorMedicalHistory, DonationType, DonationAppointment, 
    SampleType, Sample, StorageUnit, StorageLocation, ChainOfCustodyLog
)

User = get_user_model()

class DonorType(DjangoObjectType):
    class Meta:
        model = Donor

class DonorMedicalHistoryType(DjangoObjectType):
    class Meta:
        model = DonorMedicalHistory

class DonationTypeType(DjangoObjectType):
    class Meta:
        model = DonationType

class DonationAppointmentType(DjangoObjectType):
    class Meta:
        model = DonationAppointment

class SampleTypeType(DjangoObjectType):
    class Meta:
        model = SampleType

class SampleType(DjangoObjectType):
    class Meta:
        model = Sample

class StorageUnitType(DjangoObjectType):
    class Meta:
        model = StorageUnit

class StorageLocationType(DjangoObjectType):
    class Meta:
        model = StorageLocation

class ChainOfCustodyLogType(DjangoObjectType):
    class Meta:
        model = ChainOfCustodyLog

class Query(graphene.ObjectType):
    donors = graphene.List(DonorType)
    donor = graphene.Field(DonorType, id=graphene.ID(required=True))
    
    donor_medical_histories = graphene.List(DonorMedicalHistoryType, donor_id=graphene.ID())
    donor_medical_history = graphene.Field(DonorMedicalHistoryType, id=graphene.ID(required=True))
    
    donation_types = graphene.List(DonationTypeType)
    donation_type = graphene.Field(DonationTypeType, id=graphene.ID(required=True))
    
    donation_appointments = graphene.List(
        DonationAppointmentType, 
        donor_id=graphene.ID(),
        status=graphene.String()
    )
    donation_appointment = graphene.Field(DonationAppointmentType, id=graphene.ID(required=True))
    
    sample_types = graphene.List(SampleTypeType)
    sample_type = graphene.Field(SampleTypeType, id=graphene.ID(required=True))
    
    samples = graphene.List(
        SampleType, 
        donor_id=graphene.ID(),
        sample_type_id=graphene.ID(),
        status=graphene.String()
    )
    sample = graphene.Field(SampleType, id=graphene.ID(required=True))
    
    storage_units = graphene.List(StorageUnitType)
    storage_unit = graphene.Field(StorageUnitType, id=graphene.ID(required=True))
    
    storage_locations = graphene.List(
        StorageLocationType,
        storage_unit_id=graphene.ID()
    )
    storage_location = graphene.Field(StorageLocationType, id=graphene.ID(required=True))
    
    chain_of_custodies = graphene.List(
        ChainOfCustodyLogType,
        sample_id=graphene.ID()
    )
    chain_of_custody = graphene.Field(ChainOfCustodyLogType, id=graphene.ID(required=True))
    
    def resolve_donors(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view donors')
        
        user = info.context.user
        
        if user.is_superuser or user.is_staff or user.is_recruiter:
            return Donor.objects.all()
        
        if user.is_researcher:
            donors_with_samples = Donor.objects.filter(
                sample__status='AVAILABLE'
            ).distinct()
            return donors_with_samples
        
        if user.is_donor:
            try:
                return [Donor.objects.get(user=user)]
            except Donor.DoesNotExist:
                return []
        
        raise GraphQLError('You do not have permission to view donors')
    
    def resolve_donor(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view donor details')
        
        try:
            donor = Donor.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff or user.is_recruiter:
                return donor
            
            if user.is_researcher and donor.sample_set.filter(status='AVAILABLE').exists():
                return donor
            
            if user.is_donor and donor.user == user:
                return donor
            
            raise GraphQLError('You do not have permission to view this donor')
        except Donor.DoesNotExist:
            raise GraphQLError('Donor not found')
    
    def resolve_donor_medical_histories(self, info, donor_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view donor medical histories')
        
        user = info.context.user
        
        query = DonorMedicalHistory.objects.all()
        
        if donor_id:
            query = query.filter(donor_id=donor_id)
        
        if user.is_superuser or user.is_staff:
            return query
        
        if user.is_recruiter:
            return query
        
        if user.is_donor:
            try:
                donor = Donor.objects.get(user=user)
                return query.filter(donor=donor)
            except Donor.DoesNotExist:
                return []
        
        raise GraphQLError('You do not have permission to view donor medical histories')
    
    def resolve_donor_medical_history(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view donor medical history details')
        
        try:
            medical_history = DonorMedicalHistory.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff or user.is_recruiter:
                return medical_history
            
            if user.is_donor and medical_history.donor.user == user:
                return medical_history
            
            raise GraphQLError('You do not have permission to view this donor medical history')
        except DonorMedicalHistory.DoesNotExist:
            raise GraphQLError('Donor medical history not found')
    
    def resolve_samples(self, info, donor_id=None, sample_type_id=None, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view samples')
        
        user = info.context.user
        
        query = Sample.objects.all()
        
        if donor_id:
            query = query.filter(donor_id=donor_id)
        if sample_type_id:
            query = query.filter(sample_type_id=sample_type_id)
        if status:
            query = query.filter(status=status)
        
        if user.is_superuser or user.is_staff:
            return query
        
        if user.is_researcher:
            return query.filter(status='AVAILABLE')
        
        if user.is_donor:
            try:
                donor = Donor.objects.get(user=user)
                return query.filter(donor=donor)
            except Donor.DoesNotExist:
                return []
        
        raise GraphQLError('You do not have permission to view samples')
    
    def resolve_sample(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view sample details')
        
        try:
            sample = Sample.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return sample
            
            if user.is_researcher and sample.status == 'AVAILABLE':
                return sample
            
            if user.is_donor and sample.donor.user == user:
                return sample
            
            raise GraphQLError('You do not have permission to view this sample')
        except Sample.DoesNotExist:
            raise GraphQLError('Sample not found')

class DonorInput(graphene.InputObjectType):
    user_id = graphene.ID(required=True)
    donor_id = graphene.String(required=True)
    blood_type = graphene.String()
    height_cm = graphene.Float()
    weight_kg = graphene.Float()
    is_active = graphene.Boolean()
    eligibility_status = graphene.String()
    eligibility_notes = graphene.String()
    last_physical_date = graphene.Date()
    last_donation_date = graphene.Date()

class DonationAppointmentInput(graphene.InputObjectType):
    donor_id = graphene.ID(required=True)
    donation_type_id = graphene.ID(required=True)
    appointment_date = graphene.DateTime(required=True)
    status = graphene.String()
    notes = graphene.String()
    collected_by_id = graphene.ID()

class SampleInput(graphene.InputObjectType):
    donor_id = graphene.ID(required=True)
    donation_appointment_id = graphene.ID()
    sample_type_id = graphene.ID(required=True)
    sample_id = graphene.String(required=True)
    collection_date = graphene.DateTime(required=True)
    volume_ml = graphene.Float(required=True)
    status = graphene.String()
    storage_location_id = graphene.ID()
    expiration_date = graphene.Date()
    notes = graphene.String()

class CreateDonor(graphene.Mutation):
    class Arguments:
        input = DonorInput(required=True)
    
    donor = graphene.Field(DonorType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a donor')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create donors')
        
        try:
            donor_user = User.objects.get(pk=input.user_id)
        except User.DoesNotExist:
            raise GraphQLError('User not found')
        
        if Donor.objects.filter(user=donor_user).exists():
            raise GraphQLError('Donor already exists for this user')
        
        donor = Donor.objects.create(
            user=donor_user,
            donor_id=input.donor_id,
            blood_type=getattr(input, 'blood_type', None),
            height_cm=getattr(input, 'height_cm', None),
            weight_kg=getattr(input, 'weight_kg', None),
            is_active=getattr(input, 'is_active', True),
            eligibility_status=getattr(input, 'eligibility_status', 'PENDING'),
            eligibility_notes=getattr(input, 'eligibility_notes', None),
            last_physical_date=getattr(input, 'last_physical_date', None),
            last_donation_date=getattr(input, 'last_donation_date', None)
        )
        
        return CreateDonor(donor=donor)

class CreateDonationAppointment(graphene.Mutation):
    class Arguments:
        input = DonationAppointmentInput(required=True)
    
    donation_appointment = graphene.Field(DonationAppointmentType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a donation appointment')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            if user.is_donor:
                try:
                    donor = Donor.objects.get(user=user)
                    if str(donor.id) != input.donor_id:
                        raise GraphQLError('You can only create appointments for yourself')
                except Donor.DoesNotExist:
                    raise GraphQLError('Donor profile not found for your user account')
            else:
                raise GraphQLError('You do not have permission to create donation appointments')
        
        try:
            donor = Donor.objects.get(pk=input.donor_id)
        except Donor.DoesNotExist:
            raise GraphQLError('Donor not found')
        
        try:
            donation_type = DonationType.objects.get(pk=input.donation_type_id)
        except DonationType.DoesNotExist:
            raise GraphQLError('Donation type not found')
        
        collected_by = None
        if hasattr(input, 'collected_by_id') and input.collected_by_id:
            try:
                collected_by = User.objects.get(pk=input.collected_by_id)
            except User.DoesNotExist:
                raise GraphQLError('Collected by user not found')
        
        appointment = DonationAppointment.objects.create(
            donor=donor,
            donation_type=donation_type,
            appointment_date=input.appointment_date,
            status=getattr(input, 'status', 'SCHEDULED'),
            notes=getattr(input, 'notes', None),
            collected_by=collected_by
        )
        
        return CreateDonationAppointment(donation_appointment=appointment)

class CreateSample(graphene.Mutation):
    class Arguments:
        input = SampleInput(required=True)
    
    sample = graphene.Field(SampleType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a sample')
        
        user = info.context.user
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create samples')
        
        try:
            donor = Donor.objects.get(pk=input.donor_id)
        except Donor.DoesNotExist:
            raise GraphQLError('Donor not found')
        
        try:
            sample_type = SampleType.objects.get(pk=input.sample_type_id)
        except SampleType.DoesNotExist:
            raise GraphQLError('Sample type not found')
        
        donation_appointment = None
        if hasattr(input, 'donation_appointment_id') and input.donation_appointment_id:
            try:
                donation_appointment = DonationAppointment.objects.get(pk=input.donation_appointment_id)
                if donation_appointment.donor != donor:
                    raise GraphQLError('Donation appointment does not belong to this donor')
            except DonationAppointment.DoesNotExist:
                raise GraphQLError('Donation appointment not found')
        
        storage_location = None
        if hasattr(input, 'storage_location_id') and input.storage_location_id:
            try:
                storage_location = StorageLocation.objects.get(pk=input.storage_location_id)
            except StorageLocation.DoesNotExist:
                raise GraphQLError('Storage location not found')
        
        sample = Sample.objects.create(
            donor=donor,
            donation_appointment=donation_appointment,
            sample_type=sample_type,
            sample_id=input.sample_id,
            collection_date=input.collection_date,
            volume_ml=input.volume_ml,
            status=getattr(input, 'status', 'COLLECTED'),
            storage_location=storage_location,
            expiration_date=getattr(input, 'expiration_date', None),
            notes=getattr(input, 'notes', None)
        )
        
        ChainOfCustodyLog.objects.create(
            sample=sample,
            action='collected',
            performed_by=user,
            timestamp=input.collection_date,
            notes=f"Initial collection of sample {sample.sample_id}"
        )
        
        return CreateSample(sample=sample)

class Mutation(graphene.ObjectType):
    create_donor = CreateDonor.Field()
    create_donation_appointment = CreateDonationAppointment.Field()
    create_sample = CreateSample.Field()
