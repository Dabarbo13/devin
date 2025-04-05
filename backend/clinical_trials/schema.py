import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import Study, StudyPhase, StudyArm, VisitTemplate, Visit, StudyDocument, ProtocolVersion, Participant, ParticipantEligibility, AdverseEvent, ProtocolDeviation, SiteActivityLog

User = get_user_model()

class StudyType(DjangoObjectType):
    class Meta:
        model = Study

class StudyPhaseType(DjangoObjectType):
    class Meta:
        model = StudyPhase

class StudyArmType(DjangoObjectType):
    class Meta:
        model = StudyArm

class VisitTemplateType(DjangoObjectType):
    class Meta:
        model = VisitTemplate

class StudyDocumentType(DjangoObjectType):
    class Meta:
        model = StudyDocument

class ProtocolVersionType(DjangoObjectType):
    class Meta:
        model = ProtocolVersion

class ParticipantType(DjangoObjectType):
    class Meta:
        model = Participant

class VisitType(DjangoObjectType):
    class Meta:
        model = Visit

class AdverseEventType(DjangoObjectType):
    class Meta:
        model = AdverseEvent

class ProtocolDeviationType(DjangoObjectType):
    class Meta:
        model = ProtocolDeviation

class Query(graphene.ObjectType):
    studies = graphene.List(StudyType)
    study = graphene.Field(StudyType, id=graphene.ID(required=True))
    
    study_phases = graphene.List(StudyPhaseType, study_id=graphene.ID())
    study_phase = graphene.Field(StudyPhaseType, id=graphene.ID(required=True))
    
    study_arms = graphene.List(StudyArmType, study_id=graphene.ID())
    study_arm = graphene.Field(StudyArmType, id=graphene.ID(required=True))
    
    visit_templates = graphene.List(VisitTemplateType, study_id=graphene.ID(), arm_id=graphene.ID())
    visit_template = graphene.Field(VisitTemplateType, id=graphene.ID(required=True))
    
    def resolve_visit_templates(self, info, study_id=None, arm_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view visit templates')
        
        queryset = VisitTemplate.objects.all()
        
        if study_id:
            queryset = queryset.filter(study_id=study_id)
        
        if arm_id:
            queryset = queryset.filter(study_arm_id=arm_id)
        
        return queryset
    
    def resolve_visit_template(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view visit template details')
        
        try:
            template = VisitTemplate.objects.get(pk=id)
            return template
        except VisitTemplate.DoesNotExist:
            raise GraphQLError('Visit template not found')
    
    study_documents = graphene.List(StudyDocumentType, study_id=graphene.ID())
    study_document = graphene.Field(StudyDocumentType, id=graphene.ID(required=True))
    
    protocol_versions = graphene.List(ProtocolVersionType, study_id=graphene.ID())
    protocol_version = graphene.Field(ProtocolVersionType, id=graphene.ID(required=True))
    
    def resolve_study_documents(self, info, study_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study documents')
        
        queryset = StudyDocument.objects.all()
        
        if study_id:
            queryset = queryset.filter(study_id=study_id)
        
        return queryset
    
    def resolve_study_document(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study document details')
        
        try:
            document = StudyDocument.objects.get(pk=id)
            return document
        except StudyDocument.DoesNotExist:
            raise GraphQLError('Study document not found')
    
    def resolve_protocol_versions(self, info, study_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view protocol versions')
        
        queryset = ProtocolVersion.objects.all()
        
        if study_id:
            queryset = queryset.filter(study_id=study_id)
        
        return queryset
    
    def resolve_protocol_version(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view protocol version details')
        
        try:
            version = ProtocolVersion.objects.get(pk=id)
            return version
        except ProtocolVersion.DoesNotExist:
            raise GraphQLError('Protocol version not found')
    
    participants = graphene.List(ParticipantType, study_id=graphene.ID())
    participant = graphene.Field(ParticipantType, id=graphene.ID(required=True))
    
    visits = graphene.List(VisitType, participant_id=graphene.ID())
    visit = graphene.Field(VisitType, id=graphene.ID(required=True))
    
    adverse_events = graphene.List(AdverseEventType, participant_id=graphene.ID())
    adverse_event = graphene.Field(AdverseEventType, id=graphene.ID(required=True))
    
    protocol_deviations = graphene.List(ProtocolDeviationType, study_id=graphene.ID(), participant_id=graphene.ID())
    protocol_deviation = graphene.Field(ProtocolDeviationType, id=graphene.ID(required=True))
    
    def resolve_visits(self, info, participant_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view visits')
        
        queryset = Visit.objects.all()
        
        if participant_id:
            queryset = queryset.filter(participant_id=participant_id)
        
        return queryset
    
    def resolve_visit(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view visit details')
        
        try:
            visit = Visit.objects.get(pk=id)
            return visit
        except Visit.DoesNotExist:
            raise GraphQLError('Visit not found')
    
    def resolve_adverse_events(self, info, participant_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view adverse events')
        
        queryset = AdverseEvent.objects.all()
        
        if participant_id:
            queryset = queryset.filter(participant_id=participant_id)
        
        return queryset
    
    def resolve_adverse_event(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view adverse event details')
        
        try:
            event = AdverseEvent.objects.get(pk=id)
            return event
        except AdverseEvent.DoesNotExist:
            raise GraphQLError('Adverse event not found')
    
    def resolve_protocol_deviations(self, info, study_id=None, participant_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view protocol deviations')
        
        queryset = ProtocolDeviation.objects.all()
        
        if study_id:
            queryset = queryset.filter(study_id=study_id)
        
        if participant_id:
            queryset = queryset.filter(participant_id=participant_id)
        
        return queryset
    
    def resolve_protocol_deviation(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view protocol deviation details')
        
        try:
            deviation = ProtocolDeviation.objects.get(pk=id)
            return deviation
        except ProtocolDeviation.DoesNotExist:
            raise GraphQLError('Protocol deviation not found')
    
    def resolve_studies(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view studies')
        
        user = info.context.user
        
        if user.is_superuser or user.is_staff:
            return Study.objects.all()
        
        if user.is_sponsor:
            return Study.objects.filter(sponsor_name=user.get_full_name())
        
        if user.is_investigator or user.is_coordinator:
            return Study.objects.filter(studysite__investigators=user) | Study.objects.filter(studysite__coordinators=user)
        
        return Study.objects.filter(status='ACTIVE', is_public=True)
    
    def resolve_study(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study details')
        
        try:
            study = Study.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return study
            
            if user.is_sponsor and study.sponsor_name == user.get_full_name():
                return study
            
            if user.is_investigator or user.is_coordinator:
                if study.studysite_set.filter(investigators=user).exists() or study.studysite_set.filter(coordinators=user).exists():
                    return study
            
            if study.status == 'ACTIVE' and study.is_public:
                return study
            
            raise GraphQLError('You do not have permission to view this study')
        except Study.DoesNotExist:
            raise GraphQLError('Study not found')
    
    def resolve_study_phases(self, info, study_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study phases')
        
        if study_id:
            return StudyPhase.objects.filter(study_id=study_id)
        
        return StudyPhase.objects.all()
    
    def resolve_study_phase(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study phase details')
        
        try:
            return StudyPhase.objects.get(pk=id)
        except StudyPhase.DoesNotExist:
            raise GraphQLError('Study phase not found')
    
    
    def resolve_study_arms(self, info, study_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study arms')
        
        if study_id:
            return StudyArm.objects.filter(study_id=study_id)
        
        return StudyArm.objects.all()
    
    def resolve_study_arm(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view study arm details')
        
        try:
            return StudyArm.objects.get(pk=id)
        except StudyArm.DoesNotExist:
            raise GraphQLError('Study arm not found')
    
    def resolve_participants(self, info, study_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view participants')
        
        user = info.context.user
        
        query = Participant.objects.all()
        
        if study_id:
            query = query.filter(study_id=study_id)
        
        if user.is_superuser or user.is_staff:
            return query
        
        if user.is_sponsor:
            sponsor_studies = Study.objects.filter(sponsor_name=user.get_full_name())
            return query.filter(study__in=sponsor_studies)
        
        if user.is_investigator or user.is_coordinator:
            investigator_sites = user.studysite_set.all()
            return query.filter(site__in=investigator_sites)
        
        raise GraphQLError('You do not have permission to view participants')
    
    def resolve_participant(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view participant details')
        
        try:
            participant = Participant.objects.get(pk=id)
            user = info.context.user
            
            if user.is_superuser or user.is_staff:
                return participant
            
            if user.is_sponsor and participant.study.sponsor_name == user.get_full_name():
                return participant
            
            if user.is_investigator or user.is_coordinator:
                if user.studysite_set.filter(pk=participant.site.pk).exists():
                    return participant
            
            raise GraphQLError('You do not have permission to view this participant')
        except Participant.DoesNotExist:
            raise GraphQLError('Participant not found')

class StudyInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    protocol_number = graphene.String(required=True)
    status = graphene.String()
    phase = graphene.String()
    therapeutic_area = graphene.String()
    indication = graphene.String()
    sponsor_name = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    target_enrollment = graphene.Int()
    description = graphene.String()
    is_public = graphene.Boolean()

class ParticipantInput(graphene.InputObjectType):
    study_id = graphene.ID(required=True)
    site_id = graphene.ID(required=True)
    arm_id = graphene.ID()
    enrollment_date = graphene.Date()
    status = graphene.String()
    subject_id = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    date_of_birth = graphene.Date()
    gender = graphene.String()
    contact_email = graphene.String()
    contact_phone = graphene.String()
    notes = graphene.String()

class AdverseEventInput(graphene.InputObjectType):
    participant_id = graphene.ID(required=True)
    event_date = graphene.Date(required=True)
    description = graphene.String(required=True)
    severity = graphene.String(required=True)
    relation_to_treatment = graphene.String()
    action_taken = graphene.String()
    outcome = graphene.String()
    is_serious = graphene.Boolean()
    is_expected = graphene.Boolean()
    reported_by_id = graphene.ID(required=True)
    notes = graphene.String()

class CreateStudy(graphene.Mutation):
    class Arguments:
        input = StudyInput(required=True)
    
    study = graphene.Field(StudyType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a study')
        
        user = info.context.user
        
        if not (user.is_sponsor or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create studies')
        
        study = Study.objects.create(
            title=input.title,
            protocol_number=input.protocol_number,
            status=input.status or 'DRAFT',
            phase=input.phase,
            therapeutic_area=input.therapeutic_area,
            indication=input.indication,
            sponsor_name=input.sponsor_name or user.get_full_name() if user.is_sponsor else None,
            start_date=input.start_date,
            end_date=input.end_date,
            target_enrollment=input.target_enrollment,
            description=input.description,
            is_public=input.is_public or False
        )
        
        return CreateStudy(study=study)

class UpdateStudy(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = StudyInput(required=True)
    
    study = graphene.Field(StudyType)
    
    @staticmethod
    def mutate(root, info, id, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to update a study')
        
        user = info.context.user
        
        try:
            study = Study.objects.get(pk=id)
            
            if not (user.is_staff or user.is_superuser):
                if user.is_sponsor and study.sponsor_name != user.get_full_name():
                    raise GraphQLError('You do not have permission to update this study')
            
            study.title = input.title
            study.protocol_number = input.protocol_number
            
            if hasattr(input, 'status'):
                study.status = input.status
            if hasattr(input, 'phase'):
                study.phase = input.phase
            if hasattr(input, 'therapeutic_area'):
                study.therapeutic_area = input.therapeutic_area
            if hasattr(input, 'indication'):
                study.indication = input.indication
            if hasattr(input, 'sponsor_name'):
                study.sponsor_name = input.sponsor_name
            if hasattr(input, 'start_date'):
                study.start_date = input.start_date
            if hasattr(input, 'end_date'):
                study.end_date = input.end_date
            if hasattr(input, 'target_enrollment'):
                study.target_enrollment = input.target_enrollment
            if hasattr(input, 'description'):
                study.description = input.description
            if hasattr(input, 'is_public'):
                study.is_public = input.is_public
            
            study.save()
            return UpdateStudy(study=study)
            
        except Study.DoesNotExist:
            raise GraphQLError('Study not found')

class CreateParticipant(graphene.Mutation):
    class Arguments:
        input = ParticipantInput(required=True)
    
    participant = graphene.Field(ParticipantType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create a participant')
        
        user = info.context.user
        
        if not (user.is_investigator or user.is_coordinator or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create participants')
        
        try:
            study = Study.objects.get(pk=input.study_id)
        except Study.DoesNotExist:
            raise GraphQLError('Study not found')
        
        try:
            site = study.studysite_set.get(pk=input.site_id)
        except:
            raise GraphQLError('Site not found or not associated with this study')
        
        if not (user.is_staff or user.is_superuser):
            if not (site.investigators.filter(pk=user.pk).exists() or site.coordinators.filter(pk=user.pk).exists()):
                raise GraphQLError('You are not associated with this site')
        
        arm = None
        if hasattr(input, 'arm_id') and input.arm_id:
            try:
                arm = study.studyarm_set.get(pk=input.arm_id)
            except:
                raise GraphQLError('Arm not found or not associated with this study')
        
        participant = Participant.objects.create(
            study=study,
            site=site,
            arm=arm,
            enrollment_date=input.enrollment_date,
            status=input.status or 'SCREENING',
            subject_id=input.subject_id,
            first_name=input.first_name,
            last_name=input.last_name,
            date_of_birth=input.date_of_birth,
            gender=input.gender,
            contact_email=input.contact_email,
            contact_phone=input.contact_phone,
            notes=input.notes
        )
        
        return CreateParticipant(participant=participant)

class CreateAdverseEvent(graphene.Mutation):
    class Arguments:
        input = AdverseEventInput(required=True)
    
    adverse_event = graphene.Field(AdverseEventType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create an adverse event')
        
        user = info.context.user
        
        if not (user.is_investigator or user.is_coordinator or user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to create adverse events')
        
        try:
            participant = Participant.objects.get(pk=input.participant_id)
        except Participant.DoesNotExist:
            raise GraphQLError('Participant not found')
        
        if not (user.is_staff or user.is_superuser):
            site = participant.site
            if not (site.investigators.filter(pk=user.pk).exists() or site.coordinators.filter(pk=user.pk).exists()):
                raise GraphQLError('You are not associated with this participant\'s site')
        
        try:
            reported_by = User.objects.get(pk=input.reported_by_id)
        except User.DoesNotExist:
            raise GraphQLError('Reported by user not found')
        
        adverse_event = AdverseEvent.objects.create(
            participant=participant,
            event_date=input.event_date,
            description=input.description,
            severity=input.severity,
            relation_to_treatment=input.relation_to_treatment,
            action_taken=input.action_taken,
            outcome=input.outcome,
            is_serious=input.is_serious or False,
            is_expected=input.is_expected or False,
            reported_by=reported_by,
            notes=input.notes
        )
        
        return CreateAdverseEvent(adverse_event=adverse_event)

class Mutation(graphene.ObjectType):
    create_study = CreateStudy.Field()
    update_study = UpdateStudy.Field()
    create_participant = CreateParticipant.Field()
    create_adverse_event = CreateAdverseEvent.Field()
