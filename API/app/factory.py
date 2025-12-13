import factory
from factory import fuzzy
from datetime import timedelta , date
from app.models.profile import Profile
from app.models.plannedEvent import PlannedEvent
from app.models.todo import TodoItem
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates a standard Django User.
    Equivalent to creating an IdentityUser in ASP.NET.
    """
    class Meta:
        model = User

    # Sequence ensures unique values: user_0, user_1, etc.
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    
    # This ensures the password is properly hashed in the DB
    password = factory.PostGenerationMethodCall('set_password', 'strongpassword123')

class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Creates a Profile linked to a User.
    """
    class Meta:
        model = Profile

    # SubFactory triggers the UserFactory above automatically
    user = factory.SubFactory(UserFactory)

class PlannedEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlannedEvent

    # Automatically creates a Profile (and thus a User) if one isn't provided
    creator = factory.SubFactory(ProfileFactory)

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=200)
    
    date = fuzzy.FuzzyDate(date.today(), date.today() + timedelta(days=30))
    
    # Simple way to generate a random time object
    start_time = factory.Faker('time_object')
    
    duration = timedelta(hours=1)