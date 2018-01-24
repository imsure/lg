from django.contrib.auth.models import User

# Default GPS points (location: Tucson) used for testing.
from_lat = 32.27908
from_lon = -110.94449
to_lat = 32.22997
to_lon = -110.95475


def set_up_user():
    username = 'alex'
    email = 'alex@hacker.com'
    password = 'alex_knows_nothing'
    return User.objects.create_user(username, email, password)