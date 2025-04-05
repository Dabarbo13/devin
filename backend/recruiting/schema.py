import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import (
    Prospect, DemographicInfo, ContactLog, StudyQualification,
    SocialMediaCampaign, CampaignMetrics, Referral
)

User = get_user_model()

class ProspectType(DjangoObjectType):
    class Meta:
        model = Prospect

class DemographicInfoType(DjangoObjectType):
    class Meta:
        model = DemographicInfo

class ContactLogType(DjangoObjectType):
    class Meta:
        model = ContactLog

class StudyQualificationType(DjangoObjectType):
    class Meta:
        model = StudyQualification

class SocialMediaCampaignType(DjangoObjectType):
    class Meta:
        model = SocialMediaCampaign

class CampaignMetricsType(DjangoObjectType):
    class Meta:
        model = CampaignMetrics

class ReferralType(DjangoObjectType):
    class Meta:
        model = Referral

class Query(graphene.ObjectType):
    prospects = graphene.List(
        ProspectType,
        status=graphene.String(),
        source=graphene.String()
    )
    prospect = graphene.Field(ProspectType, id=graphene.ID(required=True))
    
    demographic_infos = graphene.List(
        DemographicInfoType,
        prospect_id=graphene.ID()
    )
    demographic_info = graphene.Field(DemographicInfoType, id=graphene.ID(required=True))
    
    contact_logs = graphene.List(
        ContactLogType,
        prospect_id=graphene.ID(),
        contact_type=graphene.String()
    )
    contact_log = graphene.Field(ContactLogType, id=graphene.ID(required=True))
    
    study_qualifications = graphene.List(
        StudyQualificationType,
        prospect_id=graphene.ID(),
        study_id=graphene.ID(),
        status=graphene.String()
    )
    study_qualification = graphene.Field(StudyQualificationType, id=graphene.ID(required=True))
    
    social_media_campaigns = graphene.List(
        SocialMediaCampaignType,
        status=graphene.String(),
        platform=graphene.String()
    )
    social_media_campaign = graphene.Field(SocialMediaCampaignType, id=graphene.ID(required=True))
    
    campaign_metrics = graphene.List(
        CampaignMetricsType,
        campaign_id=graphene.ID()
    )
    campaign_metric = graphene.Field(CampaignMetricsType, id=graphene.ID(required=True))
    
    referrals = graphene.List(
        ReferralType,
        referrer_id=graphene.ID(),
        status=graphene.String()
    )
    referral = graphene.Field(ReferralType, id=graphene.ID(required=True))
    
    def resolve_prospects(self, info, status=None, source=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view prospects')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view prospects')
        
        query = Prospect.objects.all()
        
        if status:
            query = query.filter(status=status)
        if source:
            query = query.filter(source=source)
        
        return query
    
    def resolve_prospect(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view prospect details')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view prospect details')
        
        try:
            return Prospect.objects.get(pk=id)
        except Prospect.DoesNotExist:
            raise GraphQLError('Prospect not found')
    
    def resolve_demographic_infos(self, info, prospect_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view demographic information')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view demographic information')
        
        query = DemographicInfo.objects.all()
        
        if prospect_id:
            query = query.filter(prospect_id=prospect_id)
        
        return query
    
    def resolve_demographic_info(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view demographic information details')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view demographic information details')
        
        try:
            return DemographicInfo.objects.get(pk=id)
        except DemographicInfo.DoesNotExist:
            raise GraphQLError('Demographic information not found')
    
    def resolve_social_media_campaigns(self, info, status=None, platform=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view social media campaigns')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view social media campaigns')
        
        query = SocialMediaCampaign.objects.all()
        
        if status:
            query = query.filter(status=status)
        if platform:
            query = query.filter(platform=platform)
        
        return query
    
    def resolve_social_media_campaign(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view social media campaign details')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view social media campaign details')
        
        try:
            return SocialMediaCampaign.objects.get(pk=id)
        except SocialMediaCampaign.DoesNotExist:
            raise GraphQLError('Social media campaign not found')
    
    def resolve_referrals(self, info, referrer_id=None, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view referrals')
        
        user = info.context.user
        
        query = Referral.objects.all()
        
        if referrer_id:
            query = query.filter(referrer_id=referrer_id)
        if status:
            query = query.filter(status=status)
        
        if user.is_superuser or user.is_staff or user.is_recruiter:
            return query
        
        if user.is_donor:
            return query.filter(referrer__user=user)
        
        raise GraphQLError('You do not have permission to view referrals')
    
    def resolve_referral(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view referral details')
        
        try:
            referral = Referral.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff or user.is_recruiter:
                return referral
            
            if user.is_donor and referral.referrer.user == user:
                return referral
            
            raise GraphQLError('You do not have permission to view this referral')
        except Referral.DoesNotExist:
            raise GraphQLError('Referral not found')

class ProspectInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()
    status = graphene.String()
    source = graphene.String()
    notes = graphene.String()

class DemographicInfoInput(graphene.InputObjectType):
    prospect_id = graphene.ID(required=True)
    age = graphene.Int()
    gender = graphene.String()
    ethnicity = graphene.String()
    race = graphene.String()
    height_cm = graphene.Float()
    weight_kg = graphene.Float()
    bmi = graphene.Float()
    blood_type = graphene.String()
    medical_conditions = graphene.String()
    medications = graphene.String()
    smoking_status = graphene.String()
    alcohol_consumption = graphene.String()

class ProspectContactInput(graphene.InputObjectType):
    prospect_id = graphene.ID(required=True)
    contact_date = graphene.DateTime(required=True)
    contact_type = graphene.String(required=True)
    contact_method = graphene.String(required=True)
    contact_by_id = graphene.ID(required=True)
    notes = graphene.String()
    outcome = graphene.String()
    follow_up_date = graphene.DateTime()

class CampaignInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    campaign_type = graphene.String(required=True)
    start_date = graphene.Date(required=True)
    end_date = graphene.Date()
    target_audience = graphene.String()
    budget = graphene.Float()
    status = graphene.String()
    created_by_id = graphene.ID(required=True)

class CreateProspect(graphene.Mutation):
    class Arguments:
        input = ProspectInput(required=True)
    
    prospect = graphene.Field(ProspectType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a prospect')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create prospects')
        
        if Prospect.objects.filter(email=input.email).exists():
            raise GraphQLError('A prospect with this email already exists')
        
        prospect = Prospect.objects.create(
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            phone=getattr(input, 'phone', None),
            status=getattr(input, 'status', 'NEW'),
            source=getattr(input, 'source', 'DIRECT'),
            notes=getattr(input, 'notes', None)
        )
        
        return CreateProspect(prospect=prospect)

class CreateDemographicInfo(graphene.Mutation):
    class Arguments:
        input = DemographicInfoInput(required=True)
    
    demographic_info = graphene.Field(DemographicInfoType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create demographic information')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create demographic information')
        
        try:
            prospect = Prospect.objects.get(pk=input.prospect_id)
        except Prospect.DoesNotExist:
            raise GraphQLError('Prospect not found')
        
        if DemographicInfo.objects.filter(prospect=prospect).exists():
            raise GraphQLError('Demographics already exist for this prospect')
        
        demographic = DemographicInfo.objects.create(
            prospect=prospect,
            gender=getattr(input, 'gender', None),
            ethnicity=getattr(input, 'ethnicity', None),
            race=getattr(input, 'race', None),
            height_cm=getattr(input, 'height_cm', None),
            weight_kg=getattr(input, 'weight_kg', None),
            blood_type=getattr(input, 'blood_type', None)
        )
        
        return CreateDemographicInfo(demographic_info=demographic)

class CreateContactLog(graphene.Mutation):
    class Arguments:
        input = ProspectContactInput(required=True)
    
    contact_log = graphene.Field(ContactLogType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create contact logs')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create contact logs')
        
        try:
            prospect = Prospect.objects.get(pk=input.prospect_id)
        except Prospect.DoesNotExist:
            raise GraphQLError('Prospect not found')
        
        try:
            contact_by = User.objects.get(pk=input.contact_by_id)
        except User.DoesNotExist:
            raise GraphQLError('Contact by user not found')
        
        contact = ContactLog.objects.create(
            prospect=prospect,
            contact_date=input.contact_date,
            contact_type=input.contact_type,
            direction=getattr(input, 'contact_method', 'outbound'),
            contacted_by=contact_by,
            notes=getattr(input, 'notes', None),
            outcome=getattr(input, 'outcome', None),
            follow_up_date=getattr(input, 'follow_up_date', None)
        )
        
        return CreateContactLog(contact_log=contact)

class CreateSocialMediaCampaign(graphene.Mutation):
    class Arguments:
        input = CampaignInput(required=True)
    
    social_media_campaign = graphene.Field(SocialMediaCampaignType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create social media campaigns')
        
        user = info.context.user
        
        if not (user.is_recruiter or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create social media campaigns')
        
        try:
            created_by = User.objects.get(pk=input.created_by_id)
        except User.DoesNotExist:
            raise GraphQLError('Created by user not found')
        
        campaign = SocialMediaCampaign.objects.create(
            name=input.name,
            description=getattr(input, 'description', None),
            platform=input.campaign_type,
            start_date=input.start_date,
            end_date=getattr(input, 'end_date', None),
            target_audience=getattr(input, 'target_audience', None),
            budget=getattr(input, 'budget', None),
            status=getattr(input, 'status', 'DRAFT'),
            created_by=created_by
        )
        
        return CreateSocialMediaCampaign(social_media_campaign=campaign)

class Mutation(graphene.ObjectType):
    create_prospect = CreateProspect.Field()
    create_demographic_info = CreateDemographicInfo.Field()
    create_contact_log = CreateContactLog.Field()
    create_social_media_campaign = CreateSocialMediaCampaign.Field()
