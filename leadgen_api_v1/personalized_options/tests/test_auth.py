from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class TokenAuthenticationTest(APITestCase):
    url = reverse('activity_list')

    def setUp(self):
        username = 'alex'
        email = 'alex@hacker.com'
        password = 'alex_knows_nothing'
        user = User.objects.create_user(username, email, password)
        self.token = Token.objects.create(user=user)

    def test_token_authentication(self):
        tokens = Token.objects.all()
        self.assertEqual(len(tokens), 1)
        for token in tokens:
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            response = client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + 'NonExistingToken')
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
