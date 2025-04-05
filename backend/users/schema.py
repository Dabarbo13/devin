import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    me = graphene.Field(UserType)
    
    user_profiles = graphene.List(UserProfileType)
    user_profile = graphene.Field(UserProfileType, id=graphene.ID(required=True))
    
    def resolve_users(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view users')
        
        if info.context.user.is_staff or info.context.user.is_superuser:
            return User.objects.all()
        else:
            raise GraphQLError('You do not have permission to view all users')
    
    def resolve_user(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view user details')
        
        try:
            user = User.objects.get(pk=id)
            
            if info.context.user.pk == user.pk or info.context.user.is_staff or info.context.user.is_superuser:
                return user
            else:
                raise GraphQLError('You do not have permission to view this user')
        except User.DoesNotExist:
            raise GraphQLError('User not found')
    
    def resolve_me(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You are not logged in')
        return user
    
    def resolve_user_profiles(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view user profiles')
        
        if info.context.user.is_staff or info.context.user.is_superuser:
            return UserProfile.objects.all()
        else:
            raise GraphQLError('You do not have permission to view all user profiles')
    
    def resolve_user_profile(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view user profile details')
        
        try:
            profile = UserProfile.objects.get(pk=id)
            
            if info.context.user.pk == profile.user.pk or info.context.user.is_staff or info.context.user.is_superuser:
                return profile
            else:
                raise GraphQLError('You do not have permission to view this user profile')
        except UserProfile.DoesNotExist:
            raise GraphQLError('User profile not found')

class CreateUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    phone_number = graphene.String()
    is_donor = graphene.Boolean()
    is_recruiter = graphene.Boolean()
    is_investigator = graphene.Boolean()
    is_coordinator = graphene.Boolean()
    is_sponsor = graphene.Boolean()
    is_researcher = graphene.Boolean()

class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInput(required=True)
    
    user = graphene.Field(UserType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            if not User.objects.exists():  # Allow first user creation
                pass
            else:
                raise GraphQLError('You must be logged in to create a user')
        
        if User.objects.exists() and not (info.context.user.is_staff or info.context.user.is_superuser):
            raise GraphQLError('You do not have permission to create users')
        
        user = User.objects.create_user(
            email=input.email,
            password=input.password,
            first_name=input.first_name,
            last_name=input.last_name,
            phone_number=getattr(input, 'phone_number', None),
            is_donor=getattr(input, 'is_donor', False),
            is_recruiter=getattr(input, 'is_recruiter', False),
            is_investigator=getattr(input, 'is_investigator', False),
            is_coordinator=getattr(input, 'is_coordinator', False),
            is_sponsor=getattr(input, 'is_sponsor', False),
            is_researcher=getattr(input, 'is_researcher', False)
        )
        
        
        return CreateUser(user=user)

class UpdateUserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_number = graphene.String()
    is_donor = graphene.Boolean()
    is_recruiter = graphene.Boolean()
    is_investigator = graphene.Boolean()
    is_coordinator = graphene.Boolean()
    is_sponsor = graphene.Boolean()
    is_researcher = graphene.Boolean()
    is_active = graphene.Boolean()

class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UpdateUserInput(required=True)
    
    user = graphene.Field(UserType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to update a user')
        
        try:
            user = User.objects.get(pk=input.id)
            
            if info.context.user.pk != user.pk and not (info.context.user.is_staff or info.context.user.is_superuser):
                raise GraphQLError('You do not have permission to update this user')
            
            if hasattr(input, 'email'):
                user.email = input.email
            if hasattr(input, 'first_name'):
                user.first_name = input.first_name
            if hasattr(input, 'last_name'):
                user.last_name = input.last_name
            if hasattr(input, 'phone_number'):
                user.phone_number = input.phone_number
            
            if info.context.user.is_staff or info.context.user.is_superuser:
                if hasattr(input, 'is_donor'):
                    user.is_donor = input.is_donor
                if hasattr(input, 'is_recruiter'):
                    user.is_recruiter = input.is_recruiter
                if hasattr(input, 'is_investigator'):
                    user.is_investigator = input.is_investigator
                if hasattr(input, 'is_coordinator'):
                    user.is_coordinator = input.is_coordinator
                if hasattr(input, 'is_sponsor'):
                    user.is_sponsor = input.is_sponsor
                if hasattr(input, 'is_researcher'):
                    user.is_researcher = input.is_researcher
                if hasattr(input, 'is_active'):
                    user.is_active = input.is_active
            
            user.save()
            return UpdateUser(user=user)
            
        except User.DoesNotExist:
            raise GraphQLError('User not found')

class UpdateUserProfileInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    bio = graphene.String()
    date_of_birth = graphene.Date()
    gender = graphene.String()
    address = graphene.String()
    city = graphene.String()
    state = graphene.String()
    zip_code = graphene.String()
    country = graphene.String()

class UpdateUserProfile(graphene.Mutation):
    class Arguments:
        input = UpdateUserProfileInput(required=True)
    
    profile = graphene.Field(UserProfileType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to update a user profile')
        
        try:
            profile = UserProfile.objects.get(pk=input.id)
            
            if info.context.user.pk != profile.user.pk and not (info.context.user.is_staff or info.context.user.is_superuser):
                raise GraphQLError('You do not have permission to update this user profile')
            
            if hasattr(input, 'bio'):
                profile.bio = input.bio
            if hasattr(input, 'date_of_birth'):
                profile.date_of_birth = input.date_of_birth
            if hasattr(input, 'gender'):
                profile.gender = input.gender
            if hasattr(input, 'address'):
                profile.address = input.address
            if hasattr(input, 'city'):
                profile.city = input.city
            if hasattr(input, 'state'):
                profile.state = input.state
            if hasattr(input, 'zip_code'):
                profile.zip_code = input.zip_code
            if hasattr(input, 'country'):
                profile.country = input.country
            
            profile.save()
            return UpdateUserProfile(profile=profile)
            
        except UserProfile.DoesNotExist:
            raise GraphQLError('User profile not found')

class ChangePasswordInput(graphene.InputObjectType):
    old_password = graphene.String(required=True)
    new_password = graphene.String(required=True)

class ChangePassword(graphene.Mutation):
    class Arguments:
        input = ChangePasswordInput(required=True)
    
    success = graphene.Boolean()
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to change your password')
        
        user = info.context.user
        
        if not user.check_password(input.old_password):
            raise GraphQLError('Old password is incorrect')
        
        user.set_password(input.new_password)
        user.save()
        
        return ChangePassword(success=True)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    update_user_profile = UpdateUserProfile.Field()
    change_password = ChangePassword.Field()
