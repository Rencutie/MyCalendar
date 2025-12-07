import factory
from factory import fuzzy
from datetime import timedelta , date
from app.models.profile import Profile
from app.models.plannedEvent import PlannedEvent
from app.models.todo import TodoItem

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user_id = factory.Sequence(lambda n: n + 1)

class PlannedEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlannedEvent

    creator = factory.SubFactory(ProfileFactory)

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=200)
    

    date = fuzzy.FuzzyDate(date.today(), date.today() + timedelta(days=30))
    start_time = factory.LazyAttribute(lambda o: fuzzy.FuzzyDateTime(o.date, o.date + timedelta(hours=23)).fuzz())
    duration = timedelta(hours=1)
