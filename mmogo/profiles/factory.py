import factory
from datetime import datetime

from django.contrib.auth.models import User

from mmogo.profiles.models import Profile

class UserFactory(factory.Factory):
  class Meta:
    model: User

    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    is_active = ''
    group = 'users'


class ProfileFactory(factory.Factory):
  class Meta:
    model: Profile

    user = factory.SubFactory(UserFactory)
    language = ''
    image = ''
    cover = ''
    mobile = factory.Sequence(lambda n: '073-083-%04d' % n)
    accepted_terms = ''
    token = ''
    mobile_token = ''
    source = ''
    invitation_code = ''
    country = factory.SubFactory('mmogo.contrib.locations.factory.CountryFactory')
    gender = ''
    life_time_value = ''
    total_savings = ''
    abandoned_value = ''
    potential_savings = ''
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    first_login = ''
    first_login_at = factory.LazyFunction(datetime.now)
    last_login_at = factory.LazyFunction(datetime.now)

