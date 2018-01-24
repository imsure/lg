from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from .common import set_up_user


class TokenAuthenticationTest(APITestCase):
    url = reverse('create_activity')

    def setUp(self):
        self.user = set_up_user()
        self.token = Token.objects.create(user=self.user)

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
