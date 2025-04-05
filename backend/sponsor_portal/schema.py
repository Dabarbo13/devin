import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import (
    SponsorProfile, ResearcherProfile, ProtocolDraft, ProtocolReview,
    RecruitmentMetrics, CustomSampleRequest, SampleOrder, Dashboard
)

User = get_user_model()

class SponsorProfileType(DjangoObjectType):
    class Meta:
        model = SponsorProfile

class ResearcherProfileType(DjangoObjectType):
    class Meta:
        model = ResearcherProfile

class ProtocolDraftType(DjangoObjectType):
    class Meta:
        model = ProtocolDraft

class ProtocolReviewType(DjangoObjectType):
    class Meta:
        model = ProtocolReview

class RecruitmentMetricsType(DjangoObjectType):
    class Meta:
        model = RecruitmentMetrics

class CustomSampleRequestType(DjangoObjectType):
    class Meta:
        model = CustomSampleRequest

class SampleOrderType(DjangoObjectType):
    class Meta:
        model = SampleOrder

class DashboardType(DjangoObjectType):
    class Meta:
        model = Dashboard

class Query(graphene.ObjectType):
    sponsor_profiles = graphene.List(SponsorProfileType)
    sponsor_profile = graphene.Field(SponsorProfileType, id=graphene.ID(required=True))
    my_sponsor_profile = graphene.Field(SponsorProfileType)
    
    researcher_profiles = graphene.List(ResearcherProfileType)
    researcher_profile = graphene.Field(ResearcherProfileType, id=graphene.ID(required=True))
    my_researcher_profile = graphene.Field(ResearcherProfileType)
    
    protocol_drafts = graphene.List(
        ProtocolDraftType,
        sponsor_id=graphene.ID(),
        status=graphene.String()
    )
    protocol_draft = graphene.Field(ProtocolDraftType, id=graphene.ID(required=True))
    
    protocol_reviews = graphene.List(
        ProtocolReviewType,
        protocol_draft_id=graphene.ID(),
        reviewer_id=graphene.ID(),
        decision=graphene.String()
    )
    protocol_review = graphene.Field(ProtocolReviewType, id=graphene.ID(required=True))
    
    recruitment_metrics = graphene.List(
        RecruitmentMetricsType,
        study_id=graphene.ID(),
        site_id=graphene.ID(),
        date_from=graphene.Date(),
        date_to=graphene.Date()
    )
    recruitment_metric = graphene.Field(RecruitmentMetricsType, id=graphene.ID(required=True))
    
    custom_sample_requests = graphene.List(
        CustomSampleRequestType,
        researcher_id=graphene.ID(),
        status=graphene.String()
    )
    custom_sample_request = graphene.Field(CustomSampleRequestType, id=graphene.ID(required=True))
    
    sample_orders = graphene.List(
        SampleOrderType,
        researcher_id=graphene.ID(),
        custom_request_id=graphene.ID(),
        status=graphene.String()
    )
    sample_order = graphene.Field(SampleOrderType, id=graphene.ID(required=True))
    
    dashboards = graphene.List(
        DashboardType,
        user_id=graphene.ID(),
        dashboard_type=graphene.String()
    )
    dashboard = graphene.Field(DashboardType, id=graphene.ID(required=True))
    my_dashboards = graphene.List(DashboardType, dashboard_type=graphene.String())
    
    def resolve_sponsor_profiles(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view sponsor profiles')
        
        user = info.context.user
        
        if user.is_superuser or user.is_staff:
            return SponsorProfile.objects.all()
        
        return SponsorProfile.objects.filter(user__is_active=True)
    
    def resolve_sponsor_profile(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view sponsor profile details')
        
        try:
            profile = SponsorProfile.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return profile
            
            if user.is_sponsor and profile.user == user:
                return profile
            
            if profile.user.is_active:
                return profile
            
            raise GraphQLError('You do not have permission to view this sponsor profile')
        except SponsorProfile.DoesNotExist:
            raise GraphQLError('Sponsor profile not found')
    
    def resolve_my_sponsor_profile(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your sponsor profile')
        
        user = info.context.user
        
        if not user.is_sponsor:
            raise GraphQLError('You do not have a sponsor profile')
        
        try:
            return SponsorProfile.objects.get(user=user)
        except SponsorProfile.DoesNotExist:
            raise GraphQLError('Sponsor profile not found')
    
    def resolve_researcher_profiles(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view researcher profiles')
        
        user = info.context.user
        
        if user.is_superuser or user.is_staff:
            return ResearcherProfile.objects.all()
        
        return ResearcherProfile.objects.filter(user__is_active=True)
    
    def resolve_researcher_profile(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view researcher profile details')
        
        try:
            profile = ResearcherProfile.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return profile
            
            if user.is_researcher and profile.user == user:
                return profile
            
            if profile.user.is_active:
                return profile
            
            raise GraphQLError('You do not have permission to view this researcher profile')
        except ResearcherProfile.DoesNotExist:
            raise GraphQLError('Researcher profile not found')
    
    def resolve_my_researcher_profile(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your researcher profile')
        
        user = info.context.user
        
        if not user.is_researcher:
            raise GraphQLError('You do not have a researcher profile')
        
        try:
            return ResearcherProfile.objects.get(user=user)
        except ResearcherProfile.DoesNotExist:
            raise GraphQLError('Researcher profile not found')
    
    def resolve_protocol_drafts(self, info, sponsor_id=None, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view protocol drafts')
        
        user = info.context.user
        
        query = ProtocolDraft.objects.all()
        
        if sponsor_id:
            query = query.filter(sponsor_id=sponsor_id)
        if status:
            query = query.filter(status=status)
        
        if user.is_superuser or user.is_staff:
            return query
        
        if user.is_sponsor:
            return query.filter(sponsor=user)
        
        if user.is_researcher:
            reviewed_drafts = query.filter(protocolreview__reviewer=user)
            return reviewed_drafts
        
        raise GraphQLError('You do not have permission to view protocol drafts')
    
    def resolve_protocol_draft(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view protocol draft details')
        
        try:
            draft = ProtocolDraft.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return draft
            
            if user.is_sponsor and draft.sponsor == user:
                return draft
            
            if user.is_researcher and draft.protocolreview_set.filter(reviewer=user).exists():
                return draft
            
            raise GraphQLError('You do not have permission to view this protocol draft')
        except ProtocolDraft.DoesNotExist:
            raise GraphQLError('Protocol draft not found')
    
    def resolve_custom_sample_requests(self, info, researcher_id=None, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view custom sample requests')
        
        user = info.context.user
        
        query = CustomSampleRequest.objects.all()
        
        if researcher_id:
            query = query.filter(researcher_id=researcher_id)
        if status:
            query = query.filter(status=status)
        
        if user.is_superuser or user.is_staff:
            return query
        
        if user.is_researcher:
            return query.filter(researcher=user)
        
        raise GraphQLError('You do not have permission to view custom sample requests')
    
    def resolve_custom_sample_request(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view custom sample request details')
        
        try:
            request = CustomSampleRequest.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return request
            
            if user.is_researcher and request.researcher == user:
                return request
            
            raise GraphQLError('You do not have permission to view this custom sample request')
        except CustomSampleRequest.DoesNotExist:
            raise GraphQLError('Custom sample request not found')
    
    def resolve_dashboards(self, info, user_id=None, dashboard_type=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view dashboards')
        
        user = info.context.user
        
        query = Dashboard.objects.all()
        
        if user_id:
            query = query.filter(user_id=user_id)
        if dashboard_type:
            query = query.filter(dashboard_type=dashboard_type)
        
        if user.is_superuser or user.is_staff:
            return query
        
        return query.filter(user=user)
    
    def resolve_dashboard(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view dashboard details')
        
        try:
            dashboard = Dashboard.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return dashboard
            
            if dashboard.user == user:
                return dashboard
            
            raise GraphQLError('You do not have permission to view this dashboard')
        except Dashboard.DoesNotExist:
            raise GraphQLError('Dashboard not found')
    
    def resolve_my_dashboards(self, info, dashboard_type=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your dashboards')
        
        user = info.context.user
        
        query = Dashboard.objects.filter(user=user)
        
        if dashboard_type:
            query = query.filter(dashboard_type=dashboard_type)
        
        return query

class SponsorProfileInput(graphene.InputObjectType):
    company_name = graphene.String(required=True)
    company_address = graphene.String()
    company_website = graphene.String()
    contact_phone = graphene.String()
    department = graphene.String()
    position = graphene.String()

class ResearcherProfileInput(graphene.InputObjectType):
    institution_name = graphene.String(required=True)
    institution_address = graphene.String()
    institution_website = graphene.String()
    department = graphene.String()
    position = graphene.String()
    research_interests = graphene.String()

class ProtocolDraftInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()
    status = graphene.String()
    version = graphene.String()
    notes = graphene.String()

class CustomSampleRequestInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    sample_type_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    donor_criteria = graphene.String()
    target_date = graphene.Date()
    status = graphene.String()

class DashboardInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    dashboard_type = graphene.String(required=True)
    is_default = graphene.Boolean()
    layout = graphene.String()

class CreateSponsorProfile(graphene.Mutation):
    class Arguments:
        input = SponsorProfileInput(required=True)
    
    sponsor_profile = graphene.Field(SponsorProfileType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a sponsor profile')
        
        user = info.context.user
        
        if not user.is_sponsor:
            raise GraphQLError('You must be a sponsor to create a sponsor profile')
        
        if SponsorProfile.objects.filter(user=user).exists():
            raise GraphQLError('Sponsor profile already exists for this user')
        
        profile = SponsorProfile.objects.create(
            user=user,
            company_name=input.company_name,
            company_address=getattr(input, 'company_address', None),
            company_website=getattr(input, 'company_website', None),
            contact_phone=getattr(input, 'contact_phone', None),
            department=getattr(input, 'department', None),
            position=getattr(input, 'position', None)
        )
        
        return CreateSponsorProfile(sponsor_profile=profile)

class CreateResearcherProfile(graphene.Mutation):
    class Arguments:
        input = ResearcherProfileInput(required=True)
    
    researcher_profile = graphene.Field(ResearcherProfileType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a researcher profile')
        
        user = info.context.user
        
        if not user.is_researcher:
            raise GraphQLError('You must be a researcher to create a researcher profile')
        
        if ResearcherProfile.objects.filter(user=user).exists():
            raise GraphQLError('Researcher profile already exists for this user')
        
        profile = ResearcherProfile.objects.create(
            user=user,
            institution_name=input.institution_name,
            institution_address=getattr(input, 'institution_address', None),
            institution_website=getattr(input, 'institution_website', None),
            department=getattr(input, 'department', None),
            position=getattr(input, 'position', None),
            research_interests=getattr(input, 'research_interests', None)
        )
        
        return CreateResearcherProfile(researcher_profile=profile)

class CreateProtocolDraft(graphene.Mutation):
    class Arguments:
        input = ProtocolDraftInput(required=True)
    
    protocol_draft = graphene.Field(ProtocolDraftType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a protocol draft')
        
        user = info.context.user
        
        if not user.is_sponsor:
            raise GraphQLError('You must be a sponsor to create a protocol draft')
        
        draft = ProtocolDraft.objects.create(
            sponsor=user,
            title=input.title,
            description=getattr(input, 'description', None),
            status=getattr(input, 'status', 'DRAFT'),
            version=getattr(input, 'version', '1.0'),
            notes=getattr(input, 'notes', None)
        )
        
        return CreateProtocolDraft(protocol_draft=draft)

class CreateCustomSampleRequest(graphene.Mutation):
    class Arguments:
        input = CustomSampleRequestInput(required=True)
    
    custom_sample_request = graphene.Field(CustomSampleRequestType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a custom sample request')
        
        user = info.context.user
        
        if not user.is_researcher:
            raise GraphQLError('You must be a researcher to create a custom sample request')
        
        from donation_management.models import SampleType
        try:
            sample_type = SampleType.objects.get(pk=input.sample_type_id)
        except SampleType.DoesNotExist:
            raise GraphQLError('Sample type not found')
        
        request = CustomSampleRequest.objects.create(
            researcher=user,
            title=input.title,
            description=input.description,
            sample_type=sample_type,
            quantity=input.quantity,
            donor_criteria=getattr(input, 'donor_criteria', None),
            target_date=getattr(input, 'target_date', None),
            status=getattr(input, 'status', 'PENDING')
        )
        
        return CreateCustomSampleRequest(custom_sample_request=request)

class CreateDashboard(graphene.Mutation):
    class Arguments:
        input = DashboardInput(required=True)
    
    dashboard = graphene.Field(DashboardType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a dashboard')
        
        user = info.context.user
        
        dashboard = Dashboard.objects.create(
            user=user,
            name=input.name,
            description=getattr(input, 'description', None),
            dashboard_type=input.dashboard_type,
            is_default=getattr(input, 'is_default', False),
            layout=getattr(input, 'layout', '{}')
        )
        
        if dashboard.is_default:
            Dashboard.objects.filter(
                user=user,
                dashboard_type=dashboard.dashboard_type,
                is_default=True
            ).exclude(pk=dashboard.pk).update(is_default=False)
        
        return CreateDashboard(dashboard=dashboard)

class Mutation(graphene.ObjectType):
    create_sponsor_profile = CreateSponsorProfile.Field()
    create_researcher_profile = CreateResearcherProfile.Field()
    create_protocol_draft = CreateProtocolDraft.Field()
    create_custom_sample_request = CreateCustomSampleRequest.Field()
    create_dashboard = CreateDashboard.Field()
