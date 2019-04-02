from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from ..models import User


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def user_signup(username="", firstname="", surname="", email="", password=""):
        User.objects.create(username=username, firstname=firstname,
                            surname=surname, email=email, password=email)

    def setUp(self):
        self.user_signup('ann', 'ann', 'ann', 'ann@gmail.com', 'ann')
        self.user_signup('ann1', 'ann1', 'ann1',
                         'ann1@gmail.com', 'ann')


class UserTest(BaseViewTest):
    def test_get_all_users(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(len(response.data), 2)
